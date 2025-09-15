# Data Analytics Chatbot

A sophisticated natural language chatbot application that converts user questions into SQL queries and provides intelligent analytics responses with interactive visualizations. Built specifically for APMT (APM Terminals) analytics data.

## 🚀 Features

- **Natural Language to SQL**: Convert plain English questions into optimized MySQL queries
- **Interactive Visualizations**: Generate dynamic Plotly charts based on query results
- **Dual Interface**: Both REST API (FastAPI) and Web UI (Streamlit) interfaces
- **Security Guardrails**: Built-in protection against data modification operations
- **Comprehensive Logging**: Transaction logging for monitoring and debugging
- **Azure OpenAI Integration**: Powered by Azure OpenAI for intelligent query generation
- **Real-time Processing**: Fast response times with optimized query execution

## 🏗️ Architecture

The application consists of several key components:

- **FastAPI Backend** (`src/main.py`): REST API server providing chat endpoints
- **Streamlit Frontend** (`src/streamlit_app.py`): Interactive web interface
- **Core Chat Engine** (`src/app_dremio_final.py`): Main logic for processing natural language queries
- **Database Interface** (`src/mysql.py`): MySQL database connection and query execution
- **Graph Generator** (`src/graphgenerator.py`): Automated chart generation using Plotly
- **Template System** (`src/templates.py`): LangChain prompt templates for AI interactions
- **Logging System** (`src/logger_config.py`): Comprehensive transaction logging

## 📋 Prerequisites

- Python 3.8+
- MySQL database with analytics data
- Azure OpenAI account and API key
- Required Python packages (see `requirements.txt`)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd naturallanguage-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   
   Create a `.env` file in the root directory with the following variables:
   ```env
   # Azure OpenAI Configuration
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   AZURE_OPENAI_DEPLOYMENT=your_deployment_name
   
   # Database Configuration
   db_uri=mysql+pymysql://username:password@host:port/database_name
   ```

4. **Database Setup**
   
   Ensure your MySQL database is accessible and contains the analytics tables that the chatbot will query.

## 🚀 Running the Application

### Option 1: Run Both Servers Simultaneously (Recommended)

```bash
python run_app.py
```

This will start both the FastAPI backend (port 8000) and Streamlit frontend (port 8501) simultaneously.

### Option 2: Run Servers Separately

**Start the FastAPI backend:**
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Start the Streamlit frontend:**
```bash
streamlit run src/streamlit_app.py
```

## 📖 Usage

### Web Interface (Streamlit)

1. Navigate to `http://localhost:8501`
2. Enter your analytics questions in natural language
3. View the generated SQL queries and results
4. Interact with automatically generated charts and visualizations

### API Interface (FastAPI)

The REST API provides programmatic access to the chatbot functionality:

**Base URL:** `http://localhost:8000`

**Main Endpoints:**

- `POST /chat` - Send a question and receive an answer with SQL query
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation

**Example API Usage:**

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"question": "What are the top 5 terminals by container volume?"}'
```

**Response Format:**
```json
{
  "answer": "Based on the data, here are the top 5 terminals...",
  "sql_query": "SELECT terminal_name, SUM(container_count) as volume...",
  "fig": {...},
  "confidence_score": 0.95,
  "timestamp": "2025-09-15T10:30:00Z",
  "response_id": "uuid-string"
}
```

## 🛡️ Security Features

- **DML Protection**: Automatically blocks INSERT, UPDATE, DELETE, and other data modification operations
- **Query Validation**: Multi-level validation of user inputs and generated SQL queries
- **Error Handling**: Comprehensive error handling and logging for security monitoring

## 📊 Supported Query Types

The chatbot can handle various types of analytics questions:

- **Performance Metrics**: "What is the average container processing time?"
- **Comparative Analysis**: "Compare revenue between terminals A and B"
- **Trend Analysis**: "Show monthly container volume trends"
- **Top/Bottom Rankings**: "Top 10 customers by revenue"
- **Time-based Queries**: "Container volumes for last quarter"

## 📁 Project Structure

```
naturallanguage-chatbot/
├── src/
│   ├── main.py                 # FastAPI application
│   ├── streamlit_app.py       # Streamlit web interface
│   ├── app_dremio_final.py    # Core chat processing logic
│   ├── mysql.py               # Database interface
│   ├── graphgenerator.py      # Chart generation
│   ├── templates.py           # LangChain prompt templates
│   └── logger_config.py       # Logging configuration
├── docs/
│   ├── maersk.jpeg           # Company logo
│   └── apmtlogo.jpg          # APMT logo
├── logs/                      # Application logs
├── requirements.txt           # Python dependencies
├── run_app.py                # Application launcher
└── README.md                 # This file
```

## 🔍 Logging and Monitoring

The application maintains comprehensive logs in the `logs/` directory:

- **Transaction Logs**: All user queries, SQL generation, and responses
- **Error Logs**: Detailed error information for debugging
- **Performance Metrics**: Query execution times and system performance
- **Security Events**: DML blocking and security-related activities

Log files are created daily with the format: `chatbot_transactions_YYYYMMDD.log`

## 🧪 Testing

The project includes testing dependencies. Run tests using:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test files
pytest tests/test_api.py
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | Yes |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | Yes |
| `AZURE_OPENAI_API_VERSION` | API version | Yes |
| `AZURE_OPENAI_DEPLOYMENT` | Deployment name | Yes |
| `db_uri` | MySQL database connection string | Yes |

### Customization

- **Modify Templates**: Edit `src/templates.py` to customize AI prompts
- **Database Schema**: Update `src/mysql.py` for different database configurations
- **UI Styling**: Customize the Streamlit interface in `src/streamlit_app.py`
- **API Extensions**: Add new endpoints in `src/main.py`

## 🐛 Troubleshooting

### Common Issues

1. **Azure OpenAI Connection Failed**
   - Verify API key and endpoint in `.env` file
   - Check network connectivity to Azure OpenAI service

2. **Database Connection Error**
   - Verify database URI format and credentials
   - Ensure database server is accessible

3. **Port Already in Use**
   - Change ports in `run_app.py` or stop conflicting services
   - Default ports: FastAPI (8000), Streamlit (8501)

4. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility (3.8+)

### Debug Mode

Enable detailed logging by setting the logging level to DEBUG in `src/logger_config.py`.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is proprietary software developed for Maersk Group / APM Terminals.

## 🏢 About

Developed for **APM Terminals (APMT)** - A Maersk Group company providing port and terminal services worldwide. This chatbot enables business users to interact with analytics data using natural language, making data insights more accessible across the organization.

---

**Note**: This application requires proper configuration of Azure OpenAI and database credentials. Ensure all environment variables are set correctly before running the application.