function base64UrlEncode(value) {
  return btoa(String.fromCharCode(...new Uint8Array(value)))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
}

function encodeJson(obj) {
  return base64UrlEncode(new TextEncoder().encode(JSON.stringify(obj)));
}

export async function createJwtToken(payload, secret) {
  const header = { alg: "HS256", typ: "JWT" };
  const encodedHeader = encodeJson(header);
  const encodedPayload = encodeJson(payload);
  const data = new TextEncoder().encode(`${encodedHeader}.${encodedPayload}`);
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const signature = await crypto.subtle.sign("HMAC", key, data);
  return `${encodedHeader}.${encodedPayload}.${base64UrlEncode(signature)}`;
}
