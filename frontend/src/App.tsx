import { useEffect, useState } from "react";
import "./App.css";
import {
  getDocuments,
  uploadDocuments,
  type UploadedDocument,
} from "./api/documents";

function App() {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedDocument[]>([]);
  const [uploadStatus, setUploadStatus] = useState<string>("Checking backend...");

  useEffect(() => {
    async function loadDocuments() {
      try {
        const documents = await getDocuments();
        setUploadedFiles(documents);
      } catch {
        setUploadStatus("Backend not connected");
      }
    }

    loadDocuments();
  }, []);

  async function handleFileUpload(event: React.ChangeEvent<HTMLInputElement>) {
    const files = event.target.files;

    if (!files || files.length === 0) {
      return;
    }

    try {
      setUploadStatus("Uploading...");
      await uploadDocuments(files);

      const documents = await getDocuments();
      setUploadedFiles(documents);
      setUploadStatus("Backend connected");

      setUploadStatus("Upload complete");
    } catch {
      setUploadStatus("Upload failed");
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
          v0.2.0: Backend API integration
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
                <span>Upload a PDF, TXT, or CSV file to begin building the knowledge base.</span>
              </div>
            ) : (
              uploadedFiles.map((file) => (
                <div className="file-row" key={file.filename}>
                  <span>✓</span>
                  <p>
                    {file.filename}
                    <small>
                      {Math.round(file.size_bytes / 1024)} KB
                      {file.uploaded_at ? ` · ${new Date(file.uploaded_at).toLocaleDateString()}` : ""}
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
            defaultValue={
              "The inverter shows rising junction temperature and intermittent switching faults. What failure mechanisms are likely?"
            }
          />

          <button>Analyse reliability issue</button>
        </section>

        <section className="panel result-panel">
          <h2>3. AI recommendation</h2>
          <div className="answer-box">
            <h3>Likely failure mechanism</h3>
            <p>
              Thermal cycling may be causing bond-wire fatigue or solder-layer
              degradation in the IGBT module.
            </p>

            <h3>Recommended action</h3>
            <p>
              Inspect thermal interface material, review cooling performance,
              compare VCE(sat) trends, and verify gate-driver behaviour.
            </p>

            <div className="confidence">
              <span>Confidence</span>
              <strong>Medium</strong>
            </div>
          </div>
        </section>
      </section>

      <section className="bottom-grid">
        <section className="panel">
          <h2>Evidence</h2>
          <ul>
            <li>IGBT datasheet: thermal limits and switching characteristics</li>
            <li>Maintenance log: repeated temperature warnings</li>
            <li>Reliability note: thermal cycling linked to fatigue mechanisms</li>
          </ul>
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