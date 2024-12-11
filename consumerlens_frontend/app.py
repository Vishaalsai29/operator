import streamlit as st
import pandas as pd
import openai
import weaviate
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set page configuration (must be the first Streamlit command)
st.set_page_config(page_title="Consumer Lens", layout="wide")

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_URL_VERBA = os.getenv("WEAVIATE_URL_VERBA")
WEAVIATE_API_KEY_VERBA = os.getenv("WEAVIATE_API_KEY_VERBA")

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

# Initialize Weaviate Client
client = None
try:
    client = weaviate.Client(
        url=WEAVIATE_URL_VERBA,
        auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY_VERBA),
    )
    # Test connection
    client.get_meta()
    st.info("Connected to Weaviate")
except Exception as e:
    st.error(f"Error connecting to Weaviate: {e}")

# Title and Description
st.title("Consumer Lens 🌟")
st.markdown(
    """
    **Empowering Consumer Protection**  
    Analyze and understand consumer complaints using Retrieval-Augmented Generation (RAG).  
    Upload datasets, query trends, and gain actionable insights with ease.  
    """
)

## Sidebar Navigation
menu = ["Query Complaints", "Upload Dataset", "Visualize Insights"]
choice = st.sidebar.selectbox("Menu", menu)

# Function: Retrieve Context from Weaviate
def retrieve_context(query, class_name="VERBA_DOCUMENTS", limit=5):
    try:
        if not client:
            st.error("Weaviate client not initialized. Check the connection.")
            return []

        # Generate embedding from OpenAI
        try:
            response = openai.Embedding.create(
                input=query,
                model="text-embedding-3-small"
            )
        except openai.error.OpenAIError as e:
            st.error(f"Failed to generate embedding: {e}")
            return []

        # Extract the embedding vector from the response
        query_vector = response['data'][0]['embedding']

        # Query Weaviate with the embedding vector
        result = client.query.get(
            class_name=class_name,
            properties=["Product", "Sub_product", "Issue"]
        ).with_near_vector({
            "vector": query_vector,
            "certainty": 0.7
        }).with_limit(limit).do()

        return result.get('data', {}).get('Get', {}).get(class_name, [])

    except Exception as e:
        st.error(f"Error retrieving context: {e}")
        return []

# Function: Generate Answer using OpenAI
def generate_answer(query, context):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant helping to analyze consumer complaints."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"},
            ],
            max_tokens=200,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Error generating answer: {e}")
        return None

# Query Complaints
if choice == "Query Complaints":
    st.header("Query Consumer Complaints")
    query = st.text_input("Enter your query", placeholder="e.g., What are the top complaint categories?")
    if st.button("Submit Query"):
        with st.spinner("Retrieving context from Weaviate..."):
            context = retrieve_context(query)
        if context:
            st.subheader("Retrieved Context")
            st.write(context)

            with st.spinner("Generating answer using OpenAI..."):
                answer = generate_answer(query, context=" ".join([item['Issue'] for item in context]))
            if answer:
                st.subheader("Generated Answer")
                st.write(answer)
        else:
            st.warning("No relevant context found.")

# Upload Dataset
elif choice == "Upload Dataset":
    st.header("Upload Dataset for Analysis")
    uploaded_file = st.file_uploader("Upload your dataset (CSV/JSON)", type=["csv", "json"])

    if uploaded_file is not None:
        try:
            # Load the dataset based on the file type
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".json"):
                df = pd.read_json(uploaded_file)

            st.success("Dataset uploaded successfully!")
            st.write("Preview of the uploaded dataset:")
            st.dataframe(df.head())

            # Rename 'Sub-product' to 'Sub_product' to conform to Weaviate's property naming rules
            df.rename(columns={"Sub-product": "Sub_product"}, inplace=True)

            # Process and load data into Weaviate
            if st.button("Process and Load Data"):
                with st.spinner("Processing and loading data into Weaviate..."):
                    try:
                        # Loop through each row in the dataset and upload to Weaviate
                        for index, row in df.iterrows():
                            data_object = {
                                "Product": row['Product'],
                                "Sub_product": row['Sub_product'],
                                "Issue": row['Issue']
                            }

                            # Add the object to Weaviate
                            client.data_object.create(
                                data_object,
                                class_name="VERBA_DOCUMENTS"
                            )

                        st.success("Data successfully loaded into Weaviate!")

                    except Exception as e:
                        st.error(f"Error loading data into Weaviate: {e}")

        except Exception as e:
            st.error(f"Error processing file: {e}")

# Visualize Insights
elif choice == "Visualize Insights":
    st.header("Visualize Complaint Trends")
    st.write("This section displays visualizations of complaint data.")
    data = {
        "Category": ["Loans", "Credit Cards", "Savings Accounts", "Mortgages", "Insurance"],
        "Complaints": [120, 95, 150, 80, 60],
    }
    df = pd.DataFrame(data)

    st.subheader("Complaints by Category")
    chart_type = st.radio("Select Chart Type", ["Bar Chart", "Line Chart", "Area Chart"])
    
    if chart_type == "Bar Chart":
        st.bar_chart(df.set_index("Category"))
    elif chart_type == "Line Chart":
        st.line_chart(df.set_index("Category"))
    elif chart_type == "Area Chart":
        st.area_chart(df.set_index("Category"))

    st.subheader("Detailed Insights")
    st.dataframe(df)

# Footer
st.markdown("---")
st.markdown("💡 **Powered by OpenAI and Weaviate**")