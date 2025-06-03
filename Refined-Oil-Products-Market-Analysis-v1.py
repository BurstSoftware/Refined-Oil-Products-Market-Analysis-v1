import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.linear_model import LinearRegression
import datetime

# Streamlit app configuration
st.set_page_config(page_title="Refined Oil Products Market Analysis", layout="wide")

# Title and description
st.title("Refined Oil Products Market Analysis and Forecasting")
st.markdown("""
This app provides forecasts, supply/demand balances, and market commentary for refined oil products (e.g., Gasoline, Diesel, Jet Fuel, etc.) through 2030. 
Use the sidebar to select products and explore data, forecasts, and investment insights.
""")

# Sidebar for user inputs
st.sidebar.header("Analysis Parameters")
product = st.sidebar.selectbox(
    "Select Refined Oil Product",
    ["Gasoline", "Diesel", "Jet Fuel", "Fuel Oils", "Lubricating Oil", "Asphalt", "LPG"]
)
forecast_horizon = st.sidebar.slider("Forecast Horizon (Years)", 2025, 2030, 2030)
analysis_type = st.sidebar.radio("Analysis Type", ["Price Forecast", "Supply/Demand Balance", "Market Commentary"])

# Synthetic data generation (replace with real data source)
np.random.seed(42)
dates = pd.date_range(start="2020-01-01", end="2024-12-31", freq="M")
data = {
    "Date": dates,
    "Gasoline_Price": np.random.normal(2.5, 0.3, len(dates)),
    "Diesel_Price": np.random.normal(2.8, 0.4, len(dates)),
    "Jet_Fuel_Price": np.random.normal(2.2, 0.35, len(dates)),
    "Fuel_Oils_Price": np.random.normal(1.8, 0.25, len(dates)),
    "Lubricating_Oil_Price": np.random.normal(3.0, 0.5, len(dates)),
    "Asphalt_Price": np.random.normal(1.5, 0.2, len(dates)),
    "LPG_Price": np.random.normal(1.2, 0.15, len(dates)),
    "Gasoline_Supply": np.random.normal(100, 10, len(dates)),
    "Gasoline_Demand": np.random.normal(95, 12, len(dates)),
    "Diesel_Supply": np.random.normal(80, 8, len(dates)),
    "Diesel_Demand": np.random.normal(82, 9, len(dates)),
}
df = pd.DataFrame(data)
df["Year"] = df["Date"].dt.year

# Forecasting function
def forecast_prices(df, product, forecast_horizon):
    price_col = f"{product}_Price"
    X = np.array(df["Year"]).reshape(-1, 1)
    y = df[price_col]
    
    # Linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Forecast future years
    future_years = np.array(range(df["Year"].max() + 1, forecast_horizon + 1)).reshape(-1, 1)
    forecast_prices = model.predict(future_years)
    
    # Create forecast DataFrame
    forecast_df = pd.DataFrame({
        "Year": range(df["Year"].max() + 1, forecast_horizon + 1),
        "Forecasted_Price": forecast_prices
    })
    return forecast_df

# Supply and Demand Balance
def supply_demand_balance(df, product):
    supply_col = f"{product}_Supply"
    demand_col = f"{product}_Demand"
    balance = df[supply_col] - df[demand_col]
    return pd.DataFrame({
        "Date": df["Date"],
        "Supply": df[supply_col],
        "Demand": df[demand_col],
        "Balance": balance
    })

# Main content based on analysis type
if analysis_type == "Price Forecast":
    st.header(f"{product} Price Forecast through {forecast_horizon}")
    
    # Plot historical and forecasted prices
    forecast_df = forecast_prices(df, product, forecast_horizon)
    historical_fig = px.line(df, x="Date", y=f"{product}_Price", title=f"{product} Historical Prices")
    forecast_fig = px.line(forecast_df, x="Year", y="Forecasted_Price", title=f"{product} Price Forecast")
    
    st.plotly_chart(historical_fig, use_container_width=True)
    st.plotly_chart(forecast_fig, use_container_width=True)
    
    st.write(f"**Forecast Insights**: Based on historical trends, {product} prices are projected to follow a linear trend. Adjust model parameters or incorporate additional factors (e.g., geopolitical events, supply shocks) for more accurate forecasts.")

elif analysis_type == "Supply/Demand Balance":
    st.header(f"{product} Supply and Demand Balance")
    
    # Calculate and plot supply/demand balance
    balance_df = supply_demand_balance(df, product)
    fig = px.line(balance_df, x="Date", y=["Supply", "Demand"], title=f"{product} Supply vs. Demand")
    st.plotly_chart(fig, use_container_width=True)
    
    fig_balance = px.bar(balance_df, x="Date", y="Balance", title=f"{product} Supply-Demand Balance")
    st.plotly_chart(fig_balance, use_container_width=True)
    
    st.write(f"**Balance Insights**: Positive balance indicates surplus; negative indicates shortage. Monitor for market-moving events like refinery outages or demand spikes.")

elif analysis_type == "Market Commentary":
    st.header(f"{product} Market Commentary")
    
    # Example commentary (replace with real-time data or analysis)
    st.markdown(f"""
    ### Daily Market Update for {product}
    - **Price Drivers**: Recent price movements in {product} are driven by [e.g., seasonal demand, refinery maintenance schedules, or geopolitical tensions]. 
    - **Supply/Demand Dynamics**: Current supply is [stable/tight], with demand influenced by [e.g., economic growth, transportation trends].
    - **Investment/Hedging Strategy**: Consider [e.g., long positions in {product} futures for Q1 2026 due to expected demand growth or hedging against supply disruptions].
    - **Key Events to Watch**: Monitor [e.g., OPEC meetings, EIA inventory reports, or regulatory changes] for potential market impacts.
    """)
    
    st.write("**Note**: This is a placeholder commentary. Integrate real-time data from sources like EIA, Bloomberg, or X posts for accurate insights.")

# Footer
st.markdown("""
---
**About**: This app is designed for the Commodities Research Team to analyze refined oil product markets, forecast prices, and provide investment insights. 
Contact the Macro Research team for custom analyses or data integration.
""")
