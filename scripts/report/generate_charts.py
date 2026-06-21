# -*- coding: utf-8 -*-
"""
生成实验图表（素材清单 G1-G5）
使用已有汇总数据，无需逐图CSV
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'STSong']
matplotlib.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = '素材/截图'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# 实验数据（来自 CONTEXT.md）
# ============================================================

# 航空图分场景结果
scene_data = {
    'QZ_SongCity': {'count': 286, 'mean_error': 1.73, 'a5m': 98.3, 'a10m': 100.0, 'a20m': 100.0},
    'Qingzhou_3_2': {'count': 59, 'mean_error': 3.04, 'a5m': 96.6, 'a10m': 100.0, 'a20m': 100.0},
    'QingZhou_2024': {'count': 142, 'mean_error': 91.75, 'a5m': 44.4, 'a10m': 66.9, 'a20m': 85.9},
}

# 定位策略对比
strategy_data = {
    'Top-N Re-rank': {'a5m': 82.3, 'a10m': 90.3, 'a20m': 95.9, 'mean': 28.1, 'median': 2.39},
    'Top-1': {'a5m': 68.8, 'a10m': 78.2, 'a20m': 81.9, 'mean': 39.7, 'median': 2.71},
    'Most Inliers': {'a5m': 79.5, 'a10m': 86.2, 'a20m': 87.3, 'mean': 81.2, 'median': 2.29},
}

# 俯仰角分析
pitch_data = {
    '20°-50°\n(倾斜)': {'count': 301, 'a5m': 79.4, 'a10m': 88.4, 'a20m': 96.7, 'mean': 35.5, 'median': 2.1},
    '50°-70°\n(过渡)': {'count': 22, 'a5m': 63.6, 'a10m': 86.4, 'a20m': 90.9, 'mean': 17.8, 'median': 4.0},
    '70°-90°\n(正下视)': {'count': 103, 'a5m': 89.3, 'a10m': 95.1, 'a20m': 96.1, 'mean': 11.7, 'median': 2.5},
}

# 匹配方法对比
matching_data = {
    'RoMa\n(密集/学习)': {'a5m': 82.3, 'a10m': 90.3, 'a20m': 95.9, 'mean': 28.1},
    'SIFT\n(稀疏/手工)': {'a5m': 32.5, 'a10m': 37.5, 'a20m': 40.9, 'mean': 125.3},
}

# 参考图对比
ref_map_data = {
    '航空图': {'a5m': 82.3, 'a10m': 90.3, 'a20m': 95.9, 'dsm_res': 0.937, 'img_res': 0.061},
    '卫星图': {'a5m': 13.6, 'a10m': 39.4, 'a20m': 63.7, 'dsm_res': 30.0, 'img_res': 0.260},
}

# 论文对照数据
paper_data = {
    '航空图': {'a5m': 74.1, 'a10m': 87.7, 'a20m': 94.2},
    '卫星图': {'a5m': 18.5, 'a10m': 38.7, 'a20m': 58.5},
}

# ============================================================
# G3: 策略对比柱状图
# ============================================================
def plot_strategy_comparison():
    print('[G3] 生成策略对比柱状图')
    fig, ax = plt.subplots(figsize=(10, 6))

    strategies = list(strategy_data.keys())
    a5m = [strategy_data[s]['a5m'] for s in strategies]
    a10m = [strategy_data[s]['a10m'] for s in strategies]
    a20m = [strategy_data[s]['a20m'] for s in strategies]

    x = np.arange(len(strategies))
    width = 0.25

    bars1 = ax.bar(x - width, a5m, width, label='A@5m', color='#2ecc71')
    bars2 = ax.bar(x, a10m, width, label='A@10m', color='#3498db')
    bars3 = ax.bar(x + width, a20m, width, label='A@20m', color='#e74c3c')

    ax.set_ylabel('定位精度 (%)', fontsize=12)
    ax.set_title('不同定位策略的精度对比', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(strategies, fontsize=11)
    ax.legend(fontsize=11)
    ax.set_ylim(0, 105)
    ax.grid(axis='y', alpha=0.3)

    # 添加数值标签
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3), textcoords="offset points",
                       ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/strategy_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  保存: {OUTPUT_DIR}/strategy_comparison.png')

# ============================================================
# G4: 俯仰角影响曲线
# ============================================================
def plot_pitch_impact():
    print('[G4] 生成俯仰角影响曲线')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    pitches = list(pitch_data.keys())
    a5m = [pitch_data[p]['a5m'] for p in pitches]
    counts = [pitch_data[p]['count'] for p in pitches]

    # 左图: A@5m 柱状图
    colors = ['#e74c3c', '#f39c12', '#2ecc71']
    bars = ax1.bar(pitches, a5m, color=colors, edgecolor='black', linewidth=0.5)
    ax1.set_ylabel('A@5m (%)', fontsize=12)
    ax1.set_title('俯仰角对定位精度的影响', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, 100)
    ax1.grid(axis='y', alpha=0.3)

    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax1.annotate(f'{height:.1f}%\n(n={count})',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)

    # 右图: 样本分布饼图
    ax2.pie(counts, labels=pitches, autopct='%1.1f%%', colors=colors, startangle=90)
    ax2.set_title('俯仰角样本分布', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/pitch_impact.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  保存: {OUTPUT_DIR}/pitch_impact.png')

# ============================================================
# G5: 分场景对比图
# ============================================================
def plot_scene_comparison():
    print('[G5] 生成分场景对比图')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    scenes = list(scene_data.keys())
    scene_labels = ['QZ_SongCity\n(286张)', 'Qingzhou_3_2\n(59张)', 'QingZhou_2024\n(142张)']
    a5m = [scene_data[s]['a5m'] for s in scenes]
    mean_err = [scene_data[s]['mean_error'] for s in scenes]

    # 左图: A@5m 柱状图
    colors = ['#2ecc71', '#3498db', '#e74c3c']
    bars = ax1.bar(scene_labels, a5m, color=colors, edgecolor='black', linewidth=0.5)
    ax1.set_ylabel('A@5m (%)', fontsize=12)
    ax1.set_title('分场景定位精度 (航空图)', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, 110)
    ax1.grid(axis='y', alpha=0.3)

    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'{height:.1f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11)

    # 右图: 平均误差柱状图 (对数刻度)
    bars2 = ax2.bar(scene_labels, mean_err, color=colors, edgecolor='black', linewidth=0.5)
    ax2.set_ylabel('平均误差 (m)', fontsize=12)
    ax2.set_title('分场景平均定位误差', fontsize=14, fontweight='bold')
    ax2.set_yscale('log')
    ax2.grid(axis='y', alpha=0.3)

    for bar in bars2:
        height = bar.get_height()
        ax2.annotate(f'{height:.1f}m',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/scene_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  保存: {OUTPUT_DIR}/scene_comparison.png')

# ============================================================
# 匹配方法对比图
# ============================================================
def plot_matching_comparison():
    print('[补充] 生成匹配方法对比图')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    methods = list(matching_data.keys())
    a5m = [matching_data[m]['a5m'] for m in methods]
    mean_err = [matching_data[m]['mean'] for m in methods]

    # 左图: A@5m
    colors = ['#2ecc71', '#e74c3c']
    bars = ax1.bar(methods, a5m, color=colors, edgecolor='black', linewidth=0.5)
    ax1.set_ylabel('A@5m (%)', fontsize=12)
    ax1.set_title('匹配方法精度对比', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, 100)
    ax1.grid(axis='y', alpha=0.3)

    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'{height:.1f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=12)

    # 右图: 平均误差
    bars2 = ax2.bar(methods, mean_err, color=colors, edgecolor='black', linewidth=0.5)
    ax2.set_ylabel('平均误差 (m)', fontsize=12)
    ax2.set_title('匹配方法平均误差', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)

    for bar in bars2:
        height = bar.get_height()
        ax2.annotate(f'{height:.1f}m',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=12)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/matching_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  保存: {OUTPUT_DIR}/matching_comparison.png')

# ============================================================
# 参考图对比图
# ============================================================
def plot_ref_map_comparison():
    print('[补充] 生成参考图对比图')
    fig, ax = plt.subplots(figsize=(10, 6))

    maps = list(ref_map_data.keys())
    a5m_ours = [ref_map_data[m]['a5m'] for m in maps]
    a5m_paper = [paper_data[m]['a5m'] for m in maps]

    x = np.arange(len(maps))
    width = 0.35

    bars1 = ax.bar(x - width/2, a5m_ours, width, label='复现结果', color='#3498db')
    bars2 = ax.bar(x + width/2, a5m_paper, width, label='论文结果', color='#e74c3c')

    ax.set_ylabel('A@5m (%)', fontsize=12)
    ax.set_title('不同参考地图的定位精度对比', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(maps, fontsize=12)
    ax.legend(fontsize=11)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)

    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}%',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 5), textcoords="offset points",
                       ha='center', va='bottom', fontsize=11)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/ref_map_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  保存: {OUTPUT_DIR}/ref_map_comparison.png')

# ============================================================
# 综合对比图（论文 vs 复现）
# ============================================================
def plot_overall_comparison():
    print('[补充] 生成综合对比图')
    fig, ax = plt.subplots(figsize=(10, 6))

    metrics = ['A@5m', 'A@10m', 'A@20m']
    ours_aerial = [82.3, 90.3, 95.9]
    paper_aerial = [74.1, 87.7, 94.2]
    ours_satellite = [13.6, 39.4, 63.7]
    paper_satellite = [18.5, 38.7, 58.5]

    x = np.arange(len(metrics))
    width = 0.2

    bars1 = ax.bar(x - 1.5*width, ours_aerial, width, label='复现-航空图', color='#2ecc71')
    bars2 = ax.bar(x - 0.5*width, paper_aerial, width, label='论文-航空图', color='#27ae60')
    bars3 = ax.bar(x + 0.5*width, ours_satellite, width, label='复现-卫星图', color='#3498db')
    bars4 = ax.bar(x + 1.5*width, paper_satellite, width, label='论文-卫星图', color='#2980b9')

    ax.set_ylabel('定位精度 (%)', fontsize=12)
    ax.set_title('复现结果 vs 论文结果', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=12)
    ax.legend(fontsize=10, ncol=2)
    ax.set_ylim(0, 105)
    ax.grid(axis='y', alpha=0.3)

    for bars in [bars1, bars2, bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3), textcoords="offset points",
                       ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/overall_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  保存: {OUTPUT_DIR}/overall_comparison.png')

# ============================================================
# 主函数
# ============================================================
def main():
    print('=' * 50)
    print('生成实验图表')
    print('=' * 50)

    plot_strategy_comparison()
    plot_pitch_impact()
    plot_scene_comparison()
    plot_matching_comparison()
    plot_ref_map_comparison()
    plot_overall_comparison()

    print('=' * 50)
    print('图表生成完成!')
    print(f'输出目录: {OUTPUT_DIR}/')
    print('=' * 50)

if __name__ == '__main__':
    main()
