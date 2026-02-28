# 鞋子产品图 Prompt 模板

## 核心 Prompt 结构

```
[产品类型] + [材质描述] + [视角] + [背景] + [质量标签]
```

## 通用 Positive Prompt 模板

```
professional product photography, [鞋子类型], [材质描述],
pure white background RGB(255,255,255), clean composition,
studio lighting, soft shadows, commercial photography,
high detail, sharp focus, photorealistic, 8k uhd,
product showcase, e-commerce standard
```

## 通用 Negative Prompt

```
blur, noise, grain, low quality, amateur, cluttered background,
harsh shadows, overexposed, underexposed, cartoon, sketch,
unrealistic materials, distorted shape, deformed,
people, model wearing, text, watermark, logo,
multiple shoes (unless specified), messy background,
artificial rendering, 3d render look, plastic toy
```

---

## 按鞋款类型的 Prompt 模板

### 运动鞋 (Sneakers)

**Positive**:
```
professional product photography, athletic sneakers, sports shoes,
mesh fabric upper, synthetic materials, rubber sole with texture,
side 45-degree angle view, single shoe display,
pure white background RGB(255,255,255), no shadows or minimal contact shadow,
studio lighting setup, bright and clean, commercial product photo,
high resolution, sharp details, photorealistic,
shoe占比 70-85%, centered composition,
for Taobao/JD/Amazon listing, e-commerce standard,
8k uhd, product showcase
```

**Negative**:
```
blur, noise, low quality, dirty, worn out, used shoes,
cluttered background, colored background, gradient background,
people, feet, model wearing, legs,
harsh shadows, dark lighting, underexposed,
cartoon, sketch, 3d render, unrealistic,
deformed shape, distorted sole, asymmetric,
text, watermark, brand logo (unless product original),
multiple shoes, shoe box, accessories
```

**参数建议**:
- Model: Product Photography XL
- LoRA: Fabric Texture (0.6) + Clean Background (0.8)
- Denoise: 0.40-0.45
- Canny: 0.95
- Depth: 0.65

---

### 皮鞋 (Leather Shoes)

**Positive**:
```
professional product photography, leather dress shoes, formal shoes,
genuine leather upper, polished finish, natural leather texture,
glossy surface with subtle reflections, leather grain visible,
side 45-degree angle view, single shoe display,
pure white background RGB(255,255,255), soft contact shadow,
studio lighting, highlights on leather surface,
commercial photography, luxury product presentation,
high detail, sharp focus, photorealistic,
shoe占比 70-85%, elegant composition,
for premium e-commerce listing, 8k uhd
```

**Negative**:
```
blur, noise, grain, low quality, cheap plastic,
matte finish (if glossy leather), synthetic materials,
cluttered background, non-white background,
harsh shadows, overexposed highlights, dull lighting,
people, model, feet, socks,
cartoon, sketch, unrealistic rendering,
deformed shape, asymmetric, cracked leather,
text, watermark, price tags,
scuffed, damaged, worn appearance
```

**参数建议**:
- Model: epiCRealism
- LoRA: Leather Material (0.7) + Professional Product (0.6)
- Denoise: 0.35-0.42
- Canny: 0.95
- Depth: 0.70

---

### 高跟鞋 (High Heels)

**Positive**:
```
professional product photography, high heels, women's dress shoes,
glossy patent leather, satin finish, metallic details,
stiletto heel, elegant design, fashion footwear,
side profile view, showcasing heel height and toe shape,
pure white background RGB(255,255,255), minimal shadow,
studio lighting, soft highlights on glossy surfaces,
commercial fashion photography, luxury presentation,
high resolution, sharp focus, photorealistic,
shoe占比 70-80%, vertical composition to show heel,
for fashion e-commerce, 8k uhd, product showcase
```

**Negative**:
```
blur, noise, low quality, cheap materials,
plastic toy appearance, unrealistic shine,
cluttered background, colored background, patterns,
harsh shadows, dark lighting, underexposed,
people, feet, model wearing, legs,
cartoon, sketch, 3d render look,
deformed heel, broken heel, asymmetric,
bent or curved heel, distorted toe,
text, watermark, brand tags,
worn, scuffed, damaged appearance
```

**参数建议**:
- Model: Fashion Product Photography XL
- LoRA: Glossy Surface (0.5) + Fashion Product (0.7)
- Denoise: 0.35-0.40
- Canny: 0.98 (鞋跟容易变形)
- Depth: 0.60

---

### 帆布鞋 / 休闲鞋 (Canvas / Casual Shoes)

**Positive**:
```
professional product photography, canvas sneakers, casual shoes,
cotton canvas fabric, rubber toe cap, lace-up design,
fabric texture visible, clean and new appearance,
side 45-degree angle view, single shoe display,
pure white background RGB(255,255,255), soft shadow,
studio lighting, bright and even, commercial photo,
high detail, sharp focus, photorealistic,
shoe占比 75-85%, casual style presentation,
for e-commerce listing, 8k uhd, product showcase
```

**Negative**:
```
blur, noise, low quality, dirty, stained,
worn canvas, frayed edges, old appearance,
cluttered background, non-white background,
harsh shadows, uneven lighting,
people, feet, model, legs,
cartoon, sketch, unrealistic,
deformed shape, asymmetric, distorted sole,
text, watermark, logos (except product original),
shoe box, packaging, accessories
```

**参数建议**:
- Model: Product Photography XL
- LoRA: Fabric Texture (0.6)
- Denoise: 0.40-0.45
- Canny: 0.95
- Depth: 0.65

---

### 靴子 (Boots)

