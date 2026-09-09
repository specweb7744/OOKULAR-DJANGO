import assert from "node:assert/strict";
import { ApiError, createMobileAuthClient, createOokularClient } from "../packages/api-client/src/index.ts";

const origin = process.argv[2];
const password = "Rzeka-zielona-784!Bezpieczna";
assert.equal((await createOokularClient(origin).status()).service, "OOKULAR");
for (const role of ["employee", "employer"] as const) {
  // In-memory store is test-only. A real app must inject native secure storage.
  let token: string | null = null;
  const store = { get: async () => token, set: async (value: string | null) => { token = value; } };
  const app = createMobileAuthClient(origin, store);
  assert.equal((await app.session()).status, 401);
  assert.equal((await app.logIn(`${role}@client.example.test`, password)).status, 200);
  assert.ok(token);
  assert.equal((await app.session()).meta?.is_authenticated, true);
  const account = await app.me();
  assert.deepEqual(account.roles, [role]);
  assert.equal(typeof account.id, "string");
  if (role === "employee") {
    assert.equal((await app.employeeProfile()).revision, 0);
    const draft = await app.saveEmployeeProfile({ revision: 0, display_name: "Ala", location: "Sopot" });
    assert.equal(draft.visibility, "private");
    assert.equal(draft.status, "draft");
    const resumed = createMobileAuthClient(origin, store);
    assert.equal((await resumed.employeeProfile()).display_name, "Ala");
    const updated = await resumed.saveEmployeeProfile({ revision: draft.revision, career_goal: "Nowy zawód" });
    assert.equal(updated.location, "Sopot");
    await assert.rejects(
      app.saveEmployeeProfile({ revision: draft.revision, display_name: "Old draft" }),
      (error: unknown) => error instanceof ApiError && error.status === 409 &&
        (error.details as { code: string }).code === "draft_conflict",
    );
  } else {
    await assert.rejects(app.employeeProfile, (error: unknown) => error instanceof ApiError && error.status === 403);
    await assert.rejects(app.saveEmployeeProfile({ revision: 0 }), (error: unknown) => error instanceof ApiError && error.status === 403);
  }
  assert.equal((await app.logOut()).status, 401);
  assert.equal(token, null);
  await assert.rejects(app.me, (error: unknown) => error instanceof ApiError && error.status === 403);
  const signup = await app.signUp({ email: `${role}.new@client.example.test`, password, role });
  assert.equal(signup.status, 401);
  assert.equal(signup.meta?.is_authenticated, false);
  assert.ok(token);
  await assert.rejects(app.me, (error: unknown) => error instanceof ApiError && error.status === 403);
  await app.logOut();
  const reset = await app.requestPasswordReset(`${role}@client.example.test`);
  assert.equal(reset.status, 200);
}

// A real cookie session exercises the browser client's explicit CSRF handling.
const cookies = new Map<string, string>();
const cookieFetch: typeof fetch = async (input, init = {}) => {
  assert.equal(new URL(String(input)).origin, new URL(origin).origin);
  const headers = new Headers(init.headers);
  headers.set("Cookie", [...cookies].map(([key, value]) => `${key}=${value}`).join("; "));
  const response = await fetch(input, { ...init, headers, redirect: "manual" });
  for (const cookie of response.headers.getSetCookie()) {
    const pair = cookie.split(";", 1)[0];
    const separator = pair.indexOf("=");
    cookies.set(pair.slice(0, separator), pair.slice(separator + 1));
  }
  return response;
};
await cookieFetch(`${origin}/konta/login/`);
const loggedIn = await cookieFetch(`${origin}/konta/login/`, {
  method: "POST",
  body: new URLSearchParams({
    login: "employee@client.example.test", password,
    csrfmiddlewaretoken: cookies.get("csrftoken")!,
  }),
});
assert.equal(loggedIn.status, 302);
const browserClient = createOokularClient(origin, cookieFetch);
const draft = await browserClient.employeeProfile();
assert.equal(draft.career_goal, "Nowy zawód");
await assert.rejects(
  browserClient.saveEmployeeProfile({ revision: draft.revision, desired_role: "Operator" }, "x".repeat(32)),
  (error: unknown) => error instanceof ApiError && error.status === 403,
);
const browserSaved = await browserClient.saveEmployeeProfile(
  { revision: draft.revision, desired_role: "Operator" }, cookies.get("csrftoken")!,
);
assert.equal(browserSaved.desired_role, "Operator");
assert.equal((await browserClient.employeeProfile()).revision, draft.revision + 1);
console.log("TypeScript HTTP: account flows, private profile resume, employee access, conflicts and browser CSRF passed.");
