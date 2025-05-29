import streamlit as st
import pandas as pd
import random
from typing import List, Optional

# Configuration variables
DATA_FILE = "inventory_data.csv"
EXPIRY_THRESHOLD = 10  
SLOW_MOVING_THRESHOLD = 5  
STOCK_THRESHOLD = 0  

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

    valid_products = df["product_name"].unique()
    matched_products = [p for p in matched_products if p in valid_products]

    return matched_products if matched_products else None

# Apply dynamic discounts based on expiry date
def apply_dynamic_discount(df: pd.DataFrame) -> pd.DataFrame:
    def calculate_discount(days_left):
        discount_range = max(10, min(50, (10 - days_left) * 5))  # Scaling discount from 10% to 50%
        return random.randint(int(discount_range * 0.8), int(discount_range))  # Randomized

    df["discount_percentage"] = df["days_to_expiry"].apply(calculate_discount)
    df["discounted_price"] = df["original_mrp"] * (1 - df["discount_percentage"] / 100)
    
    return df

# Generate recommendations based on expiry, sales, and stock criteria, then sort results
def get_recommendations(df: pd.DataFrame, products: List[str]) -> pd.DataFrame:
    filtered_df = df[df["product_name"].isin(products)]
    
    near_expiry = filtered_df[filtered_df["days_to_expiry"] <= EXPIRY_THRESHOLD]
    slow_moving = filtered_df[filtered_df["sales_last_week"] <= SLOW_MOVING_THRESHOLD]
    
    recommendations = pd.concat([near_expiry, slow_moving]).drop_duplicates()
    recommendations = recommendations[recommendations["stock_left"] > STOCK_THRESHOLD]
    
    recommendations = apply_dynamic_discount(recommendations)  # Apply discount logic

    # Sorting: First by expiry (ascending), then by stock availability (descending)
    recommendations = recommendations.sort_values(by=["days_to_expiry", "stock_left"], ascending=[True, False])
    
    return recommendations

# Streamlit UI
st.title("Retail AI Recommendation System with Intel OPEA")
st.write("Personalized recommendations powered by Intel AI")

df = load_data()
st.subheader("Full Inventory Data")
st.dataframe(df)

user_text = st.text_area("Describe what you're looking for (e.g., I need fresh dairy products)")

if user_text:
    matched_products = summarize_user_input_with_opea(user_text, df)
    
    if matched_products:
        st.subheader("Matching Products in Inventory")
        st.dataframe(df[df["product_name"].isin(matched_products)])

        recommended_df = get_recommendations(df, matched_products)
        if not recommended_df.empty:
            st.subheader("Recommended Products (Sorted: Near-expiry first, High-stock next)")
            st.dataframe(recommended_df[["product_name", "vendor_name", "days_to_expiry", "stock_left", "original_mrp", "discount_percentage", "discounted_price"]])
        else:
            st.write("No matching recommendations available!")
    else:
        st.write("No relevant products found in inventory!")
