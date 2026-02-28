---
name: ecommerce-shoes-renderer
description: 电商鞋子产品图优化工具。将低质量的鞋子图片（手机拍摄、工厂样图、3D渲染图）优化成符合电商平台标准的高质量主图。自动处理背景移除、纯白底替换、光线优化、材质增强、细节锐化。支持各类鞋款（运动鞋、皮鞋、高跟鞋、靴子等）。使用 Stable Diffusion + ControlNet 实现智能优化，确保产品结构不变形。适用场景：(1) 淘宝/京东/亚马逊主图优化 (2) 手机拍摄照片转电商图 (3) 工厂样图优化 (4) 批量鞋子产品图处理 (5) 符合平台纯白底要求。当用户提到"鞋子产品图优化"、"电商鞋图"、"淘宝主图"、"白底鞋图"、"鞋子去背景"时触发。
---

# E-commerce Shoes Renderer

将低质量的鞋子图片优化成符合电商平台标准的高质量产品图。

## 核心功能

1. **智能背景移除**：自动识别并移除复杂背景
2. **纯白底替换**：符合淘宝/京东/亚马逊平台要求 (RGB 255,255,255)
3. **光线优化**：明亮均匀，无明显阴影
4. **材质增强**：皮革/网布/橡胶材质更真实
5. **细节锐化**：品牌 logo、鞋带、纹理清晰
6. **结构保持**：使用 ControlNet 确保鞋型不变

## 支持鞋款类型

- **运动鞋**：跑步鞋、篮球鞋、板鞋、训练鞋
- **休闲鞋**：帆布鞋、乐福鞋、豆豆鞋
- **正装鞋**：皮鞋、牛津鞋、布洛克鞋
- **女鞋**：高跟鞋、单鞋、平底鞋、凉鞋
- **靴子**：马丁靴、切尔西靴、雪地靴、长靴

## 电商平台标准

### 淘宝/天猫要求
- 纯白底：RGB(255, 255, 255)
- 分辨率：800×800 像素起，推荐 1200×1200
- 格式：JPG/PNG，大小 <500KB（主图）
- 鞋子占比：画面 70-85%
- 视角：侧面 45° 或正侧面

### 京东要求
- 纯白底：RGB(255, 255, 255)
- 分辨率：≥800×800 像素，推荐 1000×1000
- 格式：JPG，大小 <1MB
- 鞋子占比：画面 60-80%
- 无水印、无边框

### 亚马逊要求
- 纯白底：RGB(255, 255, 255) 或 (246, 246, 246)
- 分辨率：≥1000×1000 像素，推荐 2000×2000
- 格式：JPG/PNG
- 鞋子占比：画面 85% 以上
- 高清细节展示

详见 [references/platform-standards.md](references/platform-standards.md)

## 工作流程

### Step 1: 接收鞋子图片

用户提供原始鞋子图片。

**输入类型**：
- 手机拍摄的鞋子照片（背景杂乱）
- 工厂样图（光线不佳）
- 3D 渲染图（需要优化）
- 已有产品图（需要提升质量）

**可选信息**：
- 鞋款类型（运动鞋/皮鞋/高跟鞋等）
- 目标平台（淘宝/京东/亚马逊）
- 特殊要求（强调某个细节、特定角度）

### Step 2: 智能分析图片

自动评估以下维度：

**背景评估**：
- 是否为纯白底
- 背景复杂度（地板/桌面/户外）
- 是否需要背景移除

**光线评估**：
- 整体亮度（是否偏暗）
- 光线均匀度
- 阴影强度（是否过重）
- 高光位置（是否过曝）

**材质评估**：
- 皮革材质的质感和光泽
- 网布材质的透气感和纹理
- 橡胶鞋底的质感
- 金属配件的反光

**细节评估**：
- 品牌 logo 清晰度
- 鞋带/鞋孔细节
- 缝线和纹理
- 整体锐利度

**构图评估**：
- 鞋子占比（是否符合平台要求）
- 视角（侧面/正面/3/4 角度）
- 位置（是否居中）

