# Paper Notes: Exploring the best way for UAV visual localization under Low-altitude Multi-view Observation Condition: a Benchmark

## 基本信息

- **标题**: Exploring the best way for UAV visual localization under Low-altitude Multi-view Observation Condition: a Benchmark
- **作者**: Yibin Ye, Xichao Teng, Shuo Chen, Leqi Liu, Kun Wang, Xiaokai Song, Zhang Li
- **机构**: National University of Defense Technology, China
- **会议**: CVPR 2026 Findings (pp. 1731–1741)
- **通讯作者**: zhangli_nudt@163.com
- **代码/数据**: https://github.com/UAV-AVL/Benchmark

---

## 1. 核心问题

无人机绝对视觉定位（AVL）在**低空（<300m）多视角（俯仰角 20°–90°）**条件下效果差。现有 AVL 研究主要针对正下视（nadir-view），低空多视角带来极端视角变化，当前方法无法有效处理。

**三断场景**（通信/电力/导航中断）下 GNSS 不可用，视觉定位是关键替代方案。

---

## 2. 三大贡献

### 2.1 AnyVisLoc 数据集

| 维度 | 详情 |
|------|------|
| 图像数量 | 18,000 张无人机图像 + 196 张参考图（124 航空 + 72 卫星） |
| 机型 | 7 种 DJI: Mavic 2, Mavic 3, Mavic 3 Pro, Phantom 3, Phantom 4, Phantom 4 RTK, Mini 4 Pro |
| 城市 | 15 个城市，25 个区域，304 个场景 |
| 飞行高度 | 30m – 300m |
| 俯仰角 | 20° – 90° |
| 航空图分辨率 | 0.02 – 0.35m |
| 卫星图分辨率 | 0.13 – 0.55m |
| 图像分辨率 | 1920×1080 到 5472×3648 |
| 焦距 | 4.5 – 28mm |
| 参考图坐标 | UTM 坐标系 |
| 场景类型 | 密集城市、典型地标、自然场景、混合场景 |

**参考图类型**：
- **航空摄影测量图（Aerial Photogrammetry Map）**: DJI 无人机拍摄 + SfM 技术构建 2D 正射影像 + DSM
- **卫星图（Satellite Map）**: Google Earth 历史图像 + ALOS 30m DSM

**数据集特点**：
- 覆盖多高度、多视角、多场景、多参考图
- 提供 UAV 图像与航空摄影测量图之间的高精度对应关系，可供训练

### 2.2 统一 AVL 框架

Pipeline: **图像检索（粗定位）→ 图像匹配（同源点提取）→ PnP 求解（坐标解算）**

框架可整合不同参考图类型和定位策略，公平对比各方法。

### 2.3 PDM@K 指标

新的检索度量，比 Recall@K 和 SDM@K 更能直接反映最终定位能力。

---

## 3. 关键公式

### 3.1 定位精度指标 A@T

$$A@T = \frac{N_s}{N} \times 100\%$$

定位误差：$e_l = \sqrt{(x_p - x_g)^2 + (y_p - y_g)^2}$，其中 $(x_p, y_p)$ 为预测坐标，$(x_g, y_g)$ 为真值坐标（UTM）。

### 3.2 PDM@K（公式 1）

$$PDM@K = \sum_{i=1}^{K} \frac{(K-i+1) \cdot e^{-\lambda(R_i - \alpha)}}{1 + e^{-\lambda(R_i - \alpha)}} \bigg/ \sum_{i=1}^{K} (K-i+1)$$

- $R_i = d_i / (w_i \cdot r)$：第 i 个检索结果与真值的空间重叠率
  - $d_i$：空间距离
  - $w_i$：gallery 图像宽度
  - $r$：参考图空间分辨率
- λ = 6，α = 0.9（本文设定）
- λ 推荐范围 4–8
- α 应设为略高于 l/2（l 为归一化对角线长度，4:3 图像 l≈1.67）

### 3.3 SDM@K（公式 2，对比指标）

