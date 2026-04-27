import { json, error } from "../../_lib/response.js";
import { createJwtToken } from "../../_lib/jwt.js";

const DEMO_USERS = {
  admin: "admin123",
  analyst: "analyst123",
};

export async function onRequestPost({ request, env }) {
  const payload = await request.json().catch(() => null);
  if (!payload || !payload.username || !payload.password) {
    return error("username and password are required", 400);
  }

  const expectedPassword = DEMO_USERS[payload.username];
  if (!expectedPassword || expectedPassword !== payload.password) {
    return error("Invalid username or password", 401);
  }

  const role = payload.username === "admin" ? "admin" : "analyst";
  const expiresAt = Math.floor(Date.now() / 1000) + 24 * 3600;
  const token = await createJwtToken(
    {
      username: payload.username,
      role,
      exp: expiresAt,
    },
    env.JWT_SECRET || "demo-secret-key-phase3-2026"
  );

  return json({
    access_token: token,
    token_type: "Bearer",
    expires_in: 24 * 3600,
  });
}
