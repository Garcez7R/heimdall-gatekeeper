# Heimdall Gatekeeper Online Usage Guide

This guide explains how to use the live dashboard and Grafana integration once Heimdall Gatekeeper is running.

## 1. Open the live console

1. Start the backend locally:
   ```bash
   uvicorn backend.api.main:app --reload
   ```
2. Open the dashboard in a browser:
   - `http://127.0.0.1:8000`

## 2. Understand the overview screen

The `Overview` page is the main operational panel:

- **Timeline** shows recent event ingestion volume in buckets.
- **Source Breakdown** reveals the top event sources by volume.
- **Quick status** surfaces health, uptime, latest ingest time, and a live clock.
- **Metric tiles** include total events, active alerts, critical alerts, and events per minute.

This page is designed for quick situational awareness.

## 3. Use alerts for triage

Navigate to `Alerts` to:

- review active detections,
- acknowledge alerts, and
- resolve alerts once they are handled.

Each alert entry includes rule context, severity, source, and relative timestamp.

## 4. Search recent events

The `Events` view helps you explore normalized signals across monitored sources.

- Use the search box to filter by keywords.
- Select severity filters to focus on high-risk events.
- Choose a source filter to isolate a specific data origin.

## 5. Inspect status and inject test signals

The `Status` view is useful for:

- checking the engine state,
- reviewing current pipeline metadata, and
- injecting sample events to verify alerting behavior.

Use the ingest form to submit a live sample event and confirm the dashboard refreshes.

## 6. Open Grafana for deeper observability

Heimdall Gatekeeper includes Grafana support for full monitoring dashboards.

### Start Grafana and Prometheus

If the observability stack is available, run the local compose command:

```bash
docker compose -f monitoring/docker-compose.monitoring.yml up -d
```

Then open:

- `http://localhost:3000` for Grafana
- `http://localhost:9090` for Prometheus

### Use the Grafana link

The frontend includes a Grafana button on the overview page.
Click it to jump directly into the dashboard and inspect:

- event throughput,
- alert counts,
- source distribution,
- endpoint reliability, and
- ingestion latency.

## 7. Refresh and cache behavior

- Use the refresh button in the top bar to pull the latest overview, alerts, events, and status data.
- The frontend includes cache-control headers to reduce stale content after deployment.

## 8. Deploying the frontend online

For Cloudflare deployment, use the provided `bash cloudflare/deploy.sh` workflow.

The public pages should expose:

- a browser dashboard endpoint, and
- a separate Workers API endpoint.

## 9. Troubleshooting

- If the dashboard appears stale, refresh the browser and use the `Refresh` button.
- If Grafana does not load, verify the monitoring stack is running and confirm `http://localhost:3000` is reachable.
- If no events appear, use the ingest form or demo bootstrap endpoint to populate sample data.

## 10. Recommended flow

1. start Heimdall backend,
2. open the dashboard,
3. check `Overview`,
4. triage alerts in `Alerts`,
5. inspect events in `Events`, and
6. use Grafana for deeper metrics.
