"""
从pkl实验结果文件中提取数据，生成CSV、聚合分析和图表。
输出:
  - 素材/实验数据/results_HIGH.csv, results_LOW.csv
  - 素材/实验数据/alt_bucket_stats.csv, pitch_bucket_stats.csv
  - 素材/截图/error_histogram.png, error_cdf.png
"""
from __future__ import annotations

import pickle
import csv
import re
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from collections import defaultdict

# ---- 路径配置 ----
BASE_DIR = Path(__file__).parent
RESULT_DIR = BASE_DIR / "Result"
OUTPUT_DATA = BASE_DIR / "素材" / "实验数据"
OUTPUT_IMG = BASE_DIR / "素材" / "截图"

OUTPUT_DATA.mkdir(parents=True, exist_ok=True)
OUTPUT_IMG.mkdir(parents=True, exist_ok=True)


def parse_folder_name(folder_name: str) -> dict:
    """
    从文件夹名解析 ref_type 和 matching_method。
    格式: {ref_type}-CAMP-{matching_method}-yp
    例如: HIGH-CAMP-Roma-yp -> ref_type=HIGH, matching_method=Roma
    """
    parts = folder_name.split("-")
    if len(parts) >= 3:
        return {
            "ref_type": parts[0],       # HIGH or LOW
            "matching_method": parts[2]  # Roma, SIFT, etc.
        }
    return {"ref_type": "UNKNOWN", "matching_method": "UNKNOWN"}


def infer_strategy_from_path(pkl_path: Path) -> str:
    """从实验目录名推断 strategy。"""
    path_str = str(pkl_path)
    if "Strategy_Top1" in path_str:
        return "Top1"
    elif "Strategy_Inliners" in path_str:
        return "Inliners"
    else:
        # Experiment1, Experiment1_HIGH, Experiment1_LOW, Matching_SIFT -> TopN_Re-rank
        return "TopN_Re-rank"


def extract_one_pkl(pkl_path: Path) -> dict | None:
    """从单个pkl文件提取所需字段，失败返回None。"""
    try:
        with open(pkl_path, "rb") as f:
            data = pickle.load(f)
    except Exception as e:
        print(f"  [WARN] 无法读取 {pkl_path.name}: {e}")
        return None

    truePos = data.get("truePos", {})
    pred_error = data.get("pred_error", None)
    inliners = data.get("inliners", [])
    opt = data.get("opt", None)

    # 从pkl的opt中获取ref_type（比从目录名推断更可靠）
    ref_type = getattr(opt, "Ref_type", None)

    # matching_method 从目录名推断（opt中没有此字段）
    # 文件夹名是pkl所在目录的父级目录名 (如 HIGH-CAMP-Roma-yp)
    folder_name = pkl_path.parent.name
    folder_info = parse_folder_name(folder_name)
    matching_method = folder_info["matching_method"]

    # 如果opt中没有ref_type，从目录名回退
    if ref_type is None:
        ref_type = folder_info["ref_type"]

    # strategy 从实验目录名推断
    strategy = infer_strategy_from_path(pkl_path)

    # image_name: 去掉扩展名
    image_name = pkl_path.stem + ".JPG"  # 统一为JPG后缀

    # scene: 从路径中提取数据集名（pkl_QingZhou_2024 等）
    parts = pkl_path.parts
    scene = "UNKNOWN"
    for part in parts:
        if part.startswith("pkl_"):
            scene = part
            break

    # 从truePos提取
    pitch = truePos.get("pitch", None)
    yaw = truePos.get("yaw", None)
    altitude = truePos.get("rel_alt", None)

    # inlier_count: 对于TopN_Re-rank取max，对于Top1/Inliners取第一个
    if isinstance(inliners, (list, np.ndarray)) and len(inliners) > 0:
        inlier_count = int(max(inliners))
    else:
        inlier_count = 0

    return {
        "image_name": image_name,
        "scene": scene,
        "pitch": pitch,
        "yaw": yaw,
        "altitude": altitude,
        "pred_error": float(pred_error) if pred_error is not None else None,
        "ref_type": ref_type,
        "strategy": strategy,
        "matching_method": matching_method,
        "inlier_count": inlier_count,
    }


