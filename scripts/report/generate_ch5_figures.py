# -*- coding: utf-8 -*-
"""
生成第五章所有图表
- 图5-3: 完整流程可视化（查询→候选→匹配→PnP）
- 图5-4: 航空图vs卫星图对比可视化
- 图5-5: 高度/视角分组示意图
- 图5-6: 策略/匹配对比说明图
- 图5-8: 成功/失败案例可视化
- 表5-1~5-12: 所有表格数据
"""

import sys
import os
import pickle
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import cv2
from PIL import Image as PILImage
from pathlib import Path

def imread_pil(path):
    """用PIL读取图像（兼容中文路径），返回RGB numpy数组"""
    try:
        img = PILImage.open(path)
        return np.array(img.convert('RGB'))
    except Exception:
        return None

# 设置中文字体
import matplotlib.font_manager as fm
# 删除旧字体缓存并重新加载
import glob
for cache_file in glob.glob(os.path.join(matplotlib.get_cachedir(), 'fontlist-*.json')):
    try:
        os.remove(cache_file)
    except Exception:
        pass
fm.fontManager.__init__()

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'STSong', 'FangSong', 'KaiTi']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300

# 学术风全局字号（参考 AnyVisLoc CVPR 2026 论文图表）
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

# 轻量化边框
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.linewidth'] = 0.6

# 极浅 grid（几乎不可见）
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.linewidth'] = 0.3
plt.rcParams['grid.alpha'] = 0.2
plt.rcParams['grid.color'] = '#d0d0d0'
plt.rcParams['axes.axisbelow'] = True

# 学术风配色（参考论文 Figure 4/7 风格）
COLORS_GLOBAL = {
    'blue': '#5B9BD5', 'orange': '#ED7D31', 'green': '#70AD47',
    'red': '#C0504D', 'purple': '#7030A0', 'gray': '#A5A5A5',
    'teal': '#2E75B6', 'gold': '#BF8F00',
}
BAR_COLOR = COLORS_GLOBAL['blue']
PAIR_3_G = [COLORS_GLOBAL['blue'], COLORS_GLOBAL['orange'], COLORS_GLOBAL['green']]

BASE = Path(__file__).resolve().parent.parent.parent
CODE = BASE / 'code'
OUT = BASE / '素材' / '截图'
OUT.mkdir(parents=True, exist_ok=True)

# ============================================================
# 工具函数
# ============================================================

def load_pkl(scene, name):
    """加载pkl文件"""
    pkl_dir = CODE / 'Result' / 'Experiment1_HIGH' / 'QZ_Town' / f'pkl_{scene}' / 'resize_0.2' / 'HIGH-CAMP-Roma-yp'
    # 处理文件名：pkl中存储的img_path可能包含反斜杠
    pkl_path = pkl_dir / name
    if not pkl_path.exists():
        # 尝试搜索
        for f in pkl_dir.glob('*.pkl'):
            if f.stem in name or name in f.stem:
                pkl_path = f
                break
    with open(pkl_path, 'rb') as f:
        return pickle.load(f)

def load_pkl_by_img(scene, img_name):
    """按图像名查找pkl"""
    pkl_dir = CODE / 'Result' / 'Experiment1_HIGH' / 'QZ_Town' / f'pkl_{scene}' / 'resize_0.2' / 'HIGH-CAMP-Roma-yp'
    for f in pkl_dir.glob('*.pkl'):
        with open(f, 'rb') as fp:
            d = pickle.load(fp)
        if img_name in d.get('img_path', ''):
            return d
    return None

def get_uav_image_path(img_path_str):
    """从pkl中的img_path获取实际文件路径"""
    # 统一路径分隔符
    clean = img_path_str.replace('\\', '/').replace('./', '')
    return str(CODE / clean)

def load_csv_results(experiment):
    """加载CSV实验结果"""
    csv_path = BASE / '素材' / '实验数据' / f'results_{experiment}.csv'
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return None

# ============================================================
# 图5-3: 完整流程可视化
# ============================================================

