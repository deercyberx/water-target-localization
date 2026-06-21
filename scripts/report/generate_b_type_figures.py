# -*- coding: utf-8 -*-
"""
B类图表生成脚本：重跑实验pipeline，保存中间结果可视化
需要GPU环境运行

生成内容：
- 图5-3: 完整定位流程（成功/一般/失败，各4列）
- 图5-4补充: 航空图/卫星图匹配可视化
- 图5-8: 成功/失败案例（4行）

用法：
  cd code
  ../.venv/Scripts/python ../scripts/report/generate_b_type_figures.py
"""

import sys
import os

# 必须在code目录下运行，因为Baseline.py和utils.py使用相对路径
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.join(_script_dir, '..', '..')  # scripts/report -> project root
_code_dir = os.path.join(_project_root, 'code')
os.chdir(_code_dir)
sys.path.insert(0, '.')

import pickle
import numpy as np
import cv2
import torch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from PIL import Image
from pathlib import Path

# 中文字体
import matplotlib.font_manager as fm
import glob as _glob
for f in _glob.glob(os.path.join(matplotlib.get_cachedir(), 'fontlist-*.json')):
    try: os.remove(f)
    except: pass
fm.fontManager.__init__()
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300

# 项目路径
BASE = Path('..').resolve()
OUT = BASE / '素材' / '截图'
OUT.mkdir(parents=True, exist_ok=True)

# ============================================================
# 导入项目模块
# ============================================================
import yaml
from utils import (
    retrieval_init, matching_init, retrieval_all, Match2Pos_all,
    load_config_parameters_new, query_data_from_file, read_data_from_file,
    computeCameraMatrix, dumpRotateImage, pos2error, get_jpg_files,
    find_values, resolution_size, view_center, process_and_save_matches,
    MATCH_REGISTRY
)
from Retrieval_Models.multi_model_loader import get_Model
from utils import estimate_drone_pose

