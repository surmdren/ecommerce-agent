# 鞋子材质增强指南

## 核心理念

电商鞋子图的材质增强目标：
1. **真实性**: 材质表现接近实物
2. **吸引力**: 强化质感，提升视觉冲击
3. **准确性**: 色彩、纹理与实物一致，避免退货

---

## 按材质类型的增强策略

### 皮革材质 (Leather)

#### 真皮 (Genuine Leather)

**材质特征**:
- 表面有天然纹理（皮革纹路）
- 光泽自然柔和，非镜面反射
- 边缘有皮革厚度感
- 色彩饱和度中等

**SD 优化参数**:
```yaml
Model: epiCRealism
LoRA: Leather Material (0.7) + Professional Product (0.6)
Denoise: 0.35-0.42
Canny: 0.95
Depth: 0.70
```

**Prompt 增强**:
```
Positive:
genuine leather, natural leather grain, pebbled texture,
soft matte finish, subtle sheen, natural leather color,
visible stitching details, leather thickness visible at edges,
high-quality leather, premium material

Negative:
fake plastic, shiny plastic, vinyl, artificial leather,
over-glossy, mirror reflection, flat texture,
cheap synthetic material
```

**后处理技巧**:
- 强化皮革纹理：使用 Clarity/Texture 增强工具（+10 ~ +20）
- 控制高光：高光部分不要过曝，保持柔和反射
- 边缘处理：确保皮革边缘有厚度感和自然切口
- 色彩调整：皮革色彩饱和度略降（-5 ~ -10），保持自然感

---

#### 漆皮 (Patent Leather)

**材质特征**:
- 高光泽镜面效果
- 反射清晰，有环境映射
- 表面平滑无纹理
- 色彩饱和度高

**SD 优化参数**:
```yaml
Model: Fashion Product Photography XL
LoRA: Glossy Surface (0.6) + Fashion Product (0.7)
Denoise: 0.35-0.40
Canny: 0.95
Depth: 0.65
```

**Prompt 增强**:
```
Positive:
patent leather, glossy finish, mirror-like surface,
high sheen, reflective coating, polished leather,
smooth texture, luxury appearance, vivid color,
controlled highlights, professional lighting

Negative:
matte finish, dull surface, rough texture,
overexposed highlights, blown out reflections,
cheap plastic, artificial gloss, vinyl
```

**后处理技巧**:
- 高光控制：确保高光位置合理（主光源位置），不要过曝
- 反射增强：适度增加 Vibrance (+10)，强化漆皮光泽感
- 色彩饱和：漆皮色彩饱和度可以略高（+5 ~ +10）

---

#### 磨砂皮 / 绒面革 (Suede / Nubuck)

**材质特征**:
- 表面柔软，有绒毛质感
- 哑光表面，无反光
- 色彩饱和度较低，柔和
- 边缘有绒毛感

**SD 优化参数**:
```yaml
Model: Realistic Vision V6.0
LoRA: Fabric Texture (0.6) + Suede Material (0.5)
Denoise: 0.38-0.45
Canny: 0.95
Depth: 0.70
```

**Prompt 增强**:
```
Positive:
suede leather, nubuck material, soft velvet-like texture,
napped finish, fuzzy surface, matte appearance,
no shine, soft and luxurious, fine nap,
subtle color variation, premium suede

Negative:
shiny surface, glossy finish, smooth leather,
reflective, patent leather, plastic appearance,
flat texture, hard surface
```

**后处理技巧**:
- 纹理强化：使用 Texture 工具（+15 ~ +25）增强绒毛质感
- 去除高光：确保表面完全哑光，无任何反光点
- 柔化处理：整体略微柔化（-5 Clarity），模拟绒面柔软感

---

### 织物材质 (Fabric)

#### 帆布 (Canvas)

**材质特征**:
- 棉质编织纹理清晰
- 哑光表面
- 颜色饱和度中等
- 边缘有织物毛边感

**SD 优化参数**:
```yaml
Model: Product Photography XL
LoRA: Fabric Texture (0.6) + Canvas Material (0.5)
Denoise: 0.40-0.45
Canny: 0.95
Depth: 0.65
```

