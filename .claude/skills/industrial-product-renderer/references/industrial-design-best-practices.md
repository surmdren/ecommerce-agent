# 工业设计产品渲染最佳实践

## 官网级产品图标准

### 1. 布光原则

**三点布光系统**：
- **主光（Key Light）**：45° 角度，强度 100%，创造主要阴影和立体感
- **辅助光（Fill Light）**：与主光相对，强度 30-50%，柔化阴影
- **轮廓光（Rim Light）**：背后或侧后方，强度 60-80%，分离产品与背景

**光学仪器特殊要求**：
- 玻璃/透镜部分：需要柔和的环境光，避免硬反射
- 金属部分：使用 HDRI 环境贴图增强真实反射
- 刻度/标识：确保清晰可读，避免过曝或阴影遮挡

### 2. 材质表现

**玻璃/光学元件**：
- IOR（折射率）：1.5-1.9（根据实际材质）
- 透明度：85-95%
- 表面粗糙度：0.01-0.05（高光洁度）
- 内部散射：subtle，避免完全透明

**金属部件**：
- 铝合金：粗糙度 0.2-0.3，灰色调（RGB: 200,200,205）
- 不锈钢：粗糙度 0.1-0.2，高反射
- 阳极氧化：哑光，粗糙度 0.4-0.6

**塑料外壳**：
- ABS/PC：粗糙度 0.3-0.5，轻微反射
- 磨砂表面：粗糙度 0.6-0.8
- 避免过度塑料感（降低反射强度）

### 3. 背景与构图

**背景选择**：
- **纯白底**：RGB(255,255,255)，适合产品目录
- **渐变底**：白到浅灰，增加空间感
- **环境场景**（高端产品）：实验室台面、测量场景

**构图原则**：
- 产品居中，占画面 60-75%
- 黄金分割构图（可选）
- 关键细节朝向相机
- 3/4 视角展示立体感

**阴影与倒影**：
- 柔和接触阴影（Opacity: 20-40%）
- 可选镜面倒影（Opacity: 10-20%，渐变衰减）

### 4. 后期处理标准

**色彩调整**：
- 对比度：+10 到 +20
- 饱和度：-5 到 +10（避免过饱和）
- 色温：中性或偏冷（工业感）
- 高光保留细节，避免过曝

**锐化与细节**：
- USM 锐化：Amount 80-120%, Radius 1.0-1.5px
- 选择性锐化：重点锐化产品边缘和文字
- 降噪（如有）：保留金属纹理，不过度平滑

**输出规格**：
- 分辨率：3000px（长边），300 DPI
- 格式：PNG（透明底）或 JPG（白底，质量 95%）
- 色彩空间：sRGB（网页）或 Adobe RGB（印刷）

### 5. 光学仪器特定标准

**显微镜类产品**：
- 强调目镜、物镜的透明度和光学涂层
- 展示调焦旋钮、载物台细节
- 金属镜筒需要真实的拉丝/抛光纹理

**光谱仪/分析仪**：
- 展示屏幕/显示区域（可添加淡入的界面）
- 接口/端口清晰可见
- 外壳接缝和按键需要精细建模

**测量仪器**：
- 刻度清晰可读
- 指针/数显部分需要高对比度
- 手持部分展示人机工程学设计

## 常见问题诊断

### 材质问题
- ❌ 玻璃完全透明无厚度 → ✅ 增加 IOR 和边缘厚度
- ❌ 金属反射过亮 → ✅ 降低粗糙度或调整 HDRI 强度
- ❌ 塑料过于"塑料感" → ✅ 增加粗糙度，降低反射

### 光线问题
- ❌ 阴影过硬 → ✅ 增大光源面积或使用柔光箱
- ❌ 整体偏暗 → ✅ 增加环境光或辅助光强度
- ❌ 高光过曝 → ✅ 降低主光强度，启用 HDR 渲染

### 构图问题
- ❌ 产品偏离中心 → ✅ 重新对齐或裁剪
- ❌ 关键细节被遮挡 → ✅ 调整角度或增加辅助视图
- ❌ 透视畸变 → ✅ 使用长焦镜头（50-85mm 等效）

## SD Prompt 最佳实践

**正向 Prompt 模板**：
```
professional product photography, industrial design, [product type],
studio lighting, white background, high detail, octane render,
photorealistic, commercial photography, clean composition,
soft shadows, professional color grading, 8k uhd
```

**负向 Prompt 模板**：
```
blur, noise, grain, low quality, amateur, cluttered background,
harsh shadows, overexposed, underexposed, cartoon, sketch,
unrealistic materials, plastic toy, cheap rendering
```

**针对光学仪器**：
```
Positive: precision optical instrument, laboratory equipment,
         glass optics, metal body, scientific grade,
         accurate materials, technical product shot

Negative: toy-like, simplified, low detail, fake materials,
         exaggerated colors, artistic rendering
```
