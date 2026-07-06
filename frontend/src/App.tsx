import { useEffect, useMemo, useState } from "react";
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

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  response?: EngineeringCopilotResponse;
};

function createMessageId() {
  return crypto.randomUUID();
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

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [selectedMessageId, setSelectedMessageId] = useState<string | null>(
    null
  );

  const [status, setStatus] = useState("Ready");
  const [isLoading, setIsLoading] = useState(false);

  const selectedAssistantMessage = useMemo(() => {
    const selected = messages.find(
      (message) =>
        message.id === selectedMessageId && message.role === "assistant"
    );

    if (selected?.response) return selected;

    return [...messages]
      .reverse()
      .find(
        (message) => message.role === "assistant" && Boolean(message.response)
      );
  }, [messages, selectedMessageId]);

  const selectedResponse = selectedAssistantMessage?.response ?? null;

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
    setMessages([]);
    setSelectedMessageId(null);
    setStatus("Ready");
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

    const userMessage: ChatMessage = {
      id: createMessageId(),
      role: "user",
      content: userQuestion,
    };

    setMessages((current) => [...current, userMessage]);

    try {
      setIsLoading(true);
      setStatus("Generating evidence-backed answer...");

      const response = await askEngineeringCopilot(
        selectedDocumentId,
        userQuestion,
        5,
        10
      );

      const assistantMessage: ChatMessage = {
        id: createMessageId(),
        role: "assistant",
        content: response.answer,
        response,
      };

      setMessages((current) => [...current, assistantMessage]);
      setSelectedMessageId(assistantMessage.id);

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

          {messages.length > 0 && (
            <div className="document-list">
              <h3>Conversation</h3>
              <button
                className="secondary-button"
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
            {messages.length === 0 ? (
              <div className="welcome-card">
                <h2>Ask an engineering reliability question</h2>
                <p>
                  The Copilot will retrieve relevant document evidence, inspect
                  Knowledge Graph context and generate a structured engineering
                  response.
                </p>
              </div>
            ) : (
              messages.map((message) => (
                <article
                  className={`message ${message.role} ${
                    message.id === selectedMessageId ? "selected-message" : ""
                  }`}
                  key={message.id}
                  onClick={() => {
                    if (message.role === "assistant") {
                      setSelectedMessageId(message.id);
                    }
                  }}
                >
                  <strong>
                    {message.role === "user" ? "You" : "Engineering Copilot"}
                  </strong>

                  {message.role === "assistant" ? (
                    <>
                      <MarkdownText text={message.content} />

                      {message.response && (
                        <div className="message-meta">
                          <span>{message.response.confidence}</span>
                          <span>
                            {message.response.metadata.semanticEvidenceCount}{" "}
                            evidence chunks
                          </span>
                          <span>
                            {message.response.metadata.graphRelationshipCount}{" "}
                            graph links
                          </span>
                        </div>
                      )}
                    </>
                  ) : (
                    <p>{message.content}</p>
                  )}
                </article>
              ))
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

        <aside className="evidence-panel">
          <section className="evidence-section">
            <h2>Evidence</h2>

            {!selectedResponse ? (
              <p className="muted">
                Retrieved evidence will appear after the first question.
              </p>
            ) : selectedResponse.semanticEvidence.length === 0 ? (
              <p className="muted">No semantic evidence returned.</p>
            ) : (
              <div className="evidence-list">
                {selectedResponse.semanticEvidence.map((item, index) => (
                  <article className="evidence-card" key={item.chunkId ?? index}>
                    <div className="evidence-card-top">
                      <strong>{item.documentId ?? "Document evidence"}</strong>
                      <span>
                        {typeof item.score === "number"
                          ? item.score.toFixed(3)
                          : "N/A"}
                      </span>
                    </div>

                    <small>Chunk: {item.chunkId ?? "Unknown"}</small>
                    <p>{item.text ?? "No evidence text available."}</p>
                  </article>
                ))}
              </div>
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
            <h2>Graph context</h2>

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
                    <div className="graph-link" key={index}>
                      <strong>{relationship.source}</strong>
                      <span>{relationship.relationshipType}</span>
                      <strong>{relationship.target}</strong>
                    </div>
                  )
                )}
              </div>
            )}
          </section>
        </aside>
      </section>
    </main>
  );
}

export default App;