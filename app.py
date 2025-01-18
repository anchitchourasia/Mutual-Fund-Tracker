import streamlit as st
import pandas as pd
from visualization_utils import plot_market_value_over_time  # Importing the visualization function

# Function to clean and extract data from uploaded Excel sheets
def clean_data(df, date):
    try:
        header_row = df[df.iloc[:, 2].str.contains("Name of the Instrument", na=False)].index[0]
        cleaned_df = df.iloc[header_row + 1:].reset_index(drop=True)
        cleaned_df.columns = df.iloc[header_row]
        cleaned_df = cleaned_df.dropna(how='all').reset_index(drop=True)
        cleaned_df["Date"] = date  # Add the date column for comparison
        return cleaned_df
    except Exception as e:
        st.error(f"Error cleaning data: {e}")
        return pd.DataFrame()

# Function to standardize and preprocess the data
def standardize_columns(df):
    try:
        df = df.rename(columns={
            "Name of the Instrument": "Instrument",
            "Market value\n(Rs. in Lakhs)": "Market Value",
            "Quantity": "Quantity",
            "% to NAV": "Percent to NAV",
            "ISIN": "ISIN"
        })
        return df[["Instrument", "ISIN", "Quantity", "Market Value", "Percent to NAV", "Date"]]
    except Exception as e:
        st.error(f"Error standardizing columns: {e}")
        return pd.DataFrame()

# Streamlit App
def main():
    st.title("Mutual Fund Allocation Change Tracker")
    st.write("Upload mutual fund portfolio files to analyze and compare allocation changes.")

    # Input fields for the user
    fund_name = st.text_input("Enter Fund Name (optional):")
    date_range = st.date_input("Select Date Range", [])

    # File uploader for multiple files
    files = st.file_uploader("Upload Portfolio Files (one per month)", type=["xlsx"], accept_multiple_files=True)

    # Check if files are uploaded and date range is selected
    if files and len(date_range) > 0:
        datasets = []

        for i, (file, date) in enumerate(zip(files, date_range)):
            st.write(f"Processing file {i+1}/{len(files)}: {file.name}")
            try:
                # Read the file and clean the data
                df = pd.ExcelFile(file).parse(sheet_name=0)
                cleaned = clean_data(df, date.strftime("%Y-%m-%d"))
                standardized = standardize_columns(cleaned)
                datasets.append(standardized)
                st.write(f"File {file.name} processed successfully!")
            except Exception as e:
                st.error(f"Error processing file {file.name}: {e}")
        
        # If datasets have been processed, show the combined data
        if datasets:
            combined_data = pd.concat(datasets, ignore_index=True)
            st.subheader("Combined Data")
            st.write(combined_data)  # Display the combined data in Streamlit

            # Optionally, filter data by fund name
            if fund_name:
                filtered_data = combined_data[combined_data["Instrument"].str.contains(fund_name, na=False)]
                st.subheader(f"Filtered Data for {fund_name}")
                st.write(filtered_data)

            # Provide download option
            csv = combined_data.to_csv(index=False)
            st.download_button(
                label="Download Combined Data as CSV",
                data=csv,
                file_name="combined_data.csv",
                mime="text/csv"
            )

            # Visualization: Market Value Over Time (Bar Chart)
            plot_market_value_over_time(combined_data)
        else:
            st.warning("No data to process. Please check the uploaded files.")
    else:
        st.info("Please upload files and select a valid date range to proceed.")

if __name__ == "__main__":
    main()
