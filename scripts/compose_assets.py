# Compose HumanBotty presentation assets from session masters.
# Run from repo root: py -3 scripts/compose_assets.py
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
MASTERS = PUBLIC / "assets" / "masters"

FONT_DISPLAY = PUBLIC / "fonts" / "fontshare" / "clash-display" / "otf" / "ClashDisplay-Bold.otf"
FONT_SANS = PUBLIC / "fonts" / "fontshare" / "satoshi" / "otf" / "Satoshi-Medium.otf"
FONT_SANS_REG = PUBLIC / "fonts" / "fontshare" / "satoshi" / "otf" / "Satoshi-Regular.otf"

CYAN = (61, 224, 255, 255)
COPPER = (201, 137, 90, 255)
CREAM = (232, 236, 244, 255)
MUTED = (180, 190, 204, 255)


def load_font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def cover(im: Image.Image, w: int, h: int) -> Image.Image:
    src = im.convert("RGB")
    scale = max(w / src.width, h / src.height)
    nw, nh = int(src.width * scale), int(src.height * scale)
    src = src.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - w) // 2
    top = (nh - h) // 2
    return src.crop((left, top, left + w, top + h))


def save_jpeg(im: Image.Image, path: Path, quality: int = 88) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rgb = im.convert("RGB")
    rgb.save(path, "JPEG", quality=quality, optimize=True, progressive=True)


def save_png(im: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, "PNG", optimize=True)


def main() -> None:
    MASTERS.mkdir(parents=True, exist_ok=True)
    hero_src = MASTERS / "hero-sense-head.jpg"
    atelier_src = MASTERS / "atelier-wide.jpg"
    mark_src = MASTERS / "mark-head.jpg"
    for src in (hero_src, atelier_src, mark_src):
        if not src.exists():
            raise SystemExit(f"missing master {src}")

    hero = Image.open(hero_src)
    atelier = Image.open(atelier_src)
    mark = Image.open(mark_src)

    save_jpeg(cover(hero, 1600, 900), PUBLIC / "assets" / "hero.jpg", 90)
    save_jpeg(cover(atelier, 1600, 900), PUBLIC / "assets" / "atelier.jpg", 88)

    # OG 1200x630: sense-head with left text well (cleaner than the atelier frame)
    og = cover(hero, 1200, 630)
    shade = Image.new("L", (1200, 630), 0)
    sd = ImageDraw.Draw(shade)
    for x in range(0, 720):
        t = 1.0 - (x / 720)
        v = int(220 * (t ** 1.15))
        sd.line([(x, 0), (x, 629)], fill=v)
    overlay = Image.new("RGB", (1200, 630), (7, 8, 12))
    og = Image.composite(overlay, og, shade.filter(ImageFilter.GaussianBlur(8)))
    draw = ImageDraw.Draw(og)
    kicker = load_font(FONT_SANS, 22)
    title = load_font(FONT_DISPLAY, 72)
    sub = load_font(FONT_SANS, 28)
    urlf = load_font(FONT_SANS_REG, 22)
    draw.text((64, 168), "PUBLIC MAKER GUIDE", font=kicker, fill=CYAN)
    draw.text((64, 210), "HumanBotty", font=title, fill=CREAM)
    draw.text((64, 300), "A body for your AI", font=sub, fill=COPPER)
    draw.text((64, 500), "humanbotty.jonbailey.xyz", font=urlf, fill=MUTED)
    save_jpeg(og, PUBLIC / "og.jpg", 90)
    save_png(og, PUBLIC / "og.png")
    save_jpeg(og, PUBLIC / "share-card.jpg", 90)

    # Hive still 1280x720
    hive = cover(hero, 1280, 720)
    save_jpeg(hive, PUBLIC / "assets" / "hive.jpg", 88)

    icon = cover(mark, 1024, 1024)
    save_png(icon.resize((512, 512), Image.Resampling.LANCZOS), PUBLIC / "icon-512.png")
    save_png(icon.resize((192, 192), Image.Resampling.LANCZOS), PUBLIC / "icon-192.png")
    save_png(icon.resize((32, 32), Image.Resampling.LANCZOS), PUBLIC / "favicon.png")
    print("assets ok")


if __name__ == "__main__":
    main()
