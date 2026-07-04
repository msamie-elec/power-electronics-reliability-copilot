from typing import Any

from app.services.evidence_reasoning_service import evidence_reasoning_service
from app.services.llm_service import generate_evidence_backed_answer


class EngineeringAnswerService:
    def answer_question(
        self,
        document_id: str,
        question: str,
        top_k: int = 5,
        graph_limit: int = 10,
    ) -> dict[str, Any]:
        reasoning_context = evidence_reasoning_service.build_reasoning_context(
            document_id=document_id,
            question=question,
            top_k=top_k,
            graph_limit=graph_limit,
        )

        semantic_evidence = reasoning_context["semanticEvidence"]
        graph_evidence = reasoning_context["graphEvidence"]

        answer = generate_evidence_backed_answer(
            question=question,
            semantic_evidence=semantic_evidence,
            graph_evidence=graph_evidence,
        )

        return {
            "status": "success",
            "documentId": document_id,
            "question": question,
            "answer": answer,
            "semanticEvidence": semantic_evidence,
            "graphEvidence": graph_evidence,
            "reasoningContext": reasoning_context["reasoningContext"],
        }


engineering_answer_service = EngineeringAnswerService()