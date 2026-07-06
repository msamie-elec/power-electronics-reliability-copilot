import { useEffect, useMemo, useRef, useState } from "react";
import "./App.css";

import {
  getDocuments,
  uploadDocuments,
  type UploadedDocument,
} from "./api/documents";

import {
  askEngineeringCopilot,
  type EngineeringCopilotResponse,
} from "./api/engineeringCopilot";

type ConversationItem = {
  id: string;
  question: string;
  response?: EngineeringCopilotResponse;
  createdAt: string;
  answeredAt?: string;
};

function createMessageId() {
  return crypto.randomUUID();
}

function formatTime(value: string) {
  return new Date(value).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}

function getPreview(text: string, limit = 220) {
  if (text.length <= limit) return text;
  return `${text.slice(0, limit).trim()}...`;
}

function MarkdownText({ text }: { text: string }) {
  return (
    <div className="markdown-text">
      {text.split("\n").map((line, index) => {
        const trimmed = line.trim();

        if (!trimmed) return <br key={index} />;

        if (trimmed.startsWith("## ")) {
          return <h3 key={index}>{trimmed.replace("## ", "")}</h3>;
        }

        if (trimmed.startsWith("### ")) {
          return <h4 key={index}>{trimmed.replace("### ", "")}</h4>;
        }

        if (trimmed.startsWith("- ")) {
          return (
            <p key={index} className="bullet">
              • {trimmed.replace("- ", "")}
            </p>
          );
        }

        return <p key={index}>{trimmed}</p>;
      })}
    </div>
  );
}

