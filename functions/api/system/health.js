import { json } from "../../_lib/response.js";

export async function onRequestGet() {
  return json({ status: "ok" });
}
