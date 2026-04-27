import { json } from "../../_lib/response.js";
import { listWebhooks } from "../../_lib/db.js";

export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const limit = Number(url.searchParams.get("limit") || 50);
  const rows = await listWebhooks(env, { limit });
  return json({ webhooks: rows.results || [], total: rows.results?.length || 0 });
}
