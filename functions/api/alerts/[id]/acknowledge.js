import { updateAlertStatus } from "../../../_lib/db.js";
import { error, json } from "../../../_lib/response.js";

export async function onRequestPost({ request, env, params }) {
  const body = await request.json().catch(() => ({}));
  if (!body.actor) return error("actor is required", 400);
  await updateAlertStatus(env, Number(params.id), "acknowledged", body.actor);
  return json({ status: "acknowledged" });
}
