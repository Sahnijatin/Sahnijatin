"""Generates the profile README's SVG assets (banner + project cards) in light and dark variants."""
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

SANS = "'Inter','SF Pro Display',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','SF Mono',ui-monospace,Menlo,Consolas,monospace"

THEMES = {
    "dark": dict(bg="#0A0A0C", panel="#111115", border="#24242B", text="#F4F4F5", sub="#A1A1AA",
                 faint="#52525B", grid="#FFFFFF", grid_op="0.05", edge="#3F3F46", node="#18181B", a2="#22D3EE"),
    "light": dict(bg="#FFFFFF", panel="#FAFAFA", border="#E4E4E7", text="#09090B", sub="#52525B",
                  faint="#A1A1AA", grid="#000000", grid_op="0.06", edge="#D4D4D8", node="#FFFFFF", a2="#0891B2"),
}
A1, A2 = "#7C5CFF", "#22D3EE"  # accent gradient: violet -> cyan


def banner(t, name):
    W, H = 1280, 420
    # agent graph on the right side
    nodes = [(820, 120), (960, 80), (1100, 140), (900, 230), (1060, 260), (1190, 220),
             (840, 330), (990, 350), (1150, 340)]
    labels = ["vision", "llm", "tools", "rag", "agent", "mcp", "voice", "edge", "memory"]
    edges = [(0, 1), (1, 2), (0, 3), (1, 3), (1, 4), (2, 4), (2, 5), (3, 4), (4, 5),
             (3, 6), (3, 7), (4, 7), (4, 8), (5, 8), (6, 7), (7, 8)]
    core = 4

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'role="img" aria-label="Jatin Sahni. I build AI systems that see, listen and act.">']
    s.append(f"""<style>
  .pulse {{ animation: pulse 3.2s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
  .flow {{ stroke-dasharray: 4 8; animation: flow 1.6s linear infinite; }}
  .blink {{ animation: blink 1.1s steps(1) infinite; }}
  .rise {{ animation: rise .9s cubic-bezier(.2,.7,.2,1) both; }}
  .d1 {{ animation-delay: .08s }} .d2 {{ animation-delay: .18s }} .d3 {{ animation-delay: .28s }} .d4 {{ animation-delay: .38s }}
  @keyframes pulse {{ 0%,100% {{ opacity:.35; transform:scale(1) }} 50% {{ opacity:.0; transform:scale(2.4) }} }}
  @keyframes flow {{ to {{ stroke-dashoffset: -24 }} }}
  @keyframes blink {{ 50% {{ opacity: 0 }} }}
  @keyframes rise {{ from {{ opacity:0; transform: translateY(10px) }} to {{ opacity:1; transform:none }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important }} }}
</style>""")
    s.append(f"""<defs>
  <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{A1}"/><stop offset="1" stop-color="{t['a2']}"/></linearGradient>
  <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{A1}" stop-opacity="{'.28' if name=='dark' else '.14'}"/><stop offset="1" stop-color="{A1}" stop-opacity="0"/></radialGradient>
  <radialGradient id="glow2" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{A2}" stop-opacity="{'.18' if name=='dark' else '.10'}"/><stop offset="1" stop-color="{A2}" stop-opacity="0"/></radialGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{t['grid']}" fill-opacity="{t['grid_op']}"/></pattern>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".45" stop-color="#fff" stop-opacity="1"/></linearGradient>
  <mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
  <clipPath id="r"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>""")
    s.append(f'<g clip-path="url(#r)"><rect width="{W}" height="{H}" fill="{t["bg"]}"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#dots)" mask="url(#m)"/>')
    s.append(f'<circle cx="1000" cy="210" r="300" fill="url(#glow)"/><circle cx="1180" cy="360" r="220" fill="url(#glow2)"/>')

    # edges
    for i, (a, b) in enumerate(edges):
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{t["edge"]}" stroke-width="1"/>')
        if core in (a, b) or i % 3 == 0:
            s.append(f'<line class="flow" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="url(#acc)" '
                     f'stroke-width="1.4" style="animation-duration:{1.2 + (i % 4) * .35:.2f}s"/>')
    # packets moving along a few edges
    for i, (a, b) in enumerate([(0, 1), (1, 4), (3, 4), (4, 8), (2, 5), (6, 7)]):
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        dur = 2.4 + i * .5
        s.append(f'<circle r="2.6" fill="{A2 if i % 2 else A1}"><animateMotion dur="{dur}s" repeatCount="indefinite" '
                 f'path="M{x1},{y1} L{x2},{y2}" begin="{i * .4}s"/></circle>')
    # nodes
    for i, ((x, y), lab) in enumerate(zip(nodes, labels)):
        r = 9 if i == core else 6
        s.append(f'<circle class="pulse" cx="{x}" cy="{y}" r="{r}" fill="{A1 if i % 2 == 0 else A2}" style="animation-delay:{i * .35:.2f}s"/>')
        s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t["node"]}" stroke="url(#acc)" stroke-width="{2 if i == core else 1.4}"/>')
        if i == core:
            s.append(f'<circle cx="{x}" cy="{y}" r="3" fill="url(#acc)"/>')
        s.append(f'<text x="{x}" y="{y + r + 16}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{t["faint"]}">{lab}</text>')

    # left copy
    x0 = 72
    s.append(f'<g class="rise"><rect x="{x0}" y="92" width="10" height="10" rx="2" fill="url(#acc)"/>'
             f'<text x="{x0 + 20}" y="102" font-family="{MONO}" font-size="14" letter-spacing="1.5" fill="{t["sub"]}">NEW DELHI, INDIA</text></g>')
    s.append(f'<text class="rise d1" x="{x0 - 4}" y="188" font-family="{SANS}" font-size="78" font-weight="700" letter-spacing="-3" fill="{t["text"]}">Jatin Sahni</text>')
    s.append(f'<text class="rise d2" x="{x0}" y="240" font-family="{SANS}" font-size="26" font-weight="500" letter-spacing="-.4" fill="{t["sub"]}">I build AI systems that '
             f'<tspan fill="{t["text"]}">see</tspan>, <tspan fill="{t["text"]}">listen</tspan> and <tspan fill="url(#acc)" font-weight="700">act</tspan>.</text>')
    # terminal-ish line
    s.append(f'<g class="rise d3"><text x="{x0}" y="300" font-family="{MONO}" font-size="15" fill="{t["faint"]}">$</text>'
             f'<text x="{x0 + 18}" y="300" font-family="{MONO}" font-size="15" fill="{t["sub"]}">agents · mcp · retrieval · voice · on-device</text>'
             f'<rect class="blink" x="{x0 + 432}" y="287" width="8" height="17" fill="{A2}"/></g>')
    s.append(f'<rect class="rise d4" x="{x0}" y="340" width="56" height="3" rx="1.5" fill="url(#acc)"/>')
    s.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{t["border"]}"/></g></svg>')
    return "\n".join(s)


def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    return lines + [cur]


def card(t, name, p):
    W, H = 600, 250
    status_col = "#22C55E" if p["status"] == "Open source" else "#F59E0B"
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{p["title"]}: {p["desc"]}">']
    s.append("""<style>
  .pulse { animation: p 2.4s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
  .sweep { animation: sw 6s ease-in-out infinite; }
  @keyframes p { 0%,100% { opacity:.5; transform:scale(1) } 50% { opacity:0; transform:scale(2.6) } }
  @keyframes sw { 0% { transform: translateX(-620px) } 60%,100% { transform: translateX(620px) } }
  @media (prefers-reduced-motion: reduce) { * { animation: none !important } }
</style>""")
    s.append(f"""<defs>
  <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{A1}"/><stop offset="1" stop-color="{t['a2']}"/></linearGradient>
  <linearGradient id="sh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{A2}" stop-opacity="0"/><stop offset=".5" stop-color="{A2}" stop-opacity=".9"/><stop offset="1" stop-color="{A1}" stop-opacity="0"/></linearGradient>
  <clipPath id="c"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16"/></clipPath>
</defs>""")
    s.append(f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{t["panel"]}"/>')
    # top accent line with sweeping highlight
    s.append(f'<rect x="0" y="0" width="{W}" height="2" fill="{t["border"]}"/><rect class="sweep" x="0" y="0" width="{W}" height="2" fill="url(#sh)"/>')
    # icon glyph
    s.append(f'<g transform="translate(32,34)"><rect width="40" height="40" rx="10" fill="{t["bg"]}" stroke="{t["border"]}"/>'
             f'<g transform="translate(8,8)" fill="none" stroke="url(#acc)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{p["icon"]}</g></g>')
    # status pill
    pill = p["status"]; pw = round(28 + len(pill) * 8.6, 1)
    s.append(f'<g transform="translate({round(W - 32 - pw, 1)},42)"><rect width="{pw}" height="28" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>'
             f'<circle class="pulse" cx="15" cy="14" r="4" fill="{status_col}"/><circle cx="15" cy="14" r="4" fill="{status_col}"/>'
             f'<text x="27" y="19" font-family="{MONO}" font-size="14" fill="{t["sub"]}">{pill}</text></g>')
    s.append(f'<text x="32" y="118" font-family="{SANS}" font-size="30" font-weight="700" letter-spacing="-.8" fill="{t["text"]}">{p["title"]}</text>')
    for i, line in enumerate(wrap(p["desc"], 52)):
        s.append(f'<text x="32" y="{152 + i * 26}" font-family="{SANS}" font-size="18.5" fill="{t["sub"]}">{line}</text>')
    x = 32
    for tag in p["tags"]:
        w = round(18 + len(tag) * 8.4, 1)
        s.append(f'<rect x="{x:g}" y="{H - 50}" width="{w:g}" height="26" rx="7" fill="{t["bg"]}" stroke="{t["border"]}"/>'
                 f'<text x="{x + 9:g}" y="{H - 32}" font-family="{MONO}" font-size="14" fill="{t["sub"]}">{tag}</text>')
        x = round(x + w + 8, 1)
    s.append(f'</g><rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{t["border"]}"/></svg>')
    return "\n".join(s)


ICONS = {
    # simple 24x24 line glyphs
    "map": '<path d="M3 6l6-3 6 3 6-3v15l-6 3-6-3-6 3z"/><path d="M9 3v15M15 6v15"/>',
    "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    "compass": '<circle cx="12" cy="12" r="9.5"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
}

PROJECTS = [
    dict(slug="livemap", title="LiveMap", status="In development", icon=ICONS["map"],
         desc="Live x-ray of what AI coding agents build: files, functions, schema, routes, and why.",
         tags=["TypeScript", "CLI", "Claude Code", "Codex"]),
    dict(slug="collar-eye", title="Collar Eye", status="Open source", icon=ICONS["eye"],
         desc="Wearable camera and voice helper that sees your hands and point of view. Any LLM, via MCP.",
         tags=["Python", "Vision", "Voice", "MCP"]),
    dict(slug="esp-box-assistant", title="esp-box-assistant", status="Open source", icon=ICONS["chip"],
         desc="Tap-to-talk AI assistant for the ESP32-S3-BOX-3, with remote config and over-the-air updates.",
         tags=["C", "ESP-IDF", "ESP32-S3", "OTA"]),
    dict(slug="outsidermap", title="OutsiderMap", status="In development", icon=ICONS["compass"],
         desc="Preference-learning recommendation engine that adapts to what you pick, as you go.",
         tags=["TypeScript", "Recommendations"]),
]


def compact(svg):
    """Move repeated font stacks into CSS classes and drop indentation to keep files small."""
    import re
    svg = svg.replace("<style>", f"<style>.fs{{font-family:{SANS}}}.fm{{font-family:{MONO}}}", 1)
    for stack, cls in ((SANS, "fs"), (MONO, "fm")):
        attr = f' font-family="{stack}"'
        # merge into an existing class attribute on the same element, else add one
        svg = re.sub(r'class="([^"]*)"([^>]*?)' + re.escape(attr), lambda m: f'class="{m.group(1)} {cls}"{m.group(2)}', svg)
        svg = svg.replace(attr, f' class="{cls}"')
    return "\n".join(line.strip() for line in svg.splitlines())


if __name__ == "__main__":
    for name, t in THEMES.items():
        (OUT / f"banner-{name}.svg").write_text(compact(banner(t, name)))
        for p in PROJECTS:
            (OUT / f"card-{p['slug']}-{name}.svg").write_text(compact(card(t, name, p)))
    print("ok", sorted(f.name for f in OUT.iterdir()))
