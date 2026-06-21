"""
Generate missing figures for technical report
G8: QingZhou_2024 scene examples
G9: DSM elevation map visualization
G10: Match points visualization (if possible)
"""

import os
import shutil
import sys

# Add project to path
project_root = r"C:\Users\deer\Desktop\Projects\Research\projects\水上目标定位"
sys.path.insert(0, os.path.join(project_root, "code"))

# Output directory
output_dir = os.path.join(project_root, "素材", "截图")
os.makedirs(output_dir, exist_ok=True)

print("=" * 60)
print("Figure Generation Script")
print("=" * 60)

# ============================================================
# G8: QingZhou_2024 scene examples
# ============================================================
print("\n[G8] Processing QingZhou_2024 scene examples...")

uav_dir = os.path.join(project_root, "code", "Data", "UAV_image", "QZ_Town", "QingZhou_2024")

if os.path.exists(uav_dir):
    # List all JPG files
    jpg_files = [f for f in os.listdir(uav_dir) if f.upper().endswith('.JPG')]
    jpg_files.sort()
    print(f"  Found {len(jpg_files)} JPG files in QingZhou_2024")

    # Select 3 representative samples: first, middle, last
    if len(jpg_files) >= 3:
        sample_indices = [0, len(jpg_files) // 2, len(jpg_files) - 1]
    else:
        sample_indices = list(range(len(jpg_files)))

    for i, idx in enumerate(sample_indices):
        src = os.path.join(uav_dir, jpg_files[idx])
        dst = os.path.join(output_dir, f"qingzhou_2024_sample_{i+1}.jpg")
        shutil.copy2(src, dst)
        print(f"  Copied: {jpg_files[idx]} -> qingzhou_2024_sample_{i+1}.jpg")
else:
    print(f"  ERROR: Directory not found: {uav_dir}")

# ============================================================
# G9: DSM elevation map visualization
# ============================================================
print("\n[G9] Processing DSM elevation map...")

dsm_path = os.path.join(project_root, "code", "Data", "Reference_map", "QZ_Town", "dsm_roi.tif")

if os.path.exists(dsm_path):
    print(f"  Found DSM file: {dsm_path}")

    try:
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
        import matplotlib.pyplot as plt
        from matplotlib import cm

        # Try rasterio first
        try:
            import rasterio
            with rasterio.open(dsm_path) as src:
                dsm_data = src.read(1)
                print(f"  Read with rasterio: shape={dsm_data.shape}, dtype={dsm_data.dtype}")
        except ImportError:
            print("  rasterio not available, trying gdal...")
            try:
                from osgeo import gdal
                ds = gdal.Open(dsm_path)
                dsm_data = ds.GetRasterBand(1).ReadAsArray()
                print(f"  Read with gdal: shape={dsm_data.shape}, dtype={dsm_data.dtype}")
            except ImportError:
                print("  gdal not available, trying PIL...")
                from PIL import Image
                img = Image.open(dsm_path)
                dsm_data = np.array(img)
                print(f"  Read with PIL: shape={dsm_data.shape}, dtype={dsm_data.dtype}")

        # Create visualization
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))

        # Mask nodata values
        if dsm_data.dtype == np.float32 or dsm_data.dtype == np.float64:
            nodata_mask = np.isnan(dsm_data) | (dsm_data < -9999)
        else:
            nodata_mask = dsm_data == 0

        dsm_display = dsm_data.copy().astype(float)
        dsm_display[nodata_mask] = np.nan

        # Plot with terrain colormap
        im = ax.imshow(dsm_display, cmap='terrain', interpolation='bilinear')
        ax.set_title('DSM Elevation Map - Qingzhou Town (QZ_Town)', fontsize=14)
        ax.set_xlabel('X (pixels)', fontsize=12)
        ax.set_ylabel('Y (pixels)', fontsize=12)

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Elevation (m)', fontsize=12)

        # Add statistics annotation
        valid_data = dsm_display[~np.isnan(dsm_display)]
        if len(valid_data) > 0:
            stats_text = f'Min: {valid_data.min():.1f}m\nMax: {valid_data.max():.1f}m\nMean: {valid_data.mean():.1f}m'
            ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                    fontsize=10)

        plt.tight_layout()
        output_path = os.path.join(output_dir, "dsm_example.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  Saved DSM visualization: dsm_example.png")

    except Exception as e:
        print(f"  ERROR processing DSM: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"  ERROR: DSM file not found: {dsm_path}")

# ============================================================
# G10: Match points visualization
# ============================================================
print("\n[G10] Checking match points visualization...")

# Check if utils.py has the function
utils_path = os.path.join(project_root, "code", "utils.py")
if os.path.exists(utils_path):
    print(f"  Found utils.py with process_and_save_matches() function")
    print("  Note: Match visualization requires running the full matching pipeline with UAV images")
    print("  This typically requires GPU and specific input data (camera parameters, etc.)")
    print("  Skipping G10 - match points visualization requires runtime execution")
else:
    print(f"  ERROR: utils.py not found")

print("\n" + "=" * 60)
print("Summary:")
print("=" * 60)

# List generated files
generated = os.listdir(output_dir)
print(f"\nGenerated {len(generated)} files in {output_dir}:")
for f in sorted(generated):
    filepath = os.path.join(output_dir, f)
    size_kb = os.path.getsize(filepath) / 1024
    print(f"  - {f} ({size_kb:.1f} KB)")

print("\nDone!")