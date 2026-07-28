from pydantic import BaseModel, Field
from typing import List, Literal


class FundamentalAnalysis(BaseModel):
    overall_investiment_thesis: str
    investiment_grade: Literal["A", "B", "C", "D"]
    confidence_score: float = Field(ge=0, le=1)
    key_strengths: List[str] = Field(min_length=3, max_length=3)
    key_concerns: List[str] = Field(min_length=3, max_length=3)
    recommendation: Literal["buy", "sell", "hold", "avoid"]

class MomentumAnalysis(BaseModel):
    overall_momentum: Literal["positive", "negative", "neutral"]
    momentum_strength: Literal["strong", "moderate", "weak"]
    key_momentum_drivers: List[str] = Field(min_length=2, max_length=3)
    momentum_risks: List[str] = Field(min_length=2, max_length=3)
    short_term_outlook: Literal["bullish", "bearish", "neutral"]
    momentum_score: float = Field(ge=0, le=10)

class SentimentAnalysis(BaseModel):
    sentiment_score: float = Field(ge=1, le=10)
    sentiment_direction: Literal["Positive","Negative","Neutral"]
    key_news_themes: List[str]
    recent_catalysts: List[str]
    market_outlook: str

class FinalRecommendation(BaseModel):
    action: Literal["BUY","SELL","HOLD"]
    confidence: float = Field(ge=0,le=1)
    rationale: str
    key_risks: List[str]
    key_opportunities: List[str]
    time_horizon: Literal["Short_term", "Medium_term", "Long_term"]
    
class AgentRequest(BaseModel):
    ticker: str
    limit: int = 3


class AgentResponse(BaseModel):
    ticker: str
    fundamental_analysis: FundamentalAnalysis
    momentum_analysis: MomentumAnalysis
    sentiment_analysis: SentimentAnalysis
    final_recommendation: FinalRecommendation
