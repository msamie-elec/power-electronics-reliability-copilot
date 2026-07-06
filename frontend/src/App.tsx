import { useEffect, useState } from "react";
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

function MarkdownText({ text }: { text: string }) {
  return (
    <div className="markdown-text">
      {text.split("\n").map((line, index) => {
        const trimmed = line.trim();

        if (!trimmed) {
          return <br key={index} />;
        }

        if (trimmed.startsWith("## ")) {
          return <h3 key={index}>{trimmed.replace("## ", "")}</h3>;
        }

        if (trimmed.startsWith("### ")) {
          return <h4 key={index}>{trimmed.replace("### ", "")}</h4>;
        }

        if (trimmed.startsWith("- ")) {
          return <p key={index} className="bullet">• {trimmed.replace("- ", "")}</p>;
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
  const [copilotResponse, setCopilotResponse] =
    useState<EngineeringCopilotResponse | null>(null);

  const [status, setStatus] = useState("Ready");
  const [isLoading, setIsLoading] = useState(false);

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

    setMessages((current) => [
      ...current,
      { role: "user", content: userQuestion },
    ]);

    try {
      setIsLoading(true);
      setStatus("Generating evidence-backed answer...");

      const response = await askEngineeringCopilot(
        selectedDocumentId,
        userQuestion,
        5,
        10
      );

      setCopilotResponse(response);

      setMessages((current) => [
        ...current,
        { role: "assistant", content: response.answer },
      ]);

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
                onChange={(event) =>
                  setSelectedDocumentId(event.target.value)
                }
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
        </aside>

        <section className="chat-panel">
          <div className="chat-header">
            <div>
              <h2>Engineering conversation</h2>
              <p>{status}</p>
            </div>
            <span className="confidence-pill">
              Confidence: {copilotResponse?.confidence ?? "Not evaluated"}
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
              messages.map((message, index) => (
                <article
                  className={`message ${message.role}`}
                  key={`${message.role}-${index}`}
                >
                  <strong>
                    {message.role === "user" ? "You" : "Engineering Copilot"}
                  </strong>

                  {message.role === "assistant" ? (
                    <MarkdownText text={message.content} />
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

            {!copilotResponse ? (
              <p className="muted">
                Retrieved evidence will appear after the first question.
              </p>
            ) : (
              <div className="evidence-list">
                {copilotResponse.semanticEvidence.map((item, index) => (
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
                    <p>{item.text}</p>
                  </article>
                ))}
              </div>
            )}
          </section>

          <section className="evidence-section">
            <h2>Citations</h2>

            {!copilotResponse || copilotResponse.citations.length === 0 ? (
              <p className="muted">No citations available yet.</p>
            ) : (
              <div className="citation-list">
                {copilotResponse.citations.map((citation, index) => (
                  <div className="citation-chip" key={index}>
                    {citation.citationType === "graph_relationship"
                      ? citation.relationship
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

            {!copilotResponse ? (
              <div className="graph-placeholder">
                <span>IGBT Module</span>
                <span>Thermal Cycling</span>
                <span>Bond Wire Fatigue</span>
              </div>
            ) : copilotResponse.graphEvidence.relationships.length === 0 ? (
              <p className="muted">No graph relationships returned.</p>
            ) : (
              <div className="graph-list">
                {copilotResponse.graphEvidence.relationships.map(
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