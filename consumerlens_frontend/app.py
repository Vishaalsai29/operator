import streamlit as st
import openai
import weaviate
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Streamlit Sidebar for Key Input
st.sidebar.header("Settings")
with st.sidebar.form(key="api_keys_form"):
    openai_key = st.text_input(
        "Enter your OpenAI API Key",
        value=os.getenv("OPENAI_API_KEY", ""),  # Load from environment if available
        type="password",
        help="Your OpenAI API key for accessing GPT models.",
    )
    weaviate_url = st.text_input(
        "Enter Weaviate URL",
        value=os.getenv("WEAVIATE_URL", ""),  # Load from environment if available
        help="The URL of your Weaviate instance.",
    )
    weaviate_api_key = st.text_input(
        "Enter Weaviate API Key",
        value=os.getenv("WEAVIATE_API_KEY", ""),  # Load from environment if available
        type="password",
        help="API key for authenticating with Weaviate.",
    )
    submit_button = st.form_submit_button(label="Save Settings")

# Save keys in session state
if submit_button:
    st.session_state["openai_key"] = openai_key
    st.session_state["weaviate_url"] = weaviate_url
    st.session_state["weaviate_api_key"] = weaviate_api_key
    st.success("Keys saved successfully!")

# Use OpenAI Key
if "openai_key" in st.session_state:
    openai.api_key = st.session_state["openai_key"]
    st.sidebar.write("✅ OpenAI Key set!")

# Connect to Weaviate
try:
    # Initialize Weaviate client with API key authentication
    client = weaviate.Client(
        url=st.session_state["weaviate_url"],
        auth_client_secret=weaviate.AuthApiKey(api_key=st.session_state["weaviate_api_key"]),
    )

    # Check if the client is ready
    if client.is_ready():
        st.sidebar.write("✅ Connected to Weaviate!")
    else:
        st.sidebar.write("❌ Failed to connect to Weaviate.")
except Exception as e:
    st.sidebar.error(f"Error connecting to Weaviate: {e}")

# Sample OpenAI API Request
if "openai_key" in st.session_state:
    st.subheader("Test OpenAI GPT Request")
    user_input = st.text_input("Enter your prompt")
    if st.button("Send"):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": user_input},
                ],
                max_tokens=100,
            )
            st.write(response["choices"][0]["message"]["content"].strip())
        except openai.error.OpenAIError as e:
            st.error(f"OpenAI API Error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# Sample Weaviate Query
if "weaviate_url" in st.session_state and "weaviate_api_key" in st.session_state:
    st.subheader("Test Weaviate Query")
    class_name = st.text_input("Enter Weaviate class name")
    if st.button("Retrieve Data"):
        try:
            query = f"""
            {{
                Get {{
                    {class_name} {{
                        name
                    }}
                }}
            }}
            """
            result = client.query.raw(query)
            st.json(result)
        except Exception as e:
            st.error(f"Weaviate Query Error: {e}")
