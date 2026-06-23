# CONTEXT.md

> 项目核心信息。结构稳定，仅在关键信息变化时更新。

---

## 论文信息

- **论文名称**: Exploring the best way for UAV visual localization under Low-altitude Multi-view Observation Condition: a Benchmark
- **作者**: Yibin Ye, Xichao Teng, Shuo Chen, Leqi Liu, Kun Wang, Xiaokai Song, Zhang Li (National University of Defense Technology, China)
- **会议**: CVPR 2026 Findings (pp. 1731–1741)
- **核心问题**: 无人机在低空（<300m）多视角（俯仰角 20°–90°）条件下做绝对视觉定位（AVL），现有方法主要针对正下视，多视角场景下效果差
- **论文方案**: 统一 AVL 框架 = 图像检索（粗定位）→ 图像匹配（同源点提取）→ PnP 求解（坐标解算）；提出 PDM@K 检索指标；构建 AnyVisLoc 数据集
- **论文 PDF**: paper/Ye_Exploring_the_best_way_for_UAV_visual_localization_under_Low-altitude_CVPRF_2026_paper.pdf
- **代码/数据**: https://github.com/UAV-AVL/Benchmark

## 技术路线

```
UAV 图像 → 图像检索（CAMP, 粗定位候选区域）
         → 图像匹配（RoMa, 提取 2D-2D 同源点对）
         → PnP 求解（P3P + RANSAC, 结合 DSM 数据计算地理坐标）
         → 输出: UAV 经纬度
```

最佳组合: **CAMP（检索）+ RoMa（匹配）+ Top N Re-rank（定位策略）**
- A@5m = 74.1%（航空图），A@20m = 94.2%

## 模型结构

### 检索模型（CAMP）

| 组件 | 说明 |
|------|------|
| 输入 | 384 × 384 无人机图像 |
| Backbone | ConvNeXt |
| 预训练 | University-1652 数据集权重 |
| 核心思想 | 同一 training batch 内比较同一平台不同场景，增加负样本用于对比学习 |
| 速度 | 6 ms/iter |

### 匹配模型（RoMa）

| 组件 | 说明 |
|------|------|
| 输入 | UAV 图像 + 参考图 patch |
| 类型 | 密集匹配（dense matching） |
| PnP 求解器 | P3P + RANSAC（OpenCV） |
| 速度 | 659 ms/frame |

### 对比方法

**检索**: NCC, MI, NetVLAD, LPN, RK-Net, RDE, DenseUAV, MEAN, LRFR, QDFL, DAC, MCCG, Sample4Geo, CAMP

**匹配**: SIFT, ORB, D2Net, ALIKE, XoFTR, LiFFeat, SP+SG, SP+LG, SP+LG_CIM, SP+LG_CIM+k2s, LoFTR, DeDoDe, DKM, RoMa 等 19 种

**定位策略**: Matching-wo-Retrieval, Top1 Matching, Top N Re-rank, Most Inliers

## 数据集

| 数据集 | 说明 | 当前状态 |
|--------|------|----------|
| AnyVisLoc | 18,000 张无人机图像，7 种 DJI 机型，15 城市 25 区域，30m–300m 高度，20°–90° 俯仰角 | ✅ 已下载 |
| 参考图（航空） | 124 张，分辨率 0.02–0.35m，SfM 构建 | ✅ 已下载 |
| 参考图（卫星） | 72 张，分辨率 0.13–0.55m，Google Earth + ALOS 30m DSM | ✅ 已下载 |
| University-1652 | 检索模型预训练权重 | ✅ 已下载 |

### 数据集关键参数

- 图像分辨率: 1920×1080 到 5472×3648
- 焦距: 4.5–28mm
- 参考图坐标系: UTM
- 场景类型: 密集城市、典型地标、自然场景、混合场景
- 提供 UAV 图像与航空图之间的高精度对应关系

## 代码结构

```
code/
├── Baseline.py              # 主入口程序
├── config.yaml              # 全局配置文件
├── utils.py                 # 核心工具函数
├── requirements.txt         # Python依赖
├── Regions_params/          # 区域参数配置
│   └── QZ_Town.yaml        # 青州古镇示例区域
├── Retrieval_Models/        # 图像检索模型
│   ├── multi_model_loader.py   # 模型加载器
│   ├── feature_extract.py      # 特征提取
│   └── CAMP/                   # CAMP检索模型
│       ├── get_CAMP.py         # 模型初始化
│       ├── checkpoints/        # 权重目录
│       └── sample4geo/         # 模型实现
├── Matching_Models/         # 图像匹配模型
│   ├── RoMa/                # RoMa匹配模型
│   │   ├── demo/Roma_match.py  # 匹配接口
│   │   ├── roma/               # 模型实现
│   │   └── ckpt/               # 权重目录
│   └── SIFT/                # SIFT匹配方法
│       └── SIFT_match.py      # 匹配实现
└── 素材/                    # code内实验数据副本
    ├── 实验数据/            # CSV结果
    └── 截图/                # 图表
```

