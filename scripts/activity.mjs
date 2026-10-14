// Builds assets/activity-{dark,light}.svg from the GitHub contributions calendar.
// Runs in a GitHub Action with GITHUB_TOKEN; no third-party services.
import { writeFileSync, mkdirSync } from "node:fs";

const USER = process.env.GH_USER || "Sahnijatin";
const TOKEN = process.env.GITHUB_TOKEN;
const OUT = new URL("../assets/", import.meta.url);

async function fetchCalendar() {
  if (process.env.FAKE) {
    // local preview data
    const days = [];
    const start = new Date(Date.now() - 370 * 864e5);
    for (let i = 0; i < 371; i++) {
      const d = new Date(start.getTime() + i * 864e5);
      const n = Math.random() < 0.3 ? 0 : Math.floor(Math.random() ** 2 * 14);
      days.push({ date: d.toISOString().slice(0, 10), contributionCount: n, weekday: d.getUTCDay() });
    }
    const weeks = [];
    for (let i = 0; i < days.length; i += 7) weeks.push({ contributionDays: days.slice(i, i + 7) });
    return { totalContributions: days.reduce((a, d) => a + d.contributionCount, 0), weeks };
  }
  const q = `query($u:String!){ user(login:$u){ contributionsCollection{ contributionCalendar{
    totalContributions weeks{ contributionDays{ date contributionCount weekday } } } } } }`;
  const r = await fetch("https://api.github.com/graphql", {
    method: "POST",
    headers: { Authorization: `bearer ${TOKEN}`, "Content-Type": "application/json" },
    body: JSON.stringify({ query: q, variables: { u: USER } }),
  });
  const j = await r.json();
  if (!j.data) throw new Error(JSON.stringify(j));
  return j.data.user.contributionsCollection.contributionCalendar;
}

function stats(cal) {
  const days = cal.weeks.flatMap((w) => w.contributionDays);
  let longest = 0, run = 0;
  for (const d of days) { run = d.contributionCount ? run + 1 : 0; longest = Math.max(longest, run); }
  let current = 0;
  for (let i = days.length - 1; i >= 0; i--) {
    if (days[i].contributionCount) current++;
    else if (i === days.length - 1) continue; // today may not have activity yet
    else break;
  }
  const byDow = Array(7).fill(0);
  days.forEach((d) => (byDow[d.weekday] += d.contributionCount));
  const dow = ["Sundays", "Mondays", "Tuesdays", "Wednesdays", "Thursdays", "Fridays", "Saturdays"][byDow.indexOf(Math.max(...byDow))];
  const active = days.filter((d) => d.contributionCount).length;
  return { total: cal.totalContributions, longest, current, dow, active };
}

const THEMES = {
  dark: { panel: "#111115", border: "#24242B", text: "#F4F4F5", sub: "#A1A1AA", faint: "#52525B",
    levels: ["#1C1C22", "#2E2366", "#4B37B8", "#7C5CFF", "#22D3EE"] },
  light: { panel: "#FAFAFA", border: "#E4E4E7", text: "#09090B", sub: "#52525B", faint: "#A1A1AA",
    levels: ["#EDEDF0", "#D9D1FF", "#AE9BFF", "#7C5CFF", "#0EA5C6"] },
};
const SANS = "'Inter','SF Pro Display',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif";
const MONO = "'JetBrains Mono','SF Mono',ui-monospace,Menlo,Consolas,monospace";

function render(cal, s, t) {
  const W = 1280, H = 320, cell = 13, gap = 4;
  const weeks = cal.weeks.slice(-53);
  const max = Math.max(1, ...weeks.flatMap((w) => w.contributionDays.map((d) => d.contributionCount)));
  const lvl = (n) => (n === 0 ? 0 : Math.min(4, 1 + Math.floor((n / max) * 3.999)));
  const gx = W - 48 - weeks.length * (cell + gap) + gap, gy = 92;
  const out = [];
  out.push(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${s.total} contributions in the last year">`);
  out.push(`<style>.c{animation:in .5s ease-out both}@keyframes in{from{opacity:0}}@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>`);
  out.push(`<defs><linearGradient id="acc" x1="0" x2="1"><stop offset="0" stop-color="#7C5CFF"/><stop offset="1" stop-color="#22D3EE"/></linearGradient></defs>`);
  out.push(`<rect x=".5" y=".5" width="${W - 1}" height="${H - 1}" rx="16" fill="${t.panel}" stroke="${t.border}"/>`);
  out.push(`<text x="48" y="58" font-family="${MONO}" font-size="13" letter-spacing="1.5" fill="${t.sub}">ACTIVITY · LAST 12 MONTHS</text>`);
  const kpis = [
    [s.total.toLocaleString("en-US"), "contributions"],
    [String(s.active), "active days"],
    [`${s.longest}d`, "longest streak"],
    [`${s.current}d`, "current streak"],
  ];
  // KPI column on the left
  kpis.forEach(([v, l], i) => {
    const y = 118 + i * 48;
    out.push(`<text x="48" y="${y}" font-family="${SANS}" font-size="30" font-weight="700" letter-spacing="-.8" fill="${i === 0 ? "url(#acc)" : t.text}">${v}</text>`);
    out.push(`<text x="48" y="${y + 18}" font-family="${MONO}" font-size="12.5" fill="${t.faint}">${l}</text>`);
  });
  weeks.forEach((w, wi) => {
    w.contributionDays.forEach((d) => {
      const x = gx + wi * (cell + gap), y = gy + d.weekday * (cell + gap);
      out.push(`<rect class="c" style="animation-delay:${(wi * 0.012).toFixed(3)}s" x="${x}" y="${y}" width="${cell}" height="${cell}" rx="3" fill="${t.levels[lvl(d.contributionCount)]}"><title>${d.date}: ${d.contributionCount}</title></rect>`);
    });
  });
  // month labels
  let last = "";
  weeks.forEach((w, wi) => {
    const m = new Date(w.contributionDays[0].date + "T00:00:00Z").toLocaleString("en-US", { month: "short", timeZone: "UTC" });
    if (m !== last && wi < weeks.length - 2) { out.push(`<text x="${gx + wi * (cell + gap)}" y="${gy - 12}" font-family="${MONO}" font-size="11" fill="${t.faint}">${m}</text>`); last = m; }
  });
  const ly = gy + 7 * (cell + gap) + 18;
  out.push(`<text x="${gx}" y="${ly + 10}" font-family="${MONO}" font-size="11" fill="${t.faint}">Most active on ${s.dow}</text>`);
  const lx = W - 48 - 5 * (cell + gap) - 40;
  out.push(`<text x="${lx - 8}" y="${ly + 10}" text-anchor="end" font-family="${MONO}" font-size="11" fill="${t.faint}">less</text>`);
  t.levels.forEach((c, i) => out.push(`<rect x="${lx + i * (cell + gap)}" y="${ly}" width="${cell}" height="${cell}" rx="3" fill="${c}"/>`));
  out.push(`<text x="${lx + 5 * (cell + gap) + 4}" y="${ly + 10}" font-family="${MONO}" font-size="11" fill="${t.faint}">more</text>`);
  out.push(`</svg>`);
  return out.join("\n");
}

const cal = await fetchCalendar();
const s = stats(cal);
mkdirSync(OUT, { recursive: true });
for (const [name, t] of Object.entries(THEMES)) writeFileSync(new URL(`activity-${name}.svg`, OUT), render(cal, s, t));
console.log("activity", s);
