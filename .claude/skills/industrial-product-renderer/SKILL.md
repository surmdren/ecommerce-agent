---
name: industrial-product-renderer
description: 工业设计产品渲染优化工具。将 KeyShot 等渲染软件输出的低质量产品图自动优化成官网级工业设计产品图，符合工业设计最佳实践和行业标准。特别针对光学仪器、精密仪器、工业设备等产品。使用 Stable Diffusion + ComfyUI 实现智能图像增强，自动分析材质、光线、构图问题并优化。适用场景：(1) 优化 KeyShot 渲染图质量 (2) 将初稿产品图提升到官网展示标准 (3) 批量处理工业产品图 (4) 保持产品结构的前提下优化渲染质量。当用户提到"产品渲染优化"、"优化产品图"、"KeyShot 渲染图优化"、"工业产品图处理"、"提升渲染质量"时触发。
---

# Industrial Product Renderer

将低质量的工业产品渲染图优化成官网级专业产品图。

## 核心功能

1. **智能问题分析**：自动识别材质、光线、构图、细节等问题
2. **ComfyUI 工作流生成**：基于分析结果生成最佳 SD 工作流配置
3. **模型推荐**：根据产品类型推荐最佳 SD 模型和参数
4. **保持产品结构**：使用 ControlNet 确保产品外形不变
5. **工业设计最佳实践**：内置官网级产品图标准

## 适用产品类型

- **光学仪器**：显微镜、光谱仪、测量仪器
- **精密仪器**：分析仪、检测设备
- **工业设备**：机械装备、电子设备
- **医疗器械**：医学影像设备、诊断仪器

## 工作流程

### Step 1: 接收产品图

用户提供 KeyShot 渲染的产品图（或其他 3D 渲染图）。

**输入格式**：
- 图片路径或图片文件
- 可选：产品类型描述（如"显微镜"、"光谱仪"）
- 可选：特殊要求（如"强调玻璃透明度"、"增强金属质感"）

### Step 2: 智能分析图片问题

使用 Claude 的图像理解能力自动分析以下维度：

**材质评估**：
- 玻璃/光学元件的透明度和折射效果
- 金属部件的反射和拉丝/抛光纹理
- 塑料外壳的质感和哑光/亮光效果
- 橡胶/皮革等其他材质表现

**光线评估**：
- 主光、辅助光、轮廓光的设置
- 阴影的硬度和自然度
- 高光位置和强度
- 整体曝光是否合理

**构图评估**：
- 产品位置是否居中
- 视角是否展示关键细节
- 背景是否简洁专业
- 阴影和倒影是否恰当

**细节评估**：
- 刻度、标识是否清晰
- 边缘是否锐利
- 表面纹理是否真实
- 整体精细度

**输出**：生成详细的问题清单和优化建议。

### Step 3: 生成 ComfyUI 工作流配置

基于分析结果，生成最佳 ComfyUI 工作流 JSON 配置。

**选择基础工作流**：
- `basic-enhancement.json`：标准优化（适用大多数场景）
- `material-refinement.json`：材质深度优化
- `lighting-optimization.json`：光线重构

**参数自动调整**：
```python
# 根据问题严重程度调整 denoising strength
if 问题较轻微:
    denoise = 0.30 - 0.35  # 轻微优化
elif 问题中等:
    denoise = 0.35 - 0.45  # 标准优化
else:
    denoise = 0.45 - 0.55  # 深度优化

# ControlNet 权重设置
canny_strength = 0.90  # 默认保持结构
depth_strength = 0.60  # 保持空间关系

# 如果产品结构复杂
if 产品结构复杂:
    canny_strength = 0.95
    depth_strength = 0.70
```

### Step 4: 推荐 SD 模型和 LoRA

根据产品类型和材质，推荐最佳模型组合。

**光学仪器推荐**：
```
Base Model: epiCRealism
LoRA 1: Product Photo Realism (0.7)
LoRA 2: Glass Material Enhancer (0.5)
```

**金属仪器推荐**：
```
Base Model: Realistic Vision V6.0
LoRA 1: Metal Material Enhancer (0.7)
LoRA 2: Industrial Design (0.5)
```

**复合材质推荐**：
```
Base Model: SDXL Product Design
ControlNet: Canny + Depth + Lineart
```

详见 [references/sd-models-guide.md](references/sd-models-guide.md)。

### Step 5: 生成优化 Prompt

基于产品类型和问题分析，生成定制化 prompt。

**Prompt 模板结构**：
```
[产品类型] + [材质描述] + [质量要求] + [光线描述] + [背景要求]
```

**示例 - 显微镜**：
```
Positive:
professional product photography, precision optical microscope,
glass optics with anti-reflective coating, brushed aluminum body,
laboratory equipment, studio lighting, white background,
high detail, photorealistic, commercial photography,
soft shadows, professional color grading, 8k uhd

Negative:
blur, noise, low quality, cluttered background, harsh shadows,
overexposed, cartoon, unrealistic materials, plastic toy,
cheap rendering, exaggerated colors
```

### Step 6: 输出完整方案

生成包含以下内容的优化方案：

**1. 问题分析报告**
```markdown
## 图片质量分析

### 材质问题
- ❌ 玻璃目镜完全透明无厚度感 → 需要增加 IOR 和边缘效果
- ✅ 金属镜筒反射自然

### 光线问题
- ❌ 阴影过硬 → 需要柔化主光源
- ❌ 整体偏暗 → 增加环境光

### 构图问题
- ✅ 产品居中，比例合适
- ❌ 关键刻度部分被阴影遮挡

### 综合评分：6.5/10
```

