# -*- coding: utf-8 -*-
"""
生成成功/失败案例截图 (G6/G7)
针对特定图像运行pipeline并保存可视化结果
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import csv
import os
import shutil

# 读取CSV数据
DATA_DIR = '素材/实验数据'
OUTPUT_DIR = '素材/截图'

def load_cases():
    """加载成功和失败案例"""
    with open(f'{DATA_DIR}/results_HIGH.csv', 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    # 按误差排序
    rows_sorted = sorted(rows, key=lambda x: float(x['pred_error']))

    # 成功案例 (error < 1m, 选取3个)
    success = [r for r in rows_sorted if float(r['pred_error']) < 1][:3]

    # 失败案例 (error > 1000m, 选取3个)
    failure = [r for r in rows_sorted if float(r['pred_error']) > 1000][-3:]

    return success, failure

def create_targeted_config(success, failure):
    """创建针对特定图像的配置"""
    # 获取需要运行的图像列表
    target_images = [r['image_name'] for r in success + failure]

    print(f'目标图像: {len(target_images)} 张')
    print(f'  成功案例: {[r[\"image_name\"] + \" (\" + str(round(float(r[\"pred_error\"]), 2)) + \"m)\" for r in success]}')
    print(f'  失败案例: {[r[\"image_name\"] + \" (\" + str(round(float(r[\"pred_error\"]), 2)) + \"m)\" for r in failure]}')

    return target_images

def main():
    print('=' * 50)
    print('生成成功/失败案例截图')
    print('=' * 50)

    success, failure = load_cases()
    target_images = create_targeted_config(success, failure)

    print(f'\n需要运行 {len(target_images)} 张图像的pipeline')
    print('请手动执行以下步骤:')
    print('1. 修改 code/config.yaml:')
    print('   - SHOW_RETRIEVAL_RESULT: True')
    print('   - TEST_INTERVAL: 1')
    print('2. 运行: cd code && python Baseline.py')
    print('3. 结果保存在 code/Result/ 目录')
    print('4. 截图保存在 code/Result/Experiment1_HIGH/QZ_Town/ 目录')

    # 保存目标图像列表
    with open(f'{OUTPUT_DIR}/target_images.txt', 'w', encoding='utf-8') as f:
        f.write('# 成功案例 (error < 1m)\n')
        for r in success:
            f.write(f'{r["image_name"]}\terror={float(r["pred_error"]):.2f}m\tscene={r["scene"]}\n')
        f.write('\n# 失败案例 (error > 1000m)\n')
        for r in failure:
            f.write(f'{r["image_name"]}\terror={float(r["pred_error"]):.2f}m\tscene={r["scene"]}\n')

    print(f'\n目标图像列表已保存: {OUTPUT_DIR}/target_images.txt')

if __name__ == '__main__':
    main()