# ============================================================
# 新增函数：保存全部匹配点（含outlier）
# ============================================================
def process_and_save_all_matches(Sen_pts, Ref_pts, inliers, uav_image, ref_image, save_path):
    """保存全部匹配点：outlier红色，inlier绿色"""
    if len(Sen_pts) == 0:
        return

    # 全部点
    all_kp_left = [cv2.KeyPoint(p[0], p[1], 1) for p in Sen_pts]
    all_kp_right = [cv2.KeyPoint(p[0], p[1], 1) for p in Ref_pts]
    all_matches = [cv2.DMatch(i, i, 0) for i in range(len(Sen_pts))]

    # 内点索引
    inlier_set = set(i[0] for i in inliers) if len(inliers) > 0 else set()

    # 绘制全部匹配
    img_all = cv2.drawMatches(uav_image, all_kp_left, ref_image, all_kp_right,
                               all_matches, None,
                               matchColor=(0, 0, 255),  # 红色
                               flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # 绘制仅内点
    if len(inliers) > 0:
        inlier_kp_left = [cv2.KeyPoint(Sen_pts[i[0]][0], Sen_pts[i[0]][1], 1) for i in inliers]
        inlier_kp_right = [cv2.KeyPoint(Ref_pts[i[0]][0], Ref_pts[i[0]][1], 1) for i in inliers]
        inlier_matches = [cv2.DMatch(i, i, 0) for i in range(len(inliers))]
        img_inlier = cv2.drawMatches(uav_image, inlier_kp_left, ref_image, inlier_kp_right,
                                      inlier_matches, None,
                                      matchColor=(0, 255, 0),  # 绿色
                                      flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    else:
        img_inlier = img_all.copy()

    cv2.imwrite(save_path + '_all_matches.png', img_all)
    cv2.imwrite(save_path + '_inliers.png', img_inlier)


# PIL版本的匹配保存函数（兼容中文路径）
def save_all_matches_pil(Sen_pts, Ref_pts, inliers, uav_image, ref_image, save_path):
    """用PIL保存全部匹配点"""
    if len(Sen_pts) == 0:
        return
    all_kp_left = [cv2.KeyPoint(p[0], p[1], 1) for p in Sen_pts]
    all_kp_right = [cv2.KeyPoint(p[0], p[1], 1) for p in Ref_pts]
    all_matches = [cv2.DMatch(i, i, 0) for i in range(len(Sen_pts))]
    img_all = cv2.drawMatches(uav_image, all_kp_left, ref_image, all_kp_right,
                               all_matches, None,
                               matchColor=(0, 0, 255),
                               flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    Image.fromarray(cv2.cvtColor(img_all, cv2.COLOR_BGR2RGB)).save(save_path + '_all_matches.png')

    if len(inliers) > 0:
        inlier_kp_left = [cv2.KeyPoint(Sen_pts[i[0]][0], Sen_pts[i[0]][1], 1) for i in inliers]
        inlier_kp_right = [cv2.KeyPoint(Ref_pts[i[0]][0], Ref_pts[i[0]][1], 1) for i in inliers]
        inlier_matches = [cv2.DMatch(i, i, 0) for i in range(len(inliers))]
        img_inlier = cv2.drawMatches(uav_image, inlier_kp_left, ref_image, inlier_kp_right,
                                      inlier_matches, None,
                                      matchColor=(0, 255, 0),
                                      flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    else:
        img_inlier = img_all.copy()
    Image.fromarray(cv2.cvtColor(img_inlier, cv2.COLOR_BGR2RGB)).save(save_path + '_inliers.png')


def save_match_pil(Sen_pts, Ref_pts, inliers, uav_image, ref_image, save_path):
    """用PIL保存内点匹配"""
    if len(inliers) == 0:
        # 保存空图
        Image.fromarray(np.zeros((100, 100, 3), dtype=np.uint8)).save(save_path)
        return
    inlier_kp_left = [cv2.KeyPoint(Sen_pts[i[0]][0], Sen_pts[i[0]][1], 1) for i in inliers]
    inlier_kp_right = [cv2.KeyPoint(Ref_pts[i[0]][0], Ref_pts[i[0]][1], 1) for i in inliers]
    inlier_matches = [cv2.DMatch(i, i, 0) for i in range(len(inliers))]
    img = cv2.drawMatches(uav_image, inlier_kp_left, ref_image, inlier_kp_right,
                           inlier_matches, None,
                           flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).save(save_path)


# ============================================================
# 新增函数：在参考地图上标注预测/真值位置
# ============================================================
def draw_pred_on_refmap(ref_map, pred_loc, true_pos, ref_resolution, initialX, initialY, save_path, region, config):
    """在参考地图上标注预测位置(红)和真值位置(绿)"""
    from pyproj import Transformer

    img = ref_map.copy()
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # 真值UTM
    utm_system = config[f'{region}_UTM_SYSTEM']
    transformer = Transformer.from_crs("epsg:4326", f"epsg:326{utm_system[:2]}")
    true_x, true_y = transformer.transform(true_pos['lat'], true_pos['lon'])

    # 预测UTM
    if pred_loc and pred_loc.get('lat') and pred_loc.get('lon'):
        pred_x, pred_y = transformer.transform(pred_loc['lat'], pred_loc['lon'])
    else:
        pred_x, pred_y = None, None

    # 转为像素坐标
    def utm_to_pixel(ux, uy):
        px = int((ux - initialX) / ref_resolution)
        py = int((initialY - uy) / ref_resolution)
        return px, py

    # 缩放显示
    scale = 0.3
    h, w = img.shape[:2]
    img_small = cv2.resize(img, (int(w * scale), int(h * scale)))

    # 真值位置（绿色）
    tx, ty = utm_to_pixel(true_x, true_y)
    txs, tys = int(tx * scale), int(ty * scale)
    cv2.circle(img_small, (txs, tys), 15, (0, 255, 0), 3)
    cv2.putText(img_small, 'GT', (txs + 20, tys), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # 预测位置（红色）
    if pred_x is not None:
        px, py = utm_to_pixel(pred_x, pred_y)
        pxs, pys = int(px * scale), int(py * scale)
        cv2.circle(img_small, (pxs, pys), 15, (0, 0, 255), 3)
        cv2.putText(img_small, 'Pred', (pxs + 20, pys), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # 距离标注
        dist = np.sqrt((true_x - pred_x)**2 + (true_y - pred_y)**2)
        mid_x, mid_y = (txs + pxs) // 2, (tys + pys) // 2
        cv2.putText(img_small, f'{dist:.1f}m', (mid_x, mid_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    Image.fromarray(cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)).save(save_path)


# ============================================================
# 可视化单个样本的完整pipeline
# ============================================================
def visualize_sample(sample_info, config, region_config, method_dict, ref_map0, dsm_map0, ref_resolution, opt, region, save_dir):
    """对单个样本跑完整pipeline并保存中间结果"""
    scene = sample_info['scene']
    img_name = sample_info['img_name']
    label = sample_info['label']

    # 找到UAV图像路径
    uav_path = None
    uav_dir = f'./Data/UAV_image/QZ_Town/{scene}/'
    for f in os.listdir(uav_dir):
        if img_name in f:
            uav_path = os.path.join(uav_dir, f)
            break
    if uav_path is None:
        print(f"  图像未找到: {img_name}")
        return None

    # 读取元数据
    json_file = './Data/metadata/QZ_Town.json'
    truePos = query_data_from_file(json_file, name=f'{os.path.dirname(uav_path)}/{os.path.basename(uav_path)}')[0]
    K = computeCameraMatrix(truePos)
    uav_image = cv2.imread(uav_path)

    # 旋转参考图
    ref_map, matRotation = dumpRotateImage(ref_map0, truePos['yaw'])

    # 检索
    print(f"  检索中...")
    IR_order, refLocX, refLocY, PDE_list, cut_H, cut_W, fineScale, retrieval_time = retrieval_all(
        ref_map, uav_path, truePos, ref_resolution, matRotation,
        str(save_dir), opt, region, region_config, method_dict
    )

    # 匹配
    print(f"  匹配中...")
    BLH_list, inliers_list, match_time, pnp_time = Match2Pos_all(
        opt, region, region_config, uav_image, fineScale, K,
        ref_map, dsm_map0, refLocY, refLocX, cut_H, cut_W,
        str(save_dir), method_dict, matRotation
    )

    # 定位误差
    pred_loc, pred_error, location_error_list = pos2error(truePos, BLH_list, inliers_list)

    # 保存匹配可视化（Top-1）
    resize_ratio = opt.resize_ratio
    refLocY_1 = refLocY[0]
    refLocX_1 = refLocX[0]
    fineRef = ref_map[refLocX_1:refLocX_1+cut_W, refLocY_1:refLocY_1+cut_H]
    fineRef = cv2.resize(fineRef, None, fx=resize_ratio/fineScale, fy=resize_ratio/fineScale)
    uav_resized = cv2.resize(uav_image, None, fx=resize_ratio, fy=resize_ratio)

    # 重新跑一次匹配获取原始点对
    name = method_dict['matching_method']
    if name in MATCH_REGISTRY:
        _, match_fn = MATCH_REGISTRY[name]
        Sen_pts, Ref_pts = match_fn(uav_resized, fineRef, method_dict['matching_model'],
                                     str(save_dir), '/temp.png',
                                     need_ransac=False, show_matches=False)

    # 获取内点
    inliers_for_viz = []
    if len(Ref_pts) >= 5:
        refCoordinate = np.array(Ref_pts) / resize_ratio * fineScale + np.array([refLocY_1, refLocX_1])
        reverseMatRotation = cv2.invertAffineTransform(matRotation)
        refCoordinate1 = np.hstack([refCoordinate, np.ones((refCoordinate.shape[0], 1))])
        refCoordinate2 = refCoordinate1 @ reverseMatRotation.T
        initialX = region_config[f'{region}_{opt.Ref_type}_REF_initialX']
        initialY = region_config[f'{region}_{opt.Ref_type}_REF_initialY']
        UTM_X = refCoordinate2[:, 0] * ref_resolution + initialX
        UTM_Y = initialY - refCoordinate2[:, 1] * ref_resolution

        dsm_resolution = region_config[f'{region}_{opt.Ref_type}_DSM_resolution']
        dsm_coor = region_config[f'{region}_{opt.Ref_type}_DSM_COORDINATE']
        ref_coor = region_config[f'{region}_{opt.Ref_type}_REF_COORDINATE']
        dsm_ratio = dsm_resolution / ref_resolution
        dsm_coor = [dsm_coor[0] * dsm_ratio, dsm_coor[1] * dsm_ratio]
        dsm_offset = (int(dsm_coor[0] - ref_coor[0]), int(dsm_coor[1] - ref_coor[1]))

        dsm_x = refCoordinate2[:, 1] + dsm_offset[1]
        dsm_y = refCoordinate2[:, 0] + dsm_offset[0]
        dsm_x, dsm_y = (dsm_x + 1) / dsm_ratio - 1, (dsm_y + 1) / dsm_ratio - 1
        dsm_x1 = np.clip(dsm_x.astype(int), 0, dsm_map0.shape[0] - 1)
        dsm_y1 = np.clip(dsm_y.astype(int), 0, dsm_map0.shape[1] - 1)
        DSM = dsm_map0[dsm_x1, dsm_y1]

        match_points = np.array(Sen_pts) / resize_ratio
        _, _, _, inliers_all = estimate_drone_pose(region, region_config, match_points, K, UTM_X, UTM_Y, DSM)
        inliers_for_viz = inliers_all

    # 保存匹配图（用PIL避免中文路径问题）
    match_save = str(save_dir / f'{img_name}_match')
    if sample_info.get('save_all_matches'):
        save_all_matches_pil(Sen_pts, Ref_pts, inliers_for_viz, uav_resized, fineRef, match_save)
    save_match_pil(Sen_pts, Ref_pts, inliers_for_viz, uav_resized, fineRef, match_save + '_clean.png')

    # 保存PnP叠加图
    initialX = region_config[f'{region}_{opt.Ref_type}_REF_initialX']
    initialY = region_config[f'{region}_{opt.Ref_type}_REF_initialY']
    draw_pred_on_refmap(ref_map, pred_loc, truePos, ref_resolution, initialX, initialY,
                         str(save_dir / f'{img_name}_pnp.png'), region, region_config)

    # 保存查询图（用PIL避免中文路径问题）
    h, w = uav_image.shape[:2]
    size = min(h, w)
    cy, cx = h // 2, w // 2
    cropped = uav_image[cy-size//2:cy+size//2, cx-size//2:cx+size//2]
    Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)).save(str(save_dir / f'{img_name}_query.png'))

    # 清理临时文件
    temp = Path(str(save_dir) + '/temp.png')
    if temp.exists():
        temp.unlink()

    # 重命名检索结果图（避免被下一个样本覆盖）
    retrieval_src = save_dir / '1_Retrieval.png'
    retrieval_dst = save_dir / f'{img_name}_retrieval.png'
    if retrieval_src.exists():
        if retrieval_dst.exists():
            retrieval_dst.unlink()
        retrieval_src.rename(retrieval_dst)

    torch.cuda.empty_cache()

    return {
        'img_name': img_name,
        'label': label,
        'pred_error': pred_error,
        'inliers': inliers_list[0] if inliers_list else 0,
        'truePos': truePos,
        'pred_loc': pred_loc,
    }


# ============================================================
# 拼接图5-3: 3行x4列
# ============================================================
def compose_fig5_3(results, save_dir):
    """拼接图5-3：成功/一般/失败 x 4列"""
    print("拼接图5-3...")

    fig, axes = plt.subplots(3, 4, figsize=(16, 11))
    col_titles = ['①查询UAV图像', '②检索Top-N候选', '③RoMa匹配点', '④PnP定位结果']

    for row, r in enumerate(results):
        img_name = r['img_name']
        label = r['label']
        error = r['pred_error']

        # 列1: 查询图
        query_path = save_dir / f'{img_name}_query.png'
        if query_path.exists():
            img = np.array(Image.open(str(query_path)).convert('RGB'))
            axes[row, 0].imshow(img)
        axes[row, 0].set_title(label, fontsize=10, fontweight='bold',
                               color='green' if error < 5 else 'orange' if error < 50 else 'red')
        axes[row, 0].axis('off')

        # 列2: 检索候选（每个样本有独立的检索结果图）
        retrieval_path = save_dir / f'{img_name}_retrieval.png'
        if retrieval_path.exists():
            ret_img = np.array(Image.open(str(retrieval_path)).convert('RGB'))
            axes[row, 1].imshow(ret_img)
        else:
            axes[row, 1].text(0.5, 0.5, f'Top-5候选图块\n(检索结果)', ha='center', va='center',
                             fontsize=9, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        axes[row, 1].set_title('②检索Top-N候选', fontsize=10)
        axes[row, 1].axis('off')

        # 列3: 匹配点
        match_path = save_dir / f'{img_name}_match_clean.png'
        if match_path.exists():
            match_img = np.array(Image.open(str(match_path)).convert('RGB'))
            axes[row, 2].imshow(match_img)
        else:
            axes[row, 2].text(0.5, 0.5, f'内点数: {r["inliers"]}', ha='center', va='center',
                             fontsize=9, bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        axes[row, 2].set_title('③RoMa匹配点', fontsize=10)
        axes[row, 2].axis('off')

        # 列4: PnP结果
        pnp_path = save_dir / f'{img_name}_pnp.png'
        if pnp_path.exists():
            pnp_img = np.array(Image.open(str(pnp_path)).convert('RGB'))
            axes[row, 3].imshow(pnp_img)
        else:
            pred = r['pred_loc']
            true = r['truePos']
            axes[row, 3].text(0.5, 0.5,
                             f'PnP求解结果\n\n预测: ({pred["lat"]:.6f}, {pred["lon"]:.6f})\n'
                             f'真值: ({true["lat"]:.6f}, {true["lon"]:.6f})\n\n'
                             f'误差: {error:.2f}m',
                             ha='center', va='center', fontsize=8, family='monospace',
                             bbox=dict(boxstyle='round',
                                      facecolor='lightgreen' if error < 5 else 'lightyellow' if error < 50 else 'lightcoral',
                                      alpha=0.8))
        axes[row, 3].set_title('④PnP定位结果', fontsize=10)
        axes[row, 3].axis('off')

    for col, title in enumerate(col_titles):
        axes[0, col].set_title(title, fontsize=11, fontweight='bold')

    plt.suptitle('图5-3 视觉定位算法完整流程可视化', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(OUT / 'fig5_3_pipeline.png', dpi=300, bbox_inches='tight', pad_inches=0.3)
    plt.close()
    print("  已保存")


# ============================================================
# 拼接图5-8: 4行（成功/视角退化/参考图差异/检测框联动）
# ============================================================
def compose_fig5_8(results, save_dir):
    """拼接图5-8"""
    print("拼接图5-8...")

    fig, axes = plt.subplots(4, 4, figsize=(16, 14))
    row_labels = ['成功案例', '视角退化失败', '参考图差异失败', '检测框联动风险']
    col_titles = ['查询UAV图像', '匹配结果', '定位输出', '原因分析']

    for row in range(4):
        if row < 3:  # 前3行用实验数据，第4行固定为检测框联动风险
            r = results[row]
            img_name = r['img_name']
            error = r['pred_error']

            # 列1: 查询图
            query_path = save_dir / f'{img_name}_query.png'
            if query_path.exists():
                img = np.array(Image.open(str(query_path)).convert('RGB'))
                axes[row, 0].imshow(img)

            # 列2: 匹配结果
            match_path = save_dir / f'{img_name}_match_all_matches.png' if row > 0 else save_dir / f'{img_name}_match_clean.png'
            if not match_path.exists():
                match_path = save_dir / f'{img_name}_match_clean.png'
            if match_path.exists():
                m_img = np.array(Image.open(str(match_path)).convert('RGB'))
                axes[row, 1].imshow(m_img)

            # 列3: PnP结果
            pnp_path = save_dir / f'{img_name}_pnp.png'
            if pnp_path.exists():
                pnp_img = np.array(Image.open(str(pnp_path)).convert('RGB'))
                axes[row, 2].imshow(pnp_img)

            # 列4: 原因分析
            if row == 0:
                reason = f'正下视+航空图\n内点数: {r["inliers"]}\n误差: {error:.2f}m\n链路稳定收敛'
            elif row == 1:
                reason = f'大倾斜角拍摄\n透视畸变严重\n与正射参考图\n相似度极低\n误差: {error:.0f}m'
            elif row == 2:
                reason = f'参考图DSM分辨率低\n(30m vs 0.937m)\nPnP约束弱\n误差: {error:.0f}m'
            else:
                reason = '检测框中心偏移\n→像素误差\n→射线角度偏差\n→地面投影误差\n放大'
            axes[row, 3].text(0.5, 0.5, reason, ha='center', va='center', fontsize=9,
                             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        else:
            # 第4行：检测框联动风险（分析框架示意）
            axes[row, 0].text(0.5, 0.5, '检测框\n中心偏移\n±Δpx', ha='center', va='center',
                             fontsize=10, bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
            axes[row, 1].text(0.5, 0.5, '像素→相机\n坐标转换\n内参矩阵K', ha='center', va='center',
                             fontsize=10, bbox=dict(boxstyle='round', facecolor='lightsalmon', alpha=0.8))
            axes[row, 2].text(0.5, 0.5, '射线投影\nDSM交会\nUTM坐标', ha='center', va='center',
                             fontsize=10, bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
            axes[row, 3].text(0.5, 0.5, '地理误差\n随像素偏移\n线性放大', ha='center', va='center',
                             fontsize=10, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

        axes[row, 0].set_ylabel(row_labels[row], fontsize=10, fontweight='bold', rotation=0, labelpad=80, va='center')

    for col, title in enumerate(col_titles):
        axes[0, col].set_title(title, fontsize=11, fontweight='bold')

    for ax in axes.flat:
        ax.set_xticks([])
        ax.set_yticks([])

    plt.suptitle('图5-8 典型定位结果与失败案例分析', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(OUT / 'fig5_8_success_failure.png', dpi=300, bbox_inches='tight', pad_inches=0.3)
    plt.close()
    print("  已保存")


# ============================================================
# 主函数
# ============================================================
def main():
    print("=" * 60)
    print("B类图表生成（需要GPU环境）")
    print("=" * 60)

    # 加载配置
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    region = 'QZ_Town'
    yaml_file = f'./Regions_params/{region}.yaml'
    with open(yaml_file, 'r') as f:
        region_config = yaml.safe_load(f)
    region_config.update(config)

    # 启用检索结果可视化
    region_config['SHOW_RETRIEVAL_RESULT'] = True

    # 创建输出目录
    save_dir = OUT / 'pipeline_vis'
    save_dir.mkdir(parents=True, exist_ok=True)

    # 初始化模型
    print("初始化检索模型...")
    method_dict = {'retrieval_method': 'CAMP'}
    method_dict = retrieval_init(method_dict, region_config)

    print("初始化匹配模型...")
    method_dict['matching_method'] = 'Roma'
    method_dict = matching_init(method_dict)

    # 加载参考图和DSM
    opt = type('Opt', (), {
        'Ref_type': 'HIGH',
        'resize_ratio': 0.2,
        'strategy': 'Topn_opt',
        'pose_priori': 'yp',
        'save_dir': str(save_dir),
    })()

    ref_map0, dsm_map0, _, ref_resolution = load_config_parameters_new(region_config, opt, region)

    # 选定样本
    samples = [
        {'scene': 'QZ_SongCity', 'img_name': 'DJI_0603', 'label': '成功定位 (误差0.09m)'},
        {'scene': 'QingZhou_2024', 'img_name': 'DJI_20240917112254_0364_D', 'label': '一般定位 (误差9.17m)'},
        {'scene': 'QingZhou_2024', 'img_name': 'DJI_20240917112350_0391_D', 'label': '定位失败 (误差4797m)', 'save_all_matches': True},
    ]

    # 跑pipeline
    results = []
    for i, sample in enumerate(samples):
        print(f"\n[{i+1}/{len(samples)}] {sample['label']}...")
        r = visualize_sample(sample, config, region_config, method_dict, ref_map0, dsm_map0, ref_resolution, opt, region, save_dir)
        if r:
            results.append(r)

    # 补充失败案例用于图5-8
    extra_samples = [
        {'scene': 'QingZhou_2024', 'img_name': 'DJI_20240917112327_0380_D', 'label': '参考图差异失败', 'save_all_matches': True},
        {'scene': 'QingZhou_2024', 'img_name': 'DJI_20240917112349_0390_D', 'label': '匹配质量失败', 'save_all_matches': True},
    ]
    extra_results = []
    for i, sample in enumerate(extra_samples):
        print(f"\n[补充 {i+1}/{len(extra_samples)}] {sample['label']}...")
        r = visualize_sample(sample, config, region_config, method_dict, ref_map0, dsm_map0, ref_resolution, opt, region, save_dir)
        if r:
            extra_results.append(r)

    # 拼接图5-3
    if len(results) >= 3:
        compose_fig5_3(results, save_dir)

    # 拼接图5-8：选取3个代表性样本（成功/视角退化/参考图差异）
    fig5_8_data = []
    if len(results) >= 1:
        fig5_8_data.append(results[0])   # 成功案例
    if len(results) >= 3:
        fig5_8_data.append(results[2])   # 视角退化失败（大倾斜角）
    if len(extra_results) >= 1:
        fig5_8_data.append(extra_results[0])  # 参考图差异失败
    if len(fig5_8_data) >= 3:
        compose_fig5_8(fig5_8_data, save_dir)

    # 图5-4补充：卫星图匹配
    print("\n卫星图匹配...")
    opt_low = type('Opt', (), {
        'Ref_type': 'LOW',
        'resize_ratio': 0.2,
        'strategy': 'Topn_opt',
        'pose_priori': 'yp',
        'save_dir': str(save_dir),
    })()
    ref_map_low, dsm_map_low, _, ref_resolution_low = load_config_parameters_new(region_config, opt_low, region)

    sample_low = {'scene': 'QZ_SongCity', 'img_name': 'DJI_0532', 'label': '卫星图匹配'}
    r_low = visualize_sample(sample_low, config, region_config, method_dict, ref_map_low, dsm_map_low, ref_resolution_low, opt_low, region, save_dir)

    print("\n" + "=" * 60)
    print("全部完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
