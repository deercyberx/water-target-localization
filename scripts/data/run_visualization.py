# -*- coding: utf-8 -*-
"""
运行pipeline生成可视化截图 (G6/G7/G10)
使用TEST_INTERVAL=100获取少量样本
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import yaml
import subprocess
import os

CONFIG_PATH = 'code/config.yaml'

def backup_config():
    """备份原始配置"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def modify_config(enable_viz=True, interval=100):
    """修改配置启用可视化"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    config['SHOW_RETRIEVAL_RESULT'] = enable_viz
    config['TEST_INTERVAL'] = interval

    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False)

    print(f'配置已修改:')
    print(f'  SHOW_RETRIEVAL_RESULT: {enable_viz}')
    print(f'  TEST_INTERVAL: {interval}')

def restore_config(backup):
    """恢复原始配置"""
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        f.write(backup)
    print('配置已恢复')

def run_baseline():
    """运行baseline"""
    print('\n运行baseline...')
    result = subprocess.run(
        ['python', 'Baseline.py'],
        cwd='code',
        capture_output=True,
        text=True
    )
    print(f'返回码: {result.returncode}')
    if result.stdout:
        print(f'输出: {result.stdout[-500:]}')
    if result.stderr:
        print(f'错误: {result.stderr[-500:]}')
    return result.returncode == 0

def main():
    print('=' * 50)
    print('生成可视化截图')
    print('=' * 50)

    # 备份配置
    backup = backup_config()

    try:
        # 修改配置
        modify_config(enable_viz=True, interval=100)

        # 运行baseline
        success = run_baseline()

        if success:
            print('\n✅ 运行成功!')
            print('可视化结果保存在 code/Result/ 目录')
        else:
            print('\n❌ 运行失败')

    finally:
        # 恢复配置
        restore_config(backup)

if __name__ == '__main__':
    main()
