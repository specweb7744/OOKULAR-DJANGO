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
 * Browser client: uses the same-origin Django session cookie.
 * Native clients should use createMobileAuthClient and their platform secure storage.
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


export interface SessionStore {
  get(): Promise<string | null>;
  set(token: string | null): Promise<void>;
}
export interface AuthEnvelope {
  status: number;
  data?: {
    user?: { id: string | null };
    flows?: Array<{ id: string; is_pending?: boolean }>;
    [key: string]: unknown;
  };
  meta?: { is_authenticated?: boolean; session_token?: string };
  errors?: Array<{ code: string; message: string; param?: string }>;
}

/**
 * Native app only. Inject Keychain/Keystore storage; never use localStorage.
 * 401 + pending verify_email is a normal signup result. Persist its token too.
 * Mail links also work in the browser; then log in from the native app.
 * All operations are serialized so token rotation cannot race with logout.
 */
export function createMobileAuthClient(
  origin: string, store: SessionStore, fetcher: typeof fetch = fetch,
) {
  const base = new URL(origin);
  if (!["http:", "https:"].includes(base.protocol) || base.username || base.password) {
    throw new Error("OOKULAR API requires an HTTP(S) origin without credentials.");
  }
  let queue: Promise<unknown> = Promise.resolve();
  function serial<T>(operation: () => Promise<T>): Promise<T> {
    const next = queue.then(operation, operation);
    queue = next.catch(() => undefined);
    return next;
  }
  async function send(path: string, method: string, data?: object): Promise<Response> {
    const token = await store.get();
    return fetcher(new URL(path, base), {
      method,
      credentials: "omit",
      headers: {
        Accept: "application/json",
        ...(data ? { "Content-Type": "application/json" } : {}),
        ...(token ? { "X-Session-Token": token } : {}),
      },
      ...(data ? { body: JSON.stringify(data) } : {}),
    });
  }
  function auth(path: string, method = "POST", data?: object): Promise<AuthEnvelope> {
    return serial(async () => {
      const response = await send("/api/auth/app/v1/" + path, method, data);
      if (response.status >= 500) throw new ApiError(response.status);
      const result = await response.json() as AuthEnvelope;
      if (result.meta?.session_token) await store.set(result.meta.session_token);
      if (response.status === 410 || (method === "DELETE" && response.status === 401)) {
        await store.set(null);
      }
      return result;
    });
  }
  return {
    signUp: (data: { email: string; password: string; role: AccountRole }) =>
      auth("auth/signup", "POST", data),
    logIn: (email: string, password: string) => auth("auth/login", "POST", { email, password }),
    session: () => auth("auth/session", "GET"),
    logOut: () => auth("auth/session", "DELETE"),
    verifyEmail: (key: string) => auth("auth/email/verify", "POST", { key }),
    resendVerification: (email: string) => auth("auth/email/verify/resend", "POST", { email }),
    requestPasswordReset: (email: string) => auth("auth/password/request", "POST", { email }),
    resetPassword: (key: string, password: string) => auth("auth/password/reset", "POST", { key, password }),
    changePassword: (current_password: string, new_password: string) =>
      auth("account/password/change", "POST", { current_password, new_password }),
    me: () => serial(async () => {
      const response = await send("/api/v1/me/", "GET");
      if (!response.ok) throw new ApiError(response.status);
      return response.json() as Promise<Account>;
    }),
  };
}
