"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field, ConfigDict
from typing import List


class AnalysisRequest(BaseModel):
    """Request model for text analysis."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "A firewall is a network security device that monitors and filters incoming and outgoing network traffic."
            }
        }
    )
    
    text: str = Field(..., min_length=1, description="Security+ technical text to analyze")


class VocabularyItem(BaseModel):
    """Model for vocabulary word with A2 definition."""
    word: str
    a2_definition: str


class AnalysisResponse(BaseModel):
    """Response model for text analysis."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "original_text": "A firewall is a network security device...",
                "az_translation": "Firewall şəbəkə təhlükəsizliyi cihazıdır...",
                "vocabulary_list": [
                    {
                        "word": "firewall",
                        "a2_definition": "A tool that protects computers from bad internet connections"
                    }
                ],
                "security_plus_mini_note": "Firewall anlayışı...",
                "unknown_words_count": 3
            }
        }
    )
    
    original_text: str
    az_translation: str
    vocabulary_list: List[VocabularyItem]
    security_plus_mini_note: str
    unknown_words_count: int
