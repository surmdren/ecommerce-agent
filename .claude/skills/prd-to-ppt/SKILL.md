---
name: prd-to-ppt
description: 根据PRD或业务需求文档生成PPT演示方案。支持自定义视觉风格（通过参考图片提取配色）和指定PPT页数（默认8-12页）。自动提取关键内容并组织成演示逻辑，应用合适的配色方案和排版。适用于产品方案汇报、项目提案演示、业务需求评审会议、向利益相关者展示。需要markitdown和pptxgenjs依赖。当用户提到"PPT"、"演示文稿"、"方案汇报"、"产品演示"时触发。
---

# PRD/业务描述 → PPT 方案生成

## Overview

将业务需求文档或PRD转化为专业的PPT演示方案。支持：
- 自定义视觉风格（通过参考图片）
- 指定PPT页数
- 自动提取关键内容并组织成演示逻辑

## Parameters

| 参数 | 必填 | 描述 |
|------|------|------|
| `文档路径` | ✅ | PRD或业务描述文档的路径 |
| `--style <图片路径>` | ❌ | 风格参考图片（用于提取配色、排版风格）|
| `--slides <数量>` | ❌ | PPT页数，默认 8-12 页 |
| `--output <路径>` | ❌ | 输出文件路径，默认 `output.pptx` |

## Usage

```bash
# 基础用法
/prd-to-ppt ./docs/requirement.md

# 指定风格和页数
/prd-to-ppt ./docs/requirement.md --style ./brand/style.png --slides 10

# 完整参数
/prd-to-ppt ./docs/requirement.md --style ./brand/logo.png --slides 15 --output ./presentation.pptx
```

## Workflow

### Step 1: 分析输入文档

读取并理解业务文档的核心内容：
1. 项目背景与目标
2. 核心功能/价值主张
3. 业务流程
4. 关键数据/指标
5. 风险与计划

### Step 2: 风格分析（如提供参考图片）

从参考图片中提取：
- **配色方案**: 主色、辅助色、强调色
- **字体风格**: 标题/正文的字体特征
- **排版特点**: 布局偏好、留白风格
- **视觉元素**: 图形、图标风格

### Step 3: 生成PPT大纲

根据文档内容和页数要求，规划PPT结构：

**标准结构（8-12页）**:
1. 封面（标题 + 副标题）
2. 目录/概览
3. 背景与痛点（1-2页）
4. 解决方案概述
5. 核心功能/价值（2-3页）
6. 业务流程/架构
7. 实施计划/里程碑
8. 风险与应对
9. 总结/下一步行动
10. 感谢页/联系方式

### Step 4: 设计决策

**配色选择**（如无参考图片，根据内容智能选择）:

| 场景 | 推荐配色 |
|------|----------|
| 科技/互联网 | 深蓝 #1C2833 + 青色 #5EA8A7 + 白 |
| 商务/金融 | 深灰 #2C3E50 + 金色 #997929 + 白 |
| 医疗/健康 | 绿色 #27AE60 + 浅绿 #A9DFBF + 白 |
| 教育/培训 | 橙色 #E67E22 + 蓝色 #3498DB + 白 |
| 创意/设计 | 紫色 #9B59B6 + 粉色 #F1948A + 白 |

**字体规范**:
- 标题: Arial Black / Impact, 32-44pt
- 副标题: Arial Bold, 24-28pt
- 正文: Arial, 16-20pt
- 仅使用 Web-safe 字体

### Step 5: 生成PPT

使用 html2pptx 工作流生成PPT：

1. 为每页创建 HTML 文件（720pt × 405pt，16:9）
2. 应用配色和排版风格
3. 转换为 PPTX 格式
4. 生成缩略图验证布局

```bash
# 生成缩略图验证
python scripts/thumbnail.py output.pptx --cols 4
```

### Step 6: 验证与调整

检查生成的PPT：
- ✅ 文字是否被截断
- ✅ 配色对比度是否足够
- ✅ 布局是否平衡
- ✅ 内容逻辑是否清晰

## Output Directory

将输出文件保存到项目根目录的 `PPT/` 目录下：

```
PPT/
├── [项目名称]-方案.pptx      # PPT 文件
├── [项目名称]-大纲.md        # PPT 大纲文档
└── thumbnails/               # 缩略图预览
    └── [项目名称]-preview.jpg
```

## Output Structure

生成的 PPT 包含：

```
📊 PPT/[项目名称]-方案.pptx
├── 封面页（项目名称、日期、作者）
├── 目录页
├── 内容页 × N（根据 --slides 参数）
└── 结束页
```

## Dependencies

需要安装官方 pptx skill 的依赖：
- markitdown: `pip install "markitdown[pptx]"`
- pptxgenjs: `npm install -g pptxgenjs`
- playwright: `npm install -g playwright`
- sharp: `npm install -g sharp`

## Examples

**示例 1: 基础用法**
```bash
/prd-to-ppt ./商品评价系统PRD.md
```
→ 生成 8-12 页 PPT，自动选择商务风格配色

**示例 2: 品牌定制**
```bash
/prd-to-ppt ./商品评价系统PRD.md --style ./公司logo.png --slides 15
```
→ 从 logo 提取品牌色，生成 15 页 PPT

**示例 3: 完整参数**
```bash
/prd-to-ppt ./docs/AI功能需求.md --style ./参考设计.png --slides 10 --output ./AI功能方案.pptx
```

## Notes

- 建议先用 `/requirement-detail` 生成规范的PRD文档，再用本 skill 生成PPT
- 参考图片建议使用清晰的品牌素材或希望模仿的PPT截图
- 复杂图表建议后续在PPT中手动调整
