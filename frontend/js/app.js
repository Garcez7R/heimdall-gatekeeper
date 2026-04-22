const state = {
  view: "overview",
  language: "pt-BR",
  theme: "dark",
  density: "comfortable",
  reduceMotion: window.matchMedia("(prefers-reduced-motion: reduce)").matches,
  dictionary: {},
  autoRefreshHandle: null,
};

async function request(path, options = {}) {
  const response = await fetch(path, options);
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(body.detail || body.error || `Request failed: ${response.status}`);
  }
  return body;
}

function text(key, fallback) {
  return state.dictionary[key] || fallback;
}

function severityBadge(severity) {
  return `<span class="badge ${severity}">${String(severity || "low").toUpperCase()}</span>`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function setView(view) {
  state.view = view;
  document.querySelectorAll(".view").forEach((el) => el.classList.remove("active"));
  document.querySelectorAll(".nav-item").forEach((el) => el.classList.remove("active"));
  document.getElementById(`view-${view}`)?.classList.add("active");
  document.querySelector(`.nav-item[data-view="${view}"]`)?.classList.add("active");
  document.getElementById("view-title").textContent = text(view, view);
}

function applyUiPreferences() {
  document.body.dataset.theme = state.theme;
  document.body.classList.toggle("compact", state.density === "compact");
  document.body.classList.toggle("reduce-motion", state.reduceMotion);
}

function renderMetrics(overview) {
  const metrics = [
    [text("events", "Events"), overview.status.events_total, text("eventsHint", "Normalized events stored in the pipeline.")],
    [text("activeAlerts", "Active Alerts"), overview.status.active_alerts, text("activeAlertsHint", "Alerts still requiring analyst action.")],
    [text("criticalAlerts", "Critical Alerts"), overview.status.critical_alerts, text("criticalAlertsHint", "Highest urgency security detections.")],
    [text("eventsPerMinute", "Events/min"), overview.events_per_minute || "0", text("eventsPerMinuteHint", "Recent operational ingestion cadence.")],
  ];

  document.getElementById("metric-grid").innerHTML = metrics
    .map(
      ([label, value, hint]) => `
        <article class="metric">
          <span>${escapeHtml(label)}</span>
          <strong>${escapeHtml(value)}</strong>
          <small>${escapeHtml(hint)}</small>
        </article>
      `
    )
    .join("");

  document.getElementById("system-health").textContent = escapeHtml(overview.status.system);
  document.getElementById("uptime-pill").textContent = `${text("uptime", "Uptime")} ${overview.status.uptime_seconds}s`;
}

function renderLatestAlerts(rows) {
  const container = document.getElementById("latest-alerts");
  if (!rows.length) {
    container.innerHTML = `<div class="stack-item">${escapeHtml(text("noAlerts", "No active alerts yet."))}</div>`;
    return;
  }
  container.innerHTML = rows
    .map(
      (row) => `
        <article class="stack-item">
          <div class="row">
            <strong>${escapeHtml(row.title)}</strong>
            ${severityBadge(row.severity)}
          </div>
          <span>${escapeHtml(row.message)}</span>
          <small>${escapeHtml(row.created_at)}</small>
        </article>
      `
    )
    .join("");
}

function renderTopIps(rows) {
  const grouped = rows.reduce((acc, row) => {
    const key = row.ip_address || "unknown";
    acc[key] = (acc[key] || 0) + 1;
    return acc;
  }, {});

  const entries = Object.entries(grouped).slice(0, 6);
  document.getElementById("top-ips").innerHTML = entries.length
    ? entries
        .map(
          ([ip, total]) => `
            <article class="stack-item">
              <div class="row">
                <strong>${escapeHtml(ip)}</strong>
                <span>${total} hits</span>
              </div>
            </article>
          `
        )
        .join("")
    : `<div class="stack-item">${escapeHtml(text("noThreatSources", "No suspicious IPs yet."))}</div>`;
}

function renderTimeline(points) {
  const container = document.getElementById("timeline-bars");
  if (!points.length) {
    container.innerHTML = `<div class="stack-item">${escapeHtml(text("noTimeline", "Timeline will populate as events are ingested."))}</div>`;
    return;
  }

  const max = Math.max(...points.map((item) => Number(item.total || 0)), 1);
  container.innerHTML = points
    .map((item) => {
      const total = Number(item.total || 0);
      const height = Math.max(10, Math.round((total / max) * 100));
      return `
        <div class="timeline-bar">
          <div class="timeline-bar-fill" style="height:${height}%"></div>
          <strong>${total}</strong>
          <span>${escapeHtml(String(item.bucket).slice(11, 16))}</span>
        </div>
      `;
    })
    .join("");
}

function renderTopCves(rows) {
  const container = document.getElementById("top-cves");
  if (!rows.length) {
    container.innerHTML = `<div class="stack-item">${escapeHtml(text("noCves", "No CVE-linked alerts observed yet."))}</div>`;
    return;
  }

  container.innerHTML = rows
    .map(
      (row) => `
        <article class="stack-item">
          <div class="row">
            <strong>${escapeHtml(row.cve_id)}</strong>
            <span>CVSS ${escapeHtml(row.score ?? "n/a")}</span>
          </div>
          <small>${escapeHtml(text("cveOccurrences", "Occurrences"))}: ${escapeHtml(row.total)}</small>
        </article>
      `
    )
    .join("");
}

async function loadOverview() {
  const overview = await request("/api/overview");
  renderMetrics(overview);
  renderLatestAlerts(overview.latest_alerts || []);
  renderTopIps(overview.top_ips || []);
  renderTimeline(overview.timeline || []);
  renderTopCves(overview.top_cves || []);
}

async function loadAlerts() {
  const status = document.getElementById("alert-status-filter").value;
  const payload = await request(`/api/alerts${status ? `?status=${encodeURIComponent(status)}` : ""}`);
  document.getElementById("alerts-table").innerHTML = payload.rows
    .map(
      (row) => `
        <tr>
          <td>${severityBadge(row.severity)}</td>
          <td>${escapeHtml(row.rule_name)}</td>
          <td>${escapeHtml(row.message)}</td>
          <td>${escapeHtml(row.status)}</td>
          <td>${escapeHtml(row.created_at)}</td>
          <td>
            <button class="table-action" data-action="ack" data-id="${row.id}">${escapeHtml(text("acknowledge", "Ack"))}</button>
            <button class="table-action" data-action="resolve" data-id="${row.id}">${escapeHtml(text("resolve", "Resolve"))}</button>
          </td>
        </tr>
      `
    )
    .join("");
}

async function loadEvents() {
  const search = document.getElementById("event-search").value;
  const severity = document.getElementById("event-severity-filter").value;
  const query = new URLSearchParams();
  if (search) query.set("search", search);
  if (severity) query.set("severity", severity);
  const payload = await request(`/api/events?${query.toString()}`);
  document.getElementById("events-table").innerHTML = payload.rows
    .map(
      (row) => `
        <tr>
          <td>${escapeHtml(row.event_type)}</td>
          <td>${escapeHtml(row.source)}</td>
          <td>${escapeHtml(row.title)}</td>
          <td>${severityBadge(row.severity)}</td>
          <td>${escapeHtml(row.created_at)}</td>
        </tr>
      `
    )
    .join("");
}

async function loadStatus() {
  const payload = await request("/api/overview");
  document.getElementById("status-json").textContent = JSON.stringify(payload.status, null, 2);
}

async function loadLanguage(language) {
  state.language = language;
  state.dictionary = await request(`/assets/i18n/${language}.json`);
  document.querySelector('[data-view="overview"]').textContent = text("overview", "Overview");
  document.querySelector('[data-view="alerts"]').textContent = text("alerts", "Alerts");
  document.querySelector('[data-view="events"]').textContent = text("events", "Events");
  document.querySelector('[data-view="status"]').textContent = text("status", "System Status");
  setView(state.view);
}

function installAutoRefresh() {
  if (state.autoRefreshHandle) clearInterval(state.autoRefreshHandle);
  state.autoRefreshHandle = window.setInterval(async () => {
    await Promise.all([loadOverview(), loadAlerts(), loadEvents(), loadStatus()]).catch(() => undefined);
  }, 15000);
}

async function bootstrap() {
  const config = await request("/api/config");
  document.getElementById("tagline").textContent = config.tagline;
  state.theme = config.default_theme || "dark";
  state.language = config.default_language || "en";
  applyUiPreferences();
  await loadLanguage(state.language);
  await Promise.all([loadOverview(), loadAlerts(), loadEvents(), loadStatus()]);
  installAutoRefresh();

  document.querySelectorAll(".nav-item").forEach((item) => item.addEventListener("click", () => setView(item.dataset.view)));
  document.getElementById("reload-alerts").addEventListener("click", loadAlerts);
  document.getElementById("reload-events").addEventListener("click", loadEvents);
  document.getElementById("alert-status-filter").addEventListener("change", loadAlerts);
  document.getElementById("event-search").addEventListener("input", loadEvents);
  document.getElementById("event-severity-filter").addEventListener("change", loadEvents);

  document.getElementById("language-switcher").value = state.language;
  document.getElementById("theme-switcher").value = state.theme;
  document.getElementById("density-switcher").value = state.density;

  document.getElementById("language-switcher").addEventListener("change", (event) => loadLanguage(event.target.value));
  document.getElementById("theme-switcher").addEventListener("change", (event) => {
    state.theme = event.target.value;
    applyUiPreferences();
  });
  document.getElementById("density-switcher").addEventListener("change", (event) => {
    state.density = event.target.value;
    applyUiPreferences();
  });
  document.getElementById("contrast-toggle").addEventListener("click", () => document.body.classList.toggle("high-contrast"));
  document.getElementById("motion-toggle").addEventListener("click", () => {
    state.reduceMotion = !state.reduceMotion;
    applyUiPreferences();
  });

  document.getElementById("alerts-table").addEventListener("click", async (event) => {
    const button = event.target.closest("button");
    if (!button) return;
    const action = button.dataset.action;
    const id = button.dataset.id;
    const endpoint = action === "resolve" ? "resolve" : "acknowledge";
    await request(`/api/alerts/${id}/${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ actor: "dashboard-operator" }),
    });
    await Promise.all([loadAlerts(), loadOverview(), loadStatus()]);
  });

  document.getElementById("ingest-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const payload = Object.fromEntries(form.entries());
    payload.tags = ["demo", "dashboard"];
    const result = await request("/api/events/ingest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    document.getElementById("ingest-result").textContent = `${text("eventProcessed", "Event processed")}: ${result.event_id}. ${text("alertsTriggered", "Alerts triggered")}: ${result.alert_ids.length}`;
    event.currentTarget.reset();
    await Promise.all([loadOverview(), loadAlerts(), loadEvents(), loadStatus()]);
  });

  setTimeout(() => {
    document.getElementById("splash").hidden = true;
    document.getElementById("app").hidden = false;
  }, config.splash_duration_ms || 1200);
}

bootstrap().catch((error) => {
  console.error(error);
  document.getElementById("splash").hidden = true;
  document.getElementById("app").hidden = false;
});
