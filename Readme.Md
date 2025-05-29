Retail AI Recommendation System with Intel OPEA
📌 Overview
The Retail AI Recommendation System leverages Intel OPEA AI to provide personalized product recommendations based on inventory insights. It automatically suggests slow-moving and near-expiry products, applying dynamic discounts based on expiry date.

🛠️ Technologies Used
Backend & AI Processing
Intel OPEA API → Summarizes user input into structured product names

Pandas & NumPy → Efficient inventory data handling

Streamlit → Lightweight UI for real-time interaction

FastAPI / Flask (Optional) → Microservices-based deployment

Intel Tiber AI Cloud → Scalable hosting for AI processing

Data & Recommendation Logic
Dynamic Discount Algorithm → Discounts range 10%-50% based on expiry

Sorting Algorithm → Prioritizes near-expiry first, then high-stock

Stock Analytics → Monitors inventory, sales trends & expiry status

Frontend UI
Streamlit UI → Displays full inventory, product filtering & cart suggestions

D3.js (Optional) → Enhances product price visualization

📂 File Structure
📦 Retail-AI-Recommendation
 ┣ 📂 data
 ┃ ┣ 📜 inventory_data.csv   # Inventory file (CSV format)
 ┣ 📜 app.py                 # Main application script
 ┣ 📜 requirements.txt       # Required dependencies
 ┣ 📜 README.md              # Documentation
📌 Installation
Ensure you have Python 3.8+ installed. Then, install dependencies:

bash
pip install streamlit pandas requests numpy
🚀 How to Run
Start the application with:

bash
streamlit run app.py
User Flow: ✅ Enter natural-language queries (e.g., "I need dairy products") ✅ Intel OPEA API maps input to valid inventory product names ✅ Slow-moving & near-expiry items are recommended ✅ Dynamic discounts applied based on expiry ✅ Sorted inventory displayed in UI

📌 Configuration Variables
Modify in app.py:

python
EXPIRY_THRESHOLD = 10  # Expiring in ≤ X days
SLOW_MOVING_THRESHOLD = 5  # Sales threshold for slow-moving stock
STOCK_THRESHOLD = 0  # Minimum stock required for recommendations
🔗 API Integration (Intel OPEA)
Once Intel OPEA integration is ready, uncomment:

python
def summarize_user_input_with_opea_api(user_text: str) -> Optional[List[str]]:
    url = "https://opea.intel.com/api/summarize"
    headers = {"Authorization": "Bearer YOUR_OPEA_API_KEY"}
    payload = {"user_input": user_text}
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("product_names", [])
    
    return None
🎯 Future Enhancements
✅ Real-time Stock Updates (Webhooks, Kafka) ✅ Advanced Pricing Models (AI-based optimization) ✅ Retail Dashboard with Analytics
