# 鞋子产品图 SD 模型推荐

## 推荐模型 (按鞋款类型)

### 运动鞋 (Sneakers)

**首选**: Product Photography XL
- 优势: 对网布、合成材质表现优秀
- LoRA: Fabric Texture (0.6) + Clean Background (0.8)
- Denoise: 0.38-0.45

**备选**: Realistic Vision V6.0
- 优势: 通用性强，稳定
- LoRA: Product Photo Realism (0.7)

### 皮鞋 (Leather Shoes)

**首选**: epiCRealism
- 优势: 皮革质感真实，光泽自然
- LoRA: Leather Material (0.7) + Professional Product (0.6)
- Denoise: 0.35-0.42

**备选**: Realistic Vision V6.0
- LoRA: Polished Leather (0.6)

### 高跟鞋 (High Heels)

**首选**: Fashion Product Photography XL
- 优势: 光泽面料和优雅感强
- LoRA: Glossy Surface (0.5) + Fashion Product (0.7)
- Denoise: 0.35-0.40

### 帆布鞋 / 休闲鞋

**首选**: Product Photography XL
- LoRA: Fabric Texture (0.6)
- Denoise: 0.40-0.45

## ControlNet 配置

**Canny (必需)**:
- 权重: 0.95
- 作用: 严格保持鞋型轮廓

**Depth (必需)**:
- 权重: 0.65
- 作用: 保持立体感

**Seg (可选，用于背景移除)**:
- 权重: 0.70
- 作用: 精确分离鞋子与背景

## 参数建议

```yaml
基础配置:
  Resolution: 1200x1200
  Sampler: dpmpp_2m_karras
  Steps: 30
  CFG: 7.5

运动鞋:
  Denoise: 0.40
  Canny: 0.95
  Depth: 0.65

皮鞋:
  Denoise: 0.38
  Canny: 0.95
  Depth: 0.70 (强调质感)

高跟鞋:
  Denoise: 0.36
  Canny: 0.98 (鞋跟容易变形)
  Depth: 0.60
```
