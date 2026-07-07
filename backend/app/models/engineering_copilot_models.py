"""
Power Electronics Reliability Copilot
Engineering Copilot Response Models
"""

from typing import Any, Literal

from pydantic import BaseModel, Field


ConfidenceLevel = Literal["High", "Medium", "Low", "Not evaluated"]


class SemanticEvidenceItem(BaseModel):
    chunkId: str | None = None
    documentId: str | None = None
    chunkIndex: int | None = None
    score: float | None = None
    text: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class GraphEntityItem(BaseModel):
    name: str | None = None
    labels: list[str] = Field(default_factory=list)
    properties: dict[str, Any] = Field(default_factory=dict)


class GraphRelationshipItem(BaseModel):
    source: str | None = None
    relationshipType: str | None = None
    target: str | None = None
    properties: dict[str, Any] = Field(default_factory=dict)


class GraphEvidence(BaseModel):
    entities: list[GraphEntityItem] = Field(default_factory=list)
    relationships: list[GraphRelationshipItem] = Field(default_factory=list)


class EngineeringCopilotMetadata(BaseModel):
    topK: int
    graphLimit: int
    semanticEvidenceCount: int
    graphEntityCount: int
    graphRelationshipCount: int

class ReasoningContextMetadata(BaseModel):
    readyForLLM: bool = True
    semanticEvidenceCount: int = 0
    graphEntityCount: int = 0
    graphRelationshipCount: int = 0

class EngineeringCitation(BaseModel):
    citationType: str
    source: str | None = None
    chunkId: str | None = None
    score: float | None = None
    relationship: str | None = None


class ConversationTurn(BaseModel):
    """A previous user/assistant exchange supplied for context-aware reasoning."""

    question: str
    answer: str | None = None

class EngineeringCopilotResponse(BaseModel):
    status: str = "success"
    documentId: str
    question: str
    answer: str
    confidence: ConfidenceLevel = "Not evaluated"
    recommendedNextStep: str | None = None
    semanticEvidence: list[SemanticEvidenceItem] = Field(default_factory=list)
    graphEvidence: GraphEvidence = Field(default_factory=GraphEvidence)
    reasoningContext: ReasoningContextMetadata
    metadata: EngineeringCopilotMetadata
    citations: list[EngineeringCitation] = Field(default_factory=list)

