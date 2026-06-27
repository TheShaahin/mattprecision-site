from PIL import Image
import os

src_dir = os.path.dirname(os.path.abspath(__file__))
files = ["IMG_2917.PNG", "IMG_2920.PNG", "IMG_2925.PNG", "IMG_2930.PNG", "IMG_2931.PNG", "IMG_2932.PNG"]
MAX_W = 1400

for f in files:
    path = os.path.join(src_dir, f)
    im = Image.open(path).convert("RGB")
    if im.width > MAX_W:
        ratio = MAX_W / im.width
        im = im.resize((MAX_W, int(im.height * ratio)), Image.LANCZOS)
    out_name = os.path.splitext(f)[0] + ".jpg"
    out_path = os.path.join(src_dir, out_name)
    im.save(out_path, "JPEG", quality=78, optimize=True)
    orig_kb = os.path.getsize(path) / 1024
    new_kb = os.path.getsize(out_path) / 1024
    print(f"{f}: {orig_kb:.0f}KB -> {out_name}: {new_kb:.0f}KB")
