import streamlit as st
import yfinance as yf
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Inicializar el chatbot
chatbot = ChatBot('Malicia')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.spanish')  # Entrena el chatbot en español

def fetch_stock_data(ticker):
    """Obtiene datos de acciones usando yfinance"""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1mo")  # Obtiene datos del último mes
        return data
    except Exception as e:
        return f"Error al obtener datos: {e}"

def generate_response(user_input):
    """Genera una respuesta del chatbot"""
    response = chatbot.get_response(user_input)
    return response

def main():
    st.title("Malicia - ChatBot Financiero")

    st.sidebar.header("Configuración")
    ticker = st.sidebar.text_input("Ingrese el ticker de la acción (por ejemplo, AAPL)")

    user_input = st.text_input("Hable con Malicia:")

    if st.button("Obtener Datos de Acción"):
        if ticker:
            data = fetch_stock_data(ticker)
            st.write(data)
        else:
            st.write("Por favor, ingrese un ticker.")

    if user_input:
        response = generate_response(user_input)
        st.write("Malicia dice:", response)

if __name__ == "__main__":
    main()
