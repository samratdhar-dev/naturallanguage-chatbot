# APMT Analytics CHATBOT

A sophisticated Python application for creating an AI-powered chatbot interface with Dremio. This chatbot can understand natural language queries, convert them to SQL, execute them against Dremio, and provide intelligent responses with optional visualizations.

## Features

- 🤖 **Natural Language to SQL**: Convert user questions to SQL queries using AI
- 🔍 **Dremio Integration**: Direct connection to Maersk's Enterprise Dremio instance
- 📊 **Interactive Data Visualization**: Generate interactive charts and graphs using Plotly
- 🚀 **FastAPI Backend**: RESTful API for integration with other applications
- 🎨 **Streamlit Frontend**: User-friendly web interface for chatbot interactions with professional Maersk branding
- 🔒 **Security Guardrails**: DML operation protection to prevent unauthorized data modifications
- 📝 **Comprehensive Logging**: Transaction logging for audit and debugging
- 🔧 **Environment Management**: Secure configuration management

## Project Structure

```
DREMIOCHATBOT/
├── src/                           # Source code
│   ├── main.py                    # FastAPI server entry point
│   ├── app_dremio.py             # Core chatbot logic with DML security
│   ├── dremio.py                 # Dremio connection and query execution
│   ├── streamlit_maersk_chatbot.py # Professional Maersk-branded web interface
│   ├── graphgenerator.py         # Interactive Plotly chart generation
│   ├── maersk_config.py          # Maersk branding and configuration
│   ├── architecture_diagram.py   # System architecture visualization
│   ├── templates.py              # AI prompt templates for SQL and Plotly
│   ├── logger_config.py          # Logging configuration
│   └── __init__.py               # Package initialization
├── tests/                         # Test files
├── logs/                         # Log files (ignored by git except .gitkeep)
├── .venv/                        # Virtual environment
├── .env                          # Environment variables (contains secrets)
├── .env.example                  # Environment template
├── requirements.txt              # Dependencies including Plotly
├── pyproject.toml               # Project configuration
├── .gitignore                   # Git ignore file
└── README.md                    # This file
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## License

[Add your license information here]
