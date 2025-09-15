from dotenv import load_dotenv
import os
import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import AzureChatOpenAI
from .mysql import get_schema, run_query
from .templates import SQL_GENERATION_TEMPLATE, NATURAL_LANGUAGE_RESPONSE_TEMPLATE
from .logger_config import log_transaction
from .graphgenerator import generate_graph

load_dotenv(override=True)

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # Single deployment name

# Create a single LLM instance using Azure OpenAI
llm = AzureChatOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION,
    deployment_name=AZURE_OPENAI_DEPLOYMENT,
    temperature=0
) if AZURE_OPENAI_API_KEY else None


def check_dml_guardrail(user_question: str, sql_query: str = None) -> tuple[bool, str]:

    dml_message = "**Security Notice**: Data modification operations are not allowed."

    # DML keywords that should be blocked
    dml_keywords = [
        'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 'TRUNCATE', 'REMOVE',
        'REPLACE', 'MERGE', 'UPSERT', 'GRANT', 'REVOKE', 'COMMIT', 'ROLLBACK'
    ]

    dml_found = list(set(dml_keywords) & set(user_question.upper().split()))
    if len(dml_found) > 0:
        return False, dml_message

    if sql_query:
        dml_found = list(set(dml_keywords) & set(sql_query.upper().split()))
        if len(dml_found) > 0:
            return False, dml_message
    
    return True, ""


def chat_with_sql(user_question: str, sql_system_prompt: str = None, response_system_prompt: str = None):
    start_time = time.time()
    original_sql_query = None
    sql_query = None
    data_output = None
    answer = None
    error = None

    try:
        # Check if LLM instance is properly initialized
        if not llm:
            raise ValueError("Azure OpenAI API key not configured. Please set AZURE_OPENAI_API_KEY in your .env file.")
        
        is_safe, dml_error = check_dml_guardrail(user_question)
        if not is_safe:
            log_transaction(
                transaction_type="DML_BLOCKED",
                user_question=user_question,
                error=dml_error,
                execution_time=time.time() - start_time
            )
            return dml_error, None, None
        
        prompt = ChatPromptTemplate.from_template(SQL_GENERATION_TEMPLATE)

        # Get schema once
        schema = get_schema('_')

        # Get sql
        sql_prompt_data = {
            "schema": schema,
            "question": user_question
        }
        original_sql_query = (prompt | llm.bind(stop=[";\n```"]) | StrOutputParser()).invoke(sql_prompt_data)
        sql_query = original_sql_query.replace("sql", "").replace("```", "").strip()

        prompt_response = ChatPromptTemplate.from_template(NATURAL_LANGUAGE_RESPONSE_TEMPLATE)
        
        # Second guardrail: Check the generated SQL query for DML operations
        is_safe, dml_error = check_dml_guardrail(user_question, sql_query)
        if not is_safe:
            log_transaction(
                transaction_type="DML_BLOCKED",
                user_question=user_question,
                sql_query=sql_query,
                error=dml_error,
                execution_time=time.time() - start_time
            )
            return dml_error, sql_query, None
        
        # Get SQL response (data output)  
        data_output = run_query(sql_query)

        # Get natural language answer using already obtained data
        answer_prompt_data = {
            "schema": schema,
            "question": user_question,
            "query": sql_query,
            "response": data_output
        }
        answer = (prompt_response | llm | StrOutputParser()).invoke(answer_prompt_data)

        # Attempt graph generation without failing entire chat on error
        fig = None
        try:
            fig = generate_graph(response=data_output, user_question=user_question)
        except Exception as graph_err:
            log_transaction(
                transaction_type="GRAPH_GENERATION_SOFT_FAIL",
                user_question=user_question,
                sql_query=sql_query,
                error=str(graph_err),
                execution_time=time.time() - start_time
            )

        execution_time = time.time() - start_time
        
        # Log successful transaction
        log_transaction(
            transaction_type="SQL_CHAT_SUCCESS",
            user_question=user_question,
            sql_query=sql_query,
            data_output=data_output,
            answer=answer,
            execution_time=execution_time
        )

        return answer, sql_query, fig.to_json()
        
    except Exception as e:
        execution_time = time.time() - start_time
        error = str(e)
        
        # Log error transaction
        log_transaction(
            transaction_type="SQL_CHAT_ERROR",
            user_question=user_question,
            sql_query=sql_query,
            data_output=data_output,
            answer=answer,
            error=error,
            execution_time=execution_time
        )
        
        raise e

#print(chat_with_sql("what is the daily trend of new and returning user for the last 2 weeks?"))


