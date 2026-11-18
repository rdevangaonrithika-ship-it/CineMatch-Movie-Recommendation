"""
assets/create_assets.py
-----------------------
Generates placeholder images used by the Streamlit app when
no TMDB poster is available and when no logo file is present.

Run once:
    python assets/create_assets.py
"""

import os

ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))


def create_placeholder_png():
    """Create a dark-grey 300×450 placeholder poster PNG."""
    path = os.path.join(ASSETS_DIR, "placeholder.png")
    if os.path.exists(path):
        return

    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGB", (300, 450), color=(30, 30, 30))
        draw = ImageDraw.Draw(img)

        # Film-strip decoration
        for y in range(0, 450, 30):
            draw.rectangle([10, y + 5, 30, y + 25], fill=(50, 50, 50))
            draw.rectangle([270, y + 5, 290, y + 25], fill=(50, 50, 50))

        # Camera icon (simple circles)
        cx, cy, r = 150, 200, 55
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(220, 50, 50), width=4)
        draw.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], outline=(220, 50, 50), width=3)

        # Text
        try:
            font_large = ImageFont.truetype("arial.ttf", 22)
            font_small = ImageFont.truetype("arial.ttf", 14)
        except Exception:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

        draw.text((150, 300), "No Poster", fill=(180, 180, 180),
                  font=font_large, anchor="mm")
        draw.text((150, 330), "Available", fill=(120, 120, 120),
                  font=font_small, anchor="mm")

        img.save(path)
        print(f"Created: {path}")

    except ImportError:
        # PIL not available – create a minimal valid 1×1 PNG manually
        # This is the raw bytes of a 1×1 dark-grey PNG
        import struct, zlib

        def _png_chunk(chunk_type, data):
            c = chunk_type + data
            return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

        signature = b"\x89PNG\r\n\x1a\n"
        ihdr = _png_chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
        raw = b"\x00\x1e\x1e\x1e"   # filter byte + R G B for dark grey
        idat = _png_chunk(b"IDAT", zlib.compress(raw))
        iend = _png_chunk(b"IEND", b"")

        with open(path, "wb") as f:
            f.write(signature + ihdr + idat + iend)
        print(f"Created minimal placeholder: {path}")


def create_logo_png():
    """Create a simple CineMatch logo PNG."""
    path = os.path.join(ASSETS_DIR, "logo.png")
    if os.path.exists(path):
        return

    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGBA", (400, 120), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Red play-button triangle
        pts = [(10, 10), (10, 110), (90, 60)]
        draw.polygon(pts, fill=(229, 9, 20))

        # Title text
        try:
            font = ImageFont.truetype("arial.ttf", 56)
        except Exception:
            font = ImageFont.load_default()

        draw.text((110, 10), "CineMatch", fill=(255, 255, 255), font=font)

        img.save(path)
        print(f"Created: {path}")

    except ImportError:
        # Minimal transparent 1×1 PNG
        import struct, zlib

        def _png_chunk(chunk_type, data):
            c = chunk_type + data
            return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

        signature = b"\x89PNG\r\n\x1a\n"
        ihdr = _png_chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0))  # RGBA
        raw = b"\x00\x00\x00\x00\x00"  # transparent pixel
        idat = _png_chunk(b"IDAT", zlib.compress(raw))
        iend = _png_chunk(b"IEND", b"")

        with open(path, "wb") as f:
            f.write(signature + ihdr + idat + iend)
        print(f"Created minimal logo: {path}")


if __name__ == "__main__":
    create_placeholder_png()
    create_logo_png()
    print("Asset generation complete.")
