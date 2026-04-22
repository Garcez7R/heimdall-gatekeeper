import { ensureSeed, ingestEvent } from "../../_lib/db.js";
import { error, json } from "../../_lib/response.js";

export async function onRequestPost({ request, env }) {
  await ensureSeed(env);
  const payload = await request.json().catch(() => null);
  if (!payload || !payload.source || !payload.event_type || !payload.title || !payload.message) {
    return error("source, event_type, title and message are required", 400);
  }
  return json(await ingestEvent(env, payload));
}