**输出**：生成问题清单和优化建议。

### Step 3: 生成 SD 优化方案

根据鞋款类型和平台要求，生成最佳配置。

**模型选择**：

```python
# 运动鞋推荐
if shoe_type == "sneaker":
    model = "Product Photography XL"
    loras = ["Fabric Texture Enhancer (0.6)", "Clean Background (0.8)"]

# 皮鞋推荐
elif shoe_type == "leather":
    model = "Realistic Vision V6.0"
    loras = ["Leather Material (0.7)", "Professional Product (0.6)"]

# 高跟鞋推荐
elif shoe_type == "heels":
    model = "epiCRealism"
    loras = ["Fashion Product (0.7)", "Glossy Surface (0.5)"]
```

详见 [references/shoe-models-guide.md](references/shoe-models-guide.md)

**背景处理策略**：

```python
# 策略 1: 背景简单（已接近白底）
if background_complexity < 30:
    strategy = "direct_enhancement"  # 直接优化，轻微白化
    denoise = 0.25

# 策略 2: 背景中等（地板/桌面）
elif background_complexity < 60:
    strategy = "background_replacement"  # 背景替换
    denoise = 0.40
    use_background_remover = True

# 策略 3: 背景复杂（户外/杂乱）
else:
    strategy = "full_reconstruction"  # 完全重构
    denoise = 0.50
    use_background_remover = True
    use_inpainting = True
```

**ControlNet 配置**：

```yaml
controlnets:
  - type: canny
    weight: 0.95  # 高权重，严格保持鞋型
    preprocessor: canny

  - type: depth
    weight: 0.65  # 保持立体感
    preprocessor: depth_midas

  - type: seg  # 可选，用于背景分离
    weight: 0.70
    preprocessor: seg_ofade20k
```

### Step 4: 生成电商专用 Prompt

根据鞋款类型和材质，生成针对性 prompt。

**运动鞋 Prompt 模板**：
```
Positive:
professional product photography, sneaker, athletic shoe,
white background RGB(255,255,255), studio lighting,
mesh fabric texture, rubber sole, clean composition,
brand logo visible, high resolution, commercial photography,
even lighting, no shadows, 8k product shot

Negative:
cluttered background, colored background, outdoor scene,
strong shadows, dark lighting, blur, low quality,
distorted shape, unrealistic materials, dirty, worn
```

**皮鞋 Prompt 模板**：
```
Positive:
professional product photography, leather dress shoe,
white background RGB(255,255,255), studio lighting,
polished leather, refined texture, formal footwear,
clear stitching, high detail, commercial photography,
soft even lighting, premium quality, 8k product shot

Negative:
casual style, worn leather, scuffs, background clutter,
harsh shadows, overexposed, blur, low resolution,
cheap materials, unrealistic shine
```

**高跟鞋 Prompt 模板**：
```
Positive:
professional product photography, high heel shoe,
white background RGB(255,255,255), studio lighting,
elegant design, glossy finish, fashion footwear,
clear heel detail, sophisticated, commercial photography,
soft lighting, premium quality, 8k product shot

Negative:
casual style, flat heel, background clutter, shadows,
dull finish, low quality, blur, distorted shape,
cheap appearance, unrealistic materials
```

详见 [references/prompt-templates.md](references/prompt-templates.md)

### Step 5: ComfyUI 工作流配置

基于分析结果，选择合适的工作流模板。

**工作流类型**：

1. **basic-white-bg.json**
   - 适用：背景已接近白底，只需轻微优化
   - Denoise: 0.25-0.30
   - 不使用背景移除

2. **background-removal.json**
   - 适用：背景中等复杂，需要替换
   - 使用 Rembg / BiRefNet 移除背景
   - Denoise: 0.35-0.45

3. **full-enhancement.json**
   - 适用：背景复杂或图片质量很差
   - 背景移除 + Inpainting + 全面优化
   - Denoise: 0.45-0.55

