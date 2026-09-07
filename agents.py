import os
import numpy as np
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

# Initialize Gemini Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Structured schema for Screenplay Parsing
class SceneMetric(BaseModel):
    scene_number: int
    setting: str = Field(description="Interior or Exterior")
    pacing_intensity: int = Field(description="Intensity score from 1 to 10")
    key_props: list[str]

class ScriptAnalysis(BaseModel):
    genre: str
    estimated_target_audience: str
    scenes: list[SceneMetric]
    complexity_score: float = Field(description="1.0 to 5.0 operational complexity")

def analyze_script(script_text: str) -> ScriptAnalysis:
    """Worker Agent 1: Extracts structured narrative data from raw script."""
    prompt = f"Analyze the following screenplay/scene and output structured JSON:\n\n{script_text}"
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ScriptAnalysis,
        ),
    )
    return ScriptAnalysis.model_validate_json(response.text)

def statistical_forecasting_engine(analysis: ScriptAnalysis, estimated_budget: float) -> dict:
    """Worker Agent 2: Deterministic statistical risk modeling."""
    intensities = [s.pacing_intensity for s in analysis.scenes] or [5]
    mean_intensity = float(np.mean(intensities))
    volatility = float(np.std(intensities))

    base_multiplier = 1.8 if analysis.genre.lower() in ["action", "thriller", "comedy", "sci-fi"] else 1.3
    adjusted_multiplier = base_multiplier * (1 - (analysis.complexity_score * 0.05))

    p50_box_office = estimated_budget * adjusted_multiplier
    p10_downside = p50_box_office * 0.60
    p90_upside = p50_box_office * 1.55

    return {
        "mean_intensity": round(mean_intensity, 2),
        "pacing_volatility_std": round(volatility, 2),
        "projected_p10": round(p10_downside, 2),
        "projected_p50": round(p50_box_office, 2),
        "projected_p90": round(p90_upside, 2),
    }

def generate_studio_memo(analysis: ScriptAnalysis, stats: dict) -> str:
    """Coordinator Agent: Synthesizes metrics into an executive brief."""
    prompt = f"""
    You are an Executive Studio Producer. Generate a professional, sharp Greenlight Memo based on these metrics:
    - Genre: {analysis.genre}
    - Audience: {analysis.estimated_target_audience}
    - Operational Complexity: {analysis.complexity_score}/5.0
    - Pacing Volatility (Std Dev): {stats['pacing_volatility_std']}
    - Box Office Risk Distribution: P10=${stats['projected_p10']:,}, P50=${stats['projected_p50']:,}, P90=${stats['projected_p90']:,}
    
    Provide an executive summary, risk analysis, and final verdict.
    """
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text
