from fastapi import APIRouter
from models.rag import RAGRequest, RAGResponse
from services.rag import RagService

from routers.search import search_service

router = APIRouter()


rag_service = RagService(search_service=search_service)


@router.post("/rag", response_model=RAGResponse)
async def rag(request: RAGRequest):
    return rag_service.generate_answer(request.query, request.limit)
