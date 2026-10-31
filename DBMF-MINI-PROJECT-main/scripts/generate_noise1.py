# generate_noise.py
import numpy as np
from PIL import Image
import random

IMG_W, IMG_H = 256, 256

# THIS LINE does the 512x512 → 256x256 conversion automatically
img = Image.open(r"C:\DBMF\standard_test_images\WhatsApp Image 2026-04-07 at 15.31.14.jpeg").convert('L').resize((IMG_W, IMG_H), Image.LANCZOS)

pixels = np.array(img, dtype=np.uint8)

# Verify size before adding noise
print(f"Image size after resize: {pixels.shape}")  # must show (256, 256)

noisy = pixels.copy()
for _ in range(int(IMG_W*IMG_H*0.05//2)):
    noisy[random.randint(0, IMG_H-1)][random.randint(0, IMG_W-1)] = 255
for _ in range(int(IMG_W*IMG_H*0.05//2)):
    noisy[random.randint(0, IMG_H-1)][random.randint(0, IMG_W-1)] = 0

Image.fromarray(noisy).save(r"C:\DBMF\noisy_preview3.png")

# Save .mem file
with open("C:/DBMF/noisy_image3.mem", "w") as f:
    for val in noisy.flatten():
        f.write(f"{val:02X}\n")

# Verify line count
with open("C:/DBMF/noisy_image3.mem") as f:
    count = len(f.readlines())
print(f"Total pixels in .mem: {count}")  # must be 65536

print("Done — noisy_image3.mem and noisy_preview3.png saved")