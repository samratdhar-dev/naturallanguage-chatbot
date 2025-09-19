# Templates for LangChain prompts

# Template for converting natural language to Dremio SQL
SQL_GENERATION_TEMPLATE = """
You are an expert SQL query generator for MySQL.
You will be provided with a database schema and a user question.
Your task is to generate a valid MySQL query that answers the user's question using only the tables and columns provided in the schema.

Schema:
{schema}

Instructions:
Use only the tables and columns defined in the schema.
Output only the SQL query, without any explanation or comments.
Focus on performance-related metrics such as counts, averages, sums, and rankings.
For string filtering, ALWAYS use LOWER(column) LIKE LOWER('%<value>%')
If multiple interpretations are possible, choose the most logical and commonly expected one.
Ensure the query is syntactically correct and optimized for readability.
performance related metrics are defined from resolution count.

Question:
{question}
"""

# Template for converting SQL results to natural language response
NATURAL_LANGUAGE_RESPONSE_TEMPLATE = """Based on the table schema below, question, sql query, and sql response, write a natural language response.
{schema}
Question: {question}
SQL Query: {query}
SQL Response: {response}"""

# Template for generating Plotly code from SQL response data
GRAPH_GENERATION_TEMPLATE = """
Generate interactive Plotly code for the given data. Consider the user's original question to create the most appropriate visualization.

User Question: {user_question}
Data: {query}

Create flashy, modern, professional, presentation-ready, stylish, bold, clean, with data labels Plotly code that:
Bold title with emojis
Bright colors with gradients or strong contrast
Data points/labels directly on the chart
Highlight maximum and minimum values
Clean background (light gray or soft color)
Grid lines only where helpful (subtle dashed lines)
Remove unnecessary borders
Make it easy to understand at a glance."*
Considers the user's intent from their original question
Uses appropriate chart type based on data structure and user's request (plotly.express recommended)
Creates clear titles and labels that reflect the user's question
Handles data parsing and visualization properly
Sets figure size with: fig.update_layout(width=800, height=500)
Uses smaller font sizes for better display: title_font_size=14, font_size=10
Makes it interactive with hover tooltips

**IMPORTANT RULES:**
- Only return executable Python Plotly code, no explanations
- Import plotly.express as px and/or plotly.graph_objects as go at the start
- DO NOT use px.data.frame or any px.data.* - these are sample datasets, not functions
- Parse the actual data provided in the query parameter
- Use pandas.DataFrame() to convert the data if needed
- Start directly with the python code. DO NOT start with: ```python 
- End with: fig (to return the figure object)
- Use the actual data structure provided, not sample data
- Boxplots should be horizontal (orientation='h')

Example data parsing:
import pandas as pd
import plotly.express as px

# Parse the data from query parameter
data = {query}
if 'rows' in data:
    df = pd.DataFrame(data['rows'])
    # Your visualization code here
fig = px.bar(df, x='column1', y='column2', title='Your Title')
fig
"""