**参数配置示例**：
```json
{
  "workflow": "background-removal",
  "model": "Product Photography XL",
  "loras": [
    {"name": "Fabric Texture Enhancer", "weight": 0.6},
    {"name": "Clean Background", "weight": 0.8}
  ],
  "controlnets": [
    {"type": "canny", "weight": 0.95},
    {"type": "depth", "weight": 0.65}
  ],
  "parameters": {
    "denoise": 0.40,
    "cfg": 7.5,
    "steps": 30,
    "sampler": "dpmpp_2m_karras",
    "resolution": "1200x1200"
  },
  "background": {
    "color": "RGB(255,255,255)",
    "shadow": "soft_contact_shadow",
    "shadow_opacity": 0.15
  }
}
```

工作流模板见 [assets/comfyui-workflows/](assets/comfyui-workflows/)

### Step 6: 输出优化方案

生成完整的操作指南。

**1. 问题分析报告**
```markdown
## 鞋子图片分析报告

### 背景问题
- ❌ 背景为木地板，需要移除
- 建议：使用 background-removal 工作流

### 光线问题
- ❌ 整体偏暗，阴影过重
- 建议：Prompt 中强调 "bright even lighting"

### 材质问题
- ✅ 网布纹理基本清晰
- ⚠️ 橡胶鞋底光泽不足
- 建议：添加 Rubber Material LoRA (0.5)

### 细节问题
- ❌ 品牌 logo 模糊
- 建议：后期锐化处理

### 构图问题
- ✅ 鞋子占比合适（约 75%）
- ✅ 侧面 45° 角度标准

### 平台合规性
- 目标平台：淘宝/天猫
- ✅ 尺寸符合（1200×1200）
- ❌ 背景需要纯白化

### 综合评分：6.0/10
需要优化：背景、光线、细节锐化
```

**2. ComfyUI 操作步骤**
```
【准备工作】
1. 确认已安装 Product Photography XL 模型
2. 下载 Fabric Texture Enhancer LoRA
3. 安装 BiRefNet 背景移除节点

【ComfyUI 操作】
1. 加载 background-removal 工作流
2. 将原图拖入 LoadImage 节点
3. 配置 BiRefNet 背景移除（threshold: 0.5）
4. 设置 Canny ControlNet 权重为 0.95
5. 设置 Denoising 为 0.40
6. 复制生成的 positive/negative prompt
7. 设置输出分辨率为 1200×1200
8. Queue Prompt 开始渲染

【后期处理】（可选）
1. 使用 Photoshop 检查白底纯度
2. 调整 Levels: 确保白底为 RGB(255,255,255)
3. 锐化品牌 logo 区域
4. 添加柔和接触阴影（Opacity 15%）
5. 导出为 JPG（质量 90%，sRGB 色彩空间）
```

**3. 预期效果**
```
优化后将达到：
✅ 纯白底 RGB(255,255,255)
✅ 光线明亮均匀，无重阴影
✅ 网布纹理清晰，鞋底质感提升
✅ 品牌 logo 清晰可读
✅ 鞋型保持完整，无变形
✅ 符合淘宝/天猫主图标准
✅ 文件大小 <500KB
```

### Step 7: 批量处理支持

对于多张鞋子图片的批量优化。

**批量工作流配置**：
```json
{
  "batch_mode": true,
  "input_folder": "./shoes_raw/",
  "output_folder": "./shoes_optimized/",
  "naming_convention": "{original_name}_ecommerce",
  "uniform_parameters": {
    "resolution": "1200x1200",
    "denoise": 0.40,
    "background": "RGB(255,255,255)"
  },
  "auto_categorize": true,  // 自动识别鞋款类型
  "parallel_processing": 4   // 同时处理 4 张图
}
```

## 使用示例

### Example 1: 手机拍摄优化

**用户输入**：
```
"这是我用手机拍的运动鞋照片，背景是地板，帮我优化成淘宝主图"
[附上图片]
```

**输出**：
1. 分析报告：背景复杂度 70%，需要完全移除
2. 推荐工作流：background-removal.json
3. 模型：Product Photography XL + Fabric Texture Enhancer
4. Denoise: 0.42
5. 详细操作步骤
6. 预期效果：纯白底、明亮、清晰

