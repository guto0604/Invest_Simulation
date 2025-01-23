import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Set darker theme
style.use('dark_background')

def calculate_investment_growth(current_amount, monthly_contribution, yearly_increase_rate, yearly_return, extra_yearly_multiplier, target_date):
    # Converting yearly return rate to monthly return rate
    monthly_return_rate = (1 + yearly_return) ** (1 / 12) - 1

    # Prepare simulation dates
    today = datetime.today().replace(day=1).date()
    target_datetime = target_date.replace(day=1)
    dates = []
    while today <= target_datetime:
        dates.append(today.strftime("%Y-%m"))
        today += relativedelta(months=1)

    # Investment simulation
    balance = current_amount
    balances = []
    contributions = []
    interests = []
    total_contributions = []
    cumulative_contributions = 0
    current_monthly_contribution = monthly_contribution

    for i, date in enumerate(dates):
        interest = balance * monthly_return_rate
        contribution = current_monthly_contribution if i > 0 else 0
        
        # Add extra yearly investment in December
        if i > 0 and (datetime.strptime(date, "%Y-%m").month == 12):
            contribution += current_monthly_contribution * extra_yearly_multiplier
        
        balance += interest + contribution
        cumulative_contributions += contribution

        # Increase contribution annually
        if i > 0 and (datetime.strptime(date, "%Y-%m").month == 1):
            current_monthly_contribution *= (1 + yearly_increase_rate)

        balances.append(round(balance, 2))
        contributions.append(round(contribution, 2))
        interests.append(round(interest, 2))
        total_contributions.append(round(cumulative_contributions, 2))

    data = {
        "Date": dates,
        "Balance": balances,
        "Contributions": contributions,
        "Interest Earned": interests,
        "Total Contributions": total_contributions
    }

    return pd.DataFrame(data)

# Streamlit app setup
st.title("Investment Growth Simulator")
st.sidebar.header("Input Parameters")

# User inputs
current_amount = st.sidebar.number_input("Current Investment Amount ($)", min_value=0.0, value=1000.0, step=100.0)
monthly_contribution = st.sidebar.number_input("Monthly Contribution ($)", min_value=0.0, value=100.0, step=10.0)
yearly_increase_rate = st.sidebar.number_input("Yearly Increase Rate for Contribution (%)", min_value=0.0, value=2.0, step=0.1) / 100
yearly_return = st.sidebar.number_input("Expected Yearly Return Rate (%)", min_value=0.0, value=5.0, step=0.1) / 100
extra_yearly_multiplier = st.sidebar.slider("Extra Yearly Investment Multiplier (x Monthly Contribution)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
target_date = st.sidebar.date_input("Target Date", value=datetime.today().replace(day=1) + relativedelta(years=10),
                                     max_value= datetime.today().replace(month=12,day=31, year = 2085))

# Calculate growth
data = calculate_investment_growth(current_amount, monthly_contribution, yearly_increase_rate, yearly_return, extra_yearly_multiplier, target_date)

# Visualization
st.header("Investment Growth Over Time")
fig, ax = plt.subplots()
ax.plot(data["Date"], data["Balance"], label="Total Balance", color="green")
ax.fill_between(range(len(data["Date"])), data["Balance"], color="green", alpha=0.3)
ax.plot(data["Date"], data["Total Contributions"], label="Total Contributions", color="red")
ax.fill_between(range(len(data["Date"])), data["Total Contributions"], color="green", alpha=0)
ax.set_title("Projected Investment Growth")
ax.set_xlabel("Date")
ax.set_ylabel("Amount ($)")

num_dates = len(data["Date"])
if num_dates > 24:
    tick_step = num_dates // 12  # Show approximately one tick per year
elif num_dates > 6:
    tick_step = num_dates // 6  # Show approximately 6 ticks
else:
    tick_step = 1  # Show all ticks for short periods

tick_positions = list(range(0, num_dates, tick_step))
ax.set_xticks(tick_positions)
ax.set_xticklabels([data["Date"][i] for i in tick_positions], rotation=45)

ax.legend()
st.pyplot(fig)

# Table output
st.subheader("Detailed Breakdown")
st.dataframe(data)