## 实验流程

### Step 1: 图像检索（粗定位）

1. **估算无人机中心位置**
   - 从JSON读取: lon, lat, yaw, pitch, 高度
   - 坐标转换: lon/lat → UTM
   - 几何计算: 高度/tan(pitch) → 中心偏移
   - 输出: 无人机中心在参考图上的像素坐标

2. **生成Gallery图像块**
   - 计算无人机视野大小: drone_size × drone_resolution
   - 计算参考图块大小: block_size (与无人机视野匹配)
   - 滑动窗口采样: step_size = block_size × (100-cover)%
   - 过滤无效块: 去除黑色区域 (>60%黑色的块)

3. **特征提取**
   - Query图像: 从无人机图像中心裁剪正方形 → resize(384×384)
   - Gallery图像: 从参考图滑动窗口裁剪 → resize(384×384)
   - CAMP模型: ConvNeXt-Base提取特征
   - 特征归一化: L2归一化

4. **相似度计算**
   - score = gallery_features @ query_feature
   - 排序: 返回Top-K最相似的图像块

### Step 2: 像素级匹配（精匹配）

1. **裁剪参考图块**
   - 从参考图裁剪检索到的位置
   - 缩放到与无人机图像相似的尺度

2. **RoMa匹配**
   - 输入: 无人机图像 + 参考图块
   - 模型: DINOv2-ViT-L backbone
   - 输出: 2D-2D点对应 (Sen_pts, Ref_pts)

3. **坐标转换（像素→地理坐标）**
   - 参考图像素坐标 → 参考图全局坐标
   - 全局坐标 → UTM坐标
   - 可选: 反向旋转（如果使用了先验偏航角对齐）

### Step 3: PnP求解（坐标解算）

1. **构建3D点**
   - 输入: UTM_X, UTM_Y (参考图匹配点的UTM坐标)
   - DSM采样: 从DSM高程图获取每个点的高度
   - 3D点: pose_3d = [UTM_X, UTM_Y, DSM]

2. **相机内参矩阵K**
   - 从JSON读取: focal_len, cam_size, width, height
   - 计算像素尺寸: pixelSize = cam_size / sqrt(w²+h²)
   - 计算焦距(像素): focal_px = focal_len / pixelSize
   - 构建K矩阵: [[fx,0,cx],[0,fy,cy],[0,0,1]]

3. **P3P + RANSAC求解**
   - 2D点: 无人机图像上的匹配点 (Sen_pts)
   - 3D点: 参考图上的UTM坐标 + DSM高程
   - 相机内参: K矩阵
   - OpenCV函数: cv2.solvePnPRansac()

4. **位姿恢复**
   - 旋转矩阵: R = Rodrigues(rvec)
   - 相机位置: X0 = -R^T × tvec
   - 坐标转换: UTM → 经纬度 (lon, lat)

### Step 4: 结果评估

1. **定位误差计算**
   - 真值: (lon_gt, lat_gt) 从JSON读取
   - 预测: (lon_pred, lat_pred) 从PnP求解得到
   - 误差公式: error = sqrt(error_lat² + error_lon²)

2. **Top-N重新排序**
   - 对Top-K检索结果分别进行匹配+PnP
   - 选择inliers最多的作为最终结果

3. **评估指标**
   - A@5m: 5米内定位成功率
   - A@10m: 10米内定位成功率
   - A@20m: 20米内定位成功率

## 关键配置参数

| 参数 | 默认值 | 作用 |
|------|--------|------|
| TEST_INTERVAL | 20 | 测试采样间隔（每20张测1张） |
| RETRIEVAL_COVER | 50 | 检索块重叠率（%） |
| RETRIEVAL_TOPN | 5 | 检索Top-N数量 |
| BATCH_SIZE | 128 | 特征提取批大小 |
| resize_ratio | 0.2 | 图像缩放比例（节省显存） |
| strategy | Topn_opt | 定位策略（Top1/Topn_opt） |
| Ref_type | HIGH | 参考图类型（HIGH=航空/LOW=卫星） |

## 环境配置

