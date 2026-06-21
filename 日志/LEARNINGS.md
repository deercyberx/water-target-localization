# LEARNINGS.md

> 可复用的经验、教训、调试技巧。跨会话保留。

---

## 代码分析经验

### 环境搭建

1. **Python版本**: 代码在README中明确说明测试于 Python 3.9，不是3.10+
2. **PyTorch版本**: requirements.txt指定 torch==2.2.1+cu121，需要CUDA 12.1
3. **不需要训练**: 代码是纯推理，所有模型权重已预训练好
4. **权重文件**: 需要从百度网盘或Google Drive下载，不是自动下载

### 代码结构

1. **模块化设计**: 检索和匹配方法通过config.yaml切换，易于扩展
2. **核心函数**: utils.py包含所有关键逻辑，约600行
3. **配置驱动**: 区域参数在YAML文件中，支持多区域测试

### 性能瓶颈

1. **RoMa匹配占98%时间**: 650ms/张，是优化重点
2. **检索很快**: CAMP仅需10ms/张
3. **PnP求解很快**: 仅需1ms/张

### GPU 内存限制与优化

1. **RTX 3080 (10GB) 原始配置不够跑 RoMa**: 模型 ~4GB + 分配 ~3.5GB + local_correlation 额外 ~1.1GB > 10GB
2. **航空图能跑**: resize_ratio=0.2 缩小了图像，降低了匹配时的显存需求
3. **卫星图 OOM**: 即使用 resize_ratio=0.1 也不够，因为 RoMa 的 dense matching 在特征图上做的操作与输入图大小无关
4. **解决方案（已验证有效）**:
   - **降低 RoMa 分辨率**: coarse_res 560→280, upsample_res 864→512，模型显存从 ~4GB 降到 ~0.4GB
   - 特征图缩小 2×，local_correlation 内存缩小 4×
   - 添加 torch.cuda.empty_cache() 每次匹配后清理
   - 设置 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True（Windows 不支持但无害）
5. **精度影响**: 降分辨率后 A@5m 从 18.5% 降到 13.6%（卫星图），但 A@10m/A@20m 反而更好

### 水面场景适配

1. **DSM依赖**: 水面高程单一，可简化DSM需求
2. **弱纹理挑战**: 需要更强的特征提取（水岸线、船只等）
3. **卫星图问题**: 分辨率低（30m DSM），定位精度差（16.5% vs 74.1%）

### 技术报告撰写

1. **素材收集**: 论文笔记 + 微信文章 + AI 参考文本，三者互补
2. **章节结构**: 6 章（背景→分析→框架→方法→实验→总结）
3. **缺失内容**: 4.1（目标检测）和 4.6（多帧融合）需要额外补充
4. **Gemini 参考**: 提供了双光融合数学模型、EKF 滤波方程等高质量内容

### 坐标系统

1. **UTM坐标系**: 代码使用UTM进行距离计算
2. **WGS84**: 输入输出使用经纬度
3. **pyproj库**: 用于坐标转换，需要正确配置EPSG代码

## 第五章撰写经验

### 素材准备

1. **素材清单要及时更新**: 2026-06-17的清单严重过时，导致误判素材缺失
2. **pkl文件验证**: 实际有2440个pkl文件，不能只看目录是否存在
3. **CSV文件已存在**: results_HIGH.csv等7个文件在2026-06-17就已生成
4. **图表已存在**: error_histogram.png等在2026-06-17就已生成

### 图表生成

1. **中文路径问题**: cv2.imread/imwrite不支持中文路径，改用PIL
2. **matplotlib字体缓存**: 首次运行需清除缓存才能显示中文
3. **图片大小控制**: 300dpi高清图可达13.5MB，需注意报告文件大小
4. **pipeline可视化**: 每个样本生成4-6个中间文件，便于调试和展示

### 表格数据

1. **JSON格式更灵活**: tables_data.json比Markdown表格更易程序化处理
2. **俯仰角分桶修正**: 70-90°样本量从103修正为164（合计487张）
3. **高度分桶无样本**: Demo子集高度33-193m，200-300m区间无样本
4. **噪声数据来源标注**: 先验噪声数据来自论文Table 7，非本文实验

### 初稿撰写

1. **提纲驱动**: 严格按照提纲的11节结构撰写
2. **表格先插入**: 先插入12张表格，再写正文引用
3. **图片后插入**: 7张图片在正文写完后插入
4. **写作口径**: 避免"复现优于/低于原论文"，应写"链路测试结果"
5. **任务边界**: 严格区分"链路测试"和"目标级定位"，5.9节是分析框架非实测

### 审核要点

1. **技术审核**: 数据准确性、公式正确性、结论一致性
2. **学术审核**: 写作口径、术语规范、引用格式
3. **数据审核**: 表格数据与CSV一致、图片与实验结果一致
4. **格式审核**: 目录、分节、样式、字体、行距

## 日志管理经验

### 更新时机

1. **任务完成时**: 立即更新TASKS.md和ACTIVE.md
2. **实验完成时**: 更新CONTEXT.md和LOG.md
3. **问题解决时**: 更新LEARNINGS.md
4. **对话结束时**: 按关闭协议更新所有文件

### 文件职责

1. **ACTIVE.md**: 当前焦点，每次新对话第一个读
2. **TASKS.md**: 任务进度，checkbox是权威来源
3. **LOG.md**: 活动记录，追加在末尾
4. **CONTEXT.md**: 核心信息，结构稳定
5. **LEARNINGS.md**: 可复用经验，跨会话保留

### 常见错误

1. **素材清单过时**: 需要及时更新，否则误判素材缺失
2. **状态不一致**: ACTIVE.md和TASKS.md需保持一致
3. **日期格式**: LOG.md使用YYYY-MM-DD格式
4. **重复内容**: 避免在多个文件中重复记录同一信息

## 工具使用经验

### Python-docx

1. **读取docx**: `from docx import Document; doc = Document('file.docx')`
2. **表格遍历**: `for table in doc.tables: for row in table.rows: for cell in row.cells:`
3. **图片统计**: `for rel in doc.part.rels.values(): if 'image' in rel.reltype:`
4. **编码问题**: Windows需`sys.stdout.reconfigure(encoding='utf-8')`

### matplotlib

1. **中文显示**: `plt.rcParams['font.sans-serif'] = ['SimHei']`
2. **负号显示**: `plt.rcParams['axes.unicode_minus'] = False`
3. **高清保存**: `plt.savefig('file.png', dpi=300, bbox_inches='tight')`
4. **字体缓存**: 首次运行需`matplotlib.font_manager._load_fontmanager()`

### PIL/Pillow

1. **读取图片**: `from PIL import Image; img = Image.open('file.png')`
2. **保存图片**: `img.save('file.png', dpi=(300, 300))`
3. **中文路径**: PIL原生支持中文路径，比cv2更可靠
4. **格式转换**: `img.convert('RGB')` 用于RGBA转RGB

### pandas

1. **读取CSV**: `df = pd.read_csv('file.csv')`
2. **分桶统计**: `pd.cut(df['col'], bins=[...], labels=[...])`
3. **聚合统计**: `df.groupby('col').agg({'col2': ['mean', 'count']})`
4. **条件筛选**: `df[df['col'] > threshold]`
