"""Generate live profile SVGs from public GitHub data (via the `gh` CLI).

Everything is drawn at its real display size, so nothing is scaled down on
phones: KPI tiles (140px), a language panel and heatmap (~440px) and a
vertical build log (440px). Outputs go to assets/.
"""
import datetime
import json
import subprocess
from pathlib import Path

USER = "Karma1028"
OUT = Path(__file__).resolve().parent.parent / "assets"
SANS = "'Segoe UI',-apple-system,Helvetica,Arial,sans-serif"
MONO = "SFMono-Regular,Consolas,'Liberation Mono',Menlo,monospace"
LANG_COLORS = {
    "Python": "#3572A5", "TypeScript": "#3178c6", "JavaScript": "#f1e05a",
    "CSS": "#a78bfa", "HTML": "#e34c26",
}
SKIP_LANGS = {"Jupyter Notebook"}  # notebook JSON inflates byte counts
STATIC_KPIS = [
    ("9,134", "customers modelled", "CLV · XGBoost"),
    ("24", "variables analysed", "CLV · IBM dataset"),
    ("10", "dashboard views", "KARMA-OS"),
    ("3", "LLM providers wired", "multi-LLM routing"),
]


def gh(*args):
    res = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", check=True)
    return json.loads(res.stdout)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fetch():
    repos = gh("api", f"users/{USER}/repos?per_page=100&type=owner")
    own = [r for r in repos if not r["fork"]]
    langs = {}
    for r in own:
        for lang, n in gh("api", f"repos/{USER}/{r['name']}/languages").items():
            langs[lang] = langs.get(lang, 0) + n
    query = (
        '{user(login:"%s"){contributionsCollection{totalCommitContributions '
        "contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}" % USER
    )
    cal = gh("api", "graphql", "-f", f"query={query}")["data"]["user"]["contributionsCollection"]
    return own, langs, cal


def open_svg(w, h, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">'
        f"<style>.s{{font-family:{SANS}}}.m{{font-family:{MONO}}}"
        "@keyframes up{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}"
        "@keyframes in{from{opacity:0}to{opacity:1}}"
        "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>"
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#2dd4bf"/><stop offset=".55" stop-color="#a78bfa"/>'
        '<stop offset="1" stop-color="#fbbf24"/></linearGradient>'
        '<linearGradient id="v" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#2dd4bf"/><stop offset=".6" stop-color="#a78bfa"/>'
        '<stop offset="1" stop-color="#fbbf24"/></linearGradient></defs>'
    )


def write_kpis(own, langs, cc):
    top = [
        (str(len([r for r in own if r["name"] != USER])), "public repos", "since Aug 2025"),
        (str(cc["totalCommitContributions"]), "commits", "last 12 months"),
        (str(len([n for n in langs if n not in SKIP_LANGS])), "languages", "Python · TS · JS"),
        (str(cc["contributionCalendar"]["totalContributions"]), "contributions", "last 12 months"),
    ]
    for i, (num, label, sub) in enumerate(top + STATIC_KPIS):
        o = [open_svg(140, 92, f"{num} {label}")]
        o.append(f'<g style="animation:up .5s ease-out {i*.08:.2f}s both">')
        o.append('<rect width="140" height="92" rx="12" fill="#10162b"/>')
        o.append('<rect x=".5" y=".5" width="139" height="91" rx="12" fill="none" stroke="#fff" stroke-opacity=".09"/>')
        o.append('<rect width="4" height="92" rx="2" fill="url(#v)"/>')
        o.append(f'<text class="s" x="18" y="43" font-size="32" font-weight="800" fill="#f8fafc">{esc(num)}</text>')
        o.append(f'<text class="s" x="18" y="62" font-size="12" font-weight="600" fill="#cbd5e1">{esc(label)}</text>')
        o.append(f'<text class="m" x="18" y="79" font-size="9.5" fill="#2dd4bf">{esc(sub)}</text>')
        o.append("</g></svg>")
        (OUT / f"kpi-{i+1}.svg").write_text("".join(o), encoding="utf-8")


def level(n, mx):
    if n == 0:
        return "#161b33"
    r = n / mx
    return "#134e4a" if r < .25 else "#0f766e" if r < .5 else "#2dd4bf" if r < .8 else "#fbbf24"