def generate_fig5_3():
    """生成完整定位流程可视化：查询→候选→匹配→PnP"""
    print("生成图5-3: 完整流程可视化...")

    # 选择3个代表性样本
    samples = [
        ('QZ_SongCity', 'VG_data_DJI_0603.pkl', '成功定位 (误差0.09m)'),
        ('QZ_SongCity', 'VG_data_DJI_0576.pkl', '一般定位 (误差1.45m)'),
        ('QZ_Town', 'pkl_QingZhou_2024/resize_0.2/HIGH-CAMP-Roma-yp/VG_data_DJI_20240917112350_0391_D.pkl', '定位失败 (误差4797m)'),
    ]

    fig, axes = plt.subplots(3, 4, figsize=(16, 10))
    col_titles = ['①查询UAV图像', '②检索Top-5候选', '③RoMa匹配点', '④PnP定位结果']

    for row, (scene, pkl_name, label) in enumerate(samples):
        # 加载pkl
        if scene == 'QZ_Town':
            pkl_path = CODE / 'Result' / 'Experiment1_HIGH' / 'QZ_Town' / pkl_name
            with open(pkl_path, 'rb') as f:
                data = pickle.load(f)
        else:
            data = load_pkl(scene, pkl_name)

        img_path = get_uav_image_path(data['img_path'])

        # ① 查询UAV图像
        uav_img = imread_pil(img_path)
        if uav_img is not None:
            # 中心裁剪
            h, w = uav_img.shape[:2]
            size = min(h, w)
            cy, cx = h // 2, w // 2
            cropped = uav_img[cy-size//2:cy+size//2, cx-size//2:cx+size//2]
            axes[row, 0].imshow(cropped)
        axes[row, 0].set_title(label, fontsize=9)
        axes[row, 0].axis('off')

        # ② 检索候选（用文字说明，因为没有保存中间图）
        axes[row, 1].text(0.5, 0.5, f'Top-5候选图块\nIR_order:\n{data["IR_order"][:5]}\n\nPDE:\n{[f"{p:.3f}" for p in data["PDE"][:5]]}',
                         ha='center', va='center', fontsize=9, family='monospace',
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        axes[row, 1].set_title('②检索Top-5候选', fontsize=9)
        axes[row, 1].axis('off')

        # ③ 匹配点信息
        inliners = data['inliners']
        n_matches = inliners[0] if inliners else 0
        axes[row, 2].text(0.5, 0.5,
                         f'RoMa密集匹配\n\nTop-1内点数: {n_matches}\nTop-5内点数: {inliners}\n\n匹配方法: RoMa\n分辨率: coarse=280',
                         ha='center', va='center', fontsize=9, family='monospace',
                         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        axes[row, 2].set_title('③RoMa匹配点', fontsize=9)
        axes[row, 2].axis('off')

        # ④ PnP定位结果
        pred_loc = data['pred_loc']
        true_pos = data['truePos']
        error = data['pred_error']
        axes[row, 3].text(0.5, 0.5,
                         f'PnP求解结果\n\n预测: ({pred_loc["lat"]:.6f}, {pred_loc["lon"]:.6f})\n真值: ({true_pos["lat"]:.6f}, {true_pos["lon"]:.6f})\n\n定位误差: {error:.2f}m\n耗时: {data["total_time"]:.1f}s',
                         ha='center', va='center', fontsize=9, family='monospace',
                         bbox=dict(boxstyle='round', facecolor='lightgreen' if error < 5 else 'lightyellow' if error < 20 else 'lightcoral', alpha=0.8))
        axes[row, 3].set_title('④PnP定位结果', fontsize=9)
        axes[row, 3].axis('off')

    plt.suptitle('图5-3 视觉定位算法完整流程可视化', fontsize=13, y=1.02)
    plt.tight_layout()
    out_path = OUT / 'fig5_3_pipeline.png'
    plt.savefig(out_path, dpi=150, bbox_inches='tight', pad_inches=0.3)
    plt.close()
    print(f"  已保存: {out_path}")


# ============================================================
# 图5-4: 航空图vs卫星图对比
# ============================================================

def generate_fig5_4():
    """航空图与卫星图定位效果对比"""
    print("生成图5-4: 航空图vs卫星图对比...")

    df_high = load_csv_results('HIGH')
    df_low = load_csv_results('LOW')
    if df_high is None or df_low is None:
        print("  跳过：CSV文件不存在")
        return

    fig, axes = plt.subplots(2, 3, figsize=(14, 8))

    # 第一行：航空图
    # 误差分布
    axes[0, 0].hist(df_high['pred_error'].clip(upper=50), bins=30, color=COLORS_GLOBAL['blue'], edgecolor='white', alpha=0.85)
    axes[0, 0].axvline(x=5, color='red', linestyle='--', label='5m阈值')
    axes[0, 0].set_xlabel('定位误差 (m)')
    axes[0, 0].set_ylabel('样本数')
    axes[0, 0].set_title('航空图 - 误差分布')
    axes[0, 0].legend()

    # A@T曲线
    thresholds = np.arange(0, 51, 1)
    acc_high = [(df_high['pred_error'] < t).mean() * 100 for t in thresholds]
    axes[0, 1].plot(thresholds, acc_high, color=COLORS_GLOBAL['blue'], linewidth=2.5)
    axes[0, 1].axhline(y=82.3, color='r', linestyle='--', alpha=0.5, label='A@5m=82.3%')
    axes[0, 1].set_xlabel('误差阈值 (m)')
    axes[0, 1].set_ylabel('定位成功率 (%)')
    axes[0, 1].set_title('航空图 - A@T曲线')
    axes[0, 1].legend()
    axes[0, 1].set_xlim(0, 50)
    axes[0, 1].set_ylim(0, 100)

    # 分场景
    scenes_high = df_high.groupby('scene')['pred_error'].apply(lambda x: (x < 5).mean() * 100)
    axes[0, 2].bar(scenes_high.index, scenes_high.values, color=BAR_COLOR, edgecolor='white')
    axes[0, 2].set_ylabel('A@5m (%)')
    axes[0, 2].set_title('航空图 - 分场景A@5m')
    axes[0, 2].set_ylim(0, 105)
    for i, v in enumerate(scenes_high.values):
        axes[0, 2].text(i, v + 1, f'{v:.1f}%', ha='center', fontsize=9)

    # 第二行：卫星图
    axes[1, 0].hist(df_low['pred_error'].clip(upper=200), bins=30, color=COLORS_GLOBAL['orange'], edgecolor='white', alpha=0.85)
    axes[1, 0].axvline(x=5, color='red', linestyle='--', label='5m阈值')
    axes[1, 0].set_xlabel('定位误差 (m)')
    axes[1, 0].set_ylabel('样本数')
    axes[1, 0].set_title('卫星图 - 误差分布')
    axes[1, 0].legend()

    acc_low = [(df_low['pred_error'] < t).mean() * 100 for t in thresholds]
    axes[1, 1].plot(thresholds, acc_low, color=COLORS_GLOBAL['orange'], linewidth=2.5)
    axes[1, 1].axhline(y=13.6, color='b', linestyle='--', alpha=0.5, label='A@5m=13.6%')
    axes[1, 1].set_xlabel('误差阈值 (m)')
    axes[1, 1].set_ylabel('定位成功率 (%)')
    axes[1, 1].set_title('卫星图 - A@T曲线')
    axes[1, 1].legend()
    axes[1, 1].set_xlim(0, 50)
    axes[1, 1].set_ylim(0, 100)

    scenes_low = df_low.groupby('scene')['pred_error'].apply(lambda x: (x < 5).mean() * 100)
    axes[1, 2].bar(scenes_low.index, scenes_low.values, color=BAR_COLOR, edgecolor='white')
    axes[1, 2].set_ylabel('A@5m (%)')
    axes[1, 2].set_title('卫星图 - 分场景A@5m')
    axes[1, 2].set_ylim(0, 105)
    for i, v in enumerate(scenes_low.values):
        axes[1, 2].text(i, v + 1, f'{v:.1f}%', ha='center', fontsize=9)

    plt.suptitle('图5-4 航空图与卫星图定位效果对比', fontsize=13)
    plt.tight_layout()
    out_path = OUT / 'fig5_4_high_vs_low.png'
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  已保存: {out_path}")


# ============================================================
# 图5-5: 高度/视角分组示意图
# ============================================================

def generate_fig5_5():
    """不同高度和视角条件下的定位效果分析"""
    print("生成图5-5: 高度/视角分组分析...")

    df = load_csv_results('HIGH')
    if df is None:
        print("  跳过：CSV文件不存在")
        return

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # ① 俯仰角分组
    if 'pitch' in df.columns:
        df['pitch_abs'] = df['pitch'].abs()
        pitch_bins = [20, 50, 70, 90]
        pitch_labels = ['20°-50°\n(倾斜)', '50°-70°\n(过渡)', '70°-90°\n(正下视)']
        df['pitch_group'] = pd.cut(df['pitch_abs'], bins=pitch_bins, labels=pitch_labels, include_lowest=True)
        pitch_stats = df.groupby('pitch_group', observed=True).agg(
            a5m=('pred_error', lambda x: (x < 5).mean() * 100),
            count=('pred_error', 'size')
        )
        bars = axes[0].bar(range(len(pitch_stats)), pitch_stats['a5m'], color=BAR_COLOR, edgecolor='white')
        axes[0].set_xticks(range(len(pitch_stats)))
        axes[0].set_xticklabels(pitch_stats.index, fontsize=9)
        axes[0].set_ylabel('A@5m (%)')
        axes[0].set_title('俯仰角分组')
        axes[0].set_ylim(0, 105)
        for i, (v, n) in enumerate(zip(pitch_stats['a5m'], pitch_stats['count'])):
            axes[0].text(i, v + 1, f'{v:.1f}%\n(n={n})', ha='center', fontsize=9)
    else:
        axes[0].text(0.5, 0.5, '无俯仰角数据', ha='center', va='center')
        axes[0].set_title('俯仰角分组')

    # ② 高度分组
    if 'altitude' in df.columns:
        alt_bins = [0, 100, 200, 300]
        alt_labels = ['30-100m', '100-200m', '200-300m']
        df['alt_group'] = pd.cut(df['altitude'], bins=alt_bins, labels=alt_labels, include_lowest=True)
        alt_stats = df.groupby('alt_group', observed=True).agg(
            a5m=('pred_error', lambda x: (x < 5).mean() * 100),
            count=('pred_error', 'size')
        )
        bars = axes[1].bar(range(len(alt_stats)), alt_stats['a5m'], color=BAR_COLOR, edgecolor='white')
        axes[1].set_xticks(range(len(alt_stats)))
        axes[1].set_xticklabels(alt_stats.index, fontsize=9)
        axes[1].set_ylabel('A@5m (%)')
        axes[1].set_title('飞行高度分组')
        axes[1].set_ylim(0, 105)
        for i, (v, n) in enumerate(zip(alt_stats['a5m'], alt_stats['count'])):
            axes[1].text(i, v + 1, f'{v:.1f}%\n(n={n})', ha='center', fontsize=9)
    else:
        axes[1].text(0.5, 0.5, '无高度数据', ha='center', va='center')
        axes[1].set_title('飞行高度分组')

    # ③ 场景分组
    scene_stats = df.groupby('scene').agg(
        a5m=('pred_error', lambda x: (x < 5).mean() * 100),
        count=('pred_error', 'size')
    )
    bars = axes[2].bar(range(len(scene_stats)), scene_stats['a5m'], color=BAR_COLOR, edgecolor='white')
    axes[2].set_xticks(range(len(scene_stats)))
    axes[2].set_xticklabels(scene_stats.index, fontsize=9, rotation=15)
    axes[2].set_ylabel('A@5m (%)')
    axes[2].set_title('测试场景分组')
    axes[2].set_ylim(0, 105)
    for i, (v, n) in enumerate(zip(scene_stats['a5m'], scene_stats['count'])):
        axes[2].text(i, v + 1, f'{v:.1f}%\n(n={n})', ha='center', fontsize=9)

    plt.suptitle('图5-5 不同高度与视角条件下定位效果分析', fontsize=13)
    plt.tight_layout()
    out_path = OUT / 'fig5_5_height_pitch_analysis.png'
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  已保存: {out_path}")


# ============================================================
# 图5-6: 策略/匹配对比说明图
# ============================================================

def generate_fig5_6():
    """定位策略与匹配方法对比"""
    print("生成图5-6: 策略/匹配对比...")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # ① 策略对比
    strategies = ['Top N Re-rank', 'Top1', 'Most Inliers']
    a5m = [82.3, 68.8, 79.5]
    a10m = [90.3, 78.2, 86.2]
    a20m = [95.9, 81.9, 87.3]

    x = np.arange(len(strategies))
    width = 0.25
    axes[0].bar(x - width, a5m, width, label='A@5m', color=COLORS_GLOBAL['blue'], edgecolor='white')
    axes[0].bar(x, a10m, width, label='A@10m', color=COLORS_GLOBAL['orange'], edgecolor='white')
    axes[0].bar(x + width, a20m, width, label='A@20m', color=COLORS_GLOBAL['green'], edgecolor='white')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(strategies, fontsize=9)
    axes[0].set_ylabel('定位成功率 (%)')
    axes[0].set_title('定位策略对比')
    axes[0].legend()
    axes[0].set_ylim(0, 105)
    # 添加数值标签
    for i, (v5, v10, v20) in enumerate(zip(a5m, a10m, a20m)):
        axes[0].text(i - width, v5 + 1, f'{v5}', ha='center', fontsize=7)
        axes[0].text(i, v10 + 1, f'{v10}', ha='center', fontsize=7)
        axes[0].text(i + width, v20 + 1, f'{v20}', ha='center', fontsize=7)

    # ② 匹配方法对比
    methods = ['RoMa\n(密集/学习)', 'SIFT\n(稀疏/手工)']
    m_a5m = [82.3, 32.5]
    m_a10m = [90.3, 37.5]
    m_a20m = [95.9, 40.9]

    x2 = np.arange(len(methods))
    axes[1].bar(x2 - width, m_a5m, width, label='A@5m', color=COLORS_GLOBAL['blue'], edgecolor='white')
    axes[1].bar(x2, m_a10m, width, label='A@10m', color=COLORS_GLOBAL['orange'], edgecolor='white')
    axes[1].bar(x2 + width, m_a20m, width, label='A@20m', color=COLORS_GLOBAL['green'], edgecolor='white')
    axes[1].set_xticks(x2)
    axes[1].set_xticklabels(methods, fontsize=9)
    axes[1].set_ylabel('定位成功率 (%)')
    axes[1].set_title('匹配方法对比')
    axes[1].legend()
    axes[1].set_ylim(0, 105)
    for i, (v5, v10, v20) in enumerate(zip(m_a5m, m_a10m, m_a20m)):
        axes[1].text(i - width, v5 + 1, f'{v5}', ha='center', fontsize=7)
        axes[1].text(i, v10 + 1, f'{v10}', ha='center', fontsize=7)
        axes[1].text(i + width, v20 + 1, f'{v20}', ha='center', fontsize=7)

    plt.suptitle('图5-6 定位策略与匹配方法对比分析', fontsize=13)
    plt.tight_layout()
    out_path = OUT / 'fig5_6_strategy_matching.png'
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  已保存: {out_path}")


# ============================================================
# 图5-7: 检测→定位误差传播链路图
# ============================================================

def generate_fig5_7():
    """检测框→定位误差传播链路（流程图）"""
    print("生成图5-7: 误差传播链路图...")

    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    # 配色
    BLUE = '#5B9BD5'
    DARK_BLUE = '#1F4E79'
    TEAL = '#2E75B6'
    ORANGE = '#ED7D31'
    LIGHT_ORANGE = '#F4B183'
    LIGHT_TEAL = '#BDD7EE'

    fig, ax = plt.subplots(figsize=(16, 7))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # ============ 主流程（6个节点） ============
    main_steps = [
        ('红外/可见光\n目标检测', DARK_BLUE),
        ('检测框\n中心提取', BLUE),
        ('像素→相机\n坐标转换', TEAL),
        ('相机→UTM\n射线投影', BLUE),
        ('DSM高程\n交会求解', TEAL),
        ('目标地理\n坐标输出', DARK_BLUE),
    ]

    BOX_W = 1.9
    BOX_H = 0.85
    MAIN_Y = 5.2
    START_X = 1.0
    GAP = (16 - 2 * START_X - BOX_W) / (len(main_steps) - 1)

    def draw_box(ax, x, y, w, h, label, color, fontsize=9, text_color='white'):
        fancy = FancyBboxPatch((x - w/2, y - h/2), w, h,
                               boxstyle="round,pad=0.08", facecolor=color,
                               edgecolor='white', linewidth=2, zorder=3)
        ax.add_patch(fancy)
        ax.text(x, y, label, ha='center', va='center', fontsize=fontsize,
                fontweight='bold', color=text_color, zorder=4)

    main_positions = []
    for i, (label, color) in enumerate(main_steps):
        x = START_X + i * GAP
        main_positions.append((x, MAIN_Y))
        draw_box(ax, x, MAIN_Y, BOX_W, BOX_H, label, color)

    # 主流程箭头（灰色细箭头）
    for i in range(len(main_steps) - 1):
        x1 = main_positions[i][0] + BOX_W/2
        x2 = main_positions[i+1][0] - BOX_W/2
        ax.annotate('', xy=(x2, MAIN_Y), xytext=(x1, MAIN_Y),
                    arrowprops=dict(arrowstyle='->', color='#666666', lw=1.5,
                                    mutation_scale=14), zorder=2)

    # ============ 误差源（4个节点） ============
    error_labels = [
        '框中心偏移\n(±1~3 px)',
        '内参标定\n误差',
        '位姿估计\n误差',
        'DSM高程\n误差',
    ]

    ERR_Y = 2.8
    ERR_W = 1.6
    ERR_H = 0.75

    error_positions = []
    for i, label in enumerate(error_labels):
        x = main_positions[i + 1][0]
        error_positions.append((x, ERR_Y))
        draw_box(ax, x, ERR_Y, ERR_W, ERR_H, label, LIGHT_ORANGE, fontsize=9, text_color='#333333')

    # 误差源 → 主流程（橙色虚线箭头）
    for i in range(4):
        x = main_positions[i + 1][0]
        ax.annotate('', xy=(x, MAIN_Y - BOX_H/2 - 0.02),
                    xytext=(x, ERR_Y + ERR_H/2 + 0.02),
                    arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.3,
                                    linestyle='--', mutation_scale=12), zorder=2)

    # ============ 误差累积框（底部） ============
    CUM_W = 13.5
    CUM_H = 0.7
    CUM_Y = 1.2
    CUM_X = 8.0

    fancy_cum = FancyBboxPatch((CUM_X - CUM_W/2, CUM_Y - CUM_H/2), CUM_W, CUM_H,
                               boxstyle="round,pad=0.1", facecolor='#F5F5F5',
                               edgecolor='#BBBBBB', linewidth=1.5, zorder=3)
    ax.add_patch(fancy_cum)
    ax.text(CUM_X, CUM_Y,
            '误差传播与累积：框偏移 → 像素误差 → 射线角度误差 → 地面投影误差 → 目标坐标误差',
            ha='center', va='center', fontsize=9, color='#555555', zorder=4)

    # 误差源 → 累积框的连接线
    for pos in error_positions:
        ax.plot([pos[0], pos[0]], [ERR_Y - ERR_H/2, CUM_Y + CUM_H/2],
                color='#CCCCCC', lw=0.8, zorder=1)
    # 汇聚到累积框中心
    ax.plot([error_positions[0][0], CUM_X - CUM_W/2], [CUM_Y, CUM_Y],
            color='#CCCCCC', lw=0.8, zorder=1)
    ax.plot([error_positions[-1][0], CUM_X + CUM_W/2], [CUM_Y, CUM_Y],
            color='#CCCCCC', lw=0.8, zorder=1)

    # ============ 标题 ============
    ax.set_title('图5-7 目标检测→定位误差传播链路', fontsize=13,
                 pad=20, color='#333333')

    out_path = OUT / 'fig5_7_error_propagation.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight', pad_inches=0.3)
    plt.close()
    print(f"  已保存: {out_path}")


# ============================================================
# 图5-8: 成功/失败案例可视化
# ============================================================

def generate_fig5_8():
    """典型成功/失败案例可视化"""
    print("生成图5-8: 成功/失败案例...")

    df = load_csv_results('HIGH')
    if df is None:
        print("  跳过：CSV文件不存在")
        return

    fig, axes = plt.subplots(2, 3, figsize=(15, 9))

    # 第一行：成功案例
    success_cases = [
        ('QZ_SongCity', 'VG_data_DJI_0603.pkl', 'QZ_SongCity\n误差0.09m\n正下视+高分辨率航空图'),
        ('Qingzhou_3_2', 'VG_data_DJI_0524.pkl', 'Qingzhou_3_2\n误差0.68m\n正下视+航空图'),
        ('QingZhou_2024', 'VG_data_DJI_20240917112805_0472_D.pkl', 'QingZhou_2024\n误差0.89m\n正下视+航空图'),
    ]

    for col, (scene, pkl_name, desc) in enumerate(success_cases):
        data = load_pkl(scene, pkl_name)
        img_path = get_uav_image_path(data['img_path'])
        uav_img = imread_pil(img_path)
        if uav_img is not None:
            h, w = uav_img.shape[:2]
            size = min(h, w)
            cy, cx = h // 2, w // 2
            cropped = uav_img[cy-size//2:cy+size//2, cx-size//2:cx+size//2]
            axes[0, col].imshow(cropped)
        axes[0, col].set_title(desc, fontsize=9, color='green')
        axes[0, col].axis('off')

    # 第二行：失败案例
    # 从QingZhou_2024找大误差样本
    qz_df = df[df['scene'] == 'QingZhou_2024'].nlargest(3, 'pred_error')
    fail_cases = []
    for _, row in qz_df.iterrows():
        img_name = row['image_name']
        fail_cases.append(('QingZhou_2024', img_name, f'QingZhou_2024\n误差{row["pred_error"]:.0f}m'))

    for col, (scene, img_name, desc) in enumerate(fail_cases):
        # 从pkl目录找对应文件
        pkl_dir = CODE / 'Result' / 'Experiment1_HIGH' / 'QZ_Town' / f'pkl_{scene}' / 'resize_0.2' / 'HIGH-CAMP-Roma-yp'
        found = False
        for f in pkl_dir.glob('*.pkl'):
            with open(f, 'rb') as fp:
                d = pickle.load(fp)
            if img_name in d.get('img_path', ''):
                img_path = get_uav_image_path(d['img_path'])
                uav_img = imread_pil(img_path)
                if uav_img is not None:
                    h, w = uav_img.shape[:2]
                    size = min(h, w)
                    cy, cx = h // 2, w // 2
                    cropped = uav_img[cy-size//2:cy+size//2, cx-size//2:cx+size//2]
                    axes[1, col].imshow(cropped)
                found = True
                break
        if not found:
            axes[1, col].text(0.5, 0.5, f'图像未找到\n{img_name}', ha='center', va='center')
        axes[1, col].set_title(desc, fontsize=9, color='red')
        axes[1, col].axis('off')

    # 添加行标题
    axes[0, 0].set_ylabel('成功案例', fontsize=10, color='green', rotation=0, labelpad=60)
    axes[1, 0].set_ylabel('失败案例', fontsize=10, color='red', rotation=0, labelpad=60)

    plt.suptitle('图5-8 典型定位成功与失败案例', fontsize=13)
    plt.tight_layout()
    out_path = OUT / 'fig5_8_success_failure.png'
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  已保存: {out_path}")


# ============================================================
# 表格数据生成
# ============================================================

def generate_tables():
    """生成所有表格数据"""
    print("生成表格数据...")

    df_high = load_csv_results('HIGH')
    df_low = load_csv_results('LOW')
    df_top1 = load_csv_results('Top1')
    df_inliners = load_csv_results('MostInliers')
    df_sift = load_csv_results('SIFT')

    tables = {}

    # 表5-7: 主结果
    if df_high is not None and df_low is None:
        df_low = load_csv_results('LOW')

    def calc_metrics(df):
        if df is None:
            return {}
        errors = df['pred_error']
        return {
            'n': len(errors),
            'a5m': f"{(errors < 5).mean() * 100:.1f}%",
            'a10m': f"{(errors < 10).mean() * 100:.1f}%",
            'a20m': f"{(errors < 20).mean() * 100:.1f}%",
            'mean': f"{errors.mean():.1f}m",
            'median': f"{errors.median():.1f}m",
        }

    tables['5-7'] = {
        '航空图(CAMP+RoMa+TopN)': calc_metrics(df_high),
        '卫星图(CAMP+RoMa+TopN)': calc_metrics(df_low),
    }

    # 表5-8: 航空vs卫星
    tables['5-8'] = tables['5-7']

    # 表5-9: 俯仰角分组
    if df_high is not None and 'pitch' in df_high.columns:
        df_high['pitch_abs'] = df_high['pitch'].abs()
        for label, lo, hi in [('20°-50°', 20, 50), ('50°-70°', 50, 70), ('70°-90°', 70, 90)]:
            subset = df_high[(df_high['pitch_abs'] >= lo) & (df_high['pitch_abs'] < hi)]
            tables[f'5-9_{label}'] = calc_metrics(subset)

    # 表5-10: 策略对比
    tables['5-10_TopN'] = calc_metrics(df_high)
    tables['5-10_Top1'] = calc_metrics(df_top1)
    tables['5-10_Inliers'] = calc_metrics(df_inliners)
    tables['5-10_RoMa'] = calc_metrics(df_high)
    tables['5-10_SIFT'] = calc_metrics(df_sift)

    # 保存为JSON
    out_path = BASE / '素材' / '实验数据' / 'tables_data.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(tables, f, ensure_ascii=False, indent=2)
    print(f"  已保存: {out_path}")

    # 打印表5-7
    print("\n=== 表5-7 主结果 ===")
    for name, m in tables['5-7'].items():
        print(f"  {name}: n={m.get('n')}, A@5m={m.get('a5m')}, A@10m={m.get('a10m')}, A@20m={m.get('a20m')}, mean={m.get('mean')}, median={m.get('median')}")


# ============================================================
# 主函数
# ============================================================

if __name__ == '__main__':
    import sys as _sys
    print("=" * 60)
    print("第五章图表生成")
    print("=" * 60)

    # 可通过命令行参数指定只生成某个图，如: python generate_ch5_figures.py fig5_7
    target = _sys.argv[1] if len(_sys.argv) > 1 else None

    if target is None or target == 'fig5_3':
        generate_fig5_3()
    if target is None or target == 'fig5_4':
        generate_fig5_4()
    if target is None or target == 'fig5_5':
        generate_fig5_5()
    if target is None or target == 'fig5_6':
        generate_fig5_6()
    if target is None or target == 'fig5_7':
        generate_fig5_7()
    if target is None or target == 'fig5_8':
        generate_fig5_8()
    if target is None or target == 'tables':
        generate_tables()

    print("\n" + "=" * 60)
    print("全部完成！")
    print("=" * 60)
