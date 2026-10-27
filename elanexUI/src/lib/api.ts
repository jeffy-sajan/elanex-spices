const API_BASE_URL =
  import.meta.env["VITE_API_BASE_URL"] ?? "http://127.0.0.1:8000/api";
const REQUEST_TIMEOUT_MS = 10000;

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status?: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function request(url: string, init?: RequestInit): Promise<Response> {
  const controller = new AbortController();
  const timeout = globalThis.setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
  try {
    return await fetch(url, { ...init, signal: controller.signal });
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new ApiError("The request timed out. Please try again.");
    }
    throw new ApiError("The service is currently unavailable. Please try again.");
  } finally {
    globalThis.clearTimeout(timeout);
  }
}

export type HealthResponse = {
  status: string;
  service: string;
};

export async function getHealth(): Promise<HealthResponse> {
  const response = await request(`${API_BASE_URL}/health/`, {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new ApiError(`Backend health check failed with status ${response.status}`, response.status);
  }

  return response.json() as Promise<HealthResponse>;
}

export type ContactMessage = {
  name: string;
  email: string;
  message: string;
};

export async function sendContactMessage(payload: ContactMessage): Promise<void> {
  const response = await request(`${API_BASE_URL}/contact/`, {
    method: "POST",
    headers: { Accept: "application/json", "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const data = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new ApiError(data?.detail ?? "We could not send your message.", response.status);
  }
}
