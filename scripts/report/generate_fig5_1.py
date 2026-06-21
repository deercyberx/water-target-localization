# -*- coding: utf-8 -*-
"""
图5-1: 测试区域图像样例
3行(场景) x 3列(UAV查询图 / 航空参考图 / 卫星参考图)
"""

import sys, os, glob
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path

for f in glob.glob(os.path.join(matplotlib.get_cachedir(), 'fontlist-*.json')):
    try: os.remove(f)
    except: pass
fm.fontManager.__init__()
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300

BASE = Path(__file__).resolve().parent.parent.parent
CODE = BASE / 'code'
OUT = BASE / '素材' / '截图'

def imread_pil(path):
    try:
        return np.array(Image.open(path).convert('RGB'))
    except:
        return None

def center_crop(img, size=None):
    h, w = img.shape[:2]
    if size is None:
        size = min(h, w)
    cy, cx = h // 2, w // 2
    return img[cy-size//2:cy+size//2, cx-size//2:cx+size//2]

# 选定样例图像
samples = [
    ('QZ_SongCity', 'DJI_0532.JPG', 'QZ_SongCity (正下视)'),
    ('Qingzhou_3_2', 'DJI_0456.JPG', 'Qingzhou_3_2 (过渡视角)'),
    ('QingZhou_2024', 'DJI_20240917112155_0351_D.JPG', 'QingZhou_2024 (倾斜视角)'),
]

# 参考地图
ref_high = CODE / 'Data' / 'Reference_map' / 'QZ_Town' / 'result_roi.tif'
ref_low = CODE / 'Data' / 'Reference_map' / 'QZ_Town' / 'satellite_roi.tif'

fig, axes = plt.subplots(3, 3, figsize=(12, 11))

for row, (scene, fname, title) in enumerate(samples):
    # 列1: UAV查询图
    uav_path = CODE / 'Data' / 'UAV_image' / 'QZ_Town' / scene / fname
    uav_img = imread_pil(str(uav_path))
    if uav_img is not None:
        cropped = center_crop(uav_img, 1000)
        axes[row, 0].imshow(cropped)
    axes[row, 0].set_title(f'{title}' if row == 0 else '', fontsize=10)
    axes[row, 0].set_ylabel(fname, fontsize=8, rotation=0, labelpad=80, va='center')
    axes[row, 0].set_xticks([])
    axes[row, 0].set_yticks([])

    # 列2: 航空参考图
    if row == 0:
        ref_h_img = imread_pil(str(ref_high))
        if ref_h_img is not None:
            # 裁剪中间区域展示
            h, w = ref_h_img.shape[:2]
            crop_size = min(h, w) // 2
            cropped = center_crop(ref_h_img, crop_size)
            axes[row, 1].imshow(cropped)
        axes[row, 1].set_title('航空参考图\n(0.061m/pix)', fontsize=10)
    else:
        axes[row, 1].axis('off')

    # 列3: 卫星参考图
    if row == 0:
        ref_l_img = imread_pil(str(ref_low))
        if ref_l_img is not None:
            h, w = ref_l_img.shape[:2]
            crop_size = min(h, w) // 2
            cropped = center_crop(ref_l_img, crop_size)
            axes[row, 2].imshow(cropped)
        axes[row, 2].set_title('卫星参考图\n(0.260m/pix)', fontsize=10)
    else:
        axes[row, 2].axis('off')

# 列2/3只在第一行显示参考图
for row in range(1, 3):
    axes[row, 1].axis('off')
    axes[row, 2].axis('off')

# 补充：在第2-3行的列2/3放不同场景的UAV图
for row, (scene, fname, title) in enumerate(samples):
    if row > 0:
        uav_path = CODE / 'Data' / 'UAV_image' / 'QZ_Town' / scene / fname
        uav_img = imread_pil(str(uav_path))
        if uav_img is not None:
            cropped = center_crop(uav_img, 1000)
            axes[row, 1].imshow(cropped)
            axes[row, 1].set_title(title, fontsize=10)
            axes[row, 1].set_xticks([])
            axes[row, 1].set_yticks([])

plt.suptitle('图5-1 测试区域图像样例', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(OUT / 'fig5_1_sample_images.png', dpi=300, bbox_inches='tight')
plt.close()
print("图5-1 已保存")
