import { useEffect, useState } from "react";
import "./App.css";

import {
  getDocuments,
  uploadDocuments,
  type UploadedDocument,
} from "./api/documents";

import { askRagQuestion, type RagResponse } from "./api/rag";

function App() {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedDocument[]>([]);
  const [uploadStatus, setUploadStatus] = useState<string>("Checking backend...");

  const [question, setQuestion] = useState<string>(
    "What does the document say about graph construction?"
  );
  const [ragResponse, setRagResponse] = useState<RagResponse | null>(null);
  const [ragStatus, setRagStatus] = useState<string>("Ready");
  const [isAnswerLoading, setIsAnswerLoading] = useState<boolean>(false);

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

    const allowedExtensions = [".pdf", ".txt", ".csv"];

    const unsupportedFiles = Array.from(files).filter((file) => {
      const fileName = file.name.toLowerCase();
      return !allowedExtensions.some((extension) => fileName.endsWith(extension));
    });

    if (unsupportedFiles.length > 0) {
      const unsupportedNames = unsupportedFiles.map((file) => file.name).join(", ");

      setUploadStatus(
        `Upload rejected: ${unsupportedNames}. Only PDF, TXT, and CSV files are supported.`
      );

      event.target.value = "";
      return;
    }

    try {
      setUploadStatus("Uploading...");
      await uploadDocuments(files);

      const documents = await getDocuments();
      setUploadedFiles(documents);
      setUploadStatus("Upload complete");
    } catch (error) {
      setUploadStatus(
        error instanceof Error ? error.message : "Upload failed"
      );
    } finally {
      event.target.value = "";
    }
  }

  async function handleAskQuestion() {
    if (!question.trim()) {
      setRagStatus("Please enter a question before analysing.");
      return;
    }

    try {
      setIsAnswerLoading(true);
      setRagStatus("Searching indexed documents...");
      const response = await askRagQuestion(question, 5);
      setRagResponse(response);
      setRagStatus("Answer generated");
    } catch {
      setRagStatus("Failed to generate answer");
    } finally {
      setIsAnswerLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Enterprise AI Copilot</p>
          <h1>Power Electronics Reliability Copilot</h1>
          <p className="subtitle">
            Diagnose power electronics reliability issues using datasheets,
            maintenance records, engineering knowledge, RAG, and graph-based
            reasoning.
          </p>
        </div>
        <div className="status-card">
          <span className="status-dot" />
          v0.3.0: Engineering Knowledge Retrieval
        </div>
      </header>

      <section className="dashboard-grid">
        <section className="panel">
          <h2>1. Upload resources</h2>
          <p className="panel-text">
            Add datasheets, reliability notes, test reports, maintenance logs,
            or technical manuals for indexing and ingestion.
          </p>

          <label className="upload-box">
            <input type="file" multiple onChange={handleFileUpload} />
            <span>Click to upload documents</span>
            <small>PDF, TXT, CSV supported now; parsing added in v0.3.0</small>
            <small>Status: {uploadStatus}</small>
          </label>

          <div className="file-list">
            <h3>Uploaded files</h3>
            {uploadedFiles.length === 0 ? (
              <div className="empty-state">
                <strong>📂 No engineering documents uploaded yet.</strong>
                <span>
                  Upload a PDF, TXT, or CSV file to begin building the knowledge
                  base.
                </span>
              </div>
            ) : (
              uploadedFiles.map((file) => (
                <div className="file-row" key={file.filename}>
                  <span>✓</span>
                  <p>
                    {file.filename}
                    <small>
                      {Math.round(file.size_bytes / 1024)} KB
                      {file.uploaded_at
                        ? ` · ${new Date(file.uploaded_at).toLocaleDateString()}`
                        : ""}
                    </small>
                  </p>
                </div>
              ))
            )}
          </div>
        </section>

        <section className="panel">
          <h2>2. Ask reliability question</h2>
          <p className="panel-text">
            Ask about failure modes, symptoms, root causes, evidence, risk, and
            recommended maintenance actions.
          </p>

          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
          />

          <button onClick={handleAskQuestion} disabled={isAnswerLoading}>
            {isAnswerLoading ? "Analysing..." : "Analyse reliability issue"}
          </button>
          <small className="rag-status">Status: {ragStatus}</small>
        </section>

        <section className="panel result-panel">
          <h2>3. AI recommendation</h2>
          <div className="answer-box">
            <h3>Engineering answer</h3>
            <p>
              {ragResponse
                ? ragResponse.answer
                : "Ask a reliability question to generate an evidence-backed answer."}
            </p>

            <div className="confidence">
              <span>Confidence</span>
              <strong>
                {ragResponse ? ragResponse.confidence : "Not evaluated"}
              </strong>
            </div>
          </div>
        </section>
      </section>

      <section className="bottom-grid">
        <section className="panel">
          <h2>Evidence</h2>
          {ragResponse ? (
            <div className="evidence-list">
              {ragResponse.sources.map((source) => (
                <article className="evidence-card" key={source.chunk_id}>
                  <div className="evidence-card-header">
                    <strong>📄 {source.source_document}</strong>
                    <span>Score {source.score}</span>
                  </div>
                  <p className="evidence-meta">Chunk: {source.chunk_id}</p>
                  <p>{source.excerpt}</p>
                </article>
              ))}
            </div>
          ) : (
            <p className="empty-state">
              Retrieved evidence will appear here after you ask a question.
            </p>
          )}
        </section>

        <section className="panel">
          <h2>Graph context</h2>
          <div className="graph-box">
            <span>IGBT Module</span>
            <span>→</span>
            <span>Thermal Cycling</span>
            <span>→</span>
            <span>Bond Wire Fatigue</span>
            <span>→</span>
            <span>Maintenance Action</span>
          </div>
        </section>
      </section>
    </main>
  );
}

export default App;