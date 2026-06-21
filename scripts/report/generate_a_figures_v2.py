# -*- coding: utf-8 -*-
"""
A类图表优化版（v2）
修正内容：字体、样本量标注、图5-6增加噪声折线子图
"""

import sys, os, glob
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from pathlib import Path

# 字体设置：删除旧缓存，重新加载
for f in glob.glob(os.path.join(matplotlib.get_cachedir(), 'fontlist-*.json')):
    try:
        os.remove(f)
    except Exception:
        pass
fm.fontManager.__init__()

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300

BASE = Path(__file__).resolve().parent.parent.parent
OUT = BASE / '素材' / '截图'
OUT.mkdir(parents=True, exist_ok=True)


def load_csv(name):
    path = BASE / '素材' / '实验数据' / f'results_{name}.csv'
    return pd.read_csv(path) if path.exists() else None


# ============================================================
# 图5-4: 航空图vs卫星图定位效果对比
# ============================================================
def generate_fig5_4():
    print("生成图5-4...")
    df_high = load_csv('HIGH')
    df_low = load_csv('LOW')
    if df_high is None or df_low is None:
        print("  跳过：CSV不存在")
        return

    fig, axes = plt.subplots(2, 3, figsize=(14, 8))

    thresholds = np.arange(0, 51, 1)

    # 第一行：航空图
    errors_h = df_high['pred_error'].clip(upper=50)
    axes[0, 0].hist(errors_h, bins=30, color='steelblue', edgecolor='black', alpha=0.8)
    axes[0, 0].axvline(x=5, color='red', linestyle='--', label='5m阈值')
    axes[0, 0].set_xlabel('定位误差 (m)')
    axes[0, 0].set_ylabel('样本数')
    axes[0, 0].set_title('航空图 — 误差分布')
    axes[0, 0].legend()

    acc_h = [(df_high['pred_error'] < t).mean() * 100 for t in thresholds]
    axes[0, 1].plot(thresholds, acc_h, 'b-', linewidth=2)
    axes[0, 1].axhline(y=82.3, color='r', linestyle='--', alpha=0.5, label='A@5m=82.3%')
    axes[0, 1].set_xlabel('误差阈值 (m)')
    axes[0, 1].set_ylabel('定位成功率 (%)')
    axes[0, 1].set_title('航空图 — A@T曲线')
    axes[0, 1].legend()
    axes[0, 1].set_xlim(0, 50)
    axes[0, 1].set_ylim(0, 100)

    scenes_h = df_high.groupby('scene')['pred_error'].apply(lambda x: (x < 5).mean() * 100)
    colors = ['#2ecc71', '#3498db', '#e74c3c']
    axes[0, 2].bar(range(len(scenes_h)), scenes_h.values, color=colors)
    axes[0, 2].set_xticks(range(len(scenes_h)))
    axes[0, 2].set_xticklabels(scenes_h.index, fontsize=8, rotation=10)
    axes[0, 2].set_ylabel('A@5m (%)')
    axes[0, 2].set_title('航空图 — 分场景A@5m')
    axes[0, 2].set_ylim(0, 105)
    for i, v in enumerate(scenes_h.values):
        n = len(df_high[df_high['scene'] == scenes_h.index[i]])
        axes[0, 2].text(i, v + 1, f'{v:.1f}%\n(n={n})', ha='center', fontsize=8)

    # 第二行：卫星图
    errors_l = df_low['pred_error'].clip(upper=200)
    axes[1, 0].hist(errors_l, bins=30, color='coral', edgecolor='black', alpha=0.8)
    axes[1, 0].axvline(x=5, color='red', linestyle='--', label='5m阈值')
    axes[1, 0].set_xlabel('定位误差 (m)')
    axes[1, 0].set_ylabel('样本数')
    axes[1, 0].set_title('卫星图 — 误差分布')
    axes[1, 0].legend()

    acc_l = [(df_low['pred_error'] < t).mean() * 100 for t in thresholds]
    axes[1, 1].plot(thresholds, acc_l, 'r-', linewidth=2)
    axes[1, 1].axhline(y=13.6, color='b', linestyle='--', alpha=0.5, label='A@5m=13.6%')
    axes[1, 1].set_xlabel('误差阈值 (m)')
    axes[1, 1].set_ylabel('定位成功率 (%)')
    axes[1, 1].set_title('卫星图 — A@T曲线')
    axes[1, 1].legend()
    axes[1, 1].set_xlim(0, 50)
    axes[1, 1].set_ylim(0, 100)

    scenes_l = df_low.groupby('scene')['pred_error'].apply(lambda x: (x < 5).mean() * 100)
    axes[1, 2].bar(range(len(scenes_l)), scenes_l.values, color=colors)
    axes[1, 2].set_xticks(range(len(scenes_l)))
    axes[1, 2].set_xticklabels(scenes_l.index, fontsize=8, rotation=10)
    axes[1, 2].set_ylabel('A@5m (%)')
    axes[1, 2].set_title('卫星图 — 分场景A@5m')
    axes[1, 2].set_ylim(0, 105)
    for i, v in enumerate(scenes_l.values):
        n = len(df_low[df_low['scene'] == scenes_l.index[i]])
        axes[1, 2].text(i, v + 1, f'{v:.1f}%\n(n={n})', ha='center', fontsize=8)

    plt.suptitle('图5-4 航空图与卫星图定位效果对比', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(OUT / 'fig5_4_high_vs_low.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  已保存")


# ============================================================
# 图5-5: 高度/视角分组分析（带样本量标注+边界说明）
# ============================================================
def generate_fig5_5():
    print("生成图5-5...")
    df = load_csv('HIGH')
    if df is None:
        print("  跳过")
        return

    fig, axes = plt.subplots(1, 3, figsize=(15, 5.5))

    # ① 俯仰角分组
    df['pitch_abs'] = df['pitch'].abs()
    pitch_bins = [20, 50, 70, 90]
    pitch_labels = ['20°-50°\n(倾斜)', '50°-70°\n(过渡)', '70°-90°\n(正下视)']
    df['pitch_group'] = pd.cut(df['pitch_abs'], bins=pitch_bins, labels=pitch_labels, include_lowest=True)
    pitch_stats = df.groupby('pitch_group', observed=True).agg(
        a5m=('pred_error', lambda x: (x < 5).mean() * 100),
        count=('pred_error', 'size')
    )
    bar_colors = ['#e74c3c', '#f39c12', '#2ecc71']
    bars = axes[0].bar(range(len(pitch_stats)), pitch_stats['a5m'], color=bar_colors)
    axes[0].set_xticks(range(len(pitch_stats)))
    axes[0].set_xticklabels(pitch_stats.index, fontsize=9)
    axes[0].set_ylabel('A@5m (%)')
    axes[0].set_title('俯仰角分组')
    axes[0].set_ylim(0, 105)
    for i, (v, n) in enumerate(zip(pitch_stats['a5m'], pitch_stats['count'])):
        label = f'{v:.1f}%\n(n={n})'
        if n < 30:
            label += '\n*样本量有限'
        axes[0].text(i, v + 1, label, ha='center', fontsize=7)

    # ② 高度分组
    alt_bins = [0, 100, 200, 300]
    alt_labels = ['30-100m', '100-200m', '200-300m']
    df['alt_group'] = pd.cut(df['altitude'], bins=alt_bins, labels=alt_labels, include_lowest=True)
    alt_stats = df.groupby('alt_group', observed=True).agg(
        a5m=('pred_error', lambda x: (x < 5).mean() * 100),
        count=('pred_error', 'size')
    )
    bar_colors2 = ['#3498db', '#9b59b6', '#95a5a6']
    bars = axes[1].bar(range(len(alt_stats)), alt_stats['a5m'], color=bar_colors2[:len(alt_stats)])
    axes[1].set_xticks(range(len(alt_stats)))
    axes[1].set_xticklabels(alt_stats.index, fontsize=9)
    axes[1].set_ylabel('A@5m (%)')
    axes[1].set_title('飞行高度分组')
    axes[1].set_ylim(0, 105)
    for i, (v, n) in enumerate(zip(alt_stats['a5m'], alt_stats['count'])):
        label = f'{v:.1f}%\n(n={n})' if n > 0 else '无样本'
        axes[1].text(i, v + 1 if n > 0 else 2, label, ha='center', fontsize=7)
    # 添加200-300m无样本说明
    axes[1].text(2, 50, 'Demo子集\n高度33-193m\n无>200m样本', ha='center', fontsize=7,
                 style='italic', color='gray',
                 bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # ③ 场景分组
    scene_stats = df.groupby('scene').agg(
        a5m=('pred_error', lambda x: (x < 5).mean() * 100),
        count=('pred_error', 'size')
    )
    bar_colors3 = ['#2ecc71', '#3498db', '#e74c3c']
    bars = axes[2].bar(range(len(scene_stats)), scene_stats['a5m'], color=bar_colors3)
    axes[2].set_xticks(range(len(scene_stats)))
    axes[2].set_xticklabels(scene_stats.index, fontsize=8, rotation=15)
    axes[2].set_ylabel('A@5m (%)')
    axes[2].set_title('测试场景分组')
    axes[2].set_ylim(0, 105)
    for i, (v, n) in enumerate(zip(scene_stats['a5m'], scene_stats['count'])):
        axes[2].text(i, v + 1, f'{v:.1f}%\n(n={n})', ha='center', fontsize=7)

    plt.suptitle('图5-5 不同高度与视角条件下定位效果分析', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(OUT / 'fig5_5_height_pitch_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  已保存")


# ============================================================
# 图5-6: 策略/匹配/噪声对比分析（3子图）
# ============================================================
def generate_fig5_6():
    print("生成图5-6...")
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # ① 策略对比
    strategies = ['Top N\nRe-rank', 'Top1', 'Most\nInliers']
    a5m = [82.3, 68.8, 79.5]
    a10m = [90.3, 78.2, 86.2]
    a20m = [95.9, 81.9, 87.3]
    x = np.arange(len(strategies))
    w = 0.25
    axes[0].bar(x - w, a5m, w, label='A@5m', color='#2ecc71')
    axes[0].bar(x, a10m, w, label='A@10m', color='#3498db')
    axes[0].bar(x + w, a20m, w, label='A@20m', color='#9b59b6')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(strategies, fontsize=9)
    axes[0].set_ylabel('定位成功率 (%)')
    axes[0].set_title('(a) 定位策略对比')
    axes[0].legend(fontsize=8)
    axes[0].set_ylim(0, 105)
    for i, (v5, v10, v20) in enumerate(zip(a5m, a10m, a20m)):
        axes[0].text(i - w, v5 + 1, f'{v5}', ha='center', fontsize=7)
        axes[0].text(i, v10 + 1, f'{v10}', ha='center', fontsize=7)
        axes[0].text(i + w, v20 + 1, f'{v20}', ha='center', fontsize=7)

    # ② 匹配方法对比
    methods = ['RoMa\n(密集/学习)', 'SIFT\n(稀疏/手工)']
    m_a5m = [82.3, 31.2]
    m_a10m = [90.3, 35.9]
    m_a20m = [95.9, 39.2]
    x2 = np.arange(len(methods))
    axes[1].bar(x2 - w, m_a5m, w, label='A@5m', color='#2ecc71')
    axes[1].bar(x2, m_a10m, w, label='A@10m', color='#3498db')
    axes[1].bar(x2 + w, m_a20m, w, label='A@20m', color='#9b59b6')
    axes[1].set_xticks(x2)
    axes[1].set_xticklabels(methods, fontsize=9)
    axes[1].set_ylabel('定位成功率 (%)')
    axes[1].set_title('(b) 匹配方法对比')
    axes[1].legend(fontsize=8)
    axes[1].set_ylim(0, 105)
    for i, (v5, v10, v20) in enumerate(zip(m_a5m, m_a10m, m_a20m)):
        axes[1].text(i - w, v5 + 1, f'{v5}', ha='center', fontsize=7)
        axes[1].text(i, v10 + 1, f'{v10}', ha='center', fontsize=7)
        axes[1].text(i + w, v20 + 1, f'{v20}', ha='center', fontsize=7)

    # ③ 先验噪声影响（论文数据）
    yaw_std = [0, 5, 10, 20, 30, 50, 60]
    yaw_a5m = [74.6, 74.3, 72.7, 72.4, 70.5, 60.9, 48.9]
    pitch_std = [0, 3, 5, 7, 10, 20, 30]
    pitch_a5m = [74.6, 73.9, 73.9, 73.3, 72.1, 71.6, 69.7]
    axes[2].plot(yaw_std, yaw_a5m, 'bo-', linewidth=2, markersize=6, label='Yaw噪声')
    axes[2].plot(pitch_std, pitch_a5m, 'rs--', linewidth=2, markersize=6, label='Pitch噪声')
    axes[2].set_xlabel('先验噪声标准差 (°)')
    axes[2].set_ylabel('A@5m (%)')
    axes[2].set_title('(c) 先验噪声影响\n(来源: AnyVisLoc论文Table 7)')
    axes[2].legend(fontsize=8)
    axes[2].set_xlim(-2, 65)
    axes[2].set_ylim(40, 80)
    axes[2].grid(True, alpha=0.3)
    # 标注关键阈值
    axes[2].axvline(x=10, color='gray', linestyle=':', alpha=0.5)
    axes[2].text(12, 75, 'Yaw>10°\n显著退化', fontsize=7, color='gray')

    plt.suptitle('图5-6 定位策略、匹配方法与先验噪声对比分析', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(OUT / 'fig5_6_strategy_matching.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  已保存")


if __name__ == '__main__':
    print("=" * 50)
    print("A类图表优化（v2）")
    print("=" * 50)
    generate_fig5_4()
    generate_fig5_5()
    generate_fig5_6()
    print("完成")