$$SDM@K = \sum_{i=1}^{K} \frac{(K-i+1)}{e^{\lambda(d_i - \alpha)}} \bigg/ \sum_{i=1}^{K} (K-i+1)$$

缺点：依赖空间距离 $d_i$，对参考图分辨率变化敏感，不同参考图间评分不一致。

### 3.4 尺度估计（公式 3）

$$r = \frac{altitude}{\sin(pitch)} \cdot \tan\left(\frac{FOV}{2}\right) \cdot \frac{2}{\sqrt{(w^2 + h^2)}}$$

r = 参考图中每个像素对应的实际空间分辨率。altitude/pitch/FOV 任一有噪声都会导致 r 估计偏差。

---

## 4. 实验配置

### 硬件

- Intel Core i9-10920X CPU @ 3.50GHz, 128GB RAM
- NVIDIA RTX 3090 GPU (24GB)

### 检索模型

- 预训练权重：University-1652 数据集
- 输入尺寸：384 × 384
- Backbone：ConvNeXt（学习方法中表现最好）

### 匹配模型

- 沿用各方法原论文的权重和输入尺寸
- PnP 求解器：P3P + RANSAC（OpenCV 实现）
- SIFT、ORB、PnP solver 均用 OpenCV 实现

### 先验信息

- 使用无人机的高度和俯仰角/偏航角信息来粗略估计图像的尺度和旋转，缩小检索和匹配的搜索空间

---

## 5. 检索方法对比（Table 2 + Table 3）

### 5.1 检索精度（Table 2）

| 方法 | R@1 | R@5 | P@1 | P@5 | ms/iter |
|------|-----|-----|-----|-----|---------|
| NCC | 0.1 | 0.6 | 0.033 | 0.020 | - |
| MI | 2.4 | 8.6 | 0.523 | 0.323 | 201 |
| NetVLAD | 31.7 | 61.9 | 0.741 | 0.652 | 11 |
| LPN | 41.1 | 70.4 | 0.799 | 0.665 | 5 |
| RK-Net | 45.3 | 76.1 | 0.848 | 0.712 | 5 |
| RDE | 52.3 | 77.7 | 0.854 | 0.754 | 9 |
| DenseUAV | 51.6 | 76.4 | 0.854 | 0.754 | 6 |
| MEAN | 48.0 | 77.1 | 0.846 | 0.684 | 4 |
| LRFR | 53.4 | 80.6 | 0.852 | 0.750 | 5 |
| QDFL | 56.0 | 80.0 | 0.879 | 0.773 | 20 |
| DAC | 58.3 | 84.4 | 0.899 | 0.733 | 8 |
| **MCCG** | **80.5** | **88.6** | **0.901** | **0.779** | 6 |
| Sample4Geo | 76.7 | 88.4 | 0.900 | 0.760 | 13 |
| **CAMP** | **82.7** | **88.8** | **0.920** | **0.768** | 6 |

**关键发现**：
- 手工方法（NCC、MI）表现最差，对视角变化敏感
- 学习方法用 ConvNeXt backbone 更好
- MCCG 优化网络结构（cross-dimensional interaction + multi-classifier）
- CAMP 通过同一 training batch 内比较同一平台不同场景增加负样本
- DenseUAV 专为 AVL 设计但多视角下表现差（为 nadir-view 训练）

### 5.2 定位精度（Table 3，CAMP 检索 + 不同匹配/策略）

