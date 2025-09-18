"""Visualization routes for natural language queries"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ..services.llm import llm_service


router = APIRouter()


class VisualizationRequest(BaseModel):
    """Request model for visualization generation"""

    prompt: str


class VisualizationResponse(BaseModel):
    """Response model for visualization generation"""

    success: bool
    visualization_type: str
    title: str
    data: list
    chart_config: dict = {}
    sql: str = ""
    error: str = ""


@router.post("/generate", response_model=VisualizationResponse)
async def generate_visualization(request: VisualizationRequest):
    """Generate visualization from natural language prompt"""
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Prompt is required")

    try:
        result = await llm_service.process_query(request.prompt.strip())
        return VisualizationResponse(**result)
    except Exception as e:
        return VisualizationResponse(
            success=False,
            visualization_type="error",
            title="Error Processing Request",
            data=[],
            error=str(e),
        )
