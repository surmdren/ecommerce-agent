# Stable Diffusion 模型推荐指南

## 工业产品渲染推荐模型

### Tier 1: 首选模型（产品渲染专用）

1. **Realistic Vision V6.0**
   - 类型：写实风格通用模型
   - 优势：材质真实、光线自然、细节丰富
   - 适用：工业产品、电子设备、机械装备
   - VAE：推荐使用 vae-ft-mse-840000-ema-pruned
   - 下载：Civitai

2. **SDXL Product Design**
   - 类型：SDXL 产品设计专用模型
   - 优势：专为产品渲染优化，结构保持好
   - 适用：所有工业设计产品
   - 注意：需要 SDXL 架构，显存要求 >8GB
   - 下载：Hugging Face

3. **epiCRealism**
   - 类型：超写实风格
   - 优势：金属材质表现优秀，光影细腻
   - 适用：金属外壳产品、精密仪器
   - VAE：自带 VAE，无需额外配置

### Tier 2: 备选模型

4. **DreamShaper XL**
   - 优势：平衡性好，速度快
   - 适用：快速原型渲染

5. **ProtoVision XL**
   - 优势：技术感强，适合科技产品
   - 适用：电子产品、实验仪器

### Tier 3: 特殊场景模型

6. **Product Photo Realism (LoRA)**
   - 类型：LoRA 增强插件
   - 配合：Realistic Vision 或 epiCRealism
   - 权重：0.6-0.8
   - 用途：增强产品照片真实感

7. **Metal Material Enhancer (LoRA)**
   - 用途：专门增强金属材质表现
   - 权重：0.5-0.7
   - 适用：金属外壳产品

## ControlNet 配置

### 必备 ControlNet

1. **Canny Edge**
   - 用途：保持产品轮廓和结构
   - 预处理器：canny
   - 权重：0.8-1.0
   - 控制模式：Balanced
   - **最重要**：确保产品结构不变形

2. **Depth Map**
   - 用途：保持空间关系和立体感
   - 预处理器：depth_midas 或 depth_zoe
   - 权重：0.5-0.7
   - 控制模式：Balanced

### 可选 ControlNet

3. **Normal Map**
   - 用途：增强表面细节和凹凸感
   - 权重：0.3-0.5
   - 适用：需要强化表面纹理的产品

4. **Lineart**
   - 用途：保持产品线条清晰
   - 预处理器：lineart_anime 或 lineart_realistic
   - 权重：0.6-0.8
   - 适用：有复杂线条结构的产品

## 参数配置建议

### 基础参数

```yaml
# Sampling Settings
Sampler: DPM++ 2M Karras
Steps: 30-40
CFG Scale: 6-8
Denoising Strength: 0.3-0.5  # 关键：保持产品结构

# Resolution
Width: 1024 (SD1.5) / 1536 (SDXL)
Height: 1024 (SD1.5) / 1536 (SDXL)
Upscaler: 4x-UltraSharp (后期放大)

# Advanced
Clip Skip: 2
ENSD: 31337
```

### Denoising Strength 指南

- **0.2-0.3**：轻微优化（保留 80% 原图，只修复明显问题）
- **0.3-0.5**：标准优化（保留 50% 原图，平衡优化和保真）
- **0.5-0.7**：深度优化（大幅改变，风险较高）
- **>0.7**：不推荐（可能完全改变产品）

**光学仪器推荐**：0.35-0.45

### CFG Scale 指南

- **4-6**：创意模式（更多变化，适合概念图）
- **6-8**：平衡模式（推荐用于产品渲染）
- **8-12**：严格遵循 prompt（适合精确要求）

## ComfyUI 工作流配置

### 基础增强工作流

**节点组成**：
1. Load Image（原图）
2. Load Checkpoint（Realistic Vision V6.0）
3. ControlNet Canny（权重 0.9）
4. ControlNet Depth（权重 0.6）
5. KSampler（Denoise 0.4）
6. VAE Decode
7. Save Image

### 材质精修工作流

**额外节点**：
- Load LoRA（Product Photo Realism, 0.7）
- Load LoRA（Metal Material, 0.6）
- Face Detailer（替换为 Product Detailer）

### 多视图批量工作流

**批量处理**：
- Image Batch（加载多张图）
- Loop Through Batch
- Auto Queue

## 模型组合推荐

### 光学仪器最佳组合

```
Base Model: epiCRealism
LoRA 1: Product Photo Realism (0.7)
LoRA 2: Glass Material Enhancer (0.5)
ControlNet: Canny (0.95) + Depth (0.6)
Denoise: 0.35
CFG: 7
Steps: 35
```

### 金属仪器最佳组合

```
Base Model: Realistic Vision V6.0
LoRA 1: Metal Material Enhancer (0.7)
LoRA 2: Industrial Design (0.5)
ControlNet: Canny (0.9) + Normal (0.4)
Denoise: 0.40
CFG: 7.5
Steps: 40
```

### 复合材质最佳组合

```
Base Model: SDXL Product Design
ControlNet: Canny (0.85) + Depth (0.55) + Lineart (0.6)
Denoise: 0.38
CFG: 7
Steps: 30
```

## 常见问题与解决方案

### 问题 1: 产品结构变形

**原因**：Denoising 过高或 ControlNet 权重过低

**解决**：
- 降低 Denoising 到 0.3-0.4
- 提高 Canny ControlNet 权重到 0.9-1.0
- 增加 Depth ControlNet（权重 0.6）

### 问题 2: 材质不真实

**原因**：模型选择不当或 prompt 不够精确

**解决**：
- 切换到 epiCRealism 或 Realistic Vision
- 添加材质 LoRA
- Prompt 中明确材质（"brushed aluminum", "polished glass"）

### 问题 3: 细节丢失

**原因**：Denoising 过高或分辨率不足

**解决**：
- 降低 Denoising
- 使用高分辨率输入（>2048px）
- 后期用 Ultimate SD Upscale 放大

### 问题 4: 光线不自然

**原因**：Prompt 中光线描述不当

**解决**：
- 添加 "studio lighting, soft shadows, professional color grading"
- 负向 prompt 加入 "harsh lighting, strong shadows"
- 降低 CFG Scale 到 6-7

## 更新与维护

**模型版本检查**：
- Realistic Vision 当前最新：V6.0 B1
- epiCRealism 当前最新：Natural Sin RC1
- SDXL 基础模型：1.0 refiner

**定期更新**：
- 每月检查 Civitai 新产品渲染模型
- 测试新 LoRA 是否提升效果
- 关注 ControlNet 新预处理器

**本地缓存**：
所有模型下载后存放在：
- Windows: `ComfyUI/models/checkpoints/`
- Mac/Linux: `ComfyUI/models/checkpoints/`