**Positive**:
```
professional product photography, leather boots, [ankle/knee-high] boots,
genuine leather or suede material, visible texture,
zipper details, heel design, toe cap,
side view showing full boot height, single boot display,
pure white background RGB(255,255,255), soft contact shadow,
studio lighting, commercial photography,
high resolution, sharp details, photorealistic,
boot占比 70-80%, vertical composition,
for e-commerce listing, 8k uhd, product showcase
```

**Negative**:
```
blur, noise, low quality, cheap materials,
plastic appearance, unrealistic texture,
cluttered background, colored background,
harsh shadows, dark lighting, underexposed,
people, legs, model wearing, feet,
cartoon, sketch, 3d render,
deformed shape, asymmetric, bent shaft,
distorted heel, crooked zipper,
text, watermark, tags,
worn, scuffed, damaged look
```

**参数建议**:
- Model: Realistic Vision V6.0
- LoRA: Leather Material (0.7) + Product Photo (0.6)
- Denoise: 0.38-0.45
- Canny: 0.95
- Depth: 0.70

---

## 按平台优化的 Prompt 调整

### 淘宝/天猫

**额外强调**:
```
Taobao product listing, Chinese e-commerce standard,
800x800 minimum resolution, 1200x1200 recommended,
pure white background RGB(255,255,255),
product占比 70-85%, clean and bright
```

**避免**:
- 过于艺术化的光影
- 过于复杂的构图
- 过于饱和的色彩

### 京东

**额外强调**:
```
JD.com product listing standard,
1000x1000 resolution, centered composition,
pure white background RGB(255,255,255),
product占比 60-80%, professional presentation
```

**特点**: 京东更偏好正式、专业的风格

### 亚马逊

**额外强调**:
```
Amazon product listing, international e-commerce standard,
2000x2000 high resolution, maximum detail,
pure white background RGB(255,255,255) or RGB(246,246,246),
product占比 85%+, fill the frame,
enable zoom function, photorealistic quality
```

**严格要求**:
- 产品占比必须 ≥85%
- 背景绝对纯白
- 无任何文字、水印、装饰

---

## 特殊场景 Prompt

### 白色鞋子（避免与白底融合）

**Positive 增加**:
```
white shoes with visible edges, subtle gray contact shadow,
edge definition, slight ambient occlusion,
differentiate from white background, clean separation
```

**技巧**: 使用淡灰色阴影分离产品与背景

### 反光材质鞋子（控制高光）

**Positive 增加**:
```
glossy surface with controlled reflections,
soft highlights, no harsh specular,
natural light reflection, professional studio lighting
```

**Negative 增加**:
```
overexposed highlights, blown out reflections,
harsh glare, mirror-like reflection
```

### 多材质组合鞋子

**Positive 增加**:
```
mixed materials, leather and mesh combination,
distinct material textures, leather grain and fabric weave visible,
material transition clear, realistic multi-material rendering
```

---

## Prompt 优化技巧

### 权重调整语法

```
(keyword:1.2) - 增加权重 20%
(keyword:0.8) - 降低权重 20%
((keyword)) - 增加权重（等同于 1.1）
[keyword] - 降低权重（等同于 0.9）
```

**示例**:
```
(pure white background:1.3), ((photorealistic)), (high detail:1.2),
[artistic], [creative lighting]
```

### 材质描述优先级

1. **材质名称**: leather, canvas, mesh, suede
2. **材质特性**: glossy, matte, textured, smooth
3. **材质细节**: grain, weave, stitching

### 光线描述

- **明亮均匀**: studio lighting, bright and even, soft shadows
- **柔和自然**: natural studio lighting, diffused light, gentle shadows
- **高光控制**: controlled highlights, no harsh specular

### 背景描述

- **纯白底**: pure white background RGB(255,255,255), solid white, no texture
- **阴影**: soft contact shadow, minimal shadow, no shadow

---

## 测试和迭代

### 首次生成建议

1. 使用推荐的基础 prompt
2. Denoise 从 0.40 开始
3. Canny 权重 0.95（保持结构）
4. 生成 4 张图片，选择最佳

### 常见问题调整

| 问题 | Prompt 调整 | 参数调整 |
|------|------------|---------|
| 结构变形 | 增加 "sharp edges, correct shape" | Canny +0.05 |
| 背景不纯白 | 强调 "(pure white background:1.3)" | — |
| 材质不真实 | 增加材质细节描述 | 增加材质 LoRA 权重 |
| 阴影过重 | "minimal shadow, soft lighting" | 降低 Denoise -0.05 |
| 细节模糊 | "(high detail:1.2), sharp focus" | Steps +5 |

### A/B 测试

对比不同 prompt 效果：
- Prompt A: 基础描述
- Prompt B: 增加材质细节
- Prompt C: 调整光线描述

选择转化率最高的 prompt 模板。

---

## 批量处理 Prompt 生成

对于批量处理多张鞋子图片，使用统一的 prompt 模板：

```python
def generate_prompt(shoe_type, material, platform):
    base = "professional product photography, "
    product = f"{shoe_type}, {material}, "
    background = "pure white background RGB(255,255,255), "
    quality = "studio lighting, high detail, photorealistic, 8k uhd"

    if platform == "amazon":
        platform_spec = "product占比 85%+, 2000x2000 resolution, "
    elif platform == "taobao":
        platform_spec = "product占比 70-85%, 1200x1200 resolution, "
    else:
        platform_spec = ""

    return base + product + platform_spec + background + quality
```

示例输出：
```
professional product photography, sneakers, mesh fabric,
product占比 70-85%, 1200x1200 resolution,
pure white background RGB(255,255,255),
studio lighting, high detail, photorealistic, 8k uhd
```