| 方法 | Top1+SP:LG A@5m | Top1+RoMa A@5m | Top5 RR+SP:LG A@5m | Top5 RR+RoMa A@5m |
|------|-----------------|----------------|---------------------|---------------------|
| NCC | 7.5 | 10.8 | 16.5 | 22.4 |
| MI | 13.6 | 18.3 | 28.9 | 36.4 |
| NetVLAD | 41.7 | 49.3 | 55.0 | 64.3 |
| LPN | 43.6 | 54.1 | 57.1 | 66.8 |
| RK-Net | 49.9 | 62.2 | 60.0 | 68.6 |
| FSRA | 51.6 | 64.9 | 60.7 | 71.7 |
| DenseUAV | 49.7 | 61.7 | 59.0 | 70.3 |
| MEAN | 48.8 | 59.8 | 59.0 | 70.2 |
| LRFR | 51.6 | 63.1 | 60.0 | 71.4 |
| QDFL | 55.1 | 67.5 | 62.4 | 73.0 |
| DAC | 53.4 | 66.9 | 62.2 | 72.7 |
| MCCG | 54.9 | 68.2 | 63.1 | 72.7 |
| Sample4Geo | 54.1 | 66.9 | 62.4 | 73.2 |
| **CAMP** | **55.8** | **70.1** | **62.4** | **74.6** |

CAMP + RoMa + Top5 Re-rank = 最佳组合

---

## 6. 匹配方法对比（Table 4，CAMP 检索）

### 6.1 完整对比（19 种方法）

| 方法 | 类型 | A@5m | A@10m | A@20m | ms/frame |
|------|------|------|-------|-------|----------|
| SIFT | 稀疏/手工 | 43.9 | 55.7 | 62.5 | 316 |
| ORB | 稀疏/手工 | 3.9 | 8.0 | 13.6 | 441 |
| D2Net | 稀疏/学习 | 27.3 | 51.6 | 68.6 | 4083 |
| ALIKE | 稀疏/学习 | 27.7 | 34.8 | 39.6 | 268 |
| XoFTR | 稀疏/学习 | 27.7 | 44.9 | 62.1 | 116 |
| LiFFeat | 稀疏/学习 | 30.3 | 47.3 | 59.1 | 40 |
| SP+SG | 稀疏/学习 | 52.1 | 71.7 | 80.9 | 92 |
| SP+SG+Omni | 稀疏/学习 | 45.3 | 64.2 | 76.1 | 3116† |
| SP+LG | 稀疏/学习 | 46.0 | 66.0 | 78.3 | 66 |
| SP+LG_CIM | 稀疏/学习 | 55.0 | 71.1 | 82.5 | 74 |
| SP+LG_CIM+k2s | 稀疏/学习 | 55.8 | 75.0 | 85.1 | 75 |
| XoFTR_MINIMA | 稀疏/学习 | 48.3 | 60.2 | 65.8 | 68 |
| LoFTR_MINIMA | 稀疏/学习 | 59.5 | 74.1 | 81.6 | 165 |
| DeDoDe | 稀疏/学习 | 51.4 | 69.9 | 80.4 | 78 |
| DKM_MINIMA | 密集/学习 | 61.6 | 80.2 | 86.4 | 4915 |
| RoMa_MINIMA | 密集/学习 | 60.3 | 71.4 | 76.2 | 495 |
| RoMa | 密集/学习 | **70.1** | **81.3** | **87.6** | 653 |

† 表示在 CPU 上运行

**关键发现**：
- **RoMa** 精度最高（A@5m=70.1），但速度 659ms
- **SP+LG_CIM+k2s** 速度是 RoMa 的 **8.9 倍**（74ms vs 659ms），精度略低（55.8 vs 70.1）
- **ORB** 几乎不可用（A@5m=3.9），对视角变化极敏感
- **DeDoDe** 未达到好的速度-精度平衡
- 密集方法精度 > 稀疏方法，但计算效率更低
- 学习方法普遍优于手工方法

---

## 7. 定位策略对比（Table 5，CAMP + SP+LG_CIM+k2s）

| 策略 | A@5m | A@10m | A@20m | ms/frame | 内存 |
|------|------|-------|-------|----------|------|
| Matching-wo-Retrieval [61] | 34.3 | 45.7 | 54.3 | 1.4 | Large |
| Top1 Matching [58] | 55.8 | 74.3 | 84.0 | 0.3 | Medium |
| Top5 Re-rank (N=5) [9] | 62.2 | 82.4 | 91.5 | 0.8 | Medium |
| Most Inliers [23] | **64.0** | **83.2** | **92.6** | 10.2 | Small |

