import { API_BASE_URL } from "./client";

export type UploadedDocument = {
  filename: string;
  size_bytes: number;
  uploaded_at?: string;
  content_type?: string;
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
    throw new Error("Failed to upload documents");
  }

  const data = await response.json();
  return data.uploaded_files;
}

export async function getDocuments(): Promise<UploadedDocument[]> {
  const response = await fetch(`${API_BASE_URL}/documents`);

  if (!response.ok) {
    throw new Error("Failed to fetch documents");
  }

  const data = await response.json();
  return data.documents;
}