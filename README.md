# 水面目标精准定位技术报告

> 面向水面应急救援的机载双光融合人体目标精准感知方法研究

## 项目概述

本项目基于 CVPR 2026 Findings 论文《Exploring the best way for UAV visual localization under Low-altitude Multi-view Observation Condition: a Benchmark》，复现并适配低空多视角UAV视觉定位链路，用于水面应急救援场景的目标精准定位。

### 技术路线

```
UAV图像 → 图像检索（CAMP）→ 图像匹配（RoMa）→ PnP求解（P3P+RANSAC）→ 地理坐标
```

### 最佳组合

- **检索模型**：CAMP（ConvNeXt-Base）
- **匹配模型**：RoMa（DINOv2-ViT-L）
- **定位策略**：Top N Re-rank
- **性能**：A@5m = 82.3%（航空图），中位数误差 2.4m

---

## 目录结构

```
water-target-localization/
├── .gitignore
├── README.md
├── code/                    # 论文代码（83个文件）
│   ├── Baseline.py
│   ├── utils.py
│   ├── config.yaml
│   ├── requirements.txt
│   ├── Retrieval_Models/    # 检索模型（CAMP）
│   ├── Matching_Models/     # 匹配模型（RoMa/SIFT）
│   ├── Regions_params/      # 区域参数
│   └── Data/                # 数据集元数据和姿态文件
├── 素材/                    # 实验数据和图表（34个文件）
│   ├── 实验数据/            # 12个CSV/JSON/MD文件
│   └── 截图/                # 18个图表文件
├── 5all素材/                # 第五章素材汇总（38个文件）
│   ├── 代码源文件/          # 5个Python文件
│   ├── 典型案例/            # 4个文件
│   ├── 报告/                # 5个文件
│   ├── 报告生成脚本/        # 12个Python文件
│   ├── 数据源/              # 1个JSON文件
│   ├── 检查报告/            # 1个文件
│   ├── 正文章节/            # 5个文件
│   └── 配置/                # 3个文件
├── scripts/                 # 报告生成脚本（24个文件）
│   ├── data/                # 2个数据处理脚本
│   └── report/              # 22个报告生成脚本
├── 日志/                    # 项目日志（5个文件）
│   ├── ACTIVE.md
│   ├── CONTEXT.md
│   ├── LEARNINGS.md
│   ├── LOG.md
│   └── TASKS.md
├── paper/                   # 论文资料（4个文件）
│   ├── 论文PDF
│   ├── notes.md
│   ├── paper_markdown.md
│   └── gemini_reference_ch1_4.md
├── reports/                 # 报告文件（2个文件）
│   ├── 可选补充内容S1-S25.md
│   └── 素材清单.md
├── results/                 # 结果目录（1个文件）
│   └── .gitkeep
└── experiments/             # 实验脚本（1个文件）
    └── run_experiment.ps1
```

---

## 新电脑恢复项目指南

### 完整恢复流程（10分钟）

#### 步骤1：克隆仓库（1分钟）

```bash
git clone https://github.com/deercyberx/water-target-localization.git
cd water-target-localization
```

#### 步骤2：安装Python 3.9（2分钟）

```bash
# Windows（使用winget）
winget install Python.Python.3.9

# 或从官网下载：https://www.python.org/downloads/release/python-3913/
```

#### 步骤3：创建虚拟环境（1分钟）

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### 步骤4：安装依赖（2分钟）

```bash
# 安装PyTorch（CUDA 12.1）
pip install torch==2.2.1 torchvision==0.17.1 --index-url https://download.pytorch.org/whl/cu121

# 安装项目依赖
pip install -r code/requirements.txt

# 安装报告生成依赖
pip install python-docx matplotlib pandas pillow
```

#### 步骤5：下载模型权重（3分钟）

从网盘下载权重文件：

| 模型 | 大小 | 下载后放到 |
|------|------|-----------|
| CAMP | 349MB | `code/Retrieval_Models/CAMP/checkpoints/` |
| RoMa | 426MB | `code/Matching_Models/RoMa/ckpt/` |
| DINOv2 | 1.2GB | `code/Matching_Models/RoMa/ckpt/` |

**目录结构示例**：
```
code/Retrieval_Models/CAMP/checkpoints/
└── university/
    └── convnext_base.fb_in22k_ft_in1k_384/
        └── best.pth

code/Matching_Models/RoMa/ckpt/
├── outdoor.pth
└── dinov2_vitl14_pretrain.pth
```

#### 步骤6：下载数据集（2分钟）

从网盘下载 `Data.rar`，解压到 `code/Data/`

**目录结构示例**：
```
code/Data/
├── metadata/
│   └── QZ_Town.json
├── UAV_image/
│   └── QZ_Town/
│       ├── QZ_SongCity/
│       ├── Qingzhou_3_2/
│       └── QingZhou_2024/
└── Reference_map/
    └── QZ_Town/
```

#### 步骤7：验证环境（1分钟）

```bash
cd code
python Baseline.py --help
```

如果显示帮助信息，说明环境配置成功。

#### 步骤8：查看项目状态

```bash
# 查看当前任务
cat 日志/ACTIVE.md

# 查看待办事项
cat 日志/TASKS.md

# 查看最新进展
tail -50 日志/LOG.md
```

---

### 环境要求

| 项目 | 要求 |
|------|------|
| Python | 3.9（必须，不要用3.10+） |
| PyTorch | 2.2.1 + CUDA 12.1 |
| GPU | NVIDIA RTX 3080 (10GB) 或更高 |
| RAM | 16GB+ |
| 磁盘 | 10GB+（代码+权重+数据集） |

---

### 文件说明

#### Git仓库已包含（185个文件）

