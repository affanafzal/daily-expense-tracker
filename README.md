# Daily Expense Tracker (Python + Pandas)

## Features
- Enter your own expense records and save them to `expenses.csv`.
- Filter by date and category.
- View total spending, expense count, average and largest expense.
- Analyze spending by category, month and payment method.
- Edit records in the Manage Records tab.
- Export cleaned data to `cleaned_expenses.csv` or download a CSV backup.
- Data is stored locally in the project folder; no account or internet connection is needed after installation.

## Run on Windows
1. Install Python 3.10 or newer from https://www.python.org/downloads/ . During setup, tick **Add Python to PATH**.
2. Extract this ZIP file to a folder, for example `Desktop\Daily_Expense_Tracker_Project`.
3. Open that folder in VS Code, or open Command Prompt in the folder.
4. Install packages:
   ```bash
   python -m pip install -r requirements.txt
   ```
   If `python` does not work, try `py -m pip install -r requirements.txt`.
5. Start the app:
   ```bash
   python -m streamlit run app.py
   ```
   If that does not work, try `py -m streamlit run app.py`.
6. Your browser should open automatically at a local address, usually `http://localhost:8501`.

## How to track expenses from October onwards
- The supplied `expenses.csv` contains **demo records for October 2026** so charts are not empty at first. These are examples, not your actual spending.
- Delete the demo rows in the **Manage Records** tab and click **Save changes**, or replace the rows in `expenses.csv` while keeping the header row.
- From then on, use **Add Expense** whenever you spend money. Select the actual date, category, description, payment method and amount.
- Keep using the same folder and `expenses.csv` every month. Your records remain there when you close the app.
- To review October or a later month, use the date filters in the sidebar.
- Back up `expenses.csv` periodically. Do not delete it if you want to retain your history.

## If commands fail
- Make sure the terminal is opened in the folder containing `app.py` and `requirements.txt`.
- Check Python: `python --version` or `py --version`.
- Check Streamlit: `python -m streamlit --version`.
- If Streamlit is missing: `python -m pip install streamlit pandas`.
- Do not type the three backticks shown around commands; type only the command itself.
