from dotenv import load_dotenv
import os
import time
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from .templates import GRAPH_GENERATION_TEMPLATE
from .logger_config import log_transaction


load_dotenv(override=True)

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Create Azure OpenAI LLM instance
llm = AzureChatOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION,
    deployment_name=AZURE_OPENAI_DEPLOYMENT,
    temperature=0
) if AZURE_OPENAI_API_KEY else None


def generate_graph(response: str, user_question: str = None):
    start_time = time.time()
    error = None
    max_retries = 3
    
    # Check if LLM instance is properly initialized
    if not llm:
        raise ValueError("Azure OpenAI API key not configured. Please set AZURE_OPENAI_API_KEY in your .env file.")
    
    for attempt in range(max_retries):
        try:
            prompt = ChatPromptTemplate.from_template(GRAPH_GENERATION_TEMPLATE)
                
            llm_chain = prompt | llm.bind(stop=["\n```"])
            
            # Pass both user_question and query to the prompt
            invoke_params = {"query": response}
            if user_question:
                invoke_params["user_question"] = user_question
                
            # If retrying, add error context to help the LLM fix the issue
            if attempt > 0 and error:
                retry_template = GRAPH_GENERATION_TEMPLATE + f"\n\nPrevious attempt failed with error: {error}. Please fix the code."
                prompt = ChatPromptTemplate.from_template(retry_template)
                llm_chain = prompt | llm.bind(stop=["\n```"])
                
            code = llm_chain.invoke(invoke_params).content

            # Provide plotly and pandas imports in execution environment
            local_vars = {"px": px, "go": go, "pd": pd}
            #print(f"Attempt {attempt + 1}: Generated code:")
            print(code)
            
            # Execute the generated Plotly code
            exec(code.replace("```python",""), {"px": px, "go": go, "pd": pd}, local_vars)

            # Try to capture the figure - Plotly figures
            fig = None
            for val in local_vars.values():
                if hasattr(val, '_figure_class') or str(type(val)).find('plotly') != -1:
                    fig = val
                    break
            
            # Look for 'fig' variable specifically
            if fig is None and 'fig' in local_vars:
                fig = local_vars['fig']
                
            # If we got a valid figure, return success
            if fig is not None:
                execution_time = time.time() - start_time
                
                # Log successful graph generation with user question
                log_transaction(
                    transaction_type="GRAPH_GENERATION_SUCCESS",
                    user_question=user_question,
                    data_output=response,
                    execution_time=execution_time
                )
                
                #print(f"Graph generation succeeded on attempt {attempt + 1}")
                return fig
                
        except Exception as e:
            error = str(e)
            #print(f"Attempt {attempt + 1} failed with error: {error}")
            
            # If this is the last attempt, log the error and raise
            if attempt == max_retries - 1:
                execution_time = time.time() - start_time
                
                # Log error in graph generation with user question
                log_transaction(
                    transaction_type="GRAPH_GENERATION_ERROR",
                    user_question=user_question,
                    data_output=response,
                    error=error,
                    execution_time=execution_time
                )
                
                #print(f"Graph generation failed after {max_retries} attempts")
                raise e
            
            # Wait a moment before retrying
            time.sleep(0.5)
    
    # This should never be reached, but just in case
    raise Exception("Graph generation failed after all retries")

# # -------------------------
# # Example usage
# # -------------------------
# user_query = "Plot user count by browser (Chrome=3079, Firefox=118, Safari=253) as a bar chart"
# code = generate_code(user_query)

# print("Generated Code:\n", code)  # for debugging

# fig = execute_code(code)
# #fig.show()  # in VS Code notebook this will render inline

# fig = generate_graph({'rowCount': 34, 'schema': [{'name': 'event_day', 'type': {'name': 'DATE'}}, {'name': 'new_user_count', 'type': {'name': 'BIGINT'}}], 'rows': [{'event_day': '2025-07-28', 'new_user_count': 4074}, {'event_day': '2025-07-29', 'new_user_count': 3807}, {'event_day': '2025-07-30', 'new_user_count': 4989}, {'event_day': '2025-07-31', 'new_user_count': 4266}, {'event_day': '2025-08-01', 'new_user_count': 3954}, {'event_day': '2025-08-02', 'new_user_count': 1877}, {'event_day': '2025-08-03', 'new_user_count': 1735}, {'event_day': '2025-08-04', 'new_user_count': 4326}, {'event_day': '2025-08-05', 'new_user_count': 4163}, {'event_day': '2025-08-06', 'new_user_count': 4130}, {'event_day': '2025-08-07', 'new_user_count': 4093}, {'event_day': '2025-08-08', 'new_user_count': 4002}, {'event_day': '2025-08-09', 'new_user_count': 2039}, {'event_day': '2025-08-10', 'new_user_count': 1719}, {'event_day': '2025-08-11', 'new_user_count': 3996}, {'event_day': '2025-08-12', 'new_user_count': 4060}, {'event_day': '2025-08-13', 'new_user_count': 4326}, {'event_day': '2025-08-14', 'new_user_count': 4231}, {'event_day': '2025-08-15', 'new_user_count': 3219}, {'event_day': '2025-08-16', 'new_user_count': 2155}, {'event_day': '2025-08-17', 'new_user_count': 1551}, {'event_day': '2025-08-18', 'new_user_count': 4276}, {'event_day': '2025-08-19', 'new_user_count': 4086}, {'event_day': '2025-08-20', 'new_user_count': 4303}, {'event_day': '2025-08-21', 'new_user_count': 3807}, {'event_day': '2025-08-22', 'new_user_count': 4064}, {'event_day': '2025-08-23', 'new_user_count': 1681}, {'event_day': '2025-08-24', 'new_user_count': 1395}, {'event_day': '2025-08-25', 'new_user_count': 4296}, {'event_day': '2025-08-26', 'new_user_count': 3675}, {'event_day': '2025-08-27', 'new_user_count': 163}, {'event_day': '2025-08-29', 'new_user_count': 1}, {'event_day': '2025-08-30', 'new_user_count': 0}]}
#                      ,"what is the daily new user trend?"
#                      )
# import streamlit as st
# with st.spinner("Thinking..."):
#     st.plotly_chart(fig, use_container_width=True)