def write_activity(cc):
    weeks = cc["contributionCalendar"]["weeks"][-20:]
    total = cc["contributionCalendar"]["totalContributions"]
    mx = max((d["contributionCount"] for wk in weeks for d in wk["contributionDays"]), default=1) or 1
    cell, pad = 18, 4
    step = cell + pad
    w, h = len(weeks) * step + 28, 7 * step + 74
    o = [open_svg(w, h, "Contribution heatmap, last 20 weeks")]
    o.append('<rect width="100%" height="100%" rx="14" fill="#10162b"/>')
    o.append(f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="#fff" stroke-opacity=".09"/>')
    o.append(f'<text class="m" x="14" y="26" font-size="11.5" fill="#94a3b8">LAST 20 WEEKS · {total} PUBLIC CONTRIBUTIONS / YR</text>')
    for wi, wk in enumerate(weeks):
        for d in wk["contributionDays"]:
            wd = datetime.date.fromisoformat(d["date"]).isoweekday() % 7
            c = d["contributionCount"]
            o.append(
                f'<rect x="{14+wi*step}" y="{42+wd*step}" width="{cell}" height="{cell}" rx="5" fill="{level(c, mx)}" '
                f'style="animation:in .5s ease-out {wi*0.04:.2f}s both"><title>{d["date"]}: {c}</title></rect>'
            )
    ly = h - 14
    o.append(f'<text class="s" x="{w-150}" y="{ly}" font-size="12" fill="#94a3b8">less</text>')
    for i, col in enumerate(("#161b33", "#134e4a", "#0f766e", "#2dd4bf", "#fbbf24")):
        o.append(f'<rect x="{w-118+i*17}" y="{ly-11}" width="12" height="12" rx="3" fill="{col}"/>')
    o.append("</svg>")
    (OUT / "activity.svg").write_text("".join(o), encoding="utf-8")


def write_langs(langs):
    items = sorted(((k, v) for k, v in langs.items() if k not in SKIP_LANGS), key=lambda kv: -kv[1])[:5]
    total = sum(v for _, v in items) or 1
    w, h = 440, 128
    o = [open_svg(w, h, "Language breakdown of public code")]
    o.append(f'<rect width="{w}" height="{h}" rx="14" fill="#10162b"/>')
    o.append(f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="#fff" stroke-opacity=".09"/>')
    o.append('<text class="m" x="16" y="26" font-size="11.5" fill="#94a3b8">LANGUAGES · PUBLIC CODE</text>')
    o.append(f'<clipPath id="c"><rect x="16" y="38" width="{w-32}" height="14" rx="7"/></clipPath>')
    o.append('<g clip-path="url(#c)"><g style="transform-origin:16px 0;animation:grow 1.2s ease-out both">')
    cur = 16.0
    for name, val in items:
        seg = (w - 32) * val / total
        o.append(f'<rect x="{cur:.1f}" y="38" width="{seg+1:.1f}" height="14" fill="{LANG_COLORS.get(name, "#64748b")}"/>')
        cur += seg
    o.append("</g></g>")
    for i, (name, val) in enumerate(items):
        x = 16 + (i % 3) * 138
        y = 80 + (i // 3) * 30
        col = LANG_COLORS.get(name, "#64748b")
        o.append(f'<circle cx="{x+5}" cy="{y-4}" r="5" fill="{col}"/>')
        o.append(f'<text class="s" x="{x+16}" y="{y}" font-size="13.5" font-weight="600" fill="#e2e8f0">{esc(name)}</text>')
        o.append(f'<text class="m" x="{x+16}" y="{y+14}" font-size="10.5" fill="#94a3b8">{100*val/total:.1f}%</text>')
    o.append("</svg>")
    (OUT / "langs.svg").write_text("".join(o), encoding="utf-8")


def write_timeline(own):
    rows = sorted((r for r in own if r["name"] != USER), key=lambda r: r["created_at"])
    gap = 66
    w, h = 440, 52 + len(rows) * gap
    o = [open_svg(w, h, "Build log of public repositories")]
    o.append(f'<rect width="{w}" height="{h}" rx="14" fill="#10162b"/>')
    o.append(f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="#fff" stroke-opacity=".09"/>')
    o.append('<text class="m" x="16" y="26" font-size="11.5" fill="#94a3b8">PUBLIC REPOS · NEWEST LAST</text>')
    top, x = 58, 34
    bottom = top + (len(rows) - 1) * gap
    o.append(f'<line x1="{x}" y1="{top}" x2="{x}" y2="{bottom}" stroke="#fff" stroke-opacity=".12" stroke-width="2"/>')
    o.append(
        f'<line x1="{x}" y1="{top}" x2="{x}" y2="{bottom}" stroke="url(#v)" stroke-width="3" '
        f'stroke-dasharray="{bottom-top}" stroke-dashoffset="{bottom-top}"><animate attributeName="stroke-dashoffset" '
        f'from="{bottom-top}" to="0" dur="1.8s" fill="freeze"/></line>'
    )
    for i, r in enumerate(rows):
        y = top + i * gap
        name = esc(r["name"].replace("---", " ").replace("_", " "))
        desc = (r.get("description") or "").strip()
        desc = esc(desc if len(desc) <= 52 else desc[:51] + "…")
        o.append(f'<g style="animation:up .5s ease-out {0.3+i*.2:.2f}s both">')
        o.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#10162b" stroke="url(#v)" stroke-width="3"/>')
        o.append(f'<text class="s" x="{x+22}" y="{y-3}" font-size="15" font-weight="700" fill="#f1f5f9">{name}</text>')
        o.append(f'<text class="m" x="{x+22}" y="{y+13}" font-size="10.5" fill="#2dd4bf">{r["created_at"][:7]}</text>')
        o.append(f'<text class="s" x="{x+22}" y="{y+29}" font-size="11.5" fill="#94a3b8">{desc}</text>')
        o.append("</g>")
    o.append("</svg>")
    (OUT / "timeline.svg").write_text("".join(o), encoding="utf-8")


def main():
    OUT.mkdir(exist_ok=True)
    own, langs, cc = fetch()
    write_kpis(own, langs, cc)
    write_activity(cc)
    write_langs(langs)
    write_timeline(own)
    print(f"[OK] repos={len(own)} langs={len(langs)}")


if __name__ == "__main__":
    main()
