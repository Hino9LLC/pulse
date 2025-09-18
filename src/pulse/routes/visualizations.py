"""Visualization routes for natural language queries"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ..services.llm import llm_service


router = APIRouter()


class VisualizationRequest(BaseModel):
    """Request model for visualization generation"""

    prompt: str


class ChartConfig(BaseModel):
    """Chart configuration with styling support"""

    x_field: str = ""
    y_field: str = ""
    colors: list[str] = []
    chart_style: str = ""
    title_style: str = ""
    background_color: str = ""
    border_color: str = ""
    grid_color: str = ""
    font_size: str = ""
    font_weight: str = ""
    legend_position: str = "bottom"


class VisualizationResponse(BaseModel):
    """Response model for visualization generation"""

    success: bool
    visualization_type: str
    title: str
    data: list
    chart_config: ChartConfig = ChartConfig()
    sql: str = ""
    error: str = ""


class ModificationRequest(BaseModel):
    """Request model for visualization modification"""

    prompt: str
    existing_visualization: dict  # The current visualization to modify


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


@router.post("/modify", response_model=VisualizationResponse)
async def modify_visualization(request: ModificationRequest):
    """Modify existing visualization with styling/format changes"""
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Prompt is required")

    try:
        # Create a context-aware prompt that includes the existing visualization
        import json as json_module

        config_str = json_module.dumps(request.existing_visualization.get("chart_config", {}))
        context_prompt = f"""
        EXISTING VISUALIZATION:
        Type: {request.existing_visualization.get('visualization_type', 'unknown')}
        Title: {request.existing_visualization.get('title', 'untitled')}
        SQL: {request.existing_visualization.get('sql', '')}
        Current Config: {config_str}

        MODIFICATION REQUEST: {request.prompt}

        Please modify the visualization based on the request. Keep the same SQL and data,
        only change styling/formatting.
        """

        result = await llm_service.process_query(context_prompt.strip())
        return VisualizationResponse(**result)
    except Exception as e:
        return VisualizationResponse(
            success=False,
            visualization_type="error",
            title="Error Modifying Visualization",
            data=[],
            error=str(e),
        )
