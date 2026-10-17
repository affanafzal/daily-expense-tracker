import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date
import io

APP_DIR = Path(__file__).parent
DATA_FILE = APP_DIR / "expenses.csv"
CLEAN_FILE = APP_DIR / "cleaned_expenses.csv"
COLUMNS = ["Date", "Category", "Description", "Payment Method", "Amount (PKR)"]
CATEGORIES = ["Food", "Transport", "Education", "Shopping", "Bills", "Health", "Personal Care", "Entertainment", "Family/Home", "Other"]
PAYMENT_METHODS = ["Cash", "Debit/Credit Card", "Bank Transfer", "Easypaisa/JazzCash", "Other"]

st.set_page_config(page_title="Daily Expense Tracker", page_icon="💸", layout="wide")
st.title("💸 Daily Expense Tracker")
st.caption("Record your own expenses, understand spending patterns, and export clean data. Currency: Pakistani Rupees (PKR).")

def load_data():
    if not DATA_FILE.exists():
        pd.DataFrame(columns=COLUMNS).to_csv(DATA_FILE, index=False)
    try:
        df = pd.read_csv(DATA_FILE)
    except (pd.errors.EmptyDataError, UnicodeDecodeError):
        df = pd.DataFrame(columns=COLUMNS)
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    df = df[COLUMNS].copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Category"] = df["Category"].fillna("Other").astype(str)
    df["Description"] = df["Description"].fillna("").astype(str)
    df["Payment Method"] = df["Payment Method"].fillna("Other").astype(str)
    df["Amount (PKR)"] = pd.to_numeric(df["Amount (PKR)"], errors="coerce")
    return df

def clean_data(raw):
    df = raw.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount (PKR)"] = pd.to_numeric(df["Amount (PKR)"], errors="coerce")
    df["Category"] = df["Category"].fillna("Other").astype(str).str.strip().replace("", "Other")
    df["Description"] = df["Description"].fillna("").astype(str).str.strip()
    df["Payment Method"] = df["Payment Method"].fillna("Other").astype(str).str.strip().replace("", "Other")
    df = df.dropna(subset=["Date", "Amount (PKR)"])
    df = df[df["Amount (PKR)"] > 0]
    df = df.drop_duplicates(subset=COLUMNS)
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    df["Amount (PKR)"] = df["Amount (PKR)"].round(2)
    return df[COLUMNS].sort_values("Date", ascending=False)

df = load_data()
# Save a cleaned version on every app load so the deliverable is always available.
clean_data(df).to_csv(CLEAN_FILE, index=False)

with st.sidebar:
    st.header("🔎 Filters")
    if not df["Date"].dropna().empty:
        min_date = df["Date"].dropna().min().date()
        max_date = df["Date"].dropna().max().date()
    else:
        min_date, max_date = date(2026, 10, 1), date.today()
    start = st.date_input("From date", value=min_date)
    end = st.date_input("To date", value=max(max_date, start))
    category_options = sorted(df["Category"].dropna().unique().tolist())
    selected_categories = st.multiselect("Categories", category_options, default=category_options)
    st.caption("Your records are saved in expenses.csv in this project folder.")

tab_add, tab_dashboard, tab_manage, tab_export = st.tabs(["➕ Add Expense", "📊 Dashboard", "🧾 Manage Records", "📤 Export Data"])

