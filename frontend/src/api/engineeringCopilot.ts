import { API_BASE_URL } from "./client";

export type SemanticEvidenceItem = {
  chunkId?: string | null;
  documentId?: string | null;
  chunkIndex?: number | null;
  score?: number | null;
  text?: string | null;
  metadata?: Record<string, unknown>;
};

export type GraphEntityItem = {
  name?: string | null;
  labels: string[];
  properties: Record<string, unknown>;
};

export type GraphRelationshipItem = {
  source?: string | null;
  relationshipType?: string | null;
  target?: string | null;
  properties: Record<string, unknown>;
};

export type GraphEvidence = {
  entities: GraphEntityItem[];
  relationships: GraphRelationshipItem[];
};

export type EngineeringCitation = {
  citationType: string;
  source?: string | null;
  chunkId?: string | null;
  score?: number | null;
  relationship?: string | null;
};

export type ConversationTurn = {
  question: string;
  answer?: string | null;
};

export type EngineeringCopilotResponse = {
  status: string;
  documentId: string;
  question: string;
  answer: string;
  confidence: "High" | "Medium" | "Low" | "Not evaluated";
  recommendedNextStep?: string | null;
  semanticEvidence: SemanticEvidenceItem[];
  graphEvidence: GraphEvidence;
  citations: EngineeringCitation[];
  reasoningContext: {
    readyForLLM: boolean;
    semanticEvidenceCount: number;
    graphEntityCount: number;
    graphRelationshipCount: number;
  };
  metadata: {
    topK: number;
    graphLimit: number;
    semanticEvidenceCount: number;
    graphEntityCount: number;
    graphRelationshipCount: number;
  };
};

export async function askEngineeringCopilot(
  documentId: string,
  question: string,
  topK: number = 5,
  graphLimit: number = 10,
  conversationHistory: ConversationTurn[] = []
): Promise<EngineeringCopilotResponse> {
  const response = await fetch(`${API_BASE_URL}/engineering-copilot/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      document_id: documentId,
      question,
      top_k: topK,
      graph_limit: graphLimit,
      conversation_history: conversationHistory,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail ?? "Failed to ask Engineering Copilot");
  }

  return response.json();
}