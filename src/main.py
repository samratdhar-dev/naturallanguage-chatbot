from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
import logging
import uuid
from .app_dremio_final import chat_with_sql
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="APMT Analytics Chatbot API",
    description="FastAPI application for APMT Analytics Chatbot with SQL query generation",
    version="1.0.0"
)

# Pydantic Models/Classes
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000, description="User question")
    user_id: Optional[str] = Field(None, description="Optional user identifier")
    session_id: Optional[str] = Field(None, description="Optional session identifier")

class ChatResponse(BaseModel):
    answer: str
    sql_query: Optional[str] = None
    fig: Optional[object] = None
    confidence_score: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    response_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class QueryHistory(BaseModel):
    query_id: str
    question: str
    answer: str
    sql_query: Optional[str]
    timestamp: datetime
    user_id: Optional[str]
    session_id: Optional[str]

class HealthStatus(BaseModel):
    status: str
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = "1.0.0"
    database_status: str = "connected"

class ErrorResponse(BaseModel):
    error: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class BatchChatRequest(BaseModel):
    questions: List[str] = Field(..., min_length=1, max_length=5, description="List of questions")
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class APIStats(BaseModel):
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time: float
    uptime_seconds: float


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "APMT Analytics Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "docs": "/docs"
        }
    }

# Health check endpoint
@app.get("/health", response_model=HealthStatus, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthStatus(
        status="healthy",
        database_status="connected"
    )

# Main chat endpoint
@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_endpoint(request: ChatRequest):
    """Process a chat question and return answer with SQL query"""
    try:
        logger.info(f"Processing chat request: {request.question[:50]}...")

        # Process the question
        answer, sql_query, fig = chat_with_sql(request.question)
        
        # Create response
        response = ChatResponse(
            answer=answer,
            sql_query=sql_query,
            fig=json.loads(fig),
            confidence_score=0.95  # Placeholder confidence score
        )
        
        # Store in history
        history_entry = QueryHistory(
            query_id=response.response_id,
            question=request.question,
            answer=answer,
            sql_query=sql_query,
            timestamp=response.timestamp,
            user_id=request.user_id,
            session_id=request.session_id
        )
        
        logger.info(f"Chat request processed successfully")
        return response
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )

# Batch chat endpoint
@app.post("/chat/batch", tags=["Chat"])
async def batch_chat_endpoint(request: BatchChatRequest):
    """Process multiple chat questions in batch"""
    try:
        logger.info(f"Processing batch request with {len(request.questions)} questions")
        
        responses = []
        for question in request.questions:
            try:
                answer, sql_query, fig = chat_with_sql(question)
                response = ChatResponse(
                    answer=answer,
                    sql_query=sql_query,
                    fig=fig,
                    confidence_score=0.95
                )
                responses.append(response)
                
                # Store in history
                history_entry = QueryHistory(
                    query_id=response.response_id,
                    question=question,
                    answer=answer,
                    sql_query=sql_query,
                    timestamp=response.timestamp,
                    user_id=request.user_id,
                    session_id=request.session_id
                )
                
            except Exception as e:
                logger.error(f"Error processing question in batch: {str(e)}")
                continue
        
        return {
            "responses": responses,
            "processed_count": len(responses),
            "total_questions": len(request.questions)
        }
        
    except Exception as e:
        logger.error(f"Error processing batch request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing batch request: {str(e)}"
        )





# To run: uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
