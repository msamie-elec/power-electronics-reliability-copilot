from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

from app.models.engineering_copilot_models import (
    EngineeringCopilotMetadata,
    EngineeringCopilotResponse,
    ReasoningContextMetadata,
)
from app.services.engineering_answer_service import engineering_answer_service
from app.services.citation_service import citation_service

from app.core.exceptions import DocumentNotFoundError, ReasoningError, RetrievalError

import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/engineering-copilot",
    tags=["Engineering Copilot"],
)


class EngineeringCopilotRequest(BaseModel):
    document_id: str = Field(..., description="Knowledge document ID")
    question: str = Field(..., description="Engineering question")
    top_k: int = Field(5, ge=1, le=20)
    graph_limit: int = Field(10, ge=1, le=50)

    @field_validator("question")
    @classmethod
    def question_must_not_be_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("question must not be empty")
        return value.strip()


@router.post("/ask", response_model=EngineeringCopilotResponse)
def ask_engineering_copilot(request: EngineeringCopilotRequest):
    try:
        logger.info(
            "Engineering Copilot request received document_id=%s top_k=%s graph_limit=%s",
            request.document_id,
            request.top_k,
            request.graph_limit,
        )

        result = engineering_answer_service.answer_question(
            document_id=request.document_id,
            question=request.question,
            top_k=request.top_k,
            graph_limit=request.graph_limit,
        )

        semantic_evidence = result.get("semanticEvidence", [])
        graph_evidence = result.get("graphEvidence", {})
        graph_entities = graph_evidence.get("entities", [])
        graph_relationships = graph_evidence.get("relationships", [])

        citations = citation_service.build_citations(
            semantic_evidence=semantic_evidence,
            graph_evidence=graph_evidence,
        )

        logger.info(
            "Engineering Copilot response prepared document_id=%s citations=%s",
            request.document_id,
            len(citations),
        )

        return EngineeringCopilotResponse(
            documentId=request.document_id,
            question=request.question,
            answer=result.get("answer", ""),
            confidence="Not evaluated",
            recommendedNextStep=None,
            semanticEvidence=semantic_evidence,
            graphEvidence=graph_evidence,
            citations=citations,
            reasoningContext=ReasoningContextMetadata(
                readyForLLM=True,
                semanticEvidenceCount=len(semantic_evidence),
                graphEntityCount=len(graph_entities),
                graphRelationshipCount=len(graph_relationships),
            ),
            metadata=EngineeringCopilotMetadata(
                topK=request.top_k,
                graphLimit=request.graph_limit,
                semanticEvidenceCount=len(semantic_evidence),
                graphEntityCount=len(graph_entities),
                graphRelationshipCount=len(graph_relationships),
            ),
        )

    except DocumentNotFoundError as ex:
        logger.warning(
            "Engineering Copilot document not found document_id=%s",
            request.document_id,
        )
        raise HTTPException(status_code=404, detail=str(ex)) from ex

    except DocumentNotFoundError as ex:
        logger.warning(
            "Engineering Copilot document not found document_id=%s",
            request.document_id,
        )
        raise HTTPException(status_code=404, detail=str(ex)) from ex

    except RetrievalError as ex:
        logger.warning(
            "Engineering Copilot retrieval failed document_id=%s",
            request.document_id,
        )
        raise HTTPException(status_code=500, detail=str(ex)) from ex

    except ReasoningError as ex:
        logger.warning(
            "Engineering Copilot reasoning failed document_id=%s",
            request.document_id,
        )
        raise HTTPException(status_code=500, detail=str(ex)) from ex

    except Exception as ex:
        logger.exception(
            "Engineering Copilot request failed document_id=%s",
            request.document_id,
        )
        raise HTTPException(
            status_code=500,
            detail="Engineering Copilot request failed",
        ) from ex

    except Exception as ex:
        logger.exception(
            "Engineering Copilot request failed document_id=%s",
            request.document_id,
        )
        raise HTTPException(status_code=500, detail="Engineering Copilot request failed") from ex