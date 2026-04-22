export function json(data, init = {}) {
  return new Response(JSON.stringify(data), {
    headers: {
      "content-type": "application/json; charset=utf-8",
      ...(init.headers || {}),
    },
    status: init.status || 200,
  });
}

export function error(message, status = 400) {
  return json({ ok: false, error: message }, { status });
}