| 项目 | 值 |
|------|-----|
| Python | 3.9（推荐） |
| 深度学习框架 | PyTorch 2.2.1+cu121 |
| GPU | NVIDIA RTX 3080 (10GB) |
| CPU | Intel Core i9-10920X @ 3.50GHz |
| RAM | 128GB |
| 核心依赖 | OpenCV, timm, pyproj, transformers, kornia, einops |
| 是否需要训练 | ❌ 不需要，纯推理代码 |
| 虚拟环境 | .venv/（项目根目录，非 code/.venv/） |

## 实验结果汇总

### 复现实验结果（2026-06-15）

**航空图 HIGH + Top N Re-rank（CAMP + RoMa）**

| 指标 | 复现 | 论文 | 差异 |
|------|------|------|------|
| A@5m | **82.3%** | 74.1% | +8.2% |
| A@10m | **90.3%** | 87.7% | +2.6% |
| A@20m | **95.9%** | 94.2% | +1.7% |

分场景结果：

| 场景 | 图像数 | 平均误差 | A@5m | A@10m | A@20m |
|------|--------|---------|------|-------|-------|
| QZ_SongCity | 286 | 1.73m | 98.3% | 100.0% | 100.0% |
| Qingzhou_3_2 | 59 | 3.04m | 96.6% | 100.0% | 100.0% |
| QingZhou_2024 | 142 | 91.75m | 44.4% | 66.9% | 85.9% |
| **总计** | **487** | **28.14m** | **82.3%** | **90.3%** | **95.9%** |

注意：QingZhou_2024 场景表现极差（A@5m=44.4%），拖累整体均值。中位数误差仅 2.39m。

**卫星图 LOW + Top N Re-rank（CAMP + RoMa，coarse_res=280）**

| 指标 | 复现 | 论文 | 差异 |
|------|------|------|------|
| A@5m | **13.6%** | 18.5% | -4.9% |
| A@10m | **39.4%** | 38.7% | +0.7% |
| A@20m | **63.7%** | 58.5% | +5.2% |

**定位策略对比（航空图 HIGH，CAMP + RoMa）**

| 策略 | A@5m | A@10m | A@20m | 平均误差 | 中位数 |
|------|------|-------|-------|---------|--------|
| Top N Re-rank | **82.3%** | **90.3%** | **95.9%** | 28.1m | 2.39m |
| Top1 | 68.8% | 78.2% | 81.9% | 39.7m | 2.71m |
| Most Inliers | 79.5% | 86.2% | 87.3% | 81.2m | 2.29m |

结论：Top N Re-rank 策略最优，与论文 Table 5 结论一致。

**俯仰角影响分析（航空图 HIGH + Top N Re-rank）**

| 俯仰角范围 | 图像数 | A@5m | A@10m | A@20m | 平均误差 | 中位数 |
|-----------|--------|------|-------|-------|---------|--------|
| 20°-50°（倾斜） | 301 | 79.4% | 88.4% | 96.7% | 35.5m | 2.1m |
| 50°-70° | 22 | 63.6% | 86.4% | 90.9% | 17.8m | 4.0m |
| 70°-90°（正下视） | 164 | 90.2% | 94.5% | 95.1% | 16.1m | 2.4m |

结论：正下视精度最高（A@5m=90.2%），倾斜视角精度下降（A@5m=79.4%），与论文 Figure 7 结论一致。

**匹配方法对比（航空图 HIGH + Top N Re-rank + CAMP）**

| 方法 | 类型 | A@5m | A@10m | A@20m | 平均误差 |
|------|------|------|-------|-------|---------|
| RoMa | 密集/学习 | **82.3%** | **90.3%** | **95.9%** | 28.1m |
| SIFT | 稀疏/手工 | 31.2% | 35.9% | 39.2% | 9423.0m |

结论：RoMa 大幅优于 SIFT，密集匹配方法远优于稀疏手工方法，与论文 Table 4 结论一致。

### 论文原始结果（最佳组合 CAMP + RoMa + Top N Re-rank）

| 参考图 | A@5m | A@10m | A@20m |
|--------|------|-------|-------|
| 航空图 | 74.1% | 87.7% | 94.2% |
| 卫星图 | 18.5% | 38.7% | 58.5% |

### 检索方法 Top 5（R@1）

| 方法 | R@1 |
|------|-----|
| CAMP | 82.7 |
| MCCG | 80.5 |
| Sample4Geo | 76.7 |
| DAC | 58.3 |
| QDFL | 56.0 |

### 匹配方法 Top 5（A@5m）

| 方法 | A@5m | 速度 |
|------|------|------|
| RoMa | 70.1 | 659ms |
| DKM_MINIMA | 61.6 | 4915ms |
| LoFTR_MINIMA | 59.5 | 165ms |
| SP+LG_CIM+k2s | 55.8 | 74ms |
| SP+LG_CIM | 55.0 | 74ms |

