"""Render a chat-friendly PNG of the activation curves using Pillow."""

from pathlib import Path
from math import tanh

from PIL import Image, ImageDraw, ImageFont

from plot_activation_functions import BLUE, GREEN, ORANGE, gelu, sigmoid, softmax


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "activation-functions.png"
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
WIDTH, HEIGHT = 1600, 860
X_VALUES = [-5 + i / 30 for i in range(301)]


def font(size):
    return ImageFont.truetype(FONT_PATH, size)


def panel(draw, col, row, title, subtitle, ymin, ymax, series):
    px, py = 34 + col * 394, 92 + row * 378
    draw.rounded_rectangle((px, py, px + 376, py + 352), radius=12,
                           fill="white", outline="#dce3ef", width=2)
    draw.text((px + 20, py + 14), title, fill="#192943", font=font(20))
    draw.text((px + 20, py + 40), subtitle, fill="#586781", font=font(14))

    x0, y0, w, h = px + 48, py + 78, 300, 225
    for tick in (-4, -2, 0, 2, 4):
        x = x0 + (tick + 5) / 10 * w
        draw.line((x, y0, x, y0 + h), fill="#e8edf5", width=1)
        draw.text((x - 7, y0 + h + 5), str(tick), fill="#64748b", font=font(12))
    if ymax <= 1.2:
        ticks = (0, 0.5, 1) if ymin >= -0.2 else (-1, -0.5, 0, 0.5, 1)
    else:
        ticks = (0, 1, 2, 3, 4, 5)
    for tick in ticks:
        if ymin <= tick <= ymax:
            y = y0 + (ymax - tick) / (ymax - ymin) * h
            draw.line((x0, y, x0 + w, y), fill="#e8edf5", width=1)
            label = f"{tick:g}"
            draw.text((x0 - 12 - draw.textlength(label, font=font(12)), y - 7),
                      label, fill="#64748b", font=font(12))

    for name, color, values in series:
        points = [(x0 + (x + 5) / 10 * w,
                   y0 + (ymax - value) / (ymax - ymin) * h)
                  for x, value in zip(X_VALUES, values)]
        draw.line(points, fill=color, width=3, joint="curve")

    for index, (name, color, _) in enumerate(series):
        x = px + 22 + index * 107
        y = py + 330
        draw.line((x, y, x + 16, y), fill=color, width=3)
        draw.text((x + 22, y - 8), name, fill="#43516a", font=font(12))


def main():
    im = Image.new("RGB", (WIDTH, HEIGHT), "#f5f7fb")
    draw = ImageDraw.Draw(im)
    draw.text((34, 15), "Activation functions and softmax",
              fill="#192943", font=font(27))
    draw.text((34, 52),
              "Horizontal axis: input x (or varying logit). Vertical axis: output. Each panel has its own vertical scale.",
              fill="#586781", font=font(15))

    panel(draw, 0, 0, "Sigmoid", "1 / (1 + exp(-x))", -0.1, 1.1,
          [("sigmoid", BLUE, [sigmoid(x) for x in X_VALUES])])
    panel(draw, 1, 0, "Tanh", "tanh(x)", -1.2, 1.2,
          [("tanh", BLUE, [tanh(x) for x in X_VALUES])])
    panel(draw, 2, 0, "ReLU", "max(0, x)", -0.5, 5.5,
          [("ReLU", BLUE, [max(0, x) for x in X_VALUES])])
    panel(draw, 3, 0, "Leaky ReLU", "max(0.1x, x)", -0.7, 5.5,
          [("Leaky ReLU", BLUE, [max(0.1 * x, x) for x in X_VALUES])])
    panel(draw, 0, 1, "GELU", "x * Phi(x)", -1, 5.2,
          [("GELU", BLUE, [gelu(x) for x in X_VALUES])])
    panel(draw, 1, 1, "SiLU / Swish", "x * sigmoid(x)", -1, 5.2,
          [("SiLU", BLUE, [x * sigmoid(x) for x in X_VALUES])])
    two = [softmax([x, 0]) for x in X_VALUES]
    panel(draw, 2, 1, "Softmax: 2 classes", "logits = [x, 0]", -0.1, 1.1,
          [("P(x)", BLUE, [p[0] for p in two]),
           ("P(0)", ORANGE, [p[1] for p in two])])
    three = [softmax([x, 0, -1]) for x in X_VALUES]
    panel(draw, 3, 1, "Softmax: 3 classes", "logits = [x, 0, -1]", -0.1, 1.1,
          [("P(x)", BLUE, [p[0] for p in three]),
           ("P(0)", ORANGE, [p[1] for p in three]),
           ("P(-1)", GREEN, [p[2] for p in three])])

    draw.text((34, 823),
              "Softmax acts on a vector; the plots hold other logits fixed while x varies.",
              fill="#586781", font=font(15))
    im.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
