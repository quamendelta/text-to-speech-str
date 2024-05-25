import streamlit as st
# from audio_recorder_streamlit import audio_recorder
import openai
import base64
import os


# pip install openai streamlit を事前にインストールしておく
# OpenAIのAPIキーを取得しておく このデモでは、StreamlitのサイドバーにAPIキーを入力する形にしている

# initialize openai client
def setup_openai_client(api_key):

    return openai.OpenAI(api_key=api_key)

# taking response from the Openai
def fetch_ai_response(client, input_text):
    messages = [ {"role": "user", "content": input_text}]
    response = client.chat.completions.create(model="gpt-4o", messages=messages) #"gpt-3.5-turbo-1106"
    return response.choices[0].message.content

# text cards function
def create_text_card(text, title="Response"):
    # 改行文字を<br>タグに置き換える
    formatted_text = text.replace("\n", "<br>")
    card_html = f"""
    <style>
        .card {{
            border-radius: 10px;
            padding: 15px;
            background-color: #000080;
            margin-bottom: 10px;
        }}
        .container {{
            padding: 2px 16px;
        }}
    </style>
    <div class="card">
        <div class="container">
            <h5><b>{title}</b></h5>
            <p style="white-space: pre-wrap;">{formatted_text}</p>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    
def main():
    
    st.sidebar.title("GPTチャットアプリ")
    api_key_option = st.sidebar.radio("Choose API Key Option", ("環境変数利用", "APIキー直接入力"))

    if api_key_option == "環境変数利用":
        api_key = os.environ.get("OPENAI_API_KEY")
    else:
        api_key = st.sidebar.text_input("Enter your Open AI API Key", type="password")
 
        
    st.title("GPT-4o対話アプリ")

    # chech if api key is there
    if api_key:
        client = setup_openai_client(api_key)
            
        prompt = st.chat_input("Say something")
        if prompt:
            create_text_card(prompt, title="あなた")
            
            ai_response = fetch_ai_response(client, prompt)
            print(ai_response)

            create_text_card(ai_response, title="AI Response")

if __name__ == "__main__":
    main()