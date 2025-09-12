import logging
import os
from datetime import datetime
import json

# Configure logging
def setup_logger():
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Create logger
    logger = logging.getLogger('chatbot_logger')
    logger.setLevel(logging.INFO)
    
    # Create file handler with timestamp
    log_filename = f"logs/chatbot_transactions_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

# Initialize logger
chatbot_logger = setup_logger()

def log_transaction(transaction_type, user_question=None, sql_query=None, data_output=None, answer=None, error=None, execution_time=None):
    """
    Log chatbot transactions
    
    Args:
        transaction_type (str): Type of transaction (e.g., 'SQL_GENERATION', 'GRAPH_GENERATION', 'ERROR')
        user_question (str): Original user question
        sql_query (str): Generated SQL query
        data_output: SQL query result
        answer (str): Natural language response
        error (str): Error message if any
        execution_time (float): Time taken to execute
    """
    # Clean SQL query by removing escape characters and normalizing whitespace
    clean_sql_query = None
    if sql_query:
        # Remove all escape characters and normalize quotes
        clean_sql_query = sql_query.replace('\\n', ' ').replace('\\t', ' ').replace('\\"', '"').replace('\"', '"').replace('\n', ' ').replace('\t', ' ')
        # Remove extra spaces
        import re
        clean_sql_query = re.sub(r'\s+', ' ', clean_sql_query).strip()
    
    log_data = {
        'transaction_type': transaction_type,
        'timestamp': datetime.now().isoformat(),
        'user_question': user_question,
        'sql_query': clean_sql_query,
        'data_output': str(data_output) if data_output else None,
        'data_output_length': len(str(data_output)) if data_output else None,
        'answer': answer,
        'answer_length': len(answer) if answer else None,
        'error': error,
        'execution_time_seconds': execution_time,
        'status': 'SUCCESS' if not error else 'ERROR'
    }
    
    # Remove None values for cleaner logs
    log_data = {k: v for k, v in log_data.items() if v is not None}
    
    if error:
        chatbot_logger.error(f"TRANSACTION_ERROR: {json.dumps(log_data, ensure_ascii=False)}")
    else:
        chatbot_logger.info(f"TRANSACTION_SUCCESS: {json.dumps(log_data, ensure_ascii=False)}")

def log_user_interaction(action, details=None):
    """
    Log user interactions
    
    Args:
        action (str): User action (e.g., 'SESSION_START', 'QUESTION_ASKED', 'VISUALIZATION_REQUESTED')
        details (dict): Additional details
    """
    log_data = {
        'action': action,
        'timestamp': datetime.now().isoformat(),
        'details': details
    }
    
    chatbot_logger.info(f"USER_INTERACTION: {json.dumps(log_data, ensure_ascii=False)}")
