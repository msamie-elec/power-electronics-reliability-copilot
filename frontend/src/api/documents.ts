import { API_BASE_URL } from "./client";

export type UploadedDocument = {
  documentId: string;
  filename: string;
  sizeBytes: number;
  uploadedAt?: string;
  source?: string;
  status?: string;
};

export async function uploadDocuments(files: FileList): Promise<UploadedDocument[]> {
  const formData = new FormData();

  Array.from(files).forEach((file) => {
    formData.append("files", file);
  });

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail ?? "Failed to upload documents");
  }

  const data = await response.json();
  return data.uploaded_files ?? [];
}

export async function getDocuments(): Promise<UploadedDocument[]> {
  const response = await fetch(`${API_BASE_URL}/documents`);

  if (!response.ok) {
    throw new Error("Failed to fetch documents");
  }

  const data = await response.json();

  return (data.documents ?? []).map((document: any) => ({
    documentId: document.documentId,
    filename: document.filename,
    sizeBytes: document.sizeBytes ?? document.size_bytes ?? 0,
    uploadedAt: document.uploadedAt ?? document.uploaded_at,
    source: document.source,
    status: document.status,
  }));
}