export async function onRequestGet() {
  const body = [
    "# HELP heimdall_uptime_seconds Heimdall uptime in seconds",
    "# TYPE heimdall_uptime_seconds gauge",
    "heimdall_uptime_seconds 1",
    "# HELP heimdall_events_total Total number of Heimdall events",
    "# TYPE heimdall_events_total gauge",
    "heimdall_events_total 0",
  ].join("\n") + "\n";

  return new Response(body, {
    status: 200,
    headers: {
      "content-type": "text/plain; version=0.0.4; charset=utf-8",
    },
  });
}
