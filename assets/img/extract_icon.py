from PIL import Image
import os

src_dir = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(src_dir, "0AEF390A-C219-4840-AE91-3C49125E499A.png")
out = os.path.join(src_dir, "icon-logo.png")

im = Image.open(src).convert("RGBA")
w, h = im.size
px = im.load()


def is_white(p, thresh=22):
    r, g, b, a = p
    return a > 0 and r > 255 - thresh and g > 255 - thresh and b > 255 - thresh


def flood_fill(seeds, match_fn):
    visited = bytearray(w * h)
    stack = list(seeds)
    count = 0
    while stack:
        x, y = stack.pop()
        if x < 0 or x >= w or y < 0 or y >= h:
            continue
        idx = y * w + x
        if visited[idx]:
            continue
        p = px[x, y]
        if not match_fn(p):
            continue
        visited[idx] = 1
        count += 1
        px[x, y] = (255, 255, 255, 0)
        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))
    return count


# 1. Strip the outer background (white, connects to all four edges)
edge_seeds = []
for x in range(w):
    edge_seeds.append((x, 0))
    edge_seeds.append((x, h - 1))
for y in range(h):
    edge_seeds.append((0, y))
    edge_seeds.append((w - 1, y))
flood_fill(edge_seeds, is_white)

# 2. Strip the inner white disk behind the house/M icon
flood_fill([(w // 2, h // 2 - 250), (w // 2 - 150, h // 2 - 150)], is_white)

# 3. Strip the gold/navy ring + lettering itself: it's one connected blob of
#    opaque pixels touching the very top/bottom/left/right edge of the (now
#    transparent-cornered) square, while the icon floats separately in the
#    middle. Flood-fill any opaque pixel reachable from a ring seed.
def is_opaque(p):
    return p[3] > 0

ring_seeds = [(w // 2, 4), (w // 2, h - 5), (4, h // 2), (w - 5, h // 2)]
flood_fill(ring_seeds, is_opaque)

# 4. Crop tightly to whatever opaque pixels remain (just the icon now)
bbox = im.getbbox()
icon = im.crop(bbox)

MAX = 600
if icon.width > MAX:
    ratio = MAX / icon.width
    icon = icon.resize((MAX, int(icon.height * ratio)), Image.LANCZOS)

icon.save(out, "PNG", optimize=True)
print(f"Saved {out} size={icon.size} ({os.path.getsize(out)/1024:.0f}KB)")
