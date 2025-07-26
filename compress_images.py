import os
from PIL import Image

SOURCE_DIR = "static/images/portfolio"
DEST_DIR = "static/images/portfolio_compressed"
os.makedirs(DEST_DIR, exist_ok=True)

for filename in os.listdir(SOURCE_DIR):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        src_path = os.path.join(SOURCE_DIR, filename)
        dst_path = os.path.join(DEST_DIR, filename)

        with Image.open(src_path) as img:
            img = img.convert("RGB")  # ensure format
            img = img.resize((800, 600))  # resize for performance
            img.save(dst_path, "JPEG", quality=60, optimize=True)

print("✅ Image compression complete!")
