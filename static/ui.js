// Shared front-end helpers for all lab apps
const $ = (sel) => document.querySelector(sel);

function toast(msg, isErr = false) {
  const t = document.createElement("div");
  t.className = "toast" + (isErr ? " err" : "");
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), isErr ? 6000 : 2500);
}

async function api(path, body) {
  const opts = body === undefined
    ? { method: "GET" }
    : { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
  const r = await fetch(path, opts);
  const data = await r.json().catch(() => ({ error: "Bad server response" }));
  if (!r.ok || data.error) {
    toast(data.error || "Request failed", true);
    throw new Error(data.error || "Request failed");
  }
  return data;
}

// Runs an async action while showing a spinner on the button
// window.__busy lets the automatic screenshot script know when the AI has finished
window.__busy = 0;
async function withLoading(btn, fn) {
  window.__busy++;
  const old = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span>Working...';
  try { return await fn(); }
  catch (e) { console.error(e); }
  finally { btn.disabled = false; btn.innerHTML = old; window.__busy--; }
}

function esc(s) {
  return String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

// Tiny markdown renderer: headings, bold, italics, bullet and numbered lists
function md(text) {
  const lines = esc(text).split(/\r?\n/);
  let html = "", list = null;
  const close = () => { if (list) { html += `</${list}>`; list = null; } };
  const inline = (s) => s.replace(/\*\*(.+?)\*\*/g, "<b>$1</b>").replace(/(^|\W)\*(?!\s)(.+?)\*(?=\W|$)/g, "$1<i>$2</i>");
  for (const raw of lines) {
    const l = raw.trim();
    let m;
    if (!l) { close(); continue; }
    if ((m = l.match(/^#{1,6}\s+(.*)/))) { close(); html += `<h3>${inline(m[1])}</h3>`; }
    else if ((m = l.match(/^[-*•]\s+(.*)/))) { if (list !== "ul") { close(); html += "<ul>"; list = "ul"; } html += `<li>${inline(m[1])}</li>`; }
    else if ((m = l.match(/^\d+[.)]\s+(.*)/))) { if (list !== "ol") { close(); html += "<ol>"; list = "ol"; } html += `<li>${inline(m[1])}</li>`; }
    else { close(); html += `<p>${inline(l)}</p>`; }
  }
  close();
  return html;
}

function showCard(id, html) {
  const card = document.getElementById(id);
  card.classList.remove("hidden");
  const out = card.querySelector(".out");
  if (out && html !== undefined) out.innerHTML = html;
  card.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function table(rows, cols) {
  const head = cols.map((c) => `<th>${esc(c[1])}</th>`).join("");
  const body = rows.map((r) => "<tr>" + cols.map((c) => `<td>${c[2] ? c[2](r) : esc(r[c[0]])}</td>`).join("") + "</tr>").join("");
  return `<table class="data"><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`;
}

async function checkStatus() {
  const pill = $("#status");
  try {
    const s = await (await fetch("/api/status")).json();
    if (s.online && s.model_ready) { pill.className = "pill on"; pill.textContent = `Ollama online · ${s.model}`; }
    else if (s.online) { pill.className = "pill off"; pill.textContent = `Run: ollama pull ${s.model}`; }
    else { pill.className = "pill off"; pill.textContent = "Ollama offline"; }
  } catch { pill.className = "pill off"; pill.textContent = "Server offline"; }
}
document.addEventListener("DOMContentLoaded", checkStatus);
