import { json } from "../../_lib/response.js";
import { listAuditEvents } from "../../_lib/db.js";

export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const limit = Number(url.searchParams.get("limit") || 10);
  const rows = await listAuditEvents(env, { limit });
  return json({ events: rows.results || [] });
}
