import { ensureSeed } from "../../_lib/db.js";
import { json } from "../../_lib/response.js";

export async function onRequestPost({ env }) {
  await ensureSeed(env);
  return json({ status: "ok" });
}

export async function onRequestGet({ env }) {
  await ensureSeed(env);
  return json({ status: "ok" });
}
