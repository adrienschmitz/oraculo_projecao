import requests
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "a36affd9-0de8-4009-8a58-c7ed169b3a6e"
FLOW_ID = "32e91124-167c-4e96-97f7-3f4d388bee25"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "oraculo" # The endpoint name of the flow


def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}", "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    st.image("logo_padrao.png", width=100) 
    st.title("Oráculo")
    container = st.container(border=True)
    container.write("Você pode perguntar sobre senhas de wi-fi (local, SSID, senha, IP, MAC)") 
    container.write("Sobre pastas de rede (local, usuario, senha)")
    container.write("Sobre outras senhas (dominio, manuteção, optix, antivirus, etc.)")
    container.write("Sobre procedimentos (configuração de impressora, range de IP, SMB, etc.)")
    
    message = st.text_area("mensagem", placeholder="Pergunte algo...", label_visibility="hidden")
    
    if st.button("Enviar"):
        if not message.strip():
            st.error("Por favor, escreva a mensagem")
            return
    
        try:
            with st.spinner("Deixe-me ver..."):
                response = run_flow(message)
            
            response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(response)
        except Exception as e:
            st.error(str(e))
    st.divider()
    footer_html = """<div style='text-align: center; font-size: 12px'>
    <p>Adrien Schmitz -  2025 - V. 0.5</p>
    </div>"""
    st.markdown(footer_html, unsafe_allow_html=True,)
            


if __name__ == "__main__":
    main()