import streamlit as st
from streamlit_chat import message
import yfinance as yf

# Create a placeholder for chat history
if 'history' not in st.session_state:
    st.session_state.history = []

# Function to fetch stock information
def get_stock_info(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return (
            f"**{info['shortName']} ({info['symbol']})**\n"
            f"Precio: ${info['regularMarketPrice']}\n"
            f"Capitalización de mercado: {info['marketCap']}\n"
            f"Relación P/E: {info['forwardEps']}\n"
            f"Rendimiento de dividendos: {info['dividendYield']*100:.2f}%\n"
        )
    except Exception as e:
        return f"Lo siento, no pude obtener información para {ticker}. Error: {str(e)}"

# Function to handle chatbot response
def get_chatbot_response(user_input):
    if user_input.startswith("acción:"):
        ticker = user_input.split(":", 1)[1].strip().upper()
        return get_stock_info(ticker)
    elif "hola" in user_input.lower():
        return "¡Hola! Soy Malicia. ¿Qué querés saber sobre acciones hoy?"
    elif "gracias" in user_input.lower():
        return "¡De nada! Si necesitás más información, acá estoy para ayudarte."
    elif "che" in user_input.lower():
        return "Che, mirá esto: Para información sobre acciones, empezá tu mensaje con 'acción:'."
    else:
        return (
            "Dale, preguntame algo sobre acciones. "
            "Podés empezar tu mensaje con 'acción:'. Por ejemplo, 'acción: AAPL'."
        )

# Display chat history
for chat in st.session_state.history:
    message(chat['text'], is_user=chat['is_user'])

# Input box for user to type message
user_input = st.text_input("Vos:", key="user_input_key")

if user_input:
    # Add user message to chat history
    st.session_state.history.append({"text": f"Vos: {user_input}", "is_user": True})
    
    # Get chatbot response
    bot_response = get_chatbot_response(user_input)
    
    # Add chatbot response to chat history
    st.session_state.history.append({"text": f"Malicia: {bot_response}", "is_user": False})
    
    # Clear the input box by updating the session state
    st.session_state.user_input_key = ""  # Ensure the key used for input box matches

# Optionally, you can ensure the input box shows the cleared value
st.text_input("Vos:", value=st.session_state.get('user_input_key', ''), key="user_input_key")
