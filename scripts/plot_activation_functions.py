"""Draw common activation functions and softmax examples as a standalone SVG."""

from math import erf, exp, sqrt, tanh
from pathlib import Path
from xml.sax.saxutils import escape


OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "activation-functions.svg"
WIDTH, HEIGHT = 1600, 860
BLUE, ORANGE, GREEN = "#315ac7", "#dd733c", "#23856d"


def sigmoid(x):
    return 1 / (1 + exp(-x))


def gelu(x):
    return x * (1 + erf(x / sqrt(2))) / 2


def softmax(logits):
    peak = max(logits)
    values = [exp(z - peak) for z in logits]
    total = sum(values)
    return [value / total for value in values]


def path_for(points, x0, y0, plot_w, plot_h, ymin, ymax):
    commands = []
    for index, (x, y) in enumerate(points):
        px = x0 + (x + 5) / 10 * plot_w
        py = y0 + (ymax - y) / (ymax - ymin) * plot_h
        commands.append(f"{'M' if index == 0 else 'L'}{px:.2f},{py:.2f}")
    return " ".join(commands)


def panel(parts, col, row, title, subtitle, ymin, ymax, series):
    panel_x, panel_y = 34 + col * 394, 92 + row * 378
    panel_w, panel_h = 376, 352
    x0, y0, plot_w, plot_h = panel_x + 48, panel_y + 78, 300, 225

    parts.append(
        f'<rect x="{panel_x}" y="{panel_y}" width="{panel_w}" '
        f'height="{panel_h}" rx="12" fill="white" stroke="#dce3ef"/>'
    )
    parts.append(
        f'<text x="{panel_x + 20}" y="{panel_y + 32}" class="title">'
        f"{escape(title)}</text>"
    )
    parts.append(
        f'<text x="{panel_x + 20}" y="{panel_y + 54}" class="subtitle">'
        f"{escape(subtitle)}</text>"
    )

    for tick in (-4, -2, 0, 2, 4):
        px = x0 + (tick + 5) / 10 * plot_w
        parts.append(
            f'<line x1="{px:.2f}" x2="{px:.2f}" y1="{y0}" '
            f'y2="{y0 + plot_h}" class="grid"/>'
        )
        parts.append(
            f'<text x="{px:.2f}" y="{y0 + plot_h + 19}" '
            f'class="tick" text-anchor="middle">{tick}</text>'
        )

    if ymax <= 1.2:
        y_ticks = (0, 0.5, 1) if ymin >= -0.2 else (-1, -0.5, 0, 0.5, 1)
    else:
        y_ticks = (0, 1, 2, 3, 4, 5)
    for tick in y_ticks:
        if not ymin <= tick <= ymax:
            continue
        py = y0 + (ymax - tick) / (ymax - ymin) * plot_h
        parts.append(
            f'<line x1="{x0}" x2="{x0 + plot_w}" y1="{py:.2f}" '
            f'y2="{py:.2f}" class="grid"/>'
        )
        parts.append(
            f'<text x="{x0 - 8}" y="{py + 4:.2f}" class="tick" '
            f'text-anchor="end">{tick:g}</text>'
        )

    for label, color, values in series:
        points = [(-5 + index / 30, value) for index, value in enumerate(values)]
        path = path_for(points, x0, y0, plot_w, plot_h, ymin, ymax)
        parts.append(
            f'<path d="{path}" fill="none" stroke="{color}" '
            f'stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
        )

    legend_y = panel_y + panel_h - 22
    for index, (label, color, _) in enumerate(series):
        legend_x = panel_x + 22 + index * 107
        parts.append(
            f'<line x1="{legend_x}" x2="{legend_x + 16}" '
            f'y1="{legend_y}" y2="{legend_y}" stroke="{color}" stroke-width="3"/>'
        )
        parts.append(
            f'<text x="{legend_x + 22}" y="{legend_y + 4}" '
            f'class="legend">{escape(label)}</text>'
        )


def main():
    xs = [-5 + index / 30 for index in range(301)]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
        'role="img" aria-labelledby="chart-title chart-desc">',
        '<title id="chart-title">Common activation functions and softmax</title>',
        '<desc id="chart-desc">Six scalar activation curves and two softmax '
        'examples with one logit varied from minus five to five.</desc>',
        '<style>text{font-family:Arial,Helvetica,sans-serif}'
        '.heading{font-size:27px;font-weight:700;fill:#192943}'
        '.note{font-size:15px;fill:#586781}'
        '.title{font-size:20px;font-weight:700;fill:#192943}'
        '.subtitle{font-size:14px;fill:#586781}'
        '.tick{font-size:12px;fill:#64748b}'
        '.legend{font-size:12px;fill:#43516a}'
        '.grid{stroke:#e8edf5;stroke-width:1}</style>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#f5f7fb"/>',
        '<text id="chart-title-visible" x="34" y="43" class="heading">'
        'Activation functions and softmax</text>',
        '<text x="34" y="70" class="note">'
        'Horizontal axis: input x (or varying logit). Vertical axis: output. '
        'Each panel has its own vertical scale.</text>',
    ]

    panel(parts, 0, 0, "Sigmoid", "1 / (1 + exp(-x))", -0.1, 1.1,
          [("sigmoid", BLUE, [sigmoid(x) for x in xs])])
    panel(parts, 1, 0, "Tanh", "tanh(x)", -1.2, 1.2,
          [("tanh", BLUE, [tanh(x) for x in xs])])
    panel(parts, 2, 0, "ReLU", "max(0, x)", -0.5, 5.5,
          [("ReLU", BLUE, [max(0, x) for x in xs])])
    panel(parts, 3, 0, "Leaky ReLU", "max(0.1x, x)", -0.7, 5.5,
          [("Leaky ReLU", BLUE, [max(0.1 * x, x) for x in xs])])
    panel(parts, 0, 1, "GELU", "x · Φ(x)", -1, 5.2,
          [("GELU", BLUE, [gelu(x) for x in xs])])
    panel(parts, 1, 1, "SiLU / Swish", "x · sigmoid(x)", -1, 5.2,
          [("SiLU", BLUE, [x * sigmoid(x) for x in xs])])

    two = [softmax([x, 0]) for x in xs]
    panel(parts, 2, 1, "Softmax: 2 classes", "logits = [x, 0]", -0.1, 1.1,
          [("P(x)", BLUE, [p[0] for p in two]),
           ("P(0)", ORANGE, [p[1] for p in two])])
    three = [softmax([x, 0, -1]) for x in xs]
    panel(parts, 3, 1, "Softmax: 3 classes", "logits = [x, 0, -1]", -0.1, 1.1,
          [("P(x)", BLUE, [p[0] for p in three]),
           ("P(0)", ORANGE, [p[1] for p in three]),
           ("P(-1)", GREEN, [p[2] for p in three])])

    parts.append(
        '<text x="34" y="842" class="note">Softmax acts on a vector; '
        'its plots hold the other logits fixed while x varies.</text>'
    )
    parts.append("</svg>")
    OUTPUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
