PHONEPE TRANSACTION ANALYTICS DASHBOARD
=======================================

Project Type:
Data Analytics / College Project

Project Description:
This project analyzes PhonePe-style transaction data and presents the results in a visual dashboard. It helps understand daily transaction amounts, transaction status, payment methods, transaction types, bank-wise amounts, and revenue by status.

Technologies Used:
1. Python - Main programming language
2. Pandas - Data cleaning and analysis
3. NumPy - Numerical calculations
4. Matplotlib - Charts and dashboard visualization
5. OpenPyXL - Reading Excel files
6. VS Code / Jupyter Notebook - Development environment
7. Microsoft Excel - Dataset format

Files:
- phonepe_dashboard.py : Complete Python dashboard code
- PhonePe_Transactions_1000_Rows.xlsx : 1000-row sample dataset
- PhonePe_Transaction_Dashboard.png : Dashboard output image
- README.txt : Project documentation

Dataset Columns:
Transaction_ID
Date
Time
Sender_Name
Receiver_Name
Mobile_Number
UPI_ID
Bank_Name
Transaction_Type
Amount
Status
Payment_Method
State
City
Device_Type

Dashboard Charts:
1. Daily Transaction Amount Activity
2. Transaction Status
3. Transaction Amount Trend by Type (Daily)
4. Payment Methods Share
5. Total Amount by Bank Name
6. Revenue by Status

Installation:
pip install pandas numpy matplotlib openpyxl

How to Run:
1. Keep the Python file and Excel dataset in the same folder.
2. Open Terminal or Command Prompt in that folder.
3. Run:
   python phonepe_dashboard.py
4. The dashboard will open and an image named PhonePe_Transaction_Dashboard.png will be created.

Project Objective:
The objective is to convert raw transaction data into meaningful visual insights that can help understand transaction patterns and payment behavior.

Important Note:
The dataset included with this project is sample/demo data created for educational and project demonstration purposes. It is not real PhonePe customer data.
