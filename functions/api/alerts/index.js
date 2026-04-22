import { ensureSeed, listAlerts } from "../../_lib/db.js";
import { json } from "../../_lib/response.js";

export async function onRequestGet({ request, env }) {
  await ensureSeed(env);
  const url = new URL(request.url);
  const status = url.searchParams.get("status") || "";
  const limit = Number(url.searchParams.get("limit") || 100);
  const rows = await listAlerts(env, { status, limit });
  return json({ rows: rows.results || [] });
}
