# generate_hex.py — run on PC
import numpy as np
from PIL import Image
import random

IMG_W, IMG_H = 256, 256
img = Image.open("C:\DBMF\lena.tif").convert('L').resize((IMG_W, IMG_H))
pixels = np.array(img, dtype=np.uint8)

noisy = pixels.copy()
for _ in range(int(IMG_W*IMG_H*0.05//2)):
    noisy[random.randint(0,255)][random.randint(0,255)] = 255
for _ in range(int(IMG_W*IMG_H*0.05//2)):
    noisy[random.randint(0,255)][random.randint(0,255)] = 0

Image.fromarray(noisy).save("noisy_preview.png")

# Write pure hex — NO header, just values
with open("noisy_image.mem", "w") as f:
    for val in noisy.flatten():
        f.write(f"{val:02X}\n")

print("Saved noisy_image.mem")