def extract_all_csv():
    """Step 1: 遍历所有pkl，提取并写入CSV。"""
    print("=" * 60)
    print("Step 1: 提取CSV")
    print("=" * 60)

    pkls = sorted(RESULT_DIR.rglob("*.pkl"))
    print(f"找到 {len(pkls)} 个pkl文件")

    rows_high = []
    rows_low = []
    errors = 0

    for i, pkl_path in enumerate(pkls):
        if (i + 1) % 200 == 0:
            print(f"  处理中... {i+1}/{len(pkls)}")

        row = extract_one_pkl(pkl_path)
        if row is None:
            errors += 1
            continue

        if row["ref_type"] == "HIGH":
            rows_high.append(row)
        elif row["ref_type"] == "LOW":
            rows_low.append(row)
        else:
            # 默认归到HIGH
            rows_high.append(row)

    # 写CSV
    fieldnames = [
        "image_name", "scene", "pitch", "yaw", "altitude",
        "pred_error", "ref_type", "strategy", "matching_method", "inlier_count"
    ]

    for fname, rows in [("results_HIGH.csv", rows_high), ("results_LOW.csv", rows_low)]:
        out_path = OUTPUT_DATA / fname
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        print(f"  写入 {out_path}: {len(rows)} 行")

    print(f"  成功: {len(rows_high) + len(rows_low)}, 失败: {errors}")
    return rows_high, rows_low


def accuracy_at(errors, threshold):
    """计算 A@threshold (误差 <= threshold 的比例)。"""
    if len(errors) == 0:
        return 0.0
    return 100.0 * np.sum(np.array(errors) <= threshold) / len(errors)


def aggregate(rows, bins, bin_label_fn, group_name):
    """
    通用聚合函数。
    rows: list of dict
    bins: 分桶边界 (升序)
    bin_label_fn: 函数(bin_edges) -> label
    group_name: 用于打印
    """
    # 过滤掉None值
    valid_rows = [r for r in rows if r["pred_error"] is not None]

    # 按 strategy+matching_method 分组
    groups = defaultdict(list)
    for r in valid_rows:
        key = (r["strategy"], r["matching_method"])
        groups[key].append(r)

    all_stats = []

    for (strategy, matching), group_rows in sorted(groups.items()):
        print(f"\n  {group_name} | {strategy} / {matching}: {len(group_rows)} 条记录")

        for i in range(len(bins) - 1):
            lo, hi = bins[i], bins[i + 1]
            label = bin_label_fn(lo, hi)

            # 筛选该桶的行
            bucket_rows = []
            for r in group_rows:
                val = r[group_name]
                if val is not None and lo <= val < hi:
                    bucket_rows.append(r)

            if len(bucket_rows) == 0:
                all_stats.append({
                    "strategy": strategy,
                    "matching_method": matching,
                    "bin": label,
                    "count": 0,
                    "A@5m": None,
                    "A@10m": None,
                    "A@20m": None,
                    "mean_error": None,
                    "median_error": None,
                })
                continue

            errors = [r["pred_error"] for r in bucket_rows]
            a5 = accuracy_at(errors, 5)
            a10 = accuracy_at(errors, 10)
            a20 = accuracy_at(errors, 20)
            # 过滤inf/nan后再计算均值
            finite_errors = [e for e in errors if np.isfinite(e)]
            mean_err = np.mean(finite_errors) if finite_errors else float('inf')
            median_err = np.median(errors)

            all_stats.append({
                "strategy": strategy,
                "matching_method": matching,
                "bin": label,
                "count": len(bucket_rows),
                "A@5m": round(a5, 1),
                "A@10m": round(a10, 1),
                "A@20m": round(a20, 1),
                "mean_error": round(mean_err, 1),
                "median_error": round(median_err, 1),
            })

            print(f"    {label}: n={len(bucket_rows)}, A@5m={a5:.1f}%, A@10m={a10:.1f}%, A@20m={a20:.1f}%, mean={mean_err:.1f}m, median={median_err:.1f}m")

    return all_stats


def write_stats(stats, fname):
    """写入聚合统计CSV。"""
    if not stats:
        print(f"  [WARN] 无统计数据可写: {fname}")
        return

    fieldnames = ["strategy", "matching_method", "bin", "count", "A@5m", "A@10m", "A@20m", "mean_error", "median_error"]
    out_path = OUTPUT_DATA / fname
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in stats:
            writer.writerow(row)
    print(f"  写入 {out_path}")


def annotate_pitch_bins(stats):
    """D3: 在俯仰角分桶结果中标注样本量不足的桶。"""
    notes = []
    seen = set()
    for s in stats:
        if s["count"] > 0 and s["count"] < 30 and s["bin"] not in seen:
            note = f'{s["bin"]} 仅{s["count"]}张，统计意义有限'
            notes.append(note)
            seen.add(s["bin"])
    return notes


