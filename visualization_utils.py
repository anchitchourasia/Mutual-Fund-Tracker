import streamlit as st
import pandas as pd

# Function to create a stylish bar chart of Market Value over time
def plot_market_value_over_time(data):
    try:
        # Ensure 'Market Value' is numeric
        data["Market Value"] = pd.to_numeric(data["Market Value"], errors='coerce')
        # Drop NaN values
        data = data.dropna(subset=["Market Value"])
        
        # Group data by 'Date' and sum the market values
        data_grouped = data.groupby("Date")["Market Value"].sum().reset_index()

        # Display the data before plotting for debugging purposes
        st.write("Data for plotting:", data_grouped)

        # Display the Bar Chart
        st.subheader("Market Value Over Time (Bar Chart)")

        # Use Streamlit's bar_chart function for a quick plot
        st.bar_chart(data_grouped.set_index('Date')['Market Value'], use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating bar chart: {e}")
