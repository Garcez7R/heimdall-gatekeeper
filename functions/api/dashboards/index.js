import { json } from "../../_lib/response.js";
import { listDashboards } from "../../_lib/db.js";

export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const limit = Number(url.searchParams.get("limit") || 20);
  const rows = await listDashboards(env, { limit });
  return json({ dashboards: rows.results || [] });
}
