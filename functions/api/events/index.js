import { ensureSeed, listEvents } from "../../_lib/db.js";
import { json } from "../../_lib/response.js";

export async function onRequestGet({ request, env }) {
  await ensureSeed(env);
  const url = new URL(request.url);
  const search = url.searchParams.get("search") || "";
  const severity = url.searchParams.get("severity") || "";
  const limit = Number(url.searchParams.get("limit") || 100);
  const rows = await listEvents(env, { search, severity, limit });
  return json({ rows: rows.results || [] });
}
