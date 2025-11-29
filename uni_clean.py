import streamlit as st
import pandas as pd
import warnings
import io

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Order Data Cleaner", layout="wide")

st.title("📦 Order Data Cleaning Application")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")

    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Required columns
    sel_columns = [
        'Sale Order Item Code', 'Display Order Code', 'COD', 'Category',
        'Invoice Created', 'Item SKU Code', 'Channel Product Id',
        'Channel Name', 'Total Price', 'Selling Price', 'Subtotal',
        'Packet Number', 'Order Date as dd/mm/yyyy hh:MM:ss',
        'Sale Order Code', 'Shipping provider', 'Shipping Courier',
        'Shipping Package Code', 'Tracking Number', 'Dispatch Date',
        'Combination Description', 'Bundle SKU Code Number', 'Batch Code',
        'Seller SKU Code'
    ]

    missing = [col for col in sel_columns if col not in df.columns]
    
    if missing:
        st.error(f"❌ Missing columns: {missing}")
    else:
        data = df[sel_columns].copy()

        # Apply cleaning steps
        data['Bundle SKU Code Number'] = data['Bundle SKU Code Number'].replace(" ", pd.NA)
        data['Bundle SKU Code Number'] = data['Bundle SKU Code Number'].fillna(data['Item SKU Code'])

        data['Tracking Number'] = data['Tracking Number'].astype(str)

        # Clean Dispatch Date
        data['Dispatch Date'] = pd.to_datetime(data['Dispatch Date'], errors='coerce').dt.strftime('%d-%m-%Y')

        # Convert Dispatch Date back to datetime for range calculation
        dispatch_date_dt = pd.to_datetime(data['Dispatch Date'], format='%d-%m-%Y', errors='coerce')

        # Calculate min and max Dispatch Date
        dispatch_date_range = (dispatch_date_dt.min(), dispatch_date_dt.max())

        # Format date range for file name
        start_date_str = dispatch_date_range[0].strftime('%d-%m-%Y')
        end_date_str = dispatch_date_range[1].strftime('%d-%m-%Y')
        file_name = f"cleaned_orders_{start_date_str}_to_{end_date_str}.xlsx"

        # Display Dispatch Date range
        st.subheader("📅 Dispatch Date Range")
        st.markdown(f"**Dispatch Date:** {start_date_str} → {end_date_str}")

        # Show preview of cleaned data
        st.subheader("Cleaned Data Preview")
        st.dataframe(data.head(20))

        # Convert DataFrame to Excel in memory
        buffer = io.BytesIO()
        data.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)

        # Download button for Excel
        st.download_button(
            label="⬇️ Download Cleaned Excel",
            data=buffer,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


