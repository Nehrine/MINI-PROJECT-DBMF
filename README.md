# MINI-PROJECT-DBMF

Decision-Based Median Filter (DBMF) for salt-and-pepper noise removal, implemented in Verilog on a PYNQ-Z2 board (Zynq `xc7z020clg400-1`, Vivado 2025.1). A 256×256 grayscale image is loaded into block RAM, filtered in hardware, and the output is captured with an ILA and rebuilt into an image in Python.

## Repository layout

| Path | Contents |
|------|----------|
| `vivado/project_1/` | Vivado project (`project_1.xpr`), Verilog sources, constraints and ILA IP config |
| `vivado/bitstream/` | `top.bit` bitstream and `top.ltx` ILA probe file |
| `vivado/reports/` | Timing, utilization and power reports |
| `scripts/` | Python scripts: noise generation, `.mem`/`.coe` generation, image reconstruction from ILA CSV, PSNR analysis |
| `data/` | Noisy image memory files (`.mem`) and ILA capture exports (`.csv`) |
| `results/` | Noisy/filtered images, comparisons and PSNR graphs |
| `test_images/` | Standard test images (lena, camera, lake, ...) |

### Hardware sources (`vivado/project_1/project_1.srcs/sources_1/new/`)

- `topp.v` – top module: input BRAM → median filter → output BRAM, ILA, status LEDs
- `median.v` – median filter core
- `braminput.v` / `bramoutput.v` – input and output block RAMs

## Flow

1. Generate a noisy image and memory file: `scripts/generate_noise1.py` (or `generate_hex1.py` / `generate_coe1.py`)
2. Synthesize, implement and program the board from Vivado (or program `vivado/bitstream/top.bit` directly)
3. Capture `pix_out` with the ILA and export to CSV
4. Rebuild the filtered image: `scripts/reconstruct1.py`
5. Compute PSNR: `scripts/psnr_analysis.py`, `scripts/psnr2.py`

> Note: scripts and `braminput.v` use absolute paths under `C:/DBMF/`. Update them to match your local checkout before running.