**Prompt 增强**:
```
Positive:
canvas fabric, cotton canvas, woven texture,
visible weave pattern, fabric grain, textile surface,
matte finish, breathable material, casual style,
clean canvas, new fabric appearance

Negative:
shiny, glossy, smooth leather, synthetic material,
plastic surface, reflective, no texture,
worn fabric, dirty, faded
```

**后处理技巧**:
- 强化编织纹理：Texture +20，Clarity +10
- 确保织物纹路清晰可见（特别是放大查看）
- 颜色调整：帆布色彩相对朴素，饱和度适中（不要过饱和）

---

#### 网布 / 透气网面 (Mesh)

**材质特征**:
- 透气孔结构明显
- 立体编织感
- 半透明效果（部分网布）
- 通常用于运动鞋

**SD 优化参数**:
```yaml
Model: Product Photography XL
LoRA: Fabric Texture (0.7) + Sport Shoes (0.5)
Denoise: 0.40-0.45
Canny: 0.95
Depth: 0.65
```

**Prompt 增强**:
```
Positive:
mesh fabric, breathable mesh, athletic mesh,
perforated textile, woven mesh pattern,
ventilation holes visible, 3D knit structure,
lightweight material, sports shoe mesh,
texture clarity, modern athletic design

Negative:
solid fabric, no holes, smooth surface,
flat texture, non-breathable, heavy material,
leather, canvas, no mesh pattern
```

**后处理技巧**:
- 强化网孔结构：Texture +25，确保透气孔清晰
- 立体感增强：Depth 权重提高到 0.70
- 半透明处理：如网布半透明，确保内层结构隐约可见

---

### 合成材质 (Synthetic Materials)

#### PU / 人造革 (PU Leather / Synthetic Leather)

**材质特征**:
- 表面纹理规律（模仿真皮）
- 光泽度略高于真皮
- 边缘切口平整（无天然皮革厚度感）

**SD 优化参数**:
```yaml
Model: Realistic Vision V6.0
LoRA: Product Photo Realism (0.7)
Denoise: 0.38-0.45
Canny: 0.95
Depth: 0.65
```

**Prompt 增强**:
```
Positive:
synthetic leather, PU leather, faux leather,
embossed texture, uniform grain pattern,
smooth finish, modern material, clean appearance,
premium synthetic, leather-like texture

Negative:
cheap plastic, shiny vinyl, toy-like,
over-glossy, artificial sheen, low quality,
flat texture, no grain
```

**后处理技巧**:
- 纹理规律化：PU 革纹理较规律，确保纹路一致
- 光泽适度：略高于真皮，但避免塑料感
- 边缘处理：切口平整，不强调厚度感

---

#### TPU / 橡胶 (Rubber / TPU)

**材质特征**:
- 半透明或不透明
- 光泽柔和，有轻微弹性感
- 边缘圆润，无锐利切口
- 常用于鞋底、防护部位

**SD 优化参数**:
```yaml
Model: Realistic Vision V6.0
LoRA: Rubber Material (0.6)
Denoise: 0.38-0.45
Canny: 0.95
Depth: 0.70
```

**Prompt 增强**:
```
Positive:
rubber material, TPU component, flexible material,
semi-transparent rubber, soft rubber texture,
smooth rubber surface, protective element,
durable material, slight sheen, rounded edges

Negative:
hard plastic, rigid material, sharp edges,
glossy plastic, brittle appearance, flat texture,
cheap rubber, cracked surface
```

**后处理技巧**:
- 半透明效果：如 TPU 半透明，确保内部结构隐约可见
- 弹性感：边缘圆润柔和，避免硬质感
- 光泽控制：轻微柔和光泽，不要镜面反射

---

### 特殊材质 (Special Materials)

#### 反光材质 (Reflective Material)

**材质特征**:
- 强反光效果
- 灰色或银色外观
- 受光角度影响大

**SD 优化参数**:
```yaml
Model: Realistic Vision V6.0
LoRA: Reflective Material (0.7)
Denoise: 0.35-0.40
Canny: 0.95
Depth: 0.65
```

