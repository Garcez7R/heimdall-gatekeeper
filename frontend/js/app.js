const state = {
  view: "overview",
  language: "pt-BR",
  theme: "dark",
  density: "comfortable",
  reduceMotion: window.matchMedia("(prefers-reduced-motion: reduce)").matches,
  dictionary: {},
};

async function request(path, options = {}) {
  const response = await fetch(path, options);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

function setView(view) {
  state.view = view;
  document.querySelectorAll(".view").forEach((el) => el.classList.remove("active"));
  document.querySelectorAll(".nav-item").forEach((el) => el.classList.remove("active"));
  document.getElementById(`view-${view}`)?.classList.add("active");
  document.querySelector(`.nav-item[data-view="${view}"]`)?.classList.add("active");
  document.getElementById("view-title").textContent = state.dictionary[view] || view;
}

function severityBadge(severity) {
  return `<span class="badge ${severity}">${severity.toUpperCase()}</span>`;
}

function renderMetrics(overview) {
  const metrics = [
    ["Events", overview.status.events_total],
    ["Active Alerts", overview.status.active_alerts],
    ["Critical Alerts", overview.status.critical_alerts],
    ["Uptime (s)", overview.status.uptime_seconds],
  ];
  document.getElementById("metric-grid").innerHTML = metrics
    .map(([label, value]) => `<article class="metric"><span>${label}</span><strong>${value}</strong></article>`)
    .join("");
  document.getElementById("system-health").textContent = overview.status.system;
  document.getElementById("uptime-pill").textContent = `Uptime ${overview.status.uptime_seconds}s`;
}

function renderLatestAlerts(rows) {
  document.getElementById("latest-alerts").innerHTML = rows
    .map(
      (row) => `
        <article class="stack-item">
          <div class="row">
            <strong>${row.title}</strong>
            ${severityBadge(row.severity)}
          </div>
          <span>${row.message}</span>
          <small>${row.created_at}</small>
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
  document.getElementById("top-ips").innerHTML = Object.entries(grouped)
    .slice(0, 6)
    .map(([ip, total]) => `<article class="stack-item"><div class="row"><strong>${ip}</strong><span>${total} hits</span></div></article>`)
    .join("") || `<div class="stack-item">No suspicious IPs yet.</div>`;
}

async function loadOverview() {
  const overview = await request("/api/overview");
  renderMetrics(overview);
  renderLatestAlerts(overview.latest_alerts || []);
  renderTopIps(overview.top_ips || []);
}

async function loadAlerts() {
  const status = document.getElementById("alert-status-filter").value;
  const payload = await request(`/api/alerts${status ? `?status=${encodeURIComponent(status)}` : ""}`);
  document.getElementById("alerts-table").innerHTML = payload.rows
    .map(
      (row) => `
        <tr>
          <td>${severityBadge(row.severity)}</td>
          <td>${row.rule_name}</td>
          <td>${row.message}</td>
          <td>${row.status}</td>
          <td>${row.created_at}</td>
          <td>
            <button data-action="ack" data-id="${row.id}">Ack</button>
            <button data-action="resolve" data-id="${row.id}">Resolve</button>
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
          <td>${row.event_type}</td>
          <td>${row.source}</td>
          <td>${row.title}</td>
          <td>${severityBadge(row.severity)}</td>
          <td>${row.created_at}</td>
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
  document.querySelector('[data-view="overview"]').textContent = state.dictionary.overview;
  document.querySelector('[data-view="alerts"]').textContent = state.dictionary.alerts;
  document.querySelector('[data-view="events"]').textContent = state.dictionary.events;
  document.querySelector('[data-view="status"]').textContent = state.dictionary.status;
  setView(state.view);
}

function applyUiPreferences() {
  document.body.dataset.theme = state.theme;
  document.body.classList.toggle("compact", state.density === "compact");
  document.body.classList.toggle("reduce-motion", state.reduceMotion);
}

async function bootstrap() {
  const config = await request("/api/config");
  document.getElementById("tagline").textContent = config.tagline;
  state.theme = config.default_theme || "dark";
  state.language = config.default_language || "en";
  applyUiPreferences();
  await loadLanguage(state.language);
  await Promise.all([loadOverview(), loadAlerts(), loadEvents(), loadStatus()]);

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
    await loadAlerts();
    await loadOverview();
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
    document.getElementById("ingest-result").textContent = `Event ${result.event_id} processed. Alerts: ${result.alert_ids.length}`;
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
