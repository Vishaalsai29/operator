# Consumer Lens
### 🌟 Empowering Consumer Protection  

**Consumer Lens** is designed to transform how consumer complaints are analyzed and understood. Leveraging **Retrieval-Augmented Generation (RAG)**, this application empowers stakeholders such as consumer advocates, regulatory bodies, and businesses to make **data-driven decisions** by exploring complaint trends and patterns.  

Simply upload your dataset of consumer complaints and experience a **seamless, queriable interface** that promotes **transparency**, **accountability**, and **actionable insights**.  

### 🛠️ Setting Up 

Getting started with **Consumer Lens** is straightforward! Follow these steps to set up and deploy the application:

1. **Clone the Repository**: Download the project to your local machine.  
2. **Prepare Your Data**: Curate and clean your dataset of consumer complaints for analysis.  
3. **Deploy Models and Infrastructure**: Optionally integrate embedding and generative models and configure a vector database (e.g., Weaviate) to serve as the RAG database.  
4. **Preprocess Your Data**: Use the preprocessing pipeline to transform raw complaint data into vector-indexed chunks ready for querying.  
5. **Deploy and Launch**: Deploy the backend to handle queries and responses, and launch the frontend to provide actionable insights and an intuitive query interface to your end users.  

With these simple steps, you'll unlock the power of Complaint Compass to explore complaint trends, discover patterns, and drive meaningful decisions.

### Code Quality Tools🛠️

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Python 3.10.12](https://img.shields.io/badge/python-3.10.12-blue.svg)](https://www.python.org/downloads/release/python-31012/)

This project maintains high code quality standards through automated tools for formatting, style checking, and security analysis.

### 🧭 System Diagram

<img width="800" alt="Preprocessing_Image" src="documents\Preprocessing_Image.svg">

### 🔑 Key Components

- **Complaint Compass App**  
  The public-facing application that empowers users to query consumer complaints and visualize insights. It integrates with a vector database, an embedding model (e.g., OpenAI or Llama), and a generative model. Optional integrations include RAG-reranking for improved context retrieval.

- **Preprocessing Pipeline**  
  A robust set of tools for cleaning and structuring complaint data into vectorized formats, enabling efficient storage and retrieval within a vector database (currently Weaviate). This includes embedding models and mechanisms for data preprocessing and cleaning.

- **Backend Services**  
  The backbone of the system, responsible for handling RAG queries, embeddings, and generative responses. It connects seamlessly with vector databases, embedding models, and optionally a ranking model for enhanced query precision.

- **Dev Notebooks**  
  A collection of development and testing notebooks designed for preprocessing, querying, and evaluating the RAG system's performance.

### [Contribute](documents/guide_to_contribute.md)


