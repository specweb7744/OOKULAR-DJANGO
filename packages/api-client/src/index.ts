/** Shared fetch-based client. User IDs are opaque strings, never arithmetic values. */
export type AccountRole = "employee" | "employer";
export interface Account {
  id: string;
  email: string;
  roles: AccountRole[];
}
export interface ApiStatus {
  service: "OOKULAR";
  api_version: "v1";
  stage: "foundation";
}
export class ApiError extends Error {
  constructor(public readonly status: number) {
    super(`OOKULAR API returned HTTP ${status}`);
    this.name = "ApiError";
  }
}

/**
 * Pass the root origin, e.g. http://127.0.0.1:8000.
 * status() is usable by web and mobile. me() currently needs a Django web session.
 * Mobile credential exchange will be added with the account module; no fake token support.
 */
export function createOokularClient(origin: string, fetcher: typeof fetch = fetch) {
  const base = new URL(origin);
  if (!["http:", "https:"].includes(base.protocol)) {
    throw new Error("OOKULAR API requires an HTTP(S) origin.");
  }
  async function get<T>(path: string, signal?: AbortSignal): Promise<T> {
    const response = await fetcher(new URL(path, base), {
      method: "GET",
      credentials: "include",
      headers: { Accept: "application/json" },
      signal,
    });
    if (!response.ok) throw new ApiError(response.status);
    return response.json() as Promise<T>;
  }
  return {
    status: (signal?: AbortSignal) => get<ApiStatus>("/api/v1/", signal),
    me: (signal?: AbortSignal) => get<Account>("/api/v1/me/", signal),
  };
}
