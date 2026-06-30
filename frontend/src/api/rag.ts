import { API_BASE_URL } from "./client";

export type RagSource = {
  source_document: string;
  chunk_id: string;
  score: number;
  excerpt: string;
};

export type RagResponse = {
  query: string;
  answer: string;
  confidence: string;
  sources: RagSource[];
  retrieved_chunks: unknown[];
};

export async function askRagQuestion(
  query: string,
  topK: number = 5
): Promise<RagResponse> {
  const response = await fetch(`${API_BASE_URL}/rag/answer`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
      top_k: topK,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to get RAG answer");
  }

  return response.json();
}