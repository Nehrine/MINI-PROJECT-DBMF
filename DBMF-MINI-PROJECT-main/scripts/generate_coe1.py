# generate_coe.py
import numpy as np
from PIL import Image
import random

IMG_W, IMG_H = 256, 256
img = Image.open("C:\DBMF\standard_test_images\milkdrop.tif").convert('L').resize((IMG_W, IMG_H))
pixels = np.array(img, dtype=np.uint8)

noisy = pixels.copy()
for _ in range(int(IMG_W*IMG_H*0.05//2)):
    noisy[random.randint(0,255)][random.randint(0,255)] = 255
for _ in range(int(IMG_W*IMG_H*0.05//2)):
    noisy[random.randint(0,255)][random.randint(0,255)] = 0

Image.fromarray(noisy).save("C:/DBMF/noisy_preview.png")

with open("C:/DBMF/noisy_image.coe", "w") as f:
    f.write("memory_initialization_radix=16;\n")
    f.write("memory_initialization_vector=\n")
    flat = noisy.flatten()
    for i, val in enumerate(flat):
        sep = "," if i < len(flat)-1 else ";"
        f.write(f"{val:02X}{sep}\n")

print("Done — check C:/project_better/noisy_image.coe")