### 关键发现

1. 学习方法 > 手工方法（检索和匹配都是）
2. 密集匹配精度 > 稀疏匹配，但速度更慢
3. 航空图 >> 卫星图（5m 内 74.1% vs 18.5%）
4. 俯仰角越小精度越差（倾斜视角更难）
5. Yaw 噪声 >10° 或 Pitch 噪声 >7° 显著退化
6. 参考图配准质量是前提（未配准时 P@1 显著降低）

## 水面场景特殊考虑

| 挑战 | 影响 | 可能的应对 |
|------|------|-----------|
| 水面弱纹理 | 检索和匹配更难 | 多尺度特征、上下文信息 |
| 动态背景（波浪） | 特征不稳定 | 时序滤波、鲁棒匹配 |
| 目标尺度变化 | 需要多尺度处理 | 多尺度金字塔 |
| 应急救援（三断） | 无法用航空图，依赖卫星图 | 卫星图增强、跨模态检索 |
| 双光融合 | 红外+可见光 | 跨模态检索/匹配 |

## 技术报告撰写

### 报告信息

- **报告名称**: 水面目标精准定位技术报告
- **项目名称**: 面向水面应急救援的机载双光融合人体目标精准感知方法研究
- **项目来源**: 北京市航空智能遥感装备工程技术研究中心开放基金
- **项目负责人**: 张洲宇
- **编撰**: 段富宇
- **报告模板**: 水面目标精准定位技术报告.docx

### 报告章节结构

| 章节 | 内容 | 素材来源 | 状态 |
|------|------|---------|------|
| 第一章 | 研究背景与任务需求 | 微信文章 + Gemini 参考 | ✅ 齐全 |
| 第二章 | 水面目标精准定位问题分析 | 论文 + 实验 + Gemini 参考 | ✅ 齐全 |
| 第三章 | 视觉定位总体框架 | 代码分析 + Gemini 参考 | ✅ 齐全 |
| 第四章 | 地理坐标解算方法 | 代码分析 + Gemini 参考 | ✅ 齐全 |
| 第五章 | 实验验证与结果分析 | 我们的实验结果 | ✅ 润色完成（v2_polished） |
| 第六章 | 总结与展望 | 实验结论 | ⚠️ 待撰写 |

### 报告文件位置

- **模板**: 水面目标精准定位技术报告.docx（项目根目录）
- **论文**: paper/Ye_Exploring_the_best_way_for_UAV_visual_localization_under_Low-altitude_CVPRF_2026_paper.pdf
- **论文笔记**: paper/notes.md
- **论文 Markdown**: paper/paper_markdown.md
- **第五章最新版**: reports/第五章_实验验证与结果分析_v2_polished.docx
- **第五章润色版**: reports/第五章_实验验证与结果分析_v2_polished.docx（Nature风格润色+审稿意见修改）
- **第五章历史版本**:
  - reports/第五章_实验验证与结果分析_v1.docx
  - reports/第五章_实验验证与结果分析_poi-tl_v5 copy.docx
  - reports/第五章_实验验证与结果分析_poi-tl_v2.docx（初稿）
  - reports/第五章_实验验证与结果分析.docx
- **第五章提纲**: reports/第五章_提纲_v1.docx / v2.docx / 源文件.docx
- **技术报告**: reports/水面目标精准定位技术报告.docx / _v5.docx
- **素材清单**: reports/素材清单.md
- **表格数据**: 素材/实验数据/第五章表格数据.md
- **图片素材**: 素材/截图/fig5_*.png（7张）
- **实验数据**: 素材/实验数据/*.csv（12个文件）

### 第五章素材状态

| 类型 | 数量 | 状态 |
|------|------|------|
| 表格 | 12张（表5-1~5-12） | ✅ 已插入 v2_polished |
| 图片 | 7张（图5-1,5-3~5-8） | ✅ 已插入 v2_polished |
| 正文 | 75段 | ✅ 已完成（Nature风格润色） |
| CSV数据 | 12个文件 | ✅ 已生成 |
| 中间文件 | 30个pipeline可视化 | ⚠️ pipeline_vis/ 为空，需GPU重跑 |

### 报告生成工具链

| 工具 | 文件 | 用途 |
|------|------|------|
| poi-tl | poi-tl-project/ | Word模板填充引擎 |
| analyze_tables.py | 根目录 | 表格结构分析 |
| check_format.py | 根目录 | 格式检查 |
| scripts/report/ | 60+ 脚本 | dump/fix/generate/verify全链路 |
