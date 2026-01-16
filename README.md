# SAIFU-PAY
SAIFU PAY is an offline personal finance manager built with Python and PyQt5. It provides a secure platform for logging income and expenses through a modern, dark-themed GUI. By leveraging Matplotlib for visualization and a local CSV database, the system ensures data privacy and real-time analytical feedback.

# 🚀 Features of SAIFU PAY

1. Modern Dark UI/UX
 Sleek Dark Theme: A fully customized dark interface designed for eye comfort and a premium "modern finance" feel.
 Intuitive Navigation: Simple tab-based navigation to switch between adding transactions, viewing logs, and analyzing stats.

2. Smart Transaction Management
 Dynamic Category Filtering: Intelligent "Type-to-Category" logic. When you select Income, only income-related categories appear; when you select Expense, only expense categories show up. This prevents data entry  errors.
 Detailed Records: Log transactions with specific dates, times, amounts, categories, and custom notes.
 High-Visibility Alerts: Includes large, custom-styled success confirmation boxes for a better user feedback experience.

3. Advanced Financial Analytics
 Visual Dashboards: Integrated Matplotlib charts providing a visual breakdown of your finances.
 Comprehensive Charting:
    Total Overview (Income vs. Expense Pie Chart)
 Category-wise Breakdown (Bar Charts):
    Specific Expense/Income Distribution charts.
 Net Balance Tracking: Automatically calculates and displays your real-time net balance with color-coded indicators (Green for profit, Red for deficit).

4. Smart Data Filtering
 Time-Based Views: Filter your entire history by specific months or years to track your spending habits over time.
 Clean Table Management: View all transactions in a structured table, with the ability to delete specific entries to keep your records accurate.

5. Portable & Lightweight
Local Storage: Uses a simple .csv backend, ensuring your data is stored locally on your machine and is easily portable.
Standalone Executable: Can be compiled into a single .exe file with a custom icon, making it easy to run on any Windows machine without installing Python.

# 🛠️ How to Run Saifu Pay
To run this application on your local machine, follow these steps:

1. Install Python
Make sure you have Python installed on your system. If not, download it from python.org.

2. Get the Code
You can either download the finance_tracker.py file directly or clone this repository using

GET:git clone https://github.com/your-username/saifu-pay.git cd saifu-pay

3. Install Required "Ingredients" (Dependencies)
This app uses two main libraries that don't come with standard Python. You need to install them using the terminal (Command Prompt or PowerShell): pip install PyQt5 matplotlib

4. Run the App
Once the libraries are installed, simply run the script: python finance_tracker.py

# 🛠️ Getting Started
When you first launch the app, you will see a modern dark-themed window with three main tabs at the top.

1. ➕ Adding a Transaction
This is where you log your daily spending or earnings.

Step 1: Choose Type (Smart Feature): Select Income or Expense first.

Note: The "Category" list changes automatically based on this choice to prevent mistakes.

Step 2: Enter Amount: Type in the numerical value (e.g., 500). Do not include currency symbols.

Step 3: Select Category: Pick from the list (e.g., Food, Salary, Shopping).

Step 4: Add a Note: (Optional) Add a brief description like "Lunch with friends" or "Monthly Bonus."

Step 5: Save: Click Save Transaction. You will see a large success message confirming the entry is stored.

2. 📄 Viewing Your History
The View Transactions tab acts as your digital passbook.

Real-time Balance: At the top, you’ll see your Net Balance. It turns Green if you are in profit and Red if you have spent more than you earned.

Monthly Filtering: Use the dropdown at the top to filter by "Year-Month" (e.g., 2024-05). This helps you focus on your budget for a specific period.

Deleting Entries: If you make a mistake, click on a row in the table and press Delete Selected. This permanently removes the entry from your data file.

3. 📊 Analyzing Statistics
The Statistics tab turns your numbers into visual insights.

Dashboard View: View three charts at once: Overall overview, Income breakdown, and Expense breakdown.

Specific Charts: Use the selector to zoom into a specific chart, such as a Bar Chart comparing categories.

Filter Data: Just like the view tab, you can filter the charts by month to see how your spending habits change over time.

4. 📂 Managing Your Data (CSV)
SAIFU PAY is designed to be "offline-first" for your privacy.

The Database: All your entries are saved in a file named finance_data.csv in the same folder as the app.

Excel Compatible: You can open this CSV file in Microsoft Excel or Google Sheets if you want to perform your own advanced calculations.

Backup: To back up your data, simply copy the finance_data.csv file to a USB drive or cloud storage.

# AUTHORS
IJAS MUHAMMED :https://github.com/ijazzzzzzzzzzzzzz
ATIF EHSAAN M :https://github.com/atiff-git
MANAS J :https://github.com/manasj1750?tab=repositories
HARI GOVIND G.H :https://github.com/HariiGovindGH/SAIFU-PAY



