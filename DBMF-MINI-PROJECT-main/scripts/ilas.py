import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

IMG_W, IMG_H = 256, 256

df = pd.read_csv("C:\DBMF\ila_output.csv")

# Print ALL columns so we can see what's there
print("ALL COLUMNS:")
for i, col in enumerate(df.columns.tolist()):
    print(f"  [{i}] {col}")

# Print first 20 values of each column
for col in df.columns:
    vals = df[col].values[:20]
    print(f"\n{col}: {vals}")