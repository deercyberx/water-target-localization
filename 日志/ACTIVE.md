# ACTIVE.md

> 当前会话焦点。每次新对话第一个读取此文件。

---

## 当前阶段

Round 6 — GitHub仓库清理完成，项目文件整理完毕

## 当前任务

GitHub仓库已清理完成，删除了75个垃圾文件，保留185个核心文件

## 已完成

- [x] 论文深度阅读和笔记
- [x] 代码 clone 和结构分析
- [x] 实验流程梳理
- [x] 搭建 Python 环境（Python 3.9 / PyTorch 2.2.1+cu121 / CUDA 12.1）
- [x] 下载并部署权重（CAMP + RoMa + DINOv2）
- [x] 下载并解压数据集（青州古镇 1/25，487 张）
- [x] 运行 Baseline.py 验证 pipeline
- [x] 航空图 HIGH 完整实验（487 张，A@5m=82.3%）
- [x] 解决 GPU OOM 问题（降低 RoMa 分辨率 coarse_res 560→280）
- [x] 卫星图 LOW 完整实验（487 张，A@5m=13.6%）
- [x] 定位策略对比实验（Top1 / Top N Re-rank / Most Inliers）
- [x] 俯仰角影响分析
- [x] 匹配方法对比实验（RoMa vs SIFT）
- [x] 收集报告素材（论文 + 微信文章 + Gemini 参考文本）
- [x] 生成第五章全部图表素材（7张图+12张表数据）
- [x] 更新素材清单（从"缺失"更新为"齐全"）
- [x] 撰写第五章初稿（12张表+7张图+完整正文）
- [x] 第五章迭代到 v5（poi-tl 格式化 + 表格优化）
- [x] 安装 nature-skills 8个技能（nature-reader/paper2ppt/polishing/figure/writing/citation/reviewer/response）
- [x] 第五章 Nature 风格润色（中文版，保留原文）
- [x] 二次润色（优化句式、段落逻辑、精确对冲）
- [x] 对齐检查（与提纲 v1 逐节对比，全部对齐）
- [x] 修正 5.9 节检测框类型描述
- [x] 生成 v2_polished.docx（保留表格、图片、格式）
- [x] Nature Reviewer 评审（3份审稿报告 + 综合意见）
- [x] Nature Response 回复（修复公式、样本选择标准、技术细节）
- [x] 子代理审核（6项检查全部通过）

## 下一步

1. 格式优化（目录、分节、样式等）
2. 内容补充（可选：PDM@K公式、噪声量化数据等）
3. 撰写第六章正文
4. 更新README.md目录结构（反映当前实际文件）

## 阻塞项

（暂无）

## 待决策

1. 是否需要补充可选内容（S1-S25）？
2. 是否直接开始撰写第六章？
3. 格式优化优先级（目录、分节、样式等）？

## 关键上下文

- 论文: CVPR 2026 Findings — UAV 低空多视角绝对视觉定位 benchmark
- 最佳组合: CAMP（检索）+ RoMa（匹配）+ Top N Re-rank
- 实际硬件: RTX 3080 (10GB) + Python 3.9 + PyTorch 2.2.1+cu121
- GPU 优化: RoMa coarse_res 从 560 降到 280，显存从 ~4GB 降到 ~0.4GB
- 代码: code/ 目录，.venv 在 .venv/（项目根目录）
- 数据集: code/Data/（487 张 UAV 图，3 场景）
- 本项目目标: 在论文框架上适配水面应急救援场景
- 报告素材来源: 论文笔记 + 微信公众号文章 + Gemini 3.1 Pro 参考文本
- 报告目标: 北京市航空智能遥感装备工程技术研究中心结题验收
- 第五章最新版: reports/第五章_实验验证与结果分析_v2_polished.docx
- 第五章润色版: reports/第五章_实验验证与结果分析_v2_polished.docx（Nature风格润色+审稿意见修改）
- 素材清单: reports/素材清单.md（已更新为当前状态）
- 表格数据: 素材/实验数据/第五章表格数据.md
- 图片素材: 素材/截图/fig5_*.png（7张）
- GitHub仓库: https://github.com/deercyberx/water-target-localization.git
- 仓库状态: 已清理，185个核心文件，无垃圾文件
