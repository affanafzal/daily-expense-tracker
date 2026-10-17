# Project Report: Daily Expense Tracker

## 1. Problem Statement
Students and households often make frequent small purchases but do not keep a consistent record of them. This makes it difficult to know how much money is spent, which categories consume the most money, and how spending changes month by month. This project provides a small interactive application for recording and analyzing expenses in Pakistani Rupees (PKR).

## 2. Dataset Description
The main file is `expenses.csv`. Each row represents one expense and contains:
- `Date`: date the expense occurred
- `Category`: spending category
- `Description`: short explanation of the purchase
- `Payment Method`: cash, card, bank transfer, mobile wallet or other
- `Amount (PKR)`: expense amount in Pakistani rupees

The supplied file contains 10 **demonstration records dated October 2026**. They are examples only and must be replaced or deleted before treating the results as personal financial information. The user can add records through the app and keep tracking October and all following months in the same CSV file.

## 3. Methods Used
Python and Pandas are used to:
- Load CSV data using `pandas.read_csv()`.
- Inspect records in interactive tables and summarize totals.
- Convert dates using `pandas.to_datetime()` and amounts using `pandas.to_numeric()`.
- Handle missing category, description and payment-method values.
- Remove rows with invalid dates, invalid or non-positive amounts, and exact duplicates.
- Group expenses by category, month and payment method with `groupby()`.
- Calculate total spending, number of records, average expense and largest expense.
- Sort records by date and export processed data with `to_csv()`.
Streamlit provides the interactive forms, filters, tables, charts and downloads.

## 4. Key Findings (Demonstration Data Only)
For the included 10 demo records:
- Total recorded spending: **Rs. 2,790**
- Number of expenses: **10**
- Average expense: **Rs. 279**
- Largest single expense: **Rs. 700** (friends outing)
- Food is the largest category in this small example, at **Rs. 980**.

These findings describe only the example records. Once the user deletes the sample rows and enters personal expenses, the dashboard will calculate updated findings automatically.

## 5. Conclusion
The project demonstrates how Pandas can transform raw expense records into useful summaries and trends. Users can maintain a persistent record from October 2026 onwards, inspect spending by category and month, edit records, and export a cleaned dataset for further analysis. The application can be extended with budgets, monthly limits, income tracking and savings goals.

## How to Run
Install Python 3.10+, open a terminal in the project folder, run `python -m pip install -r requirements.txt`, then run `python -m streamlit run app.py`. If the `python` command is unavailable on Windows, use `py` instead. See `README.md` for full instructions.