- ✅ 项目代码（83个文件，排除权重和数据集）
- ✅ 日志系统（5个文件）
- ✅ 第五章素材汇总（38个文件）
- ✅ 实验数据和图表（34个文件）
- ✅ 报告生成脚本（24个文件）
- ✅ 论文和笔记（4个文件）
- ✅ 报告文件（2个文件）
- ✅ README文档
- ✅ 数据集元数据和姿态文件

#### 需要单独下载（网盘）

- ❌ 模型权重：CAMP + RoMa + DINOv2（共2.2GB）
- ❌ 数据集：Data.rar（4.2GB）

---

### 常见问题

#### Q1: pip安装超时

```bash
# 使用国内镜像
pip install -r code/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### Q2: CUDA版本不匹配

```bash
# 检查CUDA版本
nvidia-smi

# 根据CUDA版本选择PyTorch
# CUDA 11.8: torch==2.2.1+cu118
# CUDA 12.1: torch==2.2.1+cu121
```

#### Q3: GPU OOM（显存不足）

已在代码中处理，RoMa分辨率已降低：
```python
coarse_res=280, upsample_res=512  # 原始: 560, 864
```

#### Q4: 中文路径读取失败

使用PIL替代cv2：
```python
from PIL import Image
img = Image.open('中文路径.png')  # cv2不支持中文路径
```

#### Q5: argparse冲突

CAMP初始化已修改：
```python
args = parser.parse_args([], namespace=self)  # 添加空列表参数
```

---

### 日常同步命令

```bash
# 拉取最新
git pull

# 提交修改
git add .
git commit -m "描述修改内容"
git push
```

---

## 运行实验

### 完整测试（487张）

```bash
cd code
python Baseline.py --Ref_type HIGH --strategy Topn_opt
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--Ref_type` | HIGH | 参考图类型：HIGH=航空图，LOW=卫星图 |
| `--strategy` | Topn_opt | 定位策略：Top1/Topn_opt/MostInliers |
| `--TEST_INTERVAL` | 20 | 测试间隔（每N张测1张） |
| `--RETRIEVAL_TOPN` | 5 | 检索Top-N数量 |

### 输出结果

结果保存在 `code/Result/{Ref_type}/QZ_Town/` 目录：
- `results.csv`：逐图定位结果
- `*.png`：可视化结果（需开启 `SHOW_RETRIEVAL_RESULT=True`）

---

## 实验结果

### 主结果（CAMP + RoMa + Top N Re-rank）

| 参考图 | A@5m | A@10m | A@20m | 平均误差 | 中位数误差 |
|--------|------|-------|-------|---------|-----------|
| 航空图 | 82.3% | 90.3% | 95.9% | 28.1m | 2.4m |
| 卫星图 | 13.6% | 39.4% | 63.7% | 100.0m | 13.4m |

### 分场景结果（航空图）

| 场景 | 样本数 | A@5m | 平均误差 |
|------|--------|------|---------|
| QZ_SongCity | 286 | 98.3% | 1.73m |
| Qingzhou_3_2 | 59 | 96.6% | 3.04m |
| QingZhou_2024 | 142 | 44.4% | 91.75m |

### 定位策略对比

| 策略 | A@5m | A@10m | A@20m |
|------|------|-------|-------|
| Top N Re-rank | **82.3%** | **90.3%** | **95.9%** |
| Top1 | 68.8% | 78.2% | 81.9% |
| Most Inliers | 79.5% | 86.2% | 87.3% |

---

## 报告撰写

### 当前进度

- ✅ 第一章~第四章：已完成
- ✅ 第五章：初稿完成（12张表+7张图+完整正文）
- ⏳ 第六章：待撰写

### 第五章素材

- **表格数据**：`素材/实验数据/第五章表格数据.md`
- **图表素材**：`素材/截图/fig5_*.png`（7张）
- **初稿文件**：`reports/第五章_实验验证与结果分析_poi-tl_v2.docx`
- **提纲文件**：`reports/水面目标精准定位技术报告第五章提纲_终稿.docx`

---

## 日志系统

项目使用双层日志系统追踪进度：

| 文件 | 用途 | 更新频率 |
|------|------|---------|
| `日志/ACTIVE.md` | 当前任务焦点 | 每次对话开始 |
| `日志/TASKS.md` | 任务进度（checkbox） | 任务完成时 |
| `日志/LOG.md` | 活动记录 | 每次工作结束 |
| `日志/CONTEXT.md` | 项目核心信息 | 信息变化时 |
| `日志/LEARNINGS.md` | 可复用经验 | 遇到问题时 |

### 新对话启动

```bash
cat 日志/ACTIVE.md    # 查看当前任务
cat 日志/TASKS.md     # 查看待办事项
tail -50 日志/LOG.md  # 查看最新进展
```

---

## 常见问题

### GPU OOM（显存不足）

降低RoMa分辨率：
```python
# code/Matching_Models/RoMa/demo/Roma_match.py:16
coarse_res=280, upsample_res=512  # 原始: 560, 864
```

### 中文路径读取失败

使用PIL替代cv2：
```python
from PIL import Image
img = Image.open('中文路径.png')  # cv2不支持中文路径
```

### argparse冲突

修改CAMP初始化：
```python
# code/Retrieval_Models/CAMP/get_CAMP.py:133
args = parser.parse_args([], namespace=self)  # 添加空列表参数
```

---

## 参考文献

- Ye et al. "Exploring the best way for UAV visual localization under Low-altitude Multi-view Observation Condition: a Benchmark." CVPR 2026 Findings.
- 项目代码：https://github.com/UAV-AVL/Benchmark

---

## 许可证

本项目仅供学术研究使用。

---

## 联系方式

- 项目负责人：张洲宇
- 编撰：段富宇
- 项目来源：北京市航空智能遥感装备工程技术研究中心开放基金