**Prompt 增强**:
```
Positive:
reflective material, 3M reflective tape, retroreflective surface,
high-visibility element, safety feature, bright reflection,
silver gray color, light-catching surface, nighttime visibility

Negative:
matte surface, non-reflective, dull finish,
no shine, flat color, regular fabric
```

**后处理技巧**:
- 高光增强：反光部位适度增强亮度（+10 ~ +20 Highlights）
- 色彩处理：通常为银灰色，确保色彩准确
- 光线角度：确保反光效果符合主光源位置

---

#### 金属配件 (Metal Hardware)

**材质特征**:
- 鞋扣、鞋眼、拉链等金属部件
- 金属光泽明显（金色、银色、古铜色）
- 反射清晰，有高光

**SD 优化参数**:
```yaml
Model: Realistic Vision V6.0
LoRA: Metal Material (0.7)
Denoise: 0.35-0.40
Canny: 0.95
Depth: 0.70
```

**Prompt 增强**:
```
Positive:
metal hardware, metal buckle, zipper pull, eyelets,
polished metal, [gold/silver/bronze] finish,
metallic sheen, reflective metal, premium hardware,
detailed metal work, high-quality fittings

Negative:
plastic hardware, cheap fittings, dull metal,
tarnished, rusted, scratched, low quality,
flat metal, no reflection
```

**后处理技巧**:
- 高光强化：金属部分高光清晰（+20 ~ +30 Highlights）
- 色彩准确：金色/银色/古铜色色彩准确还原
- 细节锐化：金属边缘锐化（+15 Sharpness）

---

## 多材质组合优化

很多鞋子是多材质组合（如运动鞋 = 网布 + 合成革 + 橡胶大底）。

### 优化策略

**1. 分层处理**:
- 使用 Segmentation Mask 分离不同材质区域
- 对每个材质区域应用不同的 LoRA 或 Prompt 权重

**2. Prompt 组合**:
```
Positive:
professional product photography, athletic sneakers,
mixed materials design,
[mesh fabric upper, breathable mesh, woven texture],
[synthetic leather overlays, smooth PU surface],
[rubber outsole, textured grip pattern],
each material clearly distinct, realistic multi-material rendering,
pure white background RGB(255,255,255)
```

**3. 材质对比度**:
- 确保不同材质在视觉上有明显区分
- 网布（哑光）vs 合成革（半光）vs 橡胶（柔光）

**4. 过渡区域**:
- 材质交界处要自然过渡（如缝线、胶合线）
- 避免材质突变或融合不清

---

## 材质增强检查清单

### 真皮鞋检查项

- [ ] 皮革纹理清晰可见
- [ ] 光泽自然柔和，非镜面
- [ ] 边缘有皮革厚度感
- [ ] 缝线清晰，针脚均匀
- [ ] 色彩饱和度适中，不过艳

### 运动鞋检查项

- [ ] 网布透气孔结构清晰
- [ ] 合成革部分光泽适度
- [ ] 鞋底纹路清晰，有抓地感
- [ ] 鞋带、鞋眼等细节锐利
- [ ] 不同材质对比明显

### 高跟鞋检查项

- [ ] 漆皮高光自然，无过曝
- [ ] 鞋跟光滑无变形
- [ ] 金属配件（如扣环）反光清晰
- [ ] 色彩饱和度高（如红色高跟鞋要鲜艳）
- [ ] 鞋头、鞋跟边缘锐利

### 帆布鞋检查项

- [ ] 帆布编织纹理清晰
- [ ] 橡胶大底纹路可见
- [ ] 鞋带、鞋眼金属光泽自然
- [ ] 整体哑光，无错误高光
- [ ] 色彩朴素自然，不过饱和

---

## 常见材质问题及修复

### 问题 1: 皮革看起来像塑料

**原因**: 光泽过高，纹理不自然

**修复方案**:
- Prompt 增加: `natural leather grain, soft matte finish`
- Negative 增加: `plastic, shiny vinyl, artificial`
- 降低 Denoise 到 0.35
- 后处理降低 Highlights (-10)

---

### 问题 2: 网布透气孔不清晰

**原因**: Denoise 过高，细节丢失

