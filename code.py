# ============================================================
# PHONEPE TRANSACTION ANALYTICS DASHBOARD
# ONE FILE COMPLETE PROJECT
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ============================================================
# FILE CONFIGURATION
# ============================================================

FILE_NAME = "PhonePe_Transactions_1000_Rows.csv"
OUTPUT_FILE = "PhonePe_Transaction_Dashboard.png"

# ============================================================
# LOAD DATASET
# ============================================================

print("=" * 70)
print("PHONEPE TRANSACTION ANALYTICS")
print("=" * 70)

print("\nLoading dataset...")

try:
    df = pd.read_csv(FILE_NAME)
except FileNotFoundError:
    print(f"\nERROR: File '{FILE_NAME}' not found.")
    print("Please upload the Excel file to the same folder/Colab session.")
    raise

# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = df.columns.str.strip()

print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

# ============================================================
# HANDLE COLUMN NAME DIFFERENCES
# ============================================================

# Bank column can be Bank or Bank_Name
if "Bank_Name" in df.columns:
    BANK_COLUMN = "Bank_Name"
elif "Bank" in df.columns:
    BANK_COLUMN = "Bank"
else:
    raise ValueError(
        "Bank column not found. Expected 'Bank' or 'Bank_Name'."
    )

# Check required columns
required_columns = [
    "Date",
    "Amount",
    "Status",
    "Payment_Method"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

# ============================================================
# DATA CLEANING
# ============================================================

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

df["Amount"] = pd.to_numeric(
    df["Amount"],
    errors="coerce"
)

df = df.dropna(
    subset=["Date", "Amount"]
)

# ============================================================
# DATASET INFORMATION
# ============================================================

print("\n--- DATASET INFO ---")
print(df.info())

print("\n--- DATASET SHAPE ---")
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- DESCRIPTIVE STATISTICS ---")
print(df["Amount"].describe())

# ============================================================
# ANALYSIS
# ============================================================

# ------------------------------------------------------------
# 1. DAILY TRANSACTION ANALYSIS
# ------------------------------------------------------------

daily = df.groupby("Date").agg(
    Transactions=("Amount", "count"),
    Transaction_Value=("Amount", "sum")
)

# Daily amount by day number
daily_amount = (
    df.groupby(df["Date"].dt.day)["Amount"]
    .sum()
)

# ------------------------------------------------------------
# 2. TRANSACTION STATUS
# ------------------------------------------------------------

status_count = df["Status"].value_counts()

# Revenue / amount by status
revenue_status = (
    df.groupby("Status")["Amount"]
    .sum()
)

# ------------------------------------------------------------
# 3. PAYMENT METHOD
# ------------------------------------------------------------

payment_count = (
    df["Payment_Method"]
    .value_counts()
)

# ------------------------------------------------------------
# 4. BANK PERFORMANCE
# ------------------------------------------------------------

bank = df.groupby(BANK_COLUMN).agg(
    Transactions=("Amount", "count"),
    Transaction_Value=("Amount", "sum"),
    Success_Rate=(
        "Status",
        lambda x: x.eq("Success").mean() * 100
    )
).sort_values(
    "Transaction_Value",
    ascending=False
)

bank_amount = bank["Transaction_Value"]

# ------------------------------------------------------------
# 5. TRANSACTION TYPE TREND
# ------------------------------------------------------------

if "Transaction_Type" in df.columns:

    transaction_trend = (
        df.pivot_table(
            values="Amount",
            index=df["Date"].dt.day,
            columns="Transaction_Type",
            aggfunc="sum"
        )
        .fillna(0)
    )

else:

    # If Transaction_Type does not exist,
    # create an empty DataFrame
    transaction_trend = pd.DataFrame()

# ============================================================
# PRINT ANALYSIS RESULTS
# ============================================================

print("\n" + "=" * 70)
print("DAILY TRANSACTION ANALYSIS")
print("=" * 70)

print(daily)

print("\n" + "=" * 70)
print("BANK PERFORMANCE")
print("=" * 70)

print(bank)

print("\n" + "=" * 70)
print("PAYMENT METHODS")
print("=" * 70)

print(payment_count)

print("\n" + "=" * 70)
print("TRANSACTION STATUS")
print("=" * 70)

print(status_count)

print("\n" + "=" * 70)
print("REVENUE BY STATUS")
print("=" * 70)

print(revenue_status)

# ============================================================
# KEY PERFORMANCE INDICATORS
# ============================================================

total_transactions = len(df)
total_amount = df["Amount"].sum()
average_transaction = df["Amount"].mean()

success_transactions = (
    df["Status"]
    .eq("Success")
    .sum()
)

success_rate = (
    success_transactions /
    total_transactions *
    100
)

print("\n" + "=" * 70)
print("KEY PERFORMANCE INDICATORS")
print("=" * 70)

print(f"Total Transactions     : {total_transactions:,}")
print(f"Total Transaction Value: ₹ {total_amount:,.2f}")
print(f"Average Transaction    : ₹ {average_transaction:,.2f}")
print(f"Successful Transactions: {success_transactions:,}")
print(f"Overall Success Rate   : {success_rate:.2f}%")

# ============================================================
# COLORS
# ============================================================

BLUE = "#2463D4"
GREEN = "#13AE72"
ORANGE = "#F39C12"
RED = "#EF3F3F"
PURPLE = "#8054E8"

status_colors = {
    "Success": GREEN,
    "Failed": RED,
    "Pending": ORANGE
}

# ============================================================
# CREATE DASHBOARD
# ============================================================

fig = plt.figure(
    figsize=(18, 13),
    facecolor="#F4F6F9"
)

fig.suptitle(
    "PhonePe Transaction Analytics Dashboard",
    fontsize=20,
    fontweight="bold",
    y=0.985
)

# ============================================================
# 1. DAILY TRANSACTION AMOUNT
# ============================================================

ax1 = plt.subplot2grid(
    (3, 2),
    (0, 0)
)

ax1.bar(
    daily_amount.index,
    daily_amount.values,
    color=BLUE,
    width=0.65
)

ax1.set_title(
    "Daily Transaction Amount Activity",
    fontsize=14,
    loc="left"
)

ax1.set_xlabel("Day")
ax1.set_ylabel("Amount (₹)")

ax1.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

ax1.set_axisbelow(True)

ax1.yaxis.set_major_formatter(
    FuncFormatter(
        lambda x, pos: f"₹{x/1e6:.1f}M"
    )
)

# ============================================================
# 2. TRANSACTION STATUS
# ============================================================

ax2 = plt.subplot2grid(
    (3, 2),
    (0, 1)
)

colors = [
    status_colors.get(
        x,
        BLUE
    )
    for x in status_count.index
]

ax2.pie(
    status_count.values,
    labels=status_count.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    wedgeprops={
        "edgecolor": "white"
    }
)

ax2.set_title(
    "Transaction Status",
    fontsize=14
)

ax2.axis("equal")

# ============================================================
# 3. TRANSACTION TYPE TREND
# ============================================================

ax3 = plt.subplot2grid(
    (3, 2),
    (1, 0)
)

if not transaction_trend.empty:

    line_colors = [
        BLUE,
        ORANGE,
        GREEN,
        PURPLE
    ]

    for i, column in enumerate(
        transaction_trend.columns
    ):

        ax3.plot(
            transaction_trend.index,
            transaction_trend[column],
            marker="o",
            linewidth=2,
            markersize=5,
            label=column,
            color=line_colors[
                i % len(line_colors)
            ]
        )

    ax3.legend(
        frameon=False
    )

else:

    ax3.text(
        0.5,
        0.5,
        "Transaction_Type column\nnot available",
        ha="center",
        va="center",
        fontsize=13
    )

ax3.set_title(
    "Transaction Amount Trend by Type (Daily)",
    fontsize=14,
    loc="left"
)

ax3.set_xlabel("Day")
ax3.set_ylabel("Amount (₹)")

ax3.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

ax3.set_axisbelow(True)

ax3.yaxis.set_major_formatter(
    FuncFormatter(
        lambda x, pos: f"₹{x/1000:.0f}K"
    )
)

# ============================================================
# 4. PAYMENT METHOD SHARE
# ============================================================

ax4 = plt.subplot2grid(
    (3, 2),
    (1, 1)
)

payment_colors = [
    BLUE,
    GREEN,
    ORANGE,
    PURPLE
]

ax4.pie(
    payment_count.values,
    labels=payment_count.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=payment_colors[
        :len(payment_count)
    ],
    wedgeprops={
        "width": 0.40,
        "edgecolor": "white"
    },
    pctdistance=0.72
)

ax4.set_title(
    "Payment Methods Share",
    fontsize=14
)

ax4.axis("equal")

# ============================================================
# 5. TOTAL AMOUNT BY BANK
# ============================================================

ax5 = plt.subplot2grid(
    (3, 2),
    (2, 0)
)

bank_colors = [
    BLUE,
    RED,
    GREEN,
    ORANGE,
    PURPLE,
    BLUE,
    RED,
    GREEN
]

ax5.bar(
    bank_amount.index,
    bank_amount.values,
    color=bank_colors[
        :len(bank_amount)
    ],
    width=0.60
)

ax5.set_title(
    "Total Amount by Bank Name",
    fontsize=14,
    loc="left"
)

ax5.set_xlabel("Bank")
ax5.set_ylabel("Amount (₹)")

ax5.tick_params(
    axis="x",
    rotation=45
)

ax5.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

ax5.set_axisbelow(True)

ax5.yaxis.set_major_formatter(
    FuncFormatter(
        lambda x, pos: f"₹{x/1e6:.1f}M"
    )
)

# ============================================================
# 6. REVENUE BY STATUS
# ============================================================

ax6 = plt.subplot2grid(
    (3, 2),
    (2, 1)
)

colors = [
    status_colors.get(
        x,
        BLUE
    )
    for x in revenue_status.index
]

ax6.pie(
    revenue_status.values,
    labels=revenue_status.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    wedgeprops={
        "width": 0.40,
        "edgecolor": "white"
    },
    pctdistance=0.72
)

ax6.text(
    0,
    0.08,
    "Total",
    ha="center",
    va="center",
    fontsize=11
)

ax6.text(
    0,
    -0.12,
    f"₹ {total_amount:,.0f}",
    ha="center",
    va="center",
    fontsize=12,
    fontweight="bold"
)

ax6.set_title(
    "Revenue by Status",
    fontsize=14
)

ax6.axis("equal")

# ============================================================
# FINAL DESIGN
# ============================================================

for ax in [
    ax1,
    ax2,
    ax3,
    ax4,
    ax5,
    ax6
]:

    ax.set_facecolor("white")

plt.subplots_adjust(
    left=0.06,
    right=0.97,
    top=0.94,
    bottom=0.06,
    wspace=0.22,
    hspace=0.30
)

# ============================================================
# SAVE DASHBOARD
# ============================================================

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight",
    facecolor=fig.get_facecolor()
)

print("\n" + "=" * 70)
print("DASHBOARD CREATED SUCCESSFULLY")
print("=" * 70)

print(f"\nSaved as: {OUTPUT_FILE}")

plt.show()