function App() {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedDocument[]>([]);
  const [uploadStatus, setUploadStatus] = useState("Checking backend...");
  const [selectedDocumentId, setSelectedDocumentId] = useState("DOC-B3198A5");

  const [question, setQuestion] = useState(
    "Why does VCE(sat) increase during power cycling?"
  );

  const [conversation, setConversation] = useState<ConversationItem[]>([]);
  const [selectedItemId, setSelectedItemId] = useState<string | null>(null);

  const [status, setStatus] = useState("Ready");
  const [isLoading, setIsLoading] = useState(false);

  const evidencePanelRef = useRef<HTMLElement | null>(null);

  const selectedItem = useMemo(() => {
    const selected = conversation.find((item) => item.id === selectedItemId);

    if (selected?.response) return selected;

    return [...conversation].reverse().find((item) => Boolean(item.response));
  }, [conversation, selectedItemId]);

  const selectedResponse = selectedItem?.response ?? null;

  useEffect(() => {
    async function loadDocuments() {
      try {
        const documents = await getDocuments();
        setUploadedFiles(documents);
        setUploadStatus("Backend connected");
      } catch {
        setUploadStatus("Backend not connected");
      }
    }

    loadDocuments();
  }, []);

  useEffect(() => {
    evidencePanelRef.current?.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  }, [selectedItemId, selectedResponse?.answer]);

  async function handleFileUpload(event: React.ChangeEvent<HTMLInputElement>) {
    const files = event.target.files;

    if (!files || files.length === 0) return;

    try {
      setUploadStatus("Uploading...");
      await uploadDocuments(files);

      const documents = await getDocuments();
      setUploadedFiles(documents);
      setUploadStatus("Upload complete");
    } catch (error) {
      setUploadStatus(error instanceof Error ? error.message : "Upload failed");
    } finally {
      event.target.value = "";
    }
  }

  function handleClearConversation() {
    setConversation([]);
    setSelectedItemId(null);
    setStatus("Ready");
  }

  async function handleCopySelectedAnswer() {
  if (!selectedResponse) {
    setStatus("No selected answer to copy.");
    return;
  }

  await navigator.clipboard.writeText(selectedResponse.answer);
  setStatus("Selected answer copied to clipboard.");
}

function handleExportConversationMarkdown() {
  if (conversation.length === 0) {
    setStatus("No conversation to export.");
    return;
  }

  const markdown = conversation
    .map((item, index) => {
      const questionNumber = index + 1;

      return [
        `# Question ${questionNumber}`,
        "",
        item.question,
        "",
        item.response ? `# Answer ${questionNumber}` : "# Answer pending",
        "",
        item.response?.answer ?? "No answer generated.",
        "",
        item.response
          ? `## Metadata\n\n- Confidence: ${item.response.confidence}\n- Evidence chunks: ${item.response.metadata.semanticEvidenceCount}\n- Graph entities: ${item.response.metadata.graphEntityCount}\n- Graph relationships: ${item.response.metadata.graphRelationshipCount}`
          : "",
        "",
        "---",
        "",
      ].join("\n");
    })
    .join("\n");

  const blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = "engineering-copilot-conversation.md";
  link.click();

  URL.revokeObjectURL(url);
  setStatus("Conversation exported as Markdown.");
}

  async function handleAskQuestion() {
    if (!question.trim()) {
      setStatus("Please enter a question.");
      return;
    }

    if (!selectedDocumentId.trim()) {
      setStatus("Please enter a document ID.");
      return;
    }

    const userQuestion = question.trim();
    const itemId = createMessageId();

    const newItem: ConversationItem = {
      id: itemId,
      question: userQuestion,
      createdAt: new Date().toISOString(),
    };

    setConversation((current) => [...current, newItem]);
    setSelectedItemId(itemId);

    try {
      setIsLoading(true);
      setStatus("Generating evidence-backed answer...");

      const response = await askEngineeringCopilot(
        selectedDocumentId,
        userQuestion,
        5,
        10
      );

      setConversation((current) =>
        current.map((item) =>
          item.id === itemId
            ? {
                ...item,
                response,
                answeredAt: new Date().toISOString(),
              }
            : item
        )
      );

      setSelectedItemId(itemId);
      setQuestion("");
      setStatus("Answer generated");
    } catch (error) {
      setStatus(
        error instanceof Error
          ? error.message
          : "Failed to generate engineering answer"
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="workspace-shell">
      <header className="workspace-header">
        <div className="header-left">
          <p className="eyebrow">Enterprise AI Copilot</p>
          <strong>Reliability Workspace</strong>
        </div>

        <div className="header-center">
          <h1>Power Electronics Reliability Copilot</h1>
          <p>
            Conversational engineering workspace for evidence-backed reliability
            analysis using semantic retrieval, Knowledge Graphs and AI reasoning.
          </p>
        </div>

        <div className="header-right">
          <div className="release-badge">
            <span />
            v0.5.1 Conversational Engineering Workspace
          </div>
        </div>
      </header>

      <section className="workspace-layout">
        <aside className="sidebar">
          <h2>Documents</h2>

          <label className="upload-card">
            <input type="file" multiple onChange={handleFileUpload} />
            <strong>Upload documents</strong>
            <span>PDF, TXT and CSV supported</span>
            <small>Status: {uploadStatus}</small>
          </label>

          <div className="document-id-card">
            <label>
              Knowledge document ID
              <input
                value={selectedDocumentId}
                onChange={(event) => setSelectedDocumentId(event.target.value)}
              />
            </label>
            <small>
              Temporary manual ID until the UI is connected to the knowledge
              document registry.
            </small>
          </div>

          <div className="document-list">
            <h3>Uploaded files</h3>

            {uploadedFiles.length === 0 ? (
              <p className="muted">No uploaded files found.</p>
            ) : (
              uploadedFiles.map((file) => (
                <div className="document-row" key={file.filename}>
                  <span>✓</span>
                  <div>
                    <strong>{file.filename}</strong>
                    <small>
                      {Math.round(file.size_bytes / 1024)} KB
                      {file.uploaded_at
                        ? ` · ${new Date(
                            file.uploaded_at
                          ).toLocaleDateString()}`
                        : ""}
                    </small>
                  </div>
                </div>
              ))
            )}
          </div>

          {conversation.length > 0 && (
            <div className="document-list">
              <h3>Conversation</h3>
              <button
                className="secondary-button"
                onClick={handleCopySelectedAnswer}
              >
                Copy selected answer
              </button>

              <button
                className="secondary-button"
                onClick={handleExportConversationMarkdown}
              >
                Export Markdown
              </button>

              <button
                className="secondary-button danger-button"
                onClick={handleClearConversation}
              >
                Clear conversation
              </button>
            </div>
          )}
        </aside>

        <section className="chat-panel">
          <div className="chat-header">
            <div>
              <h2>Engineering conversation</h2>
              <p>{status}</p>
            </div>

            <span className="confidence-pill">
              Confidence: {selectedResponse?.confidence ?? "Not evaluated"}
            </span>
          </div>

          <div className="chat-window">
            {conversation.length === 0 ? (
              <div className="welcome-card">
                <h2>Ask an engineering reliability question</h2>
                <p>
                  The Copilot will retrieve relevant document evidence, inspect
                  Knowledge Graph context and generate a structured engineering
                  response.
                </p>
              </div>
            ) : (
              conversation.map((item, index) => {
                const isSelected = item.id === selectedItemId;
                const answerNumber = index + 1;

                return (
                  <div className="conversation-pair" key={item.id}>
                    <article className="message user">
                      <div className="message-title-row">
                        <strong>Question #{answerNumber}</strong>
                        <span>{formatTime(item.createdAt)}</span>
                      </div>
                      <p>{item.question}</p>
                    </article>

                    {item.response ? (
                      <article
                        className={`message assistant ${
                          isSelected ? "selected-message" : "collapsed-message"
                        }`}
                        onClick={() => setSelectedItemId(item.id)}
                      >
                        <div className="message-title-row">
                          <strong>Engineering Copilot — Answer #{answerNumber}</strong>
                          <span>
                            {item.answeredAt ? formatTime(item.answeredAt) : ""}
                          </span>
                        </div>

                        {isSelected ? (
                          <MarkdownText text={item.response.answer} />
                        ) : (
                          <p className="answer-preview">
                            {getPreview(item.response.answer)}
                          </p>
                        )}

                        <div className="message-meta">
                          <span>{item.response.confidence}</span>
                          <span>
                            {item.response.metadata.semanticEvidenceCount}{" "}
                            evidence chunks
                          </span>
                          <span>
                            {item.response.metadata.graphRelationshipCount} graph
                            links
                          </span>
                          <span>{isSelected ? "Expanded" : "Click to expand"}</span>
                        </div>
                      </article>
                    ) : (
                      <article className="message assistant selected-message">
                        <strong>Engineering Copilot</strong>
                        <p>Analysing evidence and preparing answer...</p>
                      </article>
                    )}
                  </div>
                );
              })
            )}
          </div>

          <div className="composer">
            <textarea
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Ask about failure mechanisms, VCE(sat), thermal cycling, bond wire degradation, maintenance actions..."
            />

            <button onClick={handleAskQuestion} disabled={isLoading}>
              {isLoading ? "Analysing..." : "Ask Engineering Copilot"}
            </button>
          </div>
        </section>

        <aside className="evidence-panel" ref={evidencePanelRef}>
          <section className="evidence-section">
            <div className="evidence-panel-header">
              <h2>Evidence</h2>
              {selectedItem && (
                <span>
                  Question #
                  {conversation.findIndex((item) => item.id === selectedItem.id) + 1}
                </span>
              )}
            </div>

            {selectedItem && (
              <p className="evidence-question-preview">
                {selectedItem.question}
              </p>
            )}

            {!selectedResponse ? (
              <p className="muted">
                Retrieved evidence will appear after the first question.
              </p>
            ) : selectedResponse.semanticEvidence.length === 0 ? (
              <p className="muted">No semantic evidence returned.</p>
            ) : (
              <>
                <div className="evidence-summary-row">
                  <span>{selectedResponse.semanticEvidence.length} chunks</span>
                  <span>{selectedResponse.citations.length} citations</span>
                  <span>
                    {selectedResponse.graphEvidence.relationships.length} graph links
                  </span>
                </div>

                <div className="evidence-list">
                  {selectedResponse.semanticEvidence.map((item, index) => (
                    <article className="evidence-card" key={item.chunkId ?? index}>
                      <div className="evidence-card-top">
                        <strong>Evidence #{index + 1}</strong>
                        <span>
                          {typeof item.score === "number"
                            ? item.score.toFixed(3)
                            : "N/A"}
                        </span>
                      </div>

                      <small>
                        {item.documentId ?? "Document"} · Chunk{" "}
                        {item.chunkId ?? "Unknown"}
                      </small>

                      <p>{item.text ?? "No evidence text available."}</p>
                    </article>
                  ))}
                </div>
              </>
            )}
          </section>

          <section className="evidence-section">
            <h2>Citations</h2>

            {!selectedResponse || selectedResponse.citations.length === 0 ? (
              <p className="muted">No citations available yet.</p>
            ) : (
              <div className="citation-list">
                {selectedResponse.citations.map((citation, index) => (
                  <div className="citation-chip" key={index}>
                    <strong>[{index + 1}] </strong>
                    {citation.citationType === "graph_relationship"
                      ? citation.relationship ?? "Graph relationship"
                      : `${citation.source ?? "Document"} · ${
                          citation.chunkId ?? "Chunk"
                        }`}
                  </div>
                ))}
              </div>
            )}
          </section>

          <section className="evidence-section">
            <h2>Knowledge Graph</h2>

            {!selectedResponse ? (
              <div className="graph-placeholder">
                <span>IGBT Module</span>
                <span>Thermal Cycling</span>
                <span>Bond Wire Fatigue</span>
              </div>
            ) : selectedResponse.graphEvidence.relationships.length === 0 ? (
              <p className="muted">No graph relationships returned.</p>
            ) : (
              <div className="graph-list">
                {selectedResponse.graphEvidence.relationships.map(
                  (relationship, index) => (
                    <div className="graph-path-card" key={index}>
                      <strong>{relationship.source ?? "Unknown source"}</strong>
                      <span>{relationship.relationshipType ?? "RELATED_TO"}</span>
                      <strong>{relationship.target ?? "Unknown target"}</strong>
                    </div>
                  )
                )}
              </div>
            )}
          </section>

          <section className="evidence-section">
            <h2>Response Metadata</h2>

            {!selectedResponse ? (
              <p className="muted">Metadata will appear after an answer is generated.</p>
            ) : (
              <div className="metadata-grid">
                <div>
                  <strong>{selectedResponse.metadata.semanticEvidenceCount}</strong>
                  <span>Evidence chunks</span>
                </div>

                <div>
                  <strong>{selectedResponse.metadata.graphEntityCount}</strong>
                  <span>Graph entities</span>
                </div>

                <div>
                  <strong>{selectedResponse.metadata.graphRelationshipCount}</strong>
                  <span>Graph links</span>
                </div>

                <div>
                  <strong>{selectedResponse.metadata.topK}</strong>
                  <span>Top-K retrieval</span>
                </div>
              </div>
            )}
          </section>
        </aside>
      </section>
    </main>
  );
}

export default App;