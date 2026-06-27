from PIL import Image
import sys
import os

src_dir = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(src_dir, "0AEF390A-C219-4840-AE91-3C49125E499A.png")
out = os.path.join(src_dir, "badge-logo.png")

im = Image.open(src).convert("RGBA")
w, h = im.size
px = im.load()

sys.setrecursionlimit(10000)

# Flood-fill from each corner across connected near-white pixels, turning them
# transparent. This only strips the OUTER background (which connects to the
# corners) and leaves the white text/highlights *inside* the badge intact,
# since the gold/navy ring fully encloses them.
def is_white(p, thresh=18):
    r, g, b, a = p
    return a > 0 and r > 255 - thresh and g > 255 - thresh and b > 255 - thresh

visited = bytearray(w * h)
stack = []
for x in range(w):
    stack.append((x, 0))
    stack.append((x, h - 1))
for y in range(h):
    stack.append((0, y))
    stack.append((w - 1, y))

while stack:
    x, y = stack.pop()
    if x < 0 or x >= w or y < 0 or y >= h:
        continue
    idx = y * w + x
    if visited[idx]:
        continue
    p = px[x, y]
    if not is_white(p):
        continue
    visited[idx] = 1
    px[x, y] = (255, 255, 255, 0)
    stack.append((x + 1, y))
    stack.append((x - 1, y))
    stack.append((x, y + 1))
    stack.append((x, y - 1))

im.save(out, "PNG")
print(f"Saved {out} ({os.path.getsize(out) / 1024:.0f}KB)")
