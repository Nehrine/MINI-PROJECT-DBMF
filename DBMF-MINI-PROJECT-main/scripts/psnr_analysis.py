# psnr_analysis.py
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd

IMG_W, IMG_H = 256, 256

# ---- Load original clean image ----
original = np.array(
    Image.open("C:/DBMF/standard_test_images/lena.tif")
    .convert('L')
    .resize((IMG_W, IMG_H)),
    dtype=np.float64
)

# ---- Load your FPGA filtered output ----
df = pd.read_csv("C:/DBMF/ila_output.csv")
raw = df['pix_out[7:0]'].values[1:]  # skip radix row
pixels = np.array([int(str(v), 16) for v in raw], dtype=np.uint8)
filtered = pixels[:IMG_W*IMG_H].reshape(IMG_H, IMG_W).astype(np.float64)

# ---- PSNR Function ----
def calculate_psnr(original, processed):
    mse = np.mean((original - processed) ** 2)
    if mse == 0:
        return float('inf')
    psnr = 10 * np.log10((255.0 ** 2) / mse)
    return round(psnr, 2)

# ---- Generate noisy images at different densities ----
noise_levels = [10, 20, 30, 40, 50]
results = []

for noise_pct in noise_levels:
    noisy = original.copy().astype(np.uint8)
    total = IMG_W * IMG_H
    num_noise = int(total * noise_pct / 100)

    import random
    noisy_arr = original.copy().astype(np.uint8)
    pixels_list = [(r,c) for r in range(IMG_H) for c in range(IMG_W)]
    random.shuffle(pixels_list)
    for i in range(num_noise//2):
        r,c = pixels_list[i]
        noisy_arr[r][c] = 255
    for i in range(num_noise//2, num_noise):
        r,c = pixels_list[i]
        noisy_arr[r][c] = 0

    psnr_noisy    = calculate_psnr(original, noisy_arr.astype(np.float64))
    psnr_filtered = calculate_psnr(original, filtered)

    results.append({
        'Noise Density (%)': noise_pct,
        'PSNR Noisy (dB)':    psnr_noisy,
        'PSNR Filtered (dB)': psnr_filtered
    })

    print(f"Noise {noise_pct}%: Noisy PSNR={psnr_noisy} dB | Filtered PSNR={psnr_filtered} dB")

# ---- Print Table ----
print("\n--- PSNR Results Table ---")
print(f"{'Noise %':<12} {'Noisy PSNR':<15} {'Filtered PSNR'}")
print("-" * 40)
for r in results:
    print(f"{r['Noise Density (%)']:<12} {r['PSNR Noisy (dB)']:<15} {r['PSNR Filtered (dB)']}")

# ---- Plot PSNR vs Noise Density ----
noise_vals    = [r['Noise Density (%)']    for r in results]
psnr_noisy    = [r['PSNR Noisy (dB)']     for r in results]
psnr_filtered = [r['PSNR Filtered (dB)']  for r in results]

plt.figure(figsize=(8, 5))
plt.plot(noise_vals, psnr_noisy,    'r-o', label='Noisy Image')
plt.plot(noise_vals, psnr_filtered, 'g-o', label='FPGA Filtered (DBMF)')
plt.xlabel('Noise Density (%)')
plt.ylabel('PSNR (dB)')
plt.title('PSNR vs Noise Density — FPGA Median Filter')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("C:/DBMF/psnr_graph.png")
plt.show()
print("Saved psnr_graph.png")

# ---- Visual Comparison Table (like the paper) ----
fig, axes = plt.subplots(len(noise_levels), 3,
                          figsize=(10, 4*len(noise_levels)))
fig.suptitle('Noise Removal Results at Different Noise Densities',
             fontsize=14, fontweight='bold')

for idx, noise_pct in enumerate(noise_levels):
    # Generate noisy version
    noisy_arr = original.copy().astype(np.uint8)
    total = IMG_W * IMG_H
    num_noise = int(total * noise_pct / 100)
    import random
    pixels_list = [(r,c) for r in range(IMG_H) for c in range(IMG_W)]
    random.shuffle(pixels_list)
    for i in range(num_noise//2):
        r,c = pixels_list[i]
        noisy_arr[r][c] = 255
    for i in range(num_noise//2, num_noise):
        r,c = pixels_list[i]
        noisy_arr[r][c] = 0

    axes[idx][0].imshow(original.astype(np.uint8), cmap='gray')
    axes[idx][0].set_title(f'Original')
    axes[idx][0].axis('off')

    axes[idx][1].imshow(noisy_arr, cmap='gray')
    axes[idx][1].set_title(f'Noisy {noise_pct}%')
    axes[idx][1].axis('off')

    axes[idx][2].imshow(filtered.astype(np.uint8), cmap='gray')
    axes[idx][2].set_title(f'FPGA Filtered\nPSNR={calculate_psnr(original, filtered)} dB')
    axes[idx][2].axis('off')

plt.tight_layout()
plt.savefig("C:/DBMF/comparison_table.png")
plt.show()
print("Saved comparison_table.png")