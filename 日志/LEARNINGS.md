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
5. **参考素材/与日志/重复**: 参考素材/是早期版本，信息过时，以日志/为准
6. **venv路径**: 实际在项目根目录 .venv/，不是 code/.venv/

## 项目文件管理经验

### 文件归类

1. **日志系统**: `日志/` 目录 5 个文件是权威状态来源
2. **参考素材**: `参考素材/` 是早期副本，信息可能过时，以 `日志/` 为准
3. **报告版本**: reports/ 下有多个版本，最新是 poi-tl_v5
4. **脚本清理**: `scripts/report/` 有 60+ 一次性脚本，完成任务后应清理
5. **临时文件**: 根目录的 table_*.txt 等是分析中间产物，可归档

### 报告生成工具链

1. **poi-tl**: Java 库，通过 Python 调用，用于 Word 模板填充
2. **python-docx**: 直接操作 docx，用于格式修复
3. **analyze_tables.py**: 表格结构分析，识别格式问题
4. **scripts/report/**: dump（提取）→ fix（修复）→ generate（生成）→ verify（验证）全链路

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

## Nature Skills 使用经验

### 技能概览

1. **nature-polishing**: 学术文本润色/重构/翻译为Nature风格英文
2. **nature-figure**: 面向Nature级期刊的投稿级科研图工作流（Python/R）
3. **nature-writing**: 起草Nature风格手稿章节
4. **nature-reviewer**: 模拟Nature审稿人视角评审
5. **nature-response**: 起草/审查逐点回复审稿人的response letter
6. **nature-reader**: 论文PDF→中英文对照Markdown
7. **nature-paper2ppt**: 论文→中文PPTX文献汇报
8. **nature-citation**: 检索Nature/CNS系列支撑文献

### nature-polishing 使用

1. **轴值检测**: paper_type（research/methods/hypothesis/algorithmic/review）、section（abstract/intro/results/discussion/conclusion/title/methods）、language（en/zh-to-en）、journal（nature/nat-comms/generic）
2. **中文润色**: 保持中文，参考Nature写作原则优化表达
3. **二次润色**: 优化句式（10-30词）、段落聚焦（一段一意）、精确对冲
4. **术语一致性**: 建立术语表，确保全文统一

### nature-reviewer 使用

1. **输出格式**: 3份审稿报告 + 1份综合意见
2. **评审轴**: originality, scientific importance, interdisciplinary readership, technical soundness, readability
3. **审稿人差异**: Reviewer 1关注技术细节，Reviewer 2关注原创性和重要性，Reviewer 3关注跨学科吸引力和可读性

### nature-response 使用

1. **回复策略**: 接受技术性建议，对评价性意见予以确认
2. **修改映射**: 每个审稿意见映射到具体修改位置
3. **缺失标记**: 需要作者补充的内容标记为AUTHOR_INPUT_NEEDED

### python-docx 段落替换

1. **保留格式**: 保存第一个run的格式，清除所有run的文本，在第一个run中设置新文本
2. **段落匹配**: 按节匹配，处理段落数量不匹配的情况
3. **表格保留**: 只替换正文段落，不修改表格内容
4. **公式处理**: 公式以纯文本形式嵌入段落，使用斜体和Cambria Math字体

### 审核流程

1. **子代理审核**: 启动独立子代理检查修改内容
2. **6项检查**: 公式显示、样本选择标准、技术细节、段落完整性、表格完整性、格式保留
3. **改进建议**: 子代理提出可选改进，用户确认后执行

## GitHub仓库管理经验

### 仓库清理

1. **扫描云端文件**: 使用 `gh api` 获取远程仓库文件列表
2. **分析垃圾文件**: 检查临时文件、重复文件、过时文件
3. **分类清理**: 按类别删除垃圾文件（临时文件、重复文件、过时文件）
4. **验证结果**: 确认核心文件完整，垃圾文件已清理

### 常见垃圾文件类型

1. **临时文件**: tmp/目录、.tmp/.temp文件、~$临时文件
2. **编译文件**: .pyc/.pyo/.pyd文件、.so/.dll/.exe文件
3. **重复文件**: 不同目录下的相同文件（如5all素材/和素材/）
4. **过时文件**: 早期版本的文件（如参考素材/目录）
5. **个人配置**: .claude/目录、.vscode/目录

### 清理策略

1. **保留核心文件**: 论文代码、实验数据、项目日志、论文资料
2. **删除垃圾文件**: 临时文件、编译文件、重复文件、过时文件
3. **保留最新版本**: 删除旧版本文件，保留最新版本
4. **保持目录结构**: 清理后保持清晰的目录结构

### 验证清单

1. ✅ 核心文件完整（论文代码、实验数据、项目日志、论文资料）
2. ✅ 临时文件已清理（tmp/目录、.tmp/.temp文件）
3. ✅ 编译文件已清理（.pyc/.pyo/.pyd文件）
4. ✅ 重复文件已清理（不同目录下的相同文件）
5. ✅ 过时文件已清理（早期版本的文件）
6. ✅ 个人配置未提交（.claude/目录、.vscode/目录）
