# State Data Assistant 🌎

A natural language interface for querying database using LlamaIndex and Groq LLM. This application allows users to ask questions about state demographics in plain English and get instant responses powered by AI.

## 🚀 Features

- Natural language to SQL query conversion
- Real-time database querying
- Powered by Groq's 70B parameter LLM
- Enhanced query understanding with BAAI/bge-small-en-v1.5 embeddings
- Secure database connection management

## 🛠️ Tech Stack

- **Backend**: Python, SQLAlchemy, MySQL
- **AI/ML**: LlamaIndex, Groq LLM, HuggingFace Embeddings
- **Frontend**: Streamlit
- **Database**: MySQL

## 📋 Prerequisites

- Python 3.8+
- MySQL Database
- Groq API Key
- Required Python packages (see requirements.txt)

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```env
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_NAME=your_database_name
GROQ_API_KEY=your_groq_api_key
```

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/state-data-assistant.git
cd state-data-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables in `.env`

4. Run the application:
```bash
streamlit run app.py
```



