import streamlit as st
import pandas as pd
import requests
from typing import List, Optional

# Configuration variables
DATA_FILE = "inventory_data.csv"
EXPIRY_THRESHOLD = 10  # Days before expiry
SLOW_MOVING_THRESHOLD = 5  # Sales threshold for slow-moving stock
STOCK_THRESHOLD = 0  # Minimum stock required for recommendations

# Load inventory data
@st.cache_data
def load_data(file_type: str = "csv") -> pd.DataFrame:
    if file_type == "csv":
        return pd.read_csv(DATA_FILE)
    elif file_type == "json":
        return pd.read_json(DATA_FILE)
    return pd.DataFrame()

# Placeholder function simulating Intel OPEA summarization API
def summarize_user_input_with_opea(user_text: str, df: pd.DataFrame) -> Optional[List[str]]:
    user_text_lower = user_text.lower()
    
    # Hardcoded mapping (later replace with OPEA API)
    product_mapping = {
        "milk": ["Milk"],
        "juice": ["Juice"],
        "bread": ["Bread"],
        "yogurt": ["Yogurt"],
        "cheese": ["Cheese"],
        "butter": ["Butter"],
        "dairy": ["Milk", "Yogurt", "Cheese", "Butter"],
        "beverages": ["Juice", "Soda"],
        "snacks": ["Chips", "Cookies"],
        "bakery": ["Bread", "Cake"]
    }
    
    matched_products = []
    for key, products in product_mapping.items():
        if key in user_text_lower:
            matched_products.extend(products)

    # Ensure only valid inventory products are returned
    valid_products = df["product_name"].unique()
    matched_products = [p for p in matched_products if p in valid_products]

    return matched_products if matched_products else None

# Function for Intel OPEA API integration (Commented for now)
def summarize_user_input_with_opea_api(user_text: str) -> Optional[List[str]]:
    """ Uncomment and replace placeholder values to integrate Intel OPEA API """
    """
    url = "https://opea.intel.com/api/summarize"  # Replace with real API endpoint
    headers = {"Authorization": "Bearer YOUR_OPEA_API_KEY"}  # Replace with your API key
    payload = {"user_input": user_text}

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("product_names", [])  # Assuming API returns list of product names
    
    return None
    """

# Generate recommendations based on expiry, sales, and stock criteria, then sort results
def get_recommendations(df: pd.DataFrame, products: List[str]) -> pd.DataFrame:
    filtered_df = df[df["product_name"].isin(products)]
    
    near_expiry = filtered_df[filtered_df["days_to_expiry"] <= EXPIRY_THRESHOLD]
    slow_moving = filtered_df[filtered_df["sales_last_week"] <= SLOW_MOVING_THRESHOLD]
    
    recommendations = pd.concat([near_expiry, slow_moving]).drop_duplicates()
    recommendations = recommendations[recommendations["stock_left"] > STOCK_THRESHOLD]
    
    # Apply correct sorting: First by expiry (ascending), then by stock availability (descending)
    recommendations = recommendations.sort_values(by=["days_to_expiry", "stock_left"], ascending=[True, False])
    
    return recommendations

# Streamlit UI
st.title("Retail AI Recommendation System with Intel OPEA")
st.write("Personalized recommendations powered by Intel AI")

# Load inventory data
df = load_data()
st.subheader("Full Inventory Data")
st.dataframe(df)

# User natural text input
user_text = st.text_area("Describe what you're looking for (e.g., I need fresh dairy products)")

if user_text:  # Show recommendations ONLY after user enters text
    matched_products = summarize_user_input_with_opea(user_text, df)
    
    # Uncomment this line once OPEA API is ready for integration
    # matched_products = summarize_user_input_with_opea_api(user_text)

    if matched_products:
        st.subheader("Matching Products in Inventory")
        st.dataframe(df[df["product_name"].isin(matched_products)])

        recommended_df = get_recommendations(df, matched_products)
        if not recommended_df.empty:
            st.subheader("Recommended Products (Sorted: Near-expiry first, High-stock next)")
            st.dataframe(recommended_df)
        else:
            st.write("No matching recommendations available!")
    else:
        st.write("No relevant products found in inventory!")
