"""Generate live profile SVGs (KPI strip, activity heatmap, language bar).

Reads public GitHub data through the `gh` CLI (GH_TOKEN is set inside Actions).
Writes assets/kpi.svg, assets/activity.svg, assets/langs.svg.
"""
import datetime
import json
import subprocess
from pathlib import Path

USER = "Karma1028"
OUT = Path(__file__).resolve().parent.parent / "assets"
FONT_SANS = "'Segoe UI',-apple-system,Helvetica,Arial,sans-serif"
FONT_MONO = "SFMono-Regular,Consolas,'Liberation Mono',Menlo,monospace"
LANG_COLORS = {
    "Python": "#3572A5", "TypeScript": "#3178c6", "JavaScript": "#f1e05a",
    "CSS": "#a78bfa", "HTML": "#e34c26", "Jupyter Notebook": "#DA5B0B",
}
SKIP_LANGS = {"Jupyter Notebook"}  # notebook JSON inflates byte counts


def gh(*args):
    res = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", check=True)
    return json.loads(res.stdout)


def gql(query):
    return gh("api", "graphql", "-f", f"query={query}")["data"]["user"]


def fetch():
    repos = gh("api", f"users/{USER}/repos?per_page=100&type=owner")
    own = [r for r in repos if not r["fork"]]
    langs = {}
    for r in own:
        for lang, n in gh("api", f"repos/{USER}/{r['name']}/languages").items():
            langs[lang] = langs.get(lang, 0) + n
    cal = gql(
        '{user(login:"%s"){createdAt contributionsCollection{totalCommitContributions '
        "contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}" % USER
    )
    return own, langs, cal


def svg_open(w, h):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
        f"<style>.s{{font-family:{FONT_SANS}}}.m{{font-family:{FONT_MONO}}}"
        "@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}"
        "@keyframes in{from{opacity:0}to{opacity:1}}"
        "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>"
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#2dd4bf"/><stop offset=".55" stop-color="#a78bfa"/>'
        '<stop offset="1" stop-color="#fbbf24"/></linearGradient></defs>'
    )


def card(x, y, w, h, delay):
    return (
        f'<g style="animation:up .6s ease-out {delay}s both">'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#10162b" stroke="#ffffff" stroke-opacity=".08"/>'
    )


def kpi_svg(own, langs, cal):
    cc = cal["contributionsCollection"]
    top = [
        (str(len([r for r in own if r["name"] != USER])), "public repos", "since Aug 2025"),
        (str(cc["totalCommitContributions"]), "commits", "last 12 months"),
        (str(len([l for l in langs if l not in SKIP_LANGS])), "languages", "Python · TS · JS"),
        (str(cc["contributionCalendar"]["totalContributions"]), "contributions", "last 12 months"),
    ]
    work = [
        ("9,134", "customers modelled", "CLV · XGBoost"),
        ("24", "variables analysed", "CLV · IBM dataset"),
        ("10", "dashboard views", "KARMA-OS"),
        ("3", "AI providers wired", "Groq·Gemini·OpenRouter"),
    ]
    w, h = 900, 300
    o = [svg_open(w, h)]
    o.append('<text class="s" x="4" y="22" fill="#94a3b8" font-size="13" letter-spacing="2">ACTIVITY</text>')
    o.append('<text class="s" x="4" y="166" fill="#94a3b8" font-size="13" letter-spacing="2">WORK IN NUMBERS</text>')
    cw, gap = 213, 16
    for row, (items, y0, base) in enumerate(((top, 32, 0.0), (work, 178, 0.5))):
        for i, (num, label, sub) in enumerate(items):
            x = i * (cw + gap)
            d = base + i * 0.12
            o.append(card(x, y0, cw, 112, d))
            o.append(f'<rect x="{x}" y="{y0}" width="5" height="112" rx="2.5" fill="url(#g)"/>')
            o.append(f'<text class="s" x="{x+22}" y="{y0+54}" font-size="40" font-weight="800" fill="#f8fafc">{num}</text>')
            o.append(f'<text class="s" x="{x+22}" y="{y0+80}" font-size="15" font-weight="600" fill="#cbd5e1">{label}</text>')
            o.append(f'<text class="m" x="{x+22}" y="{y0+100}" font-size="11.5" fill="#2dd4bf">{sub}</text>')
            o.append("</g>")
    o.append("</svg>")
    return "".join(o)


def level(n, mx):
    if n == 0:
        return "#161b33"
    r = n / mx
    return "#134e4a" if r < .25 else "#0f766e" if r < .5 else "#2dd4bf" if r < .8 else "#fbbf24"