**修复方案**:
- 降低 Denoise 到 0.38
- Prompt 增加: `mesh pattern clearly visible, perforated textile`
- 提高 Depth ControlNet 权重到 0.70
- 后处理增加 Texture (+20)

---

### 问题 3: 金属配件反光过亮

**原因**: 高光过曝

**修复方案**:
- Negative 增加: `overexposed highlights, blown out reflections`
- 降低 CFG Scale 到 6.5
- 后处理降低 Highlights (-15)
- 调整 Prompt: `controlled highlights, soft metallic sheen`

---

### 问题 4: 多材质融合不清

**原因**: 材质边界模糊

**修复方案**:
- 提高 Canny ControlNet 权重到 0.98
- Prompt 强调: `each material clearly distinct, sharp material transition`
- 使用 Segmentation ControlNet 辅助分离材质区域
- 后处理局部锐化材质交界处

---

### 问题 5: 绒面革看起来太平滑

**原因**: 缺乏绒毛质感

**修复方案**:
- 更换 LoRA: Suede Material (0.6) 或 Fabric Texture (0.7)
- Prompt 增加: `napped finish, fuzzy surface, soft velvet-like texture`
- Negative 增加: `smooth surface, glossy, shiny`
- 后处理增加 Texture (+20) 和降低 Clarity (-5)

---

## 材质增强工作流

### 步骤 1: 材质识别

分析原图，识别鞋子包含的材质类型：
- 鞋面材质（皮革/网布/帆布）
- 鞋底材质（橡胶/TPU）
- 配件材质（金属/塑料）

### 步骤 2: 选择合适的模型和 LoRA

根据主要材质选择基础模型：
- 皮革为主 → epiCRealism
- 织物为主 → Product Photography XL
- 多材质 → Realistic Vision V6.0

### 步骤 3: 编写 Prompt

使用材质专用 Prompt 模板，强调关键材质特征。

### 步骤 4: 调整参数

根据材质复杂度调整 Denoise 和 ControlNet 权重。

### 步骤 5: 生成和检查

生成图片，使用材质检查清单验证效果。

### 步骤 6: 后处理优化

使用 Photoshop 或其他工具微调材质表现（Texture、Clarity、Highlights）。

---

## 批量材质优化

对于批量处理，建议按材质类型分组：

**皮鞋批次**:
- 统一使用 epiCRealism + Leather Material LoRA
- Denoise: 0.38
- Canny: 0.95, Depth: 0.70

**运动鞋批次**:
- 统一使用 Product Photography XL + Fabric Texture LoRA
- Denoise: 0.40
- Canny: 0.95, Depth: 0.65

**高跟鞋批次**:
- 统一使用 Fashion Product Photography XL + Glossy Surface LoRA
- Denoise: 0.36
- Canny: 0.98, Depth: 0.60

---

## 材质增强最佳实践

1. **了解材质特性**: 不同材质有不同的光泽、纹理、反射特性
2. **保持真实性**: 材质增强不要过度，避免与实物差距过大
3. **细节优先**: 材质的细节（纹理、缝线、边缘）是关键
4. **对比测试**: 生成多张图片，对比选择材质表现最佳的
5. **后处理补充**: SD 生成后，使用后处理工具进一步优化材质
6. **平台适配**: 电商图要求色彩准确，避免因材质失真导致退货

---

## 工具推荐

### LoRA 推荐

- **Leather Material Enhancer**: 增强皮革质感
- **Fabric Texture Booster**: 增强织物纹理
- **Glossy Surface**: 增强光泽表面（漆皮、高跟鞋）
- **Metal Material**: 增强金属配件
- **Product Photo Realism**: 通用产品图真实感

### 后处理工具

- **Photoshop**: Texture, Clarity, Highlights 调整
- **Lightroom**: 局部调整工具（针对不同材质区域）
- **Topaz Sharpen AI**: 细节锐化（特别是纹理）
- **DxO PhotoLab**: 材质质感增强

### 测试工具

- **放大查看**: 使用 2x/4x 放大查看材质细节是否清晰
- **色彩校准**: 使用色卡或实物对比色彩准确性
- **多设备预览**: 在手机、电脑、平板上查看材质表现