**结论**：Most Inliers 精度最高但计算量大。Top5 Re-rank 综合最优（精度、速度、内存平衡）。

---

## 8. 参考图对比（Table 6）

| 参考图 | 分辨率 (Avg) | DSM | R@1 | P@1 | A@5m | A@10m | A@20m |
|--------|-------------|-----|-----|-----|------|-------|-------|
| 航空图 | 0.070m | 0.947m | 61.6 | 0.922 | **74.1** | **87.7** | **94.2** |
| 卫星图 | 0.197m | 30m | 42.8 | 0.814 | 18.5 | 38.7 | 58.5 |

**关键发现**：
- 卫星图精度远低于航空图（5m 内 18.5% vs 74.1%）
- 原因：①分辨率低（尤其 DSM 30m vs 0.02m）②时相/模态差异
- 航空图需要预先摄影测量和 3D 建模，对时间敏感任务（应急救援）不太适用
- 卫星图作为航空图不可用时的替代

---

## 9. 影响因素分析

### 9.1 俯仰角（Figure 7）

- 俯仰角越小（越倾斜），精度越差
- 原因：倾斜视角捕捉 3D 物体侧面信息，与正射参考图的全局/局部相似性降低

### 9.2 先验信息噪声（Table 7）

**Yaw 噪声**：

| Std | A@5m (±std) | A@10m | A@20m |
|-----|-------------|-------|-------|
| 0° | 74.6 | 87.6 | 94.2 |
| 5° | 74.3 (±0.3) | 86.3 | 93.2 |
| 10° | 72.7 (±1.9) | 86.4 | 92.8 |
| 20° | 72.4 (±2.2) | 86.4 | 93.6 |
| 30° | 70.5 (±4.1) | 83.5 | 90.2 |
| 50° | 60.9 (±13.7) | 72.8 | 79.5 |
| 60° | 48.9 (±25.7) | 63.0 | 70.0 |

- std > 10° 时检索和匹配精度显著下降
- std = 30° 时 A@5m 下降 4.1%，std = 60° 时下降 25.7%
- 大 std 时方差急剧增大（60° 时 ±25.7），说明定位极不稳定

**Pitch 噪声**：

| Std | A@5m (±std) | A@10m | A@20m |
|-----|-------------|-------|-------|
| 0° | 74.6 | 87.6 | 94.2 |
| 3° | 73.9 (±0.7) | 87.2 | 94.2 |
| 5° | 73.9 (±0.7) | 87.1 | 93.2 |
| 7° | 73.3 (±1.3) | 87.3 | 93.4 |
| 10° | 72.1 (±2.5) | 86.5 | 92.2 |
| 20° | 71.6 (±3.0) | 86.2 | 92.9 |
| 30° | 69.7 (±4.9) | 83.7 | 90.4 |

- std < 5° 影响极小
- std > 7° 时尺度差异导致检索和匹配困难，A@5m 下降 4.9%（std=30°）
- Pitch 噪声比 Yaw 噪声影响小（同 std 下 A@5m 下降更少）

### 9.3 高度噪声

论文说影响小，详见附录（本文未包含附录内容）。

---

## 10. 失败模式（Figure 6）

1. **倾斜视角检索失败**: 俯仰角小时，侧视图捕捉 3D 物体侧面信息，与正射参考图差异大，Top5 检索结果全部错误
2. **参考图时相/模态差异**: 航空图 vs 卫星图的时间和传感器差异导致匹配困难
3. **未配准场景**: 参考图未配准时检索精度极差（R@1=45.8, P@1=0.014）

---

## 11. 最佳组合总结

**CAMP（检索）+ RoMa（匹配）+ Top N Re-rank（定位策略）**

- A@5m = **74.1%**（航空图）
- A@20m = **94.2%**（航空图）
- 在卫星图上 A@5m 仅 16.5%