def generate_charts(rows_high, rows_low):
    """Step 3: 生成误差分布直方图和CDF曲线。"""
    print("\n" + "=" * 60)
    print("Step 3: 生成图表")
    print("=" * 60)

    all_errors = []
    for r in rows_high + rows_low:
        if r["pred_error"] is not None:
            all_errors.append(r["pred_error"])

    errors = np.array(all_errors)
    # 过滤inf/nan
    errors = errors[np.isfinite(errors)]
    print(f"  总样本数: {len(errors)}")

    # 过滤极端值用于可视化（保留99%的数据范围）
    p99 = np.percentile(errors, 99)
    errors_clipped = errors[errors <= p99]

    # ---- G1: 误差分布直方图 ----
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(errors_clipped, bins=50, edgecolor="black", alpha=0.7, color="steelblue")
    ax.set_xlabel("Localization Error (m)", fontsize=13)
    ax.set_ylabel("Count", fontsize=13)
    ax.set_title("Error Distribution Histogram", fontsize=15)
    ax.axvline(x=5, color="red", linestyle="--", alpha=0.7, label="5m threshold")
    ax.axvline(x=10, color="orange", linestyle="--", alpha=0.7, label="10m threshold")
    ax.axvline(x=20, color="green", linestyle="--", alpha=0.7, label="20m threshold")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    out_path = OUTPUT_IMG / "error_histogram.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  G1 直方图已保存: {out_path}")

    # ---- G2: 误差CDF曲线 ----
    sorted_errors = np.sort(errors)
    cdf = np.arange(1, len(sorted_errors) + 1) / len(sorted_errors)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(sorted_errors, cdf, color="steelblue", linewidth=2)
    ax.set_xlabel("Localization Error (m)", fontsize=13)
    ax.set_ylabel("Cumulative Probability", fontsize=13)
    ax.set_title("Error CDF Curve", fontsize=15)
    ax.axhline(y=0.5, color="gray", linestyle=":", alpha=0.5)
    ax.axvline(x=np.median(errors), color="red", linestyle="--", alpha=0.7,
               label=f"Median = {np.median(errors):.1f}m")

    # 标注 A@5m, A@10m, A@20m
    for threshold, color in [(5, "red"), (10, "orange"), (20, "green")]:
        acc = accuracy_at(errors, threshold)
        ax.axvline(x=threshold, color=color, linestyle="--", alpha=0.5)
        ax.annotate(f"A@{threshold}m = {acc:.1f}%",
                     xy=(threshold, acc / 100), fontsize=10,
                     xytext=(threshold + 5, acc / 100 - 0.05),
                     arrowprops=dict(arrowstyle="->", color=color),
                     color=color)

    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, p99)
    plt.tight_layout()
    out_path = OUTPUT_IMG / "error_cdf.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  G2 CDF曲线已保存: {out_path}")


def main():
    print("开始提取pkl实验数据...\n")

    # D1: 提取CSV
    rows_high, rows_low = extract_all_csv()
    all_rows = rows_high + rows_low

    # D2: 聚合分析
    print("\n" + "=" * 60)
    print("Step 2: 聚合分析")
    print("=" * 60)

    # 高度分桶: bins=[30,100,200,300]
    alt_bins = [0, 30, 100, 200, 300, 10000]
    alt_label_fn = lambda lo, hi: f"{lo}-{hi}m" if hi < 10000 else f"{lo}m+"
    print("\n--- 高度分桶 ---")
    alt_stats = aggregate(all_rows, alt_bins, alt_label_fn, "altitude")
    write_stats(alt_stats, "alt_bucket_stats.csv")

    # 俯仰角分桶 (注意：pitch是负值，向下为负)
    # 用角度绝对值分桶: 70-90°(正下视), 50-70°(过渡), 20-50°(倾斜), 0-20°(近水平)
    # pitch -90~-70 对应 70~90°, -70~-50 对应 50~70°, -50~-20 对应 20~50°, -20~0 对应 0~20°
    pitch_bins = [-90, -70, -50, -20, 0]
    PITCH_LABELS = {
        (-90, -70): "70-90°(正下视)",
        (-70, -50): "50-70°(过渡)",
        (-50, -20): "20-50°(倾斜)",
        (-20, 0):   "0-20°(近水平)",
    }
    def pitch_label_fn(lo, hi):
        return PITCH_LABELS.get((lo, hi), f"{lo}~{hi}°")

    print("\n--- 俯仰角分桶 ---")
    pitch_stats = aggregate(all_rows, pitch_bins, pitch_label_fn, "pitch")
    write_stats(pitch_stats, "pitch_bucket_stats.csv")

    # D3: 标注样本量不足的桶
    notes = annotate_pitch_bins(pitch_stats)
    if notes:
        print("\n--- D3 标注 ---")
        for note in notes:
            print(f"  [!] {note}")

    # G1/G2: 图表
    generate_charts(rows_high, rows_low)

    print("\n" + "=" * 60)
    print("全部完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