### Example 2: 工厂样图优化

**用户输入**：
```
"工厂发来的皮鞋样图，光线很暗，需要优化成京东主图标准"
[附上图片]
```

**输出**：
1. 分析报告：光线偏暗、背景可接受但需白化
2. 推荐工作流：basic-white-bg.json（轻度优化）
3. 模型：Realistic Vision V6.0 + Leather Material LoRA
4. Prompt 重点："bright studio lighting, polished leather"
5. 后期处理：提亮整体、强化皮革质感

### Example 3: 批量处理

**用户输入**：
```
"我有 50 张不同款式的鞋子照片，需要批量优化成亚马逊主图"
[指定文件夹路径]
```

**输出**：
1. 批量工作流配置
2. 自动分类：运动鞋 30 张、皮鞋 15 张、凉鞋 5 张
3. 针对每类的参数配置
4. 预计处理时间：约 30 分钟
5. 自动化脚本

## 质量检查清单

优化完成后，检查以下项目：

**平台合规性**：
- [ ] 背景为纯白底 RGB(255,255,255)
- [ ] 分辨率符合平台要求（≥1000×1000）
- [ ] 文件大小符合限制
- [ ] 无水印、无边框、无文字

**视觉质量**：
- [ ] 鞋子占比 60-85%
- [ ] 光线明亮均匀
- [ ] 无明显阴影或过曝
- [ ] 色彩真实自然

**细节质量**：
- [ ] 品牌 logo 清晰
- [ ] 鞋带/鞋孔细节可见
- [ ] 材质纹理真实
- [ ] 缝线清晰

**结构完整性**：
- [ ] 鞋型无变形
- [ ] 比例正确
- [ ] 透视合理

## 参考资源

- **平台标准规范**：[references/platform-standards.md](references/platform-standards.md)
- **SD 模型推荐**：[references/shoe-models-guide.md](references/shoe-models-guide.md)
- **Prompt 模板库**：[references/prompt-templates.md](references/prompt-templates.md)
- **材质优化指南**：[references/material-enhancement.md](references/material-enhancement.md)
- **ComfyUI 工作流**：[assets/comfyui-workflows/](assets/comfyui-workflows/)

## 前置要求

**必需**：
- ComfyUI 已安装
- Product Photography XL 或 Realistic Vision V6.0
- ControlNet (Canny + Depth)
- 背景移除工具（BiRefNet / Rembg）

**推荐**：
- Fabric Texture Enhancer LoRA
- Leather Material LoRA
- Clean Background LoRA
- 显存 ≥ 8GB

## 常见问题

**Q: 背景移除后边缘有毛边怎么办？**
A: 提高 Canny ControlNet 权重到 0.98，或使用 Alpha Matting 精修边缘

**Q: 鞋子颜色变化了怎么办？**
A: 降低 Denoising 到 0.30-0.35，或在 prompt 中明确颜色："black sneaker"

**Q: 鞋底变形了怎么办？**
A: 提高 Depth ControlNet 权重到 0.75，或降低 Denoising

**Q: 如何符合亚马逊纯白底要求？**
A: 最终输出后用 Photoshop 确保背景为 RGB(255,255,255)，可用"色阶"工具调整

**Q: 批量处理时不同鞋子需要不同参数怎么办？**
A: 使用 auto_categorize 功能，自动根据鞋款类型应用不同配置

## 与工业产品图的区别

| 特征 | 电商鞋子图 | 工业产品图 |
|------|----------|-----------|
| 用途 | 电商销售 | 官网展示 |
| 背景 | 纯白底 RGB(255,255,255) | 渐变或纯白 |
| 光线 | 明亮均匀，无阴影 | 柔和自然，有环境光 |
| 风格 | 吸引眼球 | 专业技术感 |
| 细节 | 强调完整性 | 强调工艺 |
| 平台 | 淘宝/京东/亚马逊 | 官网/宣传册 |

如需优化工业设计产品图，请使用 `industrial-product-renderer` skill。
