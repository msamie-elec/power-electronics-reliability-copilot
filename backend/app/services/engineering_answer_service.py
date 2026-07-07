"""
Power Electronics Reliability Copilot
Engineering Answer Service

Orchestrates evidence retrieval, evidence preparation, and evidence-backed
LLM answer generation.

v0.5.2 update
-------------
The service accepts recent conversation history and passes it to the reasoning
prompt so follow-up questions can use prior engineering context without losing
evidence-first grounding.
"""

import logging
from typing import Any

from app.core.exceptions import DocumentNotFoundError, ReasoningError, RetrievalError
from app.services.evidence_preparation_service import evidence_preparation_service
from app.services.evidence_reasoning_service import evidence_reasoning_service
from app.services.llm_service import generate_evidence_backed_answer


logger = logging.getLogger(__name__)


class EngineeringAnswerService:
    def answer_question(
        self,
        document_id: str,
        question: str,
        top_k: int = 5,
        graph_limit: int = 10,
        conversation_history: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        logger.info(
            "Building engineering answer for document_id=%s history_turns=%s",
            document_id,
            len(conversation_history or []),
        )

        try:
            reasoning_context = evidence_reasoning_service.build_reasoning_context(
                document_id=document_id,
                question=question,
                top_k=top_k,
                graph_limit=graph_limit,
            )
        except FileNotFoundError as ex:
            raise DocumentNotFoundError(str(ex)) from ex
        except Exception as ex:
            raise RetrievalError("Failed to build evidence reasoning context") from ex

        try:
            semantic_evidence = (
                evidence_preparation_service.rank_and_deduplicate_semantic_evidence(
                    reasoning_context.get("semanticEvidence", []),
                    limit=top_k,
                )
            )

            graph_evidence = evidence_preparation_service.prepare_graph_evidence(
                reasoning_context.get("graphEvidence", {}),
                limit=graph_limit,
            )

            logger.info(
                "Prepared evidence for document_id=%s semantic=%s graph_entities=%s graph_relationships=%s history_turns=%s",
                document_id,
                len(semantic_evidence),
                len(graph_evidence["entities"]),
                len(graph_evidence["relationships"]),
                len(conversation_history or []),
            )

            answer = generate_evidence_backed_answer(
                question=question,
                semantic_evidence=semantic_evidence,
                graph_evidence=graph_evidence,
                conversation_history=conversation_history or [],
            )

        except Exception as ex:
            raise ReasoningError(
                "Failed to generate evidence-backed engineering answer"
            ) from ex

        logger.info("Generated engineering answer for document_id=%s", document_id)

        return {
            "status": "success",
            "documentId": document_id,
            "question": question,
            "answer": answer,
            "semanticEvidence": semantic_evidence,
            "graphEvidence": graph_evidence,
            "reasoningContext": {
                **reasoning_context.get("reasoningContext", {}),
                "semanticEvidenceCount": len(semantic_evidence),
                "graphEntityCount": len(graph_evidence["entities"]),
                "graphRelationshipCount": len(graph_evidence["relationships"]),
                "conversationHistoryCount": len(conversation_history or []),
            },
        }


engineering_answer_service = EngineeringAnswerService()
