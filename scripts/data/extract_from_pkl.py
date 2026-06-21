# -*- coding: utf-8 -*-
"""
从已有pkl文件提取实验数据，生成CSV
替代重跑实验，直接利用2460个已有pkl文件
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pickle
import glob
import csv
import os
import numpy as np

# 输出目录
OUTPUT_DIR = '素材/实验数据'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_from_pkls():
    """遍历所有pkl文件，提取关键数据"""

    results = []

    # 遍历所有实验目录
    experiment_dirs = [
        ('code/Result/Experiment1_HIGH', 'HIGH', 'TopN'),
        ('code/Result/Experiment1_LOW', 'LOW', 'TopN'),
        ('code/Result/Strategy_Top1', 'HIGH', 'Top1'),
        ('code/Result/Strategy_Inliners', 'HIGH', 'MostInliers'),
        ('code/Result/Matching_SIFT', 'HIGH', 'TopN_SIFT'),
    ]

    for base_dir, ref_type, strategy in experiment_dirs:
        pkls = glob.glob(f'{base_dir}/**/*.pkl', recursive=True)
        print(f'处理 {base_dir}: {len(pkls)} 个文件')

        for pkl_path in pkls:
            try:
                with open(pkl_path, 'rb') as f:
                    data = pickle.load(f)

                # 提取基本信息
                true_pos = data.get('truePos', {})
                img_path = data.get('img_path', '')
                img_name = os.path.basename(img_path)

                # 从路径提取场景名（pkl_QZ_SongCity → QZ_SongCity）
                parts = pkl_path.replace('\\', '/').split('/')
                scene = 'unknown'
                # 优先找 pkl_ 前缀的目录
                for p in parts:
                    if p.startswith('pkl_'):
                        scene = p.replace('pkl_', '')
                        break
                # 如果没找到pkl_前缀，找场景关键词
                if scene == 'unknown':
                    for p in parts:
                        if p in ['QZ_SongCity', 'Qingzhou_3_2', 'QingZhou_2024']:
                            scene = p
                            break

                # 提取误差
                pred_error = data.get('pred_error', None)
                if pred_error is None:
                    continue

                # 处理inf值
                if np.isinf(pred_error):
                    pred_error = 99999.0  # 用大值替代inf

                # 提取内点数
                inliners = data.get('inliners', [])
                max_inliers = max(inliners) if inliners else 0

                # 提取时间
                total_time = data.get('total_time', 0)
                retrieval_time = data.get('retrieval_time', 0)
                match_time = data.get('match_time', [])
                match_time_total = sum(match_time) if match_time else 0

                results.append({
                    'image_name': img_name,
                    'scene': scene,
                    'ref_type': ref_type,
                    'strategy': strategy,
                    'matching_method': 'SIFT' if 'SIFT' in strategy else 'RoMa',
                    'pitch': true_pos.get('pitch', 0),
                    'yaw': true_pos.get('yaw', 0),
                    'altitude': true_pos.get('rel_alt', 0),
                    'pred_error': pred_error,
                    'inlier_count': max_inliers,
                    'total_time': total_time,
                    'retrieval_time': retrieval_time,
                    'match_time': match_time_total,
                })
            except Exception as e:
                print(f'  跳过 {os.path.basename(pkl_path)}: {e}')

    return results

def save_to_csv(results, filename):
    """保存到CSV文件"""
    filepath = f'{OUTPUT_DIR}/{filename}'
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f'保存: {filepath} ({len(results)} 行)')

def main():
    print('=' * 50)
    print('从pkl文件提取实验数据')
    print('=' * 50)

    results = extract_from_pkls()

    # 按实验类型分组保存
    df_high = [r for r in results if r['ref_type'] == 'HIGH' and r['strategy'] == 'TopN']
    df_low = [r for r in results if r['ref_type'] == 'LOW' and r['strategy'] == 'TopN']
    df_top1 = [r for r in results if r['strategy'] == 'Top1']
    df_inliers = [r for r in results if r['strategy'] == 'MostInliers']
    df_sift = [r for r in results if r['matching_method'] == 'SIFT']

    save_to_csv(results, 'results_all.csv')
    if df_high:
        save_to_csv(df_high, 'results_HIGH.csv')
    if df_low:
        save_to_csv(df_low, 'results_LOW.csv')
    if df_top1:
        save_to_csv(df_top1, 'results_Top1.csv')
    if df_inliers:
        save_to_csv(df_inliers, 'results_MostInliers.csv')
    if df_sift:
        save_to_csv(df_sift, 'results_SIFT.csv')

    print('=' * 50)
    print('提取完成!')
    print('=' * 50)

if __name__ == '__main__':
    main()
