# 第五章素材汇总

> 《水面目标精准定位技术报告》第五章「实验验证与结果分析」全部素材
> 归类时间：2026-06-23

---

## 目录结构

```
5all素材/
├── 实验数据/          ← 12个文件：CSV原始数据 + JSON + Markdown表格
├── 图表/              ← 16张图：7张论文图 + 9张辅助图
├── 参考文献/          ← 2个文件：论文笔记 + Gemini参考文本
├── 报告/              ← 2个文件：第五章v5 docx + 素材清单
├── 脚本/              ← 6个文件：图表生成Python脚本
└── 配置/              ← 3个文件：实验配置 + 区域参数 + 元数据JSON
```

---

## 实验数据（12个文件）

| 文件 | 内容 | 用途 |
|------|------|------|
| `第五章表格数据.md` | 表5-1~5-12 完整Markdown | **直接复制到报告** |
| `统计报告.md` | 9节统计分析 + 一致性校验 | 数据核对参考 |
| `tables_data.json` | 表格数据JSON格式 | 程序化处理 |
| `results_HIGH.csv` | 航空图487张逐图结果 | 原始数据 |
| `results_LOW.csv` | 卫星图487张逐图结果 | 原始数据 |
| `results_Top1.csv` | Top1策略487张结果 | 原始数据 |
| `results_MostInliers.csv` | Most Inliers策略487张结果 | 原始数据 |
| `results_SIFT.csv` | SIFT匹配487张结果 | 原始数据 |
| `results_all.csv` | 全部实验结果汇总 | 原始数据 |
| `all_results.csv` | 全部结果（含元数据） | 原始数据 |
| `pitch_bucket_stats.csv` | 俯仰角分桶统计 | 统计数据 |
| `alt_bucket_stats.csv` | 高度分桶统计 | 统计数据 |

---

## 图表（16张）

### 论文图（7张，300dpi高清）

| 文件 | 图号 | 内容 | 大小 |
|------|------|------|------|
| `fig5_1_sample_images.png` | 图5-1 | 测试区域样例（3场景UAV+参考地图） | 6.5MB |
| `fig5_3_pipeline.png` | 图5-3 | 完整流程可视化（查询→候选→匹配→PnP） | 13.5MB |
| `fig5_4_high_vs_low.png` | 图5-4 | 航空图vs卫星图对比 | 170KB |
| `fig5_5_height_pitch_analysis.png` | 图5-5 | 高度/视角分组分析 | 251KB |
| `fig5_6_strategy_matching.png` | 图5-6 | 策略/匹配/噪声三子图 | 313KB |
| `fig5_7_error_propagation.png` | 图5-7 | 检测→定位误差传播链路 | 154KB |
| `fig5_8_success_failure.png` | 图5-8 | 成功/失败案例可视化 | 11.4MB |

### 辅助图（9张）

| 文件 | 内容 | 大小 |
|------|------|------|
| `error_histogram.png` | 误差分布直方图 | 55KB |
| `error_cdf.png` | 误差CDF曲线 | 62KB |
| `pitch_impact.png` | 俯仰角影响曲线 | 173KB |
| `scene_comparison.png` | 分场景对比图 | 132KB |
| `strategy_comparison.png` | 策略对比柱状图 | 100KB |
| `matching_comparison.png` | 匹配方法对比图 | 119KB |
| `overall_comparison.png` | 总体对比图 | 109KB |
| `ref_map_comparison.png` | 参考地图对比图 | 91KB |
| `dsm_example.png` | DSM高程图示例 | 395KB |

---

## 参考文献（2个文件）

| 文件 | 内容 | 用途 |
|------|------|------|
| `notes.md` | 论文笔记（359行，15节） | 公式、表格、失败模式、数据集对比 |
| `gemini_reference_ch1_4.md` | Gemini生成的前四章参考文本 | 第五章引用的背景内容 |

---

## 报告（2个文件）

| 文件 | 内容 | 用途 |
|------|------|------|
| `第五章_实验验证与结果分析_poi-tl_v5.docx` | 第五章当前最新版 | 正文基础 |
| `素材清单.md` | 素材完整度 + 格式优化待办 | 参考 |

---

## 脚本（6个文件）

| 文件 | 内容 | 用途 |
|------|------|------|
| `generate_a_figures_v2.py` | 生成A类图表（fig5-1/4/5/6） | 图表生成 |
| `generate_b_type_figures.py` | 生成B类图表（fig5-3/8，需GPU） | 图表生成 |
| `generate_ch5_figures.py` | 第五章图表汇总生成 | 图表生成 |
| `generate_charts.py` | 辅助图表生成 | 图表生成 |
| `generate_fig5_1.py` | 图5-1测试区域样例生成 | 图表生成 |
| `generate_case_screenshots.py` | 成功/失败案例截图 | 图表生成 |

---

## 配置（3个文件）

| 文件 | 内容 | 用途 |
|------|------|------|
| `config.yaml` | 全局实验配置 | 参数参考 |
| `QZ_Town.yaml` | 青州古镇区域参数 | 分辨率/坐标系参考 |
| `QZ_Town.json` | 487张UAV图元数据 | GPS/姿态/相机参数 |
