import { json } from "../_lib/response.js";

export async function onRequestGet() {
  return json({
    product_name: "Heimdall Gatekeeper",
    tagline: "Minimal SIEM for Blue Teams",
    languages: ["pt-BR", "en", "es"],
    default_language: "pt-BR",
    default_theme: "dark",
    splash_duration_ms: 1200,
  });
}
