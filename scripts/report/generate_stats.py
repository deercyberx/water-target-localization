# -*- coding: utf-8 -*-
"""
从CSV生成聚合统计和图表
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'STSong']
matplotlib.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = '素材/截图'
DATA_DIR = '素材/实验数据'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_csv(filename):
    filepath = f'{DATA_DIR}/{filename}'
    with open(filepath, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def compute_stats(errors, thresholds=[5, 10, 20]):
    """计算统计指标"""
    n = len(errors)
    result = {
        'count': n,
        'mean': np.mean(errors),
        'median': np.median(errors),
        'std': np.std(errors),
    }
    for t in thresholds:
        result[f'a{t}m'] = sum(1 for e in errors if e < t) / n * 100
    return result

def generate_all_stats():
    """生成所有统计数据"""

    print('=' * 60)
    print('生成聚合统计')
    print('=' * 60)

    # 1. HIGH 航空图
    print('\n--- HIGH 航空图 ---')
    rows = load_csv('results_HIGH.csv')
    errors = [float(r['pred_error']) for r in rows]
    stats = compute_stats(errors)
    print(f'N={stats["count"]}, A@5m={stats["a5m"]:.1f}%, A@10m={stats["a10m"]:.1f}%, A@20m={stats["a20m"]:.1f}%')
    print(f'平均={stats["mean"]:.2f}m, 中位数={stats["median"]:.2f}m')

    # 分场景
    scenes = {}
    for r in rows:
        s = r['scene']
        if s not in scenes:
            scenes[s] = []
        scenes[s].append(float(r['pred_error']))

    print('\n分场景:')
    for scene, errs in sorted(scenes.items()):
        s = compute_stats(errs)
        print(f'  {scene}: N={s["count"]}, A@5m={s["a5m"]:.1f}%, 平均={s["mean"]:.2f}m, 中位数={s["median"]:.2f}m')

    # 2. LOW 卫星图
    print('\n--- LOW 卫星图 ---')
    rows = load_csv('results_LOW.csv')
    errors = [float(r['pred_error']) for r in rows]
    stats = compute_stats(errors)
    print(f'N={stats["count"]}, A@5m={stats["a5m"]:.1f}%, A@10m={stats["a10m"]:.1f}%, A@20m={stats["a20m"]:.1f}%')
    print(f'平均={stats["mean"]:.2f}m, 中位数={stats["median"]:.2f}m')

    # 3. 策略对比
    print('\n--- 策略对比 ---')
    for fname, label in [('results_HIGH.csv', 'TopN'), ('results_Top1.csv', 'Top1'), ('results_MostInliers.csv', 'MostInliers')]:
        rows = load_csv(fname)
        errors = [float(r['pred_error']) for r in rows]
        stats = compute_stats(errors)
        print(f'{label}: A@5m={stats["a5m"]:.1f}%, A@10m={stats["a10m"]:.1f}%, A@20m={stats["a20m"]:.1f}%')

    # 4. SIFT
    print('\n--- SIFT 匹配方法 ---')
    rows = load_csv('results_SIFT.csv')
    errors = [float(r['pred_error']) for r in rows]
    stats = compute_stats(errors)
    print(f'N={stats["count"]}, A@5m={stats["a5m"]:.1f}%, A@10m={stats["a10m"]:.1f}%, A@20m={stats["a20m"]:.1f}%')
    print(f'平均={stats["mean"]:.2f}m, 中位数={stats["median"]:.2f}m')

    # 5. 俯仰角分析
    print('\n--- 俯仰角分析 ---')
    rows = load_csv('results_HIGH.csv')
    pitch_bins = {
        '20-50°': (-50, -20),
        '50-70°': (-70, -50),
        '70-90°': (-90, -70),
    }
    for label, (low, high) in pitch_bins.items():
        errs = [float(r['pred_error']) for r in rows if low <= float(r['pitch']) < high]
        if errs:
            s = compute_stats(errs)
            print(f'{label}: N={s["count"]}, A@5m={s["a5m"]:.1f}%, 平均={s["mean"]:.2f}m')

    # 6. 高度分桶
    print('\n--- 高度分桶 ---')
    alt_bins = {
        '30-100m': (30, 100),
        '100-200m': (100, 200),
        '200-300m': (200, 300),
    }
    for label, (low, high) in alt_bins.items():
        errs = [float(r['pred_error']) for r in rows if low <= float(r['altitude']) < high]
        if errs:
            s = compute_stats(errs)
            print(f'{label}: N={s["count"]}, A@5m={s["a5m"]:.1f}%, 平均={s["mean"]:.2f}m')

if __name__ == '__main__':
    generate_all_stats()
