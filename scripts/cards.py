"""Build the static project-card SVGs and the terminal 'about' card.

Run once (outputs are committed): python scripts/cards.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
SANS = "'Segoe UI',-apple-system,Helvetica,Arial,sans-serif"
MONO = "SFMono-Regular,Consolas,'Liberation Mono',Menlo,monospace"

HEAD = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">'
    "<style>"
    ".s{{font-family:" + SANS + "}}.m{{font-family:" + MONO + "}}"
    "@keyframes rise{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}"
    "@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}"
    "@keyframes draw{{to{{stroke-dashoffset:0}}}}"
    "@keyframes bounce{{0%,100%{{transform:scaleY(.25)}}50%{{transform:scaleY(1)}}}}"
    "@keyframes sweep{{from{{transform:translateX(0)}}to{{transform:translateX(120px)}}}}"
    "@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}"
    "@keyframes blink{{50%{{opacity:0}}}}"
    "@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}"
    "@media (prefers-reduced-motion:reduce){{*{{animation:none!important;opacity:1!important}}}}"
    "{extra}</style>"
)


def card(slug, color, tag, title, lines, chips, viz, linked=False):
    w, h = 440, 232
    o = [HEAD.format(w=w, h=h, label=f"{title}: {' '.join(lines)}", extra="")]
    o.append(
        f'<defs><linearGradient id="a" x1="0" x2="1"><stop offset="0" stop-color="{color}"/>'
        f'<stop offset="1" stop-color="{color}" stop-opacity=".15"/></linearGradient></defs>'
    )
    o.append(f'<rect width="{w}" height="{h}" rx="16" fill="#10162b"/>')
    o.append(f'<rect width="{w}" height="4" rx="2" fill="url(#a)"/>')
    o.append(f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="none" stroke="#fff" stroke-opacity=".09"/>')
    tw = 8 * len(tag) + 22
    o.append(f'<rect x="22" y="24" width="{tw}" height="22" rx="11" fill="{color}" fill-opacity=".14"/>')
    o.append(f'<text class="m" x="33" y="39" font-size="10.5" letter-spacing="1" fill="{color}">{tag}</text>')
    o.append(f'<text class="s" x="22" y="78" font-size="19" font-weight="800" fill="#f8fafc">{title}</text>')
    for i, ln in enumerate(lines):
        o.append(f'<text class="s" x="22" y="{102+i*19}" font-size="14" fill="#b6c2d6">{ln}</text>')
    x = 22
    for val, lab in chips:
        o.append(f'<text class="m" x="{x}" y="200" font-size="12" font-weight="700" fill="#e2e8f0">{val}</text>')
        o.append(f'<text class="m" x="{x}" y="215" font-size="11" fill="#94a3b8">{lab}</text>')
        x += max(len(val), len(lab)) * 7.4 + 22
    if linked:
        o.append(f'<text class="m" x="{w-20}" y="39" text-anchor="end" font-size="11" font-weight="700" fill="{color}">open repo ↗</text>')
    o.append(f'<g transform="translate(286,56)">{viz}</g>')
    o.append("</svg>")
    (OUT / f"card-{slug}-v2.svg").write_text("".join(o), encoding="utf-8")


def viz_clv(c):
    heights = [96, 66, 48, 34, 24, 17, 12]
    bars = "".join(
        f'<rect x="{i*19}" y="{104-h}" width="13" height="{h}" rx="3" fill="{c}" fill-opacity="{.95-i*.1:.2f}" '
        f'style="transform-origin:{i*19+6}px 104px;animation:rise .6s ease-out {i*.12:.2f}s both"/>'
        for i, h in enumerate(heights)
    )
    curve = (
        f'<path d="M6 8 C 30 -6, 60 -10, 126 -14" transform="translate(0,12)" fill="none" stroke="#fbbf24" '
        f'stroke-width="2.5" stroke-linecap="round" stroke-dasharray="200" stroke-dashoffset="200" '
        f'style="animation:draw 1.8s ease-out .9s forwards"/>'
    )
    dot = '<circle cx="126" cy="-2" r="4.5" fill="#fbbf24" style="animation:fade .4s ease-out 2.6s both"/>'
    lab = f'<text class="m" x="0" y="124" font-size="11" fill="#94a3b8">value is concentrated</text>'
    return bars + curve + dot + lab


def viz_stock(c):
    candles = [(0, 70, 40, 62, 48, 1), (1, 58, 30, 52, 36, 1), (2, 66, 38, 44, 60, 0), (3, 62, 32, 36, 54, 0),
               (4, 80, 52, 74, 58, 1), (5, 70, 42, 50, 66, 0), (6, 54, 24, 30, 48, 1), (7, 46, 16, 22, 40, 1)]
    out = []
    for i, hi, lo, op, cl, up in candles:
        x = 6 + i * 16
        col = "#2dd4bf" if up else "#fb7185"
        top, bot = min(op, cl) + 12, max(op, cl) + 12
        out.append(
            f'<g style="animation:rise .5s ease-out {i*.15:.2f}s both">'
            f'<line x1="{x+4}" x2="{x+4}" y1="{lo+14}" y2="{hi+22}" stroke="{col}" stroke-width="1.5"/>'
            f'<rect x="{x}" y="{top}" width="8" height="{max(bot-top,4)}" rx="1.5" fill="{col}"/></g>'
        )
    out.append('<line x1="62" x2="62" y1="2" y2="104" stroke="#fbbf24" stroke-dasharray="3 4" stroke-opacity=".8"/>')
    out.append('<text class="m" x="66" y="8" font-size="10" fill="#fbbf24">demerger</text>')
    out.append(
        f'<path d="M0 98 Q 30 70 62 88 T 128 80" fill="none" stroke="{c}" stroke-opacity=".5" stroke-width="2" '
        f'stroke-dasharray="200" stroke-dashoffset="200" style="animation:draw 2s ease-out 1.2s forwards"/>'
    )
    out.append('<text class="m" x="0" y="124" font-size="11" fill="#94a3b8">TMCV  vs  TMPV</text>')
    return "".join(out)


def viz_os(c):
    rings = [(46, "#2dd4bf", .78), (34, "#a78bfa", .55), (22, "#fbbf24", .9)]
    out = []
    for i, (r, col, frac) in enumerate(rings):
        circ = 2 * 3.14159 * r
        out.append(f'<circle cx="64" cy="54" r="{r}" fill="none" stroke="#fff" stroke-opacity=".07" stroke-width="8"/>')
        out.append(
            f'<circle cx="64" cy="54" r="{r}" fill="none" stroke="{col}" stroke-width="8" stroke-linecap="round" '
            f'stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ:.1f}" transform="rotate(-90 64 54)" '
            f'><animate attributeName="stroke-dashoffset" from="{circ:.1f}" to="{circ*(1-frac):.1f}" '
            f'dur="1.6s" begin="{i*.3:.1f}s" fill="freeze"/></circle>'
        )
    out.append('<text class="m" x="64" y="58" text-anchor="middle" font-size="16" font-weight="800" fill="#f8fafc">10</text>')
    out.append('<text class="m" x="64" y="70" text-anchor="middle" font-size="9" fill="#94a3b8">views</text>')
    out.append('<text class="m" x="0" y="124" font-size="11" fill="#94a3b8">fitness · vault · memory</text>')
    return "".join(out)


def viz_radio(c):
    hs = [40, 78, 56, 96, 64, 84, 48, 70, 36]
    bars = "".join(
        f'<rect x="{i*14}" y="{104-h}" width="9" height="{h}" rx="3" fill="{c}" fill-opacity="{.5+ (h/200):.2f}" '
        f'style="transform-box:fill-box;transform-origin:bottom;animation:bounce {0.7+(i%4)*.18:.2f}s ease-in-out {i*.09:.2f}s infinite"/>'
        for i, h in enumerate(hs)
    )
    live = (
        '<circle cx="4" cy="-2" r="3.5" fill="#34d399" style="animation:pulse 1.6s infinite"/>'
        '<text class="m" x="13" y="1.5" font-size="11" fill="#34d399">live</text>'
        '<text class="m" x="0" y="124" font-size="11" fill="#94a3b8">log jaag rahe hain</text>'
    )
    return bars + live


def viz_case(c):
    out = []
    for i in range(3):
        out.append(
            f'<g style="animation:bob {3+i*.4:.1f}s ease-in-out {i*.5:.1f}s infinite">'
            f'<rect x="{i*14}" y="{6+i*14}" width="96" height="62" rx="6" fill="#161b33" stroke="{c}" stroke-opacity="{.9-i*.28:.2f}"/>'
            f'<rect x="{i*14+10}" y="{16+i*14}" width="44" height="6" rx="3" fill="{c}" fill-opacity=".7"/>'
            f'<rect x="{i*14+10}" y="{30+i*14}" width="70" height="4" rx="2" fill="#fff" fill-opacity=".14"/>'
            f'<rect x="{i*14+10}" y="{40+i*14}" width="56" height="4" rx="2" fill="#fff" fill-opacity=".14"/></g>'
        )
    out.append(
        '<g style="animation:fade .5s ease-out 1.2s both"><circle cx="118" cy="30" r="12" fill="#34d399" fill-opacity=".18"/>'
        '<path d="M112 30 l5 5 l9 -10" fill="none" stroke="#34d399" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></g>'
    )
    out.append('<text class="m" x="0" y="124" font-size="11" fill="#94a3b8">html → pptx · gate ✓</text>')
    return "".join(out)


def viz_reel(c):
    rows = [(0, [(0, 34), (40, 20), (66, 44), (116, 12)]), (1, [(6, 52), (64, 30), (100, 28)]), (2, [(0, 12), (20, 12), (46, 12), (72, 12), (98, 12)])]
    out = []
    for r, blocks in rows:
        y = 8 + r * 30
        out.append(f'<rect x="0" y="{y}" width="128" height="22" rx="5" fill="#fff" fill-opacity=".05"/>')
        for x, w in blocks:
            out.append(f'<rect x="{x}" y="{y+3}" width="{w}" height="16" rx="4" fill="{c}" fill-opacity="{.85-r*.2:.2f}"/>')
    out.append(f'<g style="animation:sweep 3.4s linear infinite"><rect x="0" y="0" width="2" height="100" fill="#fbbf24"/></g>')
    out.append('<text class="m" x="0" y="124" font-size="11" fill="#94a3b8">script · voice · render</text>')
    return "".join(out)


def terminal():
    w, h = 520, 262
    lines = [
        ("cmd", "whoami", 0.3),
        ("out", "Tuhin Bhattacharya · Goa, India", 0.9),
        ("cmd", "cat focus.txt", 1.7),
        ("out", "data -> models -> products people use", 2.3),
        ("cmd", "ls shipped/", 3.1),
        ("out", "clv/  quant/  karma-os/  radio/  case/  reel/", 3.7),
        ("cmd", "status --hiring", 4.5),
        ("hot", "open to analyst / AI engineer roles", 5.1),
    ]
    o = [HEAD.format(w=w, h=h, label="Terminal card: about Tuhin", extra="")]
    o.append(f'<rect width="{w}" height="{h}" rx="14" fill="#0b1020"/>')
    o.append(f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="#fff" stroke-opacity=".09"/>')
    o.append(f'<rect width="{w}" height="34" rx="14" fill="#151a33"/><rect y="20" width="{w}" height="14" fill="#151a33"/>')
    for i, col in enumerate(("#fb7185", "#fbbf24", "#34d399")):
        o.append(f'<circle cx="{20+i*18}" cy="17" r="5.5" fill="{col}"/>')
    o.append(f'<text class="m" x="{w//2}" y="21" text-anchor="middle" font-size="12" fill="#94a3b8">karma: about.sh</text>')
    for i, (kind, text, delay) in enumerate(lines):
        y = 68 + i * 24
        o.append(f'<g style="animation:fade .01s linear {delay}s both">')
        if kind == "cmd":
            o.append(f'<text class="m" x="20" y="{y}" font-size="16"><tspan fill="#2dd4bf" font-weight="700">$ </tspan><tspan fill="#e2e8f0">{text}</tspan></text>')
        else:
            fill = "#fbbf24" if kind == "hot" else "#94a3b8"
            o.append(f'<text class="m" x="20" y="{y}" font-size="16" fill="{fill}">{text}</text>')
        o.append("</g>")
    o.append(f'<rect x="20" y="{68+8*24-12}" width="9" height="16" fill="#2dd4bf" style="animation:blink 1s steps(1) 6s infinite"/>')
    o.append("</svg>")
    (OUT / "about-v3.svg").write_text("".join(o), encoding="utf-8")


def main():
    OUT.mkdir(exist_ok=True)
    card("clv", "#2dd4bf", "LIVE · DATA SCIENCE", "Customer Lifetime Value",
         ["Which customers bleed money,", "and which ones pay the bills?", "Told as an interactive story."],
         [("9,134", "customers"), ("R² 0.68", "cross-validated"), ("$1,378", "mean error")], viz_clv("#2dd4bf"), linked=True)
    card("quant", "#fbbf24", "RESEARCH · QUANT", "Quant Terminal",
         ["Did ML beat buy-and-hold after", "the Tata Motors split? The", "honest answer is inside."],
         [("23", "notebooks"), ("6", "app pages"), ("~55%", "best accuracy")], viz_stock("#fbbf24"), linked=True)
    card("os", "#a78bfa", "PERSONAL OS", "KARMA-OS",
         ["My life as a dashboard:", "workouts, music, notes, agents", "and what correlates."],
         [("10", "views"), ("React", "D3 · Zustand"), ("1", "user: me")], viz_os("#a78bfa"), linked=True)
    card("radio", "#fb7185", "LIVE · PRODUCT", "Hostel Vibes Radio",
         ["An always-on radio for Indian", "hostel life. Every room is", "a mood, every hour a vibe."],
         [("5", "rooms"), ("Realtime", "Supabase"), ("Hinglish", "all copy")], viz_radio("#fb7185"), linked=True)
    card("case", "#38bdf8", "PRIVATE · AUTOMATION", "Case-Comp Engine",
         ["From messy case brief to a", "defended deck, with a quality", "gate on every slide."],
         [("HTML→PPTX", "native export"), ("gates", "fidelity checks"), ("loop", "auto-improve")], viz_case("#38bdf8"))
    card("reel", "#a3e635", "PRIVATE · AI AGENTS", "Reel Crew",
         ["AI agents that research,", "script, voice and render short", "videos. I approve each stage."],
         [("24", "agents"), ("local", "TTS + ASR"), ("Remotion", "render")], viz_reel("#a3e635"))
    terminal()
    print("[OK] cards written")


if __name__ == "__main__":
    main()
