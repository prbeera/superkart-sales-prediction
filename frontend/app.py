
import streamlit as st
import pandas as pd
import requests


# ---------------------------------------------------------
# Backend API URL
# ---------------------------------------------------------

BACKEND_URL = "http://localhost:7860"


# ---------------------------------------------------------
# Streamlit App
# ---------------------------------------------------------

st.title("SuperKart Sales Prediction")

st.write(
    """
    Predict the expected sales revenue of a product in a SuperKart
    store based on product and store characteristics.
    """
)


# =========================================================
# ONLINE PREDICTION
# =========================================================

st.subheader("Online Prediction")


# ---------------------------------------------------------
# Product Information
# ---------------------------------------------------------

st.markdown("### Product Details")

product_weight = st.number_input(
    "Product Weight",
    min_value=4.0,
    max_value=22.0,
    value=12.65,
    step=0.01
)


product_sugar_content = st.selectbox(
    "Product Sugar Content",
    [
        "Low Sugar",
        "Regular",
        "No Sugar"
    ]
)


product_allocated_area = st.number_input(
    "Product Allocated Area",
    min_value=0.004,
    max_value=0.298,
    value=0.068,
    step=0.001
)


product_type = st.selectbox(
    "Product Type",
    [
        "Fruits and Vegetables",
        "Snack Foods",
        "Frozen Foods",
        "Dairy",
        "Household",
        "Baking Goods",
        "Canned",
        "Health and Hygiene",
        "Meat",
        "Soft Drinks",
        "Breads",
        "Hard Drinks",
        "Others",
        "Starchy Foods",
        "Breakfast",
        "Seafood"
    ]
)


product_mrp = st.number_input(
    "Product MRP",
    min_value=31.0,
    max_value=266.0,
    value=147.0,
    step=0.01
)


# ---------------------------------------------------------
# Store Information
# ---------------------------------------------------------

st.markdown("### Store Details")


store_id = st.selectbox(
    "Store ID",
    [
        "OUT001",
        "OUT002",
        "OUT003",
        "OUT004"
    ]
)


store_establishment_year = st.selectbox(
    "Store Establishment Year",
    [
        1987,
        1998,
        2009
    ]
)


store_size = st.selectbox(
    "Store Size",
    [
        "Small",
        "Medium",
        "High"
    ]
)


store_location_city_type = st.selectbox(
    "Store Location City Type",
    [
        "Tier 1",
        "Tier 2",
        "Tier 3"
    ]
)


store_type = st.selectbox(
    "Store Type",
    [
        "Departmental Store",
        "Supermarket Type1",
        "Supermarket Type2",
        "Food Mart"
    ]
)


# =========================================================
# CREATE INPUT DATA
# =========================================================

input_data = pd.DataFrame([{
    "Product_Weight": product_weight,
    "Product_Sugar_Content": product_sugar_content,
    "Product_Allocated_Area": product_allocated_area,
    "Product_Type": product_type,
    "Product_MRP": product_mrp,
    "Store_Id": store_id,
    "Store_Establishment_Year": store_establishment_year,
    "Store_Size": store_size,
    "Store_Location_City_Type": store_location_city_type,
    "Store_Type": store_type
}])


# =========================================================
# ONLINE PREDICTION
# =========================================================

if st.button("Predict Sales", type="primary"):

    try:

        response = requests.post(
            f"{BACKEND_URL}/v1/sales",
            json=input_data.to_dict(orient="records")[0]
        )

        if response.status_code == 200:

            prediction = response.json()["Predicted Sales"]

            st.success(
                f"Predicted Product Store Sales: ${prediction:,.2f}"
            )

        else:

            st.error(
                f"Prediction API returned an error: "
                f"{response.text}"
            )

    except requests.exceptions.RequestException:

        st.error(
            "Unable to connect to the SuperKart prediction API."
        )


# =========================================================
# BATCH PREDICTION
# =========================================================

st.subheader("Batch Prediction")

st.write(
    "Upload a CSV file containing multiple product-store records "
    "to generate sales predictions in bulk."
)


uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"]
)


if uploaded_file is not None:

    if st.button("Predict Batch", type="primary"):

        try:

            response = requests.post(
                f"{BACKEND_URL}/v1/salesbatch",
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file,
                        "text/csv"
                    )
                }
            )

            if response.status_code == 200:

                predictions = response.json()

                st.success(
                    "Batch predictions completed successfully!"
                )

                prediction_df = pd.DataFrame(predictions)

                st.dataframe(
                    prediction_df,
                    use_container_width=True
                )

            else:

                st.error(
                    f"Batch prediction API returned an error: "
                    f"{response.text}"
                )

        except requests.exceptions.RequestException:

            st.error(
                "Unable to connect to the SuperKart prediction API."
            )