with tab_add:
    st.subheader("Add a new expense")
    with st.form("expense_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            expense_date = st.date_input("Expense date", value=date.today(), min_value=date(2000, 1, 1))
            category = st.selectbox("Category", CATEGORIES)
            description = st.text_input("Description", placeholder="e.g., lunch at university")
        with c2:
            amount = st.number_input("Amount (PKR)", min_value=1.0, value=100.0, step=50.0)
            payment = st.selectbox("Payment method", PAYMENT_METHODS)
        submitted = st.form_submit_button("Save Expense", type="primary")
        if submitted:
            new_row = pd.DataFrame([{
                "Date": expense_date.strftime("%Y-%m-%d"),
                "Category": category,
                "Description": description.strip(),
                "Payment Method": payment,
                "Amount (PKR)": float(amount)
            }])
            current = pd.read_csv(DATA_FILE) if DATA_FILE.exists() and DATA_FILE.stat().st_size else pd.DataFrame(columns=COLUMNS)
            for col in COLUMNS:
                if col not in current.columns:
                    current[col] = pd.NA
            current = pd.concat([current[COLUMNS], new_row], ignore_index=True)
            current.to_csv(DATA_FILE, index=False)
            st.success("Expense saved! The dashboard will include it.")
            st.rerun()
    st.info("Tip: enter expenses on the day you spend money. Use clear descriptions so you can understand the record later.")

with tab_dashboard:
    st.subheader("Your spending overview")
    filtered = df.copy()
    if not filtered["Date"].dropna().empty:
        filtered = filtered[filtered["Date"].dt.date.between(start, end)]
    if selected_categories:
        filtered = filtered[filtered["Category"].isin(selected_categories)]
    elif category_options:
        filtered = filtered.iloc[0:0]
    total = float(filtered["Amount (PKR)"].fillna(0).sum())
    count = len(filtered)
    avg = total / count if count else 0
    largest = float(filtered["Amount (PKR)"].max()) if count else 0
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Total spending", f"Rs. {total:,.0f}")
    m2.metric("Number of expenses", f"{count:,}")
    m3.metric("Average expense", f"Rs. {avg:,.0f}")
    m4.metric("Largest expense", f"Rs. {largest:,.0f}")
    if filtered.empty:
        st.warning("No expenses match these filters yet. Add an expense or widen the date range.")
    else:
        left, right = st.columns(2)
        with left:
            st.markdown("**Spending by category**")
            by_cat = filtered.groupby("Category", as_index=False)["Amount (PKR)"].sum().sort_values("Amount (PKR)", ascending=False)
            st.bar_chart(by_cat.set_index("Category"))
            st.dataframe(by_cat, use_container_width=True, hide_index=True)
        with right:
            st.markdown("**Monthly spending trend**")
            monthly = filtered.assign(Month=filtered["Date"].dt.to_period("M").astype(str)).groupby("Month", as_index=False)["Amount (PKR)"].sum()
            st.line_chart(monthly.set_index("Month"))
            st.markdown("**Payment methods**")
            st.dataframe(filtered.groupby("Payment Method", as_index=False)["Amount (PKR)"].sum().sort_values("Amount (PKR)", ascending=False), use_container_width=True, hide_index=True)
        st.markdown("**Recent expenses**")
        show = filtered.sort_values("Date", ascending=False).copy()
        show["Date"] = show["Date"].dt.strftime("%Y-%m-%d")
        st.dataframe(show[COLUMNS], use_container_width=True, hide_index=True)

with tab_manage:
    st.subheader("Edit or delete your records")
    st.write("Edit cells directly, then click **Save changes**. To delete a row, select it using the table's row selection if supported, or remove it from the CSV file.")
    editable = df.copy()
    editable["Date"] = editable["Date"].dt.strftime("%Y-%m-%d")
    edited = st.data_editor(editable, num_rows="dynamic", use_container_width=True, key="expense_editor",
                            column_config={"Date": st.column_config.TextColumn("Date (YYYY-MM-DD)"),
                                           "Amount (PKR)": st.column_config.NumberColumn("Amount (PKR)", min_value=0.01, format="%.2f")})
    if st.button("Save changes", type="primary"):
        edited.to_csv(DATA_FILE, index=False)
        st.success("Records updated.")
        st.rerun()
    st.caption("For a full reset, make a backup and clear the rows in expenses.csv. Keep the column headers.")

with tab_export:
    st.subheader("Download your data")
    cleaned = clean_data(df)
    st.write(f"Raw records: **{len(df)}** · Clean records: **{len(cleaned)}**")
    st.caption("Cleaning converts dates and amounts to valid types, removes missing/invalid dates and amounts, removes non-positive amounts, standardizes blank category/payment fields, removes exact duplicates, and sorts by date.")
    st.download_button("Download cleaned CSV", data=cleaned.to_csv(index=False).encode("utf-8-sig"),
                       file_name="cleaned_expenses.csv", mime="text/csv")
    st.download_button("Download raw CSV backup", data=DATA_FILE.read_bytes() if DATA_FILE.exists() else b"",
                       file_name="expenses_backup.csv", mime="text/csv")
    cleaned.to_csv(CLEAN_FILE, index=False)
    st.success(f"A cleaned copy is also saved automatically as: {CLEAN_FILE.name}")