---

## 12. 局限性与未来方向

1. 5m 内精度 74.1% 未达到精确 AVL 要求
2. 低空多视角条件仍是挑战
3. 航空图需要预先建模，不适用于所有场景
4. 密集匹配方法计算效率低
5. 先验信息噪声（尤其 yaw > 10°）显著影响精度

---

## 13. 对本项目的启示

### 复现重点

1. **环境搭建**: Python 3.10+, PyTorch, CUDA, OpenCV
2. **数据集获取**: AnyVisLoc (GitHub: UAV-AVL/Benchmark)
3. **预训练权重**: University-1652 (检索), 各匹配方法原论文权重
4. **核心依赖**: ConvNeXt (backbone), CAMP, RoMa, OpenCV PnP

### 水面场景特殊考虑

1. 水面弱纹理 → 检索和匹配更难
2. 动态背景（波浪）→ 特征不稳定
3. 目标尺度变化 → 需要多尺度处理
4. 应急救援 → 可能无法使用航空图，需依赖卫星图
5. 双光融合 → 可能需要红外+可见光的跨模态检索/匹配

---

## 14. 方法缩写对照

| 缩写 | 全称 | 出处 |
|------|------|------|
| MINIMA | Modality Invariant Image Matching | Ren et al., CVPR 2025 |
| GIM | Generalizable Image Matcher | Shen et al., ICLR 2024 |
| k2s | sub-pixel keypoint learning | Kim et al., ECCV 2024 |
| SG | SuperGlue | Sarlin et al., CVPR 2020 |
| LG | LightGlue | Lindenberger et al., ICCV 2023 |
| SP | SuperPoint | DeTone et al., CVPRw 2018 |
| Omni | OmniGlue | Jiang et al., CVPR 2024 |

---

## 15. 数据集对比（Table 1）

| 名称 | 年份 | UAV 数据 | 机型数 | UAV 位置 | 2D 参考图 | DSM | 飞行高度 | 观测方式 | 场景 | 时相 |
|------|------|----------|--------|----------|-----------|-----|----------|----------|------|------|
| ATM [37] | 2021 | 真实 | 1 | ✓ | Aerial | ✗ | unknown | Nadir-view | Urban | Multiple |
| University-1652 [63] | 2021 | 合成 | - | ✗ | Satellite | ✗ | 121.5–256m | Multi-view | Buildings | - |
| WildNav [23] | 2022 | 合成 | - | ✗ | Satellite | ✗ | unknown | Nadir-view | Wilderness | - |
| VPAIR [42] | 2022 | 真实 | 1 | ✓ | Satellite | ✓ | 300–400m | Nadir-view | Multiple | - |
| SEUS-200 [65] | 2023 | 真实 | - | ✗ | Satellite | ✗ | 150/200/250/300m | Multi-view | Urban | - |
| DenseUAV [14] | 2024 | 真实 | 1 | ✓ | Satellite | ✗ | 80/90/100m | Nadir-view | Urban | Multiple |
| UAVD4L [54] | 2024 | 真实 | 1 | ✓ | Aerial | ✓ | 50–151m | Multi-view | Urban | - |
| UAV-VisLoc [56] | 2024 | 真实 | unknown | ✓ | Satellite | ✗ | 400–2000m | Nadir-view | Multiple | Multiple |
| GTA-UAV [27] | 2025 | 合成 | - | ✓ | Satellite | ✗ | 80–650m | Near nadir-view | Multiple | - |
| CVGL-RGBT [64] | 2025 | 真实 | 1 | ✓ | Satellite | ✗ | unknown | Multi-view | Multiple | Multiple |
| **AnyVisLoc (Ours)** | **2026** | **真实** | **7** | **✓** | **Aerial & Satellite** | **✓** | **30–300m** | **Multi-view** | **Multiple** | **Multiple** |

AnyVisLoc 是唯一同时提供航空+卫星参考图、DSM、多高度、多视角、多时相的数据集。
