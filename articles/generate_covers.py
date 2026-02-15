"""Generate cover images for 'The Universal Paste Pattern' article."""
from PIL import Image, ImageDraw, ImageFont
import os

# Color scheme
BG = (15, 23, 42)       # #0F172A dark slate
AMBER = (251, 191, 36)  # #FBBF24 amber
WHITE = (255, 255, 255)
GRAY = (148, 163, 184)  # #94A3B8 slate-400
DIM = (51, 65, 85)      # #334155 slate-700

# Try to find a good font, fall back to default
def get_font(size, bold=False):
    font_paths = [
        "/System/Library/Fonts/SFPro-Bold.otf" if bold else "/System/Library/Fonts/SFPro-Regular.otf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def get_mono_font(size):
    mono_paths = [
        "/System/Library/Fonts/SFMono-Regular.otf",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
        "/System/Library/Fonts/Monaco.ttf",
    ]
    for path in mono_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def draw_code_snippet(draw, x, y, w, h):
    """Draw a stylized code block representing the universal paste pattern."""
    # Code block background
    draw.rounded_rectangle([x, y, x+w, y+h], radius=8, fill=(30, 41, 59))
    # Border
    draw.rounded_rectangle([x, y, x+w, y+h], radius=8, outline=DIM, width=1)

    mono = get_mono_font(13)
    line_h = 18
    cy = y + 12

    lines = [
        ("const ", GRAY), ("clipboardData", AMBER), (" = new ", GRAY), ("DataTransfer", WHITE), ("();", GRAY),
    ]
    # Line 1
    cx = x + 14
    for text, color in lines:
        draw.text((cx, cy), text, fill=color, font=mono)
        bbox = mono.getbbox(text)
        cx += bbox[2] - bbox[0]

    cy += line_h
    # Line 2
    cx = x + 14
    parts = [("clipboardData", AMBER), (".setData(", GRAY), ("'text/html'", (134, 239, 172)), (", html);", GRAY)]
    for text, color in parts:
        draw.text((cx, cy), text, fill=color, font=mono)
        bbox = mono.getbbox(text)
        cx += bbox[2] - bbox[0]

    cy += line_h
    # Line 3
    cx = x + 14
    parts = [("editor", AMBER), (".dispatchEvent(", GRAY), ("pasteEvent", WHITE), (");", GRAY)]
    for text, color in parts:
        draw.text((cx, cy), text, fill=color, font=mono)
        bbox = mono.getbbox(text)
        cx += bbox[2] - bbox[0]


def draw_platform_nodes(draw, cx, cy, r):
    """Draw three platform circles connected by lines."""
    import math
    positions = []
    labels = ["Substack", "LinkedIn", "Twitter/X"]
    for i, angle in enumerate([-90, 30, 150]):
        rad = math.radians(angle)
        px = cx + int(r * math.cos(rad))
        py = cy + int(r * math.sin(rad))
        positions.append((px, py))

    # Draw connecting lines
    for i in range(3):
        for j in range(i+1, 3):
            draw.line([positions[i], positions[j]], fill=DIM, width=2)

    # Draw center dot
    draw.ellipse([cx-4, cy-4, cx+4, cy+4], fill=AMBER)

    # Draw platform circles
    font_sm = get_font(13, bold=True)
    node_r = 28
    for (px, py), label in zip(positions, labels):
        draw.ellipse([px-node_r, py-node_r, px+node_r, py+node_r], fill=DIM, outline=AMBER, width=2)
        bbox = font_sm.getbbox(label)
        tw = bbox[2] - bbox[0]
        # Label below circle
        draw.text((px - tw//2, py + node_r + 6), label, fill=GRAY, font=font_sm)


def create_linkedin_cover():
    """1200x628 - LinkedIn / general cover."""
    w, h = 1200, 628
    img = Image.new('RGB', (w, h), BG)
    draw = ImageDraw.Draw(img)

    # Title
    title_font = get_font(42, bold=True)
    subtitle_font = get_font(18)

    # Left side: text
    draw.text((60, 80), "The Universal", fill=WHITE, font=title_font)
    draw.text((60, 130), "Paste Pattern", fill=AMBER, font=title_font)

    draw.text((60, 200), "Publishing one article across three", fill=GRAY, font=subtitle_font)
    draw.text((60, 226), "platforms with browser automation", fill=GRAY, font=subtitle_font)

    # Decorative line
    draw.line([(60, 275), (380, 275)], fill=AMBER, width=2)

    # Code snippet - left-center
    draw_code_snippet(draw, 60, 310, 420, 80)

    # Footer
    footer_font = get_font(14)
    draw.text((60, 560), "The Hybrid Builder  |  chatwithgpt.substack.com", fill=DIM, font=footer_font)

    # Right side: platform nodes
    draw_platform_nodes(draw, 850, 300, 130)

    # Decorative dots (grid pattern)
    for gx in range(700, 1150, 30):
        for gy in range(480, 600, 30):
            draw.ellipse([gx, gy, gx+3, gy+3], fill=DIM)

    img.save(os.path.join(os.path.dirname(__file__), '2026-02-15-universal-paste-cover-linkedin.png'))
    print(f"LinkedIn cover: {w}x{h}")


def create_substack_banner():
    """1100x220 - Substack banner (wide and short)."""
    w, h = 1100, 220
    img = Image.new('RGB', (w, h), BG)
    draw = ImageDraw.Draw(img)

    title_font = get_font(30, bold=True)
    subtitle_font = get_font(15)

    # Left: title
    draw.text((40, 40), "The Universal Paste Pattern", fill=WHITE, font=title_font)
    draw.text((40, 80), "One article. Three platforms. Zero APIs.", fill=AMBER, font=subtitle_font)

    # Small code hint
    mono = get_mono_font(12)
    draw.text((40, 130), "editor.dispatchEvent(new ClipboardEvent('paste', { clipboardData }))", fill=GRAY, font=mono)

    # Decorative line
    draw.line([(40, 170), (300, 170)], fill=AMBER, width=2)

    footer_font = get_font(12)
    draw.text((40, 182), "The Hybrid Builder", fill=DIM, font=footer_font)

    # Right: mini platform icons
    import math
    cx, cy, r = 900, 110, 60
    labels = ["S", "L", "X"]
    colors = [AMBER, (59, 130, 246), GRAY]  # amber, blue, gray
    for i, angle in enumerate([-90, 30, 150]):
        rad = math.radians(angle)
        px = cx + int(r * math.cos(rad))
        py = cy + int(r * math.sin(rad))
        node_r = 18
        draw.ellipse([px-node_r, py-node_r, px+node_r, py+node_r], fill=DIM, outline=colors[i], width=2)
        char_font = get_font(16, bold=True)
        bbox = char_font.getbbox(labels[i])
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((px - tw//2, py - th//2 - 2), labels[i], fill=colors[i], font=char_font)

    # Connecting lines
    for i, angle_i in enumerate([-90, 30, 150]):
        for j, angle_j in enumerate([-90, 30, 150]):
            if i < j:
                rad_i = math.radians(angle_i)
                rad_j = math.radians(angle_j)
                pi = (cx + int(r * math.cos(rad_i)), cy + int(r * math.sin(rad_i)))
                pj = (cx + int(r * math.cos(rad_j)), cy + int(r * math.sin(rad_j)))
                draw.line([pi, pj], fill=DIM, width=1)

    # Center dot
    draw.ellipse([cx-3, cy-3, cx+3, cy+3], fill=AMBER)

    # Dot grid
    for gx in range(1000, 1080, 20):
        for gy in range(30, 200, 20):
            draw.ellipse([gx, gy, gx+2, gy+2], fill=DIM)

    img.save(os.path.join(os.path.dirname(__file__), '2026-02-15-universal-paste-cover-substack.png'))
    print(f"Substack banner: {w}x{h}")


def create_twitter_card():
    """1200x675 - Twitter card (slightly taller than LinkedIn)."""
    w, h = 1200, 675
    img = Image.new('RGB', (w, h), BG)
    draw = ImageDraw.Draw(img)

    title_font = get_font(46, bold=True)
    subtitle_font = get_font(20)

    # Left side: text
    draw.text((60, 80), "The Universal", fill=WHITE, font=title_font)
    draw.text((60, 136), "Paste Pattern", fill=AMBER, font=title_font)

    draw.text((60, 210), "Publishing one article across three", fill=GRAY, font=subtitle_font)
    draw.text((60, 238), "platforms with browser automation", fill=GRAY, font=subtitle_font)

    # Decorative line
    draw.line([(60, 290), (400, 290)], fill=AMBER, width=2)

    # Code snippet
    draw_code_snippet(draw, 60, 320, 440, 80)

    # Footer
    footer_font = get_font(14)
    draw.text((60, 610), "The Hybrid Builder  |  chatwithgpt.substack.com", fill=DIM, font=footer_font)

    # Right side: platform nodes (larger)
    draw_platform_nodes(draw, 860, 320, 140)

    # Decorative dots
    for gx in range(700, 1150, 30):
        for gy in range(520, 640, 30):
            draw.ellipse([gx, gy, gx+3, gy+3], fill=DIM)

    img.save(os.path.join(os.path.dirname(__file__), '2026-02-15-universal-paste-cover-twitter.png'))
    print(f"Twitter card: {w}x{h}")


if __name__ == '__main__':
    create_linkedin_cover()
    create_substack_banner()
    create_twitter_card()
    print("All covers generated!")