def activity_svg(cal):
    weeks = cal["contributionsCollection"]["contributionCalendar"]["weeks"][-26:]
    mx = max((d["contributionCount"] for wk in weeks for d in wk["contributionDays"]), default=1) or 1
    total = cal["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    cell, pad = 28, 6
    w, h = 900, 7 * (cell + pad) + 70
    o = [svg_open(w, h)]
    o.append(f'<text class="s" x="4" y="22" fill="#94a3b8" font-size="13" letter-spacing="2">LAST 6 MONTHS · {total} CONTRIBUTIONS IN THE LAST YEAR</text>')
    x0 = 4
    step = (w - 8) / max(len(weeks), 1)
    for wi, wk in enumerate(weeks):
        for d in wk["contributionDays"]:
            wd = datetime.date.fromisoformat(d["date"]).isoweekday() % 7
            x = x0 + wi * step
            y = 40 + wd * (cell + pad)
            c = d["contributionCount"]
            o.append(
                f'<rect x="{x:.1f}" y="{y}" width="{cell}" height="{cell}" rx="6" fill="{level(c, mx)}" '
                f'style="animation:in .5s ease-out {wi*0.025:.2f}s both"><title>{d["date"]}: {c}</title></rect>'
            )
    ly = h - 14
    o.append(f'<text class="s" x="{w-250}" y="{ly}" font-size="13" fill="#94a3b8">less</text>')
    for i, col in enumerate(("#161b33", "#134e4a", "#0f766e", "#2dd4bf", "#fbbf24")):
        o.append(f'<rect x="{w-215+i*22}" y="{ly-11}" width="14" height="14" rx="3.5" fill="{col}"/>')
    o.append(f'<text class="s" x="{w-95}" y="{ly}" font-size="13" fill="#94a3b8">more</text>')
    o.append("</svg>")
    return "".join(o)


def langs_svg(langs):
    items = sorted(((k, v) for k, v in langs.items() if k not in SKIP_LANGS), key=lambda kv: -kv[1])[:5]
    total = sum(v for _, v in items) or 1
    w, h = 900, 130
    o = [svg_open(w, h)]
    o.append('<text class="s" x="4" y="22" fill="#94a3b8" font-size="13" letter-spacing="2">LANGUAGES · PUBLIC CODE</text>')
    bar_x, bar_w, bar_y = 4, w - 8, 38
    o.append(f'<clipPath id="c"><rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="16" rx="8"/></clipPath>')
    o.append(f'<g clip-path="url(#c)"><g style="transform-origin:{bar_x}px 0;animation:grow 1.2s ease-out both">')
    cur = bar_x
    for name, val in items:
        seg = bar_w * val / total
        o.append(f'<rect x="{cur:.1f}" y="{bar_y}" width="{seg+1:.1f}" height="16" fill="{LANG_COLORS.get(name, "#64748b")}"/>')
        cur += seg
    o.append("</g></g>")
    col_w = bar_w / max(len(items), 1)
    for i, (name, val) in enumerate(items):
        x = bar_x + i * col_w
        o.append(f'<circle cx="{x+7}" cy="92" r="6" fill="{LANG_COLORS.get(name, "#64748b")}"/>')
        o.append(f'<text class="s" x="{x+20}" y="97" font-size="15" font-weight="600" fill="#e2e8f0">{name}</text>')
        o.append(f'<text class="m" x="{x+20}" y="116" font-size="13" fill="#94a3b8">{100*val/total:.1f}%</text>')
    o.append("</svg>")
    return "".join(o)


def timeline_svg(own):
    """Build log: public repos on a horizontal timeline by creation date."""
    rows = sorted((r for r in own if r["name"] != USER), key=lambda r: r["created_at"])
    n = len(rows)
    w, h = 900, 250
    o = [svg_open(w, h)]
    o.append('<text class="s" x="4" y="22" fill="#94a3b8" font-size="13" letter-spacing="2">BUILD LOG · PUBLIC REPOS BY DATE</text>')
    y0, x0, x1 = 128, 50, w - 50
    o.append(f'<line x1="{x0-20}" y1="{y0}" x2="{x1+20}" y2="{y0}" stroke="#fff" stroke-opacity=".12" stroke-width="2"/>')
    o.append(f'<line x1="{x0-20}" y1="{y0}" x2="{x1+20}" y2="{y0}" stroke="url(#g)" stroke-width="3" stroke-dasharray="{w}" stroke-dashoffset="{w}"><animate attributeName="stroke-dashoffset" from="{w}" to="0" dur="2s" fill="freeze"/></line>')
    for i, r in enumerate(rows):
        x = x0 + (x1 - x0) * (i / max(n - 1, 1))
        up = i % 2 == 0
        ty = y0 - 38 if up else y0 + 52
        d = r["created_at"][:7]
        name = r["name"].replace("---", " ").replace("_", " ")
        name = name if len(name) <= 20 else name[:19] + "…"
        o.append(f'<g style="animation:up .6s ease-out {0.4+i*0.25:.2f}s both">')
        o.append(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{ty + (6 if up else -16):.1f}" stroke="#fff" stroke-opacity=".18"/>')
        o.append(f'<circle cx="{x:.1f}" cy="{y0}" r="7" fill="#0b1020" stroke="url(#g)" stroke-width="3"/>')
        o.append(f'<text class="s" x="{x:.1f}" y="{ty:.1f}" text-anchor="middle" font-size="14" font-weight="700" fill="#f1f5f9">{name}</text>')
        o.append(f'<text class="m" x="{x:.1f}" y="{ty+16:.1f}" text-anchor="middle" font-size="11.5" fill="#2dd4bf">{d}</text>')
        o.append("</g>")
    o.append("</svg>")
    return "".join(o)


def main():
    OUT.mkdir(exist_ok=True)
    own, langs, cal = fetch()
    (OUT / "kpi.svg").write_text(kpi_svg(own, langs, cal), encoding="utf-8")
    (OUT / "activity.svg").write_text(activity_svg(cal), encoding="utf-8")
    (OUT / "langs.svg").write_text(langs_svg(langs), encoding="utf-8")
    (OUT / "timeline.svg").write_text(timeline_svg(own), encoding="utf-8")
    print(f"[OK] repos={len(own)} langs={len(langs)}")


if __name__ == "__main__":
    main()
