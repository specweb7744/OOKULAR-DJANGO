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
console.log("TypeScript client: both roles, session persistence, logout, pending verification and reset passed.");
