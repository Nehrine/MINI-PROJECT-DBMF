  # reconstruct.py
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

IMG_W, IMG_H = 256, 256

df = pd.read_csv('C:\DBMF\ila_output3.csv')
print("Columns:", df.columns.tolist())

# Get pix_out column — skip first row (radix header)
raw = df['pix_out[7:0]'].values[1:]

# Convert hex to int
pixels = np.array([int(str(v), 16) for v in raw], dtype=np.uint8)
pixels = pixels[:IMG_W * IMG_H]

filtered = pixels.reshape(IMG_H, IMG_W)
Image.fromarray(filtered).save("C:/DBMF/filtered_output3.png")

noisy = np.array(Image.open("C:/DBMF/noisy_preview3.png"))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.imshow(noisy,    cmap='gray'); ax1.set_title('Noisy Input')
ax2.imshow(filtered, cmap='gray'); ax2.set_title('FPGA Filtered Output (DBMF)')
plt.tight_layout()
plt.savefig("C:/DBMF/comparison3.png")
plt.show()
print("Done! filtered_output1.png saved")