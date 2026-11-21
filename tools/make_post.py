#!/usr/bin/env python3
"""Generate a CyberAlerts post (post.jpg, 1080x1350) and reel (reel.mp4, 1080x1920, 8 s)
in the house style, from a small JSON spec.

Usage:
    python3 tools/make_post.py posts/07-qr-code/spec.json

spec.json:
{
  "headline": "Scanning a QR code never *gets* you money.",   # *...* = yellow highlight
  "sub": "QR codes are for paying, not receiving. Don't scan, don't enter your PIN.",
  "cta": "Don't scan"
}

The reel reuses the shared soundtrack in assets/soundtrack.m4a (if present).
Needs: Pillow, numpy, ffmpeg.
"""
import json, os, re, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = "/usr/share/fonts/truetype/google-fonts"
ANTON = os.path.join(FONT_DIR, "ofl/anton/Anton-Regular.ttf")
POP_REG = os.path.join(FONT_DIR, "Poppins-Regular.ttf")
POP_BOLD = os.path.join(FONT_DIR, "Poppins-Bold.ttf")

BG = (11, 31, 58)
RED = (229, 57, 69)
YELLOW = (255, 214, 10)
WHITE = (255, 255, 255)
SUBTLE = (202, 214, 236)
NAVY_TEXT = (11, 31, 58)

BADGE = "NO GLAMOUR  ·  ONLY CYBERALERTS"
HANDLE = "@gskumar20012018"
LEFT = 90
RIGHT = 990
FPS = 30
DURATION = 8.0


def tokens(headline):
    """Split headline into (word, highlighted) tuples; *...* marks highlight."""
    out = []
    for i, part in enumerate(re.split(r"\*", headline)):
        for w in part.split():
            out.append((w.upper(), i % 2 == 1))
    return out


def wrap_words(words, font, width, draw):
    lines, cur = [], []
    for w in words:
        trial = cur + [w]
        text = " ".join(t[0] for t in trial)
        if cur and draw.textlength(text, font=font) > width:
            lines.append(cur)
            cur = [w]
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def wrap_text(text, font, width, draw):
    return [" ".join(t[0] for t in l) for l in wrap_words([(w, False) for w in text.split()], font, width, draw)]


def layout(spec, h, d):
    """Return list of drawable elements with their reveal time (seconds)."""
    head_font = ImageFont.truetype(ANTON, 116)
    sub_font = ImageFont.truetype(POP_REG, 52)
    badge_font = ImageFont.truetype(POP_BOLD, 34)
    cta_font = ImageFont.truetype(POP_BOLD, 48)
    handle_font = ImageFont.truetype(POP_REG, 34)

    head_lines = wrap_words(tokens(spec["headline"]), head_font, RIGHT - LEFT, d)
    sub_lines = wrap_text(spec["sub"], sub_font, RIGHT - LEFT - 20, d)
    head_lh, sub_lh = 132, 70
    block_h = len(head_lines) * head_lh + 24 + len(sub_lines) * sub_lh

    reel = h == 1920
    badge_y = 250 if reel else 90
    center = 900 if reel else 670
    cta_y = 1400 if reel else 1160
    top = center - block_h // 2

    els = []
    # badge
    bw = d.textlength(BADGE, font=badge_font) + 56
    els.append(("box", (LEFT, badge_y, LEFT + bw, badge_y + 78), RED, 0.2))
    els.append(("text", (LEFT + 28, badge_y + 39), BADGE, badge_font, WHITE, "lm", 0.2))
    # headline, line by line; words are drawn individually to allow highlights
    y = top
    t = 0.8
    space = d.textlength(" ", font=head_font)
    for line in head_lines:
        x = LEFT
        for word, hl in line:
            els.append(("text", (x, y), word, head_font, YELLOW if hl else WHITE, "la", t))
            x += d.textlength(word, font=head_font) + space
        y += head_lh
        t += 0.6
    y += 24
    for s in sub_lines:
        els.append(("text", (LEFT, y), s, sub_font, SUBTLE, "la", t))
        y += sub_lh
    t += 0.7
    # CTA
    cw = d.textlength(spec["cta"], font=cta_font) + 76
    els.append(("box", (LEFT, cta_y, LEFT + cw, cta_y + 102), YELLOW, t))
    els.append(("text", (LEFT + 38, cta_y + 51), spec["cta"], cta_font, NAVY_TEXT, "lm", t))
    # handle
    if reel:
        els.append(("text", (LEFT, cta_y + 140), HANDLE, handle_font, SUBTLE, "lm", 0.0))
    else:
        els.append(("text", (RIGHT - 2, cta_y + 51), HANDLE, handle_font, SUBTLE, "rm", 0.0))
    return els


def render(els, size, now=None):
    img = Image.new("RGB", size, BG)
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for el in els:
        start = el[-1]
        if now is None:
            alpha, dy = 255, 0
        else:
            p = max(0.0, min(1.0, (now - start) / 0.35))
            if p <= 0:
                continue
            p = 1 - (1 - p) ** 3  # ease-out
            alpha, dy = int(255 * p), int(24 * (1 - p))
        if el[0] == "box":
            x0, y0, x1, y1 = el[1]
            d.rounded_rectangle((x0, y0 + dy, x1, y1 + dy), radius=12, fill=el[2] + (alpha,))
        else:
            _, (x, y), text, font, color, anchor, _ = el
            d.text((x, y + dy), text, font=font, fill=color + (alpha,), anchor=anchor)
    img.paste(layer, (0, 0), layer)
    return img


def main(spec_path):
    spec = json.load(open(spec_path))
    out_dir = os.path.dirname(os.path.abspath(spec_path))
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))

    # Static post
    render(layout(spec, 1350, probe), (1080, 1350)).save(os.path.join(out_dir, "post.jpg"), quality=92)

    # Reel
    els = layout(spec, 1920, probe)
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(int(DURATION * FPS)):
            render(els, (1080, 1920), now=i / FPS).save(os.path.join(tmp, f"f{i:04d}.png"))
        cmd = ["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%04d.png")]
        audio = os.path.join(ROOT, "assets", "soundtrack.m4a")
        if os.path.exists(audio):
            cmd += ["-i", audio, "-c:a", "aac", "-shortest"]
        cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", os.path.join(out_dir, "reel.mp4")]
        subprocess.run(cmd, check=True)
    print("wrote", out_dir)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
