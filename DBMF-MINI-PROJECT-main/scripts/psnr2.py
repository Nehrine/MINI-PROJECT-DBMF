import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import random

IMG_W, IMG_H = 256, 256

# Load original
original = np.array(
    Image.open("C:/DBMF/standard_test_images/lena.tif")
    .convert('L').resize((IMG_W, IMG_H)),
    dtype=np.uint8
)

# Load FPGA filtered output from CSV
df = pd.read_csv("C:/DBMF/ila_output.csv")
raw = df['pix_out[7:0]'].values[1:]
fpga_filtered = np.array(
    [int(str(v),16) for v in raw],
    dtype=np.uint8
)[:IMG_W*IMG_H].reshape(IMG_H, IMG_W)

def psnr(orig, processed):
    mse = np.mean((orig.astype(np.float64) -
                   processed.astype(np.float64))**2)
    if mse == 0: return 100.0
    return round(10 * np.log10(255.0**2 / mse), 2)

def add_noise(img, pct):
    noisy = img.copy()
    total = IMG_W * IMG_H
    coords = [(r,c) for r in range(IMG_H) for c in range(IMG_W)]
    random.shuffle(coords)
    for i in range(int(total*pct/200)):
        noisy[coords[i][0]][coords[i][1]] = 255
    for i in range(int(total*pct/200), int(total*pct/100)):
        noisy[coords[i][0]][coords[i][1]] = 0
    return noisy

# Software median filter for comparison
from scipy.ndimage import median_filter as scipy_median

noise_levels = [10, 20, 30, 40, 50, 60, 70, 80]
results = []

print(f"{'Noise%':<10} {'Noisy PSNR':<15} {'SW Median':<15} {'FPGA DBMF'}")
print("-" * 55)

for n in noise_levels:
    noisy     = add_noise(original, n)
    sw_filt   = scipy_median(noisy, size=3)
    
    p_noisy   = psnr(original, noisy)
    p_sw      = psnr(original, sw_filt)
    p_fpga    = psnr(original, fpga_filtered)
    
    results.append({
        'noise': n,
        'noisy': p_noisy,
        'sw':    p_sw,
        'fpga':  p_fpga
    })
    print(f"{n:<10} {p_noisy:<15} {p_sw:<15} {p_fpga}")

# ---- Plot like paper Figure ----
fig, axes = plt.subplots(len(noise_levels), 3,
                          figsize=(12, 4*len(noise_levels)))
fig.suptitle('FPGA DBMF — Results at Various Noise Densities',
             fontsize=14, fontweight='bold')

for idx, r in enumerate(results):
    n = r['noise']
    noisy   = add_noise(original, n)
    sw_filt = scipy_median(noisy, size=3)

    axes[idx][0].imshow(noisy,        cmap='gray')
    axes[idx][0].set_ylabel(f'{n}% noise', fontsize=12)
    axes[idx][0].set_title('Noisy Image')
    axes[idx][0].axis('off')

    axes[idx][1].imshow(sw_filt,      cmap='gray')
    axes[idx][1].set_title(f'SW Median\nPSNR={psnr(original,sw_filt)} dB')
    axes[idx][1].axis('off')

    axes[idx][2].imshow(fpga_filtered, cmap='gray')
    axes[idx][2].set_title(f'FPGA DBMF\nPSNR={r["fpga"]} dB')
    axes[idx][2].axis('off')

plt.tight_layout()
plt.savefig("C:/DBMF/paper_figure.png", dpi=150)
plt.show()

# ---- PSNR Graph ----
plt.figure(figsize=(10, 6))
plt.plot([r['noise'] for r in results],
         [r['noisy'] for r in results], 'r-o', label='Noisy')
plt.plot([r['noise'] for r in results],
         [r['sw']    for r in results], 'b-o', label='SW Median')
plt.plot([r['noise'] for r in results],
         [r['fpga']  for r in results], 'g-o', label='FPGA DBMF')
plt.xlabel('Noise Density (%)')
plt.ylabel('PSNR (dB)')
plt.title('PSNR Comparison — FPGA DBMF vs Software Median')
plt.legend()
plt.grid(True)
plt.savefig("C:/DBMF/psnr_comparison.png", dpi=150)
plt.show()

print("\nFiles saved:")
print("  paper_figure.png    ← visual table like the paper")
print("  psnr_comparison.png ← PSNR graph")