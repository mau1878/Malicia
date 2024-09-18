import streamlit as st
import yfinance as yf
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

# Initialize the Streamlit app
st.title("Malicia - Your Stock Chatbot")

# Initialize the model and tokenizer
@st.cache_resource
def load_model():
    model_name = "facebook/blenderbot-400M-distill"  # Adjust to a compatible model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    chatbot = pipeline("conversational", model=model, tokenizer=tokenizer)
    return chatbot

chatbot = load_model()

# Function to fetch stock data
def fetch_stock_data(ticker):
    """Fetch stock data using yfinance"""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        return data
    except Exception as e:
        st.error(f"Error fetching data for ticker {ticker}: {e}")
        return None

# Sidebar for user input
st.sidebar.header("User Input")
ticker = st.sidebar.text_input("Enter stock ticker (e.g., AAPL):").upper()
user_input = st.sidebar.text_area("Your message:")

# Display stock data
if ticker:
    data = fetch_stock_data(ticker)
    if data is not None:
        st.write(f"### Data for {ticker}")
        st.dataframe(data)

# Handle chatbot interaction
if user_input:
    response = chatbot(user_input)
    st.write(f"### Chatbot Response")
    st.write(response[0]['generated_text'])

# Run Streamlit app
if __name__ == "__main__":
    st.write("Use the sidebar to interact with Malicia!")