**2. ComfyUI 工作流配置**
```json
{
  "workflow": "basic-enhancement",
  "model": "epiCRealism",
  "loras": [
    {"name": "Product Photo Realism", "weight": 0.7},
    {"name": "Glass Material", "weight": 0.5}
  ],
  "controlnets": [
    {"type": "canny", "weight": 0.90},
    {"type": "depth", "weight": 0.60}
  ],
  "parameters": {
    "denoise": 0.40,
    "cfg": 7.0,
    "steps": 35,
    "sampler": "dpmpp_2m_karras"
  },
  "positive_prompt": "...",
  "negative_prompt": "..."
}
```

**3. 操作步骤**
```
1. 在 ComfyUI 中加载 basic-enhancement 工作流
2. 将原图拖入 LoadImage 节点
3. 确认使用 epiCRealism 模型
4. 加载 Product Photo Realism LoRA (权重 0.7)
5. 设置 Denoising 为 0.40
6. 复制生成的 positive/negative prompt
7. Queue Prompt 开始渲染
8. 如果结构变形，提高 Canny 权重到 0.95
```

**4. 预期效果说明**
```
优化后将达到：
✅ 玻璃目镜透明度真实，有边缘反射
✅ 金属镜筒拉丝纹理清晰，反射自然
✅ 光线柔和均匀，阴影适度
✅ 刻度清晰可读
✅ 整体色彩专业，符合官网展示标准
```

### Step 7: 后续调优建议

如果首次渲染效果不理想，提供调优方案：

**问题排查树**：
```
结构变形？
├─ Yes → 提高 Canny 权重到 0.95，降低 Denoise 到 0.35
└─ No
    └─ 材质不真实？
        ├─ Yes → 切换模型到 epiCRealism，增加材质 LoRA
        └─ No
            └─ 光线不自然？
                ├─ Yes → 调整 prompt，降低 CFG 到 6.5
                └─ No → 效果满意，完成
```

**迭代优化**：
1. 首次渲染：使用推荐参数
2. 评估结果：对比原图和优化图
3. 微调参数：根据具体问题调整
4. 重新渲染：直到达到满意效果

## 使用示例

### Example 1: 基础优化

**用户输入**：
```
"优化这张显微镜的 KeyShot 渲染图，提升到官网展示标准"
[附上图片]
```

**输出**：
1. 分析报告（材质、光线、构图评分）
2. ComfyUI 工作流 JSON
3. 推荐模型：epiCRealism + Glass Material LoRA
4. 详细操作步骤
5. 预期效果说明

### Example 2: 特定要求优化

**用户输入**：
```
"这个光谱仪的金属外壳看起来太假了，玻璃窗口也不够通透，帮我优化"
[附上图片]
```

**输出**：
1. 重点分析金属和玻璃材质问题
2. 推荐 Metal Material Enhancer LoRA (0.8)
3. 调整 prompt 强调 "brushed stainless steel, polished glass"
4. 提供针对性的参数建议

### Example 3: 批量处理

**用户输入**：
```
"我有 10 张不同角度的产品图需要优化，生成批量处理工作流"
```

**输出**：
1. ComfyUI 批量处理工作流
2. Image Batch 节点配置
3. 统一的参数设置
4. 自动输出命名规则

## 参考资源

- **工业设计最佳实践**：[references/industrial-design-best-practices.md](references/industrial-design-best-practices.md)
- **SD 模型推荐指南**：[references/sd-models-guide.md](references/sd-models-guide.md)
- **ComfyUI 工作流模板**：[assets/comfyui-workflows/](assets/comfyui-workflows/)

## 前置要求

**必需**：
- ComfyUI 已安装并配置
- Stable Diffusion 模型（Realistic Vision V6.0 或 epiCRealism）
- ControlNet 模型（Canny、Depth）

**推荐**：
- Product Photo Realism LoRA
- Metal Material Enhancer LoRA
- Glass Material Enhancer LoRA
- 显存 ≥ 8GB（SDXL 需 ≥ 12GB）

## 注意事项

1. **保持产品结构**：Canny ControlNet 权重始终 ≥ 0.85
2. **适度优化**：Denoising 一般不超过 0.50
3. **迭代调整**：首次渲染后根据效果微调参数
4. **模型选择**：光学仪器首选 epiCRealism，金属产品首选 Realistic Vision
5. **批量处理**：确保所有图片分辨率一致

## 与电商产品图的区别

本 skill 专注于**工业设计产品图**（官网展示），区别于电商产品图：

| 特征 | 工业设计产品图 | 电商产品图 |
|------|--------------|----------|
| 用途 | 官网、宣传册、技术文档 | 淘宝、京东、亚马逊 |
| 背景 | 白底或渐变，简洁专业 | 纯白底（RGB 255,255,255） |
| 构图 | 3/4 视角，展示立体感 | 正面或多角度平铺 |
| 光线 | 柔和自然，有环境光 | 明亮均匀，无明显阴影 |
| 细节 | 强调材质和工艺 | 强调商品完整性 |
| 风格 | 专业、技术感 | 吸引眼球、促销导向 |

如需优化电商产品图，请使用专门的 `ecommerce-product-renderer` skill（待开发）。
