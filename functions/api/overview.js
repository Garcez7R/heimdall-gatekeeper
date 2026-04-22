import { ensureSeed, overviewSnapshot } from "../_lib/db.js";
import { json } from "../_lib/response.js";

export async function onRequestGet({ env }) {
  await ensureSeed(env);
  return json(await overviewSnapshot(env));
}
