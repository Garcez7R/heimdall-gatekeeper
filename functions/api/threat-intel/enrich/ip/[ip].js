import { json } from "../../../../_lib/response.js";

export async function onRequestGet({ params }) {
  const ip = params.ip;
  return json({
    ip,
    reputation: "unknown",
    score: null,
    tags: [],
    summary: "Threat intelligence enrichment is available when API keys are configured.",
    source: "stub",
  });
}
