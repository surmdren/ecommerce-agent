#!/usr/bin/env python3
"""
ComfyUI 工作流生成器
根据图片分析结果自动生成最佳 ComfyUI 工作流配置
"""

import json
from typing import Dict, List, Optional


class WorkflowGenerator:
    """生成定制化的 ComfyUI 工作流"""

    # 推荐模型配置
    MODELS = {
        "optical": {
            "base": "epiCRealism",
            "vae": "vae-ft-mse-840000-ema-pruned",
            "loras": [
                {"name": "Product Photo Realism", "weight": 0.7},
                {"name": "Glass Material Enhancer", "weight": 0.5}
            ]
        },
        "metal": {
            "base": "Realistic Vision V6.0",
            "vae": "vae-ft-mse-840000-ema-pruned",
            "loras": [
                {"name": "Metal Material Enhancer", "weight": 0.7},
                {"name": "Industrial Design", "weight": 0.5}
            ]
        },
        "composite": {
            "base": "SDXL Product Design",
            "vae": "sdxl_vae",
            "loras": []
        }
    }

    def __init__(self, product_type: str = "optical"):
        self.product_type = product_type
        self.model_config = self.MODELS.get(product_type, self.MODELS["optical"])

    def generate_workflow(
        self,
        denoise: float = 0.40,
        canny_strength: float = 0.90,
        depth_strength: float = 0.60,
        cfg: float = 7.0,
        steps: int = 35,
        positive_prompt: Optional[str] = None,
        negative_prompt: Optional[str] = None
    ) -> Dict:
        """
        生成完整的 ComfyUI 工作流配置

        Args:
            denoise: 降噪强度 (0.3-0.5)
            canny_strength: Canny ControlNet 权重 (0.85-1.0)
            depth_strength: Depth ControlNet 权重 (0.5-0.7)
            cfg: CFG Scale (6-8)
            steps: 采样步数 (30-40)
            positive_prompt: 正向提示词
            negative_prompt: 负向提示词

        Returns:
            ComfyUI 工作流配置字典
        """

        if positive_prompt is None:
            positive_prompt = self._get_default_positive_prompt()

        if negative_prompt is None:
            negative_prompt = self._get_default_negative_prompt()

        workflow = {
            "workflow_name": f"Industrial Product - {self.product_type.title()}",
            "model_config": self.model_config,
            "parameters": {
                "denoise": denoise,
                "canny_strength": canny_strength,
                "depth_strength": depth_strength,
                "cfg_scale": cfg,
                "steps": steps,
                "sampler": "dpmpp_2m_karras",
                "scheduler": "karras"
            },
            "prompts": {
                "positive": positive_prompt,
                "negative": negative_prompt
            },
            "controlnets": [
                {
                    "type": "canny",
                    "model": "control_v11p_sd15_canny",
                    "strength": canny_strength,
                    "preprocessor": "canny"
                },
                {
                    "type": "depth",
                    "model": "control_v11f1p_sd15_depth",
                    "strength": depth_strength,
                    "preprocessor": "depth_midas"
                }
            ]
        }

        return workflow

    def _get_default_positive_prompt(self) -> str:
        """获取默认正向提示词"""
        base = "professional product photography, industrial design, "

        if self.product_type == "optical":
            specific = "precision optical instrument, laboratory equipment, glass optics, metal body, scientific grade, "
        elif self.product_type == "metal":
            specific = "precision industrial equipment, brushed metal, stainless steel, high-end manufacturing, "
        else:
            specific = "precision instrument, professional equipment, "

        quality = "studio lighting, white background, high detail, octane render, photorealistic, commercial photography, clean composition, soft shadows, professional color grading, 8k uhd"

        return base + specific + quality

    def _get_default_negative_prompt(self) -> str:
        """获取默认负向提示词"""
        return (
            "blur, noise, grain, low quality, amateur, cluttered background, "
            "harsh shadows, overexposed, underexposed, cartoon, sketch, "
            "unrealistic materials, plastic toy, cheap rendering, toy-like, "
            "simplified, low detail, fake materials, exaggerated colors, "
            "artistic rendering"
        )

    def suggest_parameters(self, analysis: Dict) -> Dict:
        """
        根据分析结果建议最佳参数

        Args:
            analysis: 图片分析结果字典，包含 material_issues, lighting_issues 等

        Returns:
            建议的参数配置
        """
        # 基础参数
        denoise = 0.40
        canny = 0.90
        depth = 0.60
        cfg = 7.0

        # 根据问题严重程度调整
        issue_count = sum([
            len(analysis.get("material_issues", [])),
            len(analysis.get("lighting_issues", [])),
            len(analysis.get("composition_issues", []))
        ])

        if issue_count <= 2:  # 问题较少
            denoise = 0.35
        elif issue_count <= 4:  # 问题中等
            denoise = 0.40
        else:  # 问题较多
            denoise = 0.45
            canny = 0.85  # 降低结构约束，允许更多变化

        # 如果有复杂结构
        if analysis.get("complex_structure", False):
            canny = 0.95
            depth = 0.70

        return {
            "denoise": denoise,
            "canny_strength": canny,
            "depth_strength": depth,
            "cfg": cfg,
            "steps": 35
        }

    def export_to_file(self, workflow: Dict, output_path: str):
        """导出工作流到 JSON 文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(workflow, f, indent=2, ensure_ascii=False)
        print(f"✅ 工作流已导出到: {output_path}")


def main():
    """示例用法"""
    # 创建生成器
    generator = WorkflowGenerator(product_type="optical")

    # 模拟分析结果
    analysis = {
        "material_issues": ["玻璃透明度不足", "金属反射过亮"],
        "lighting_issues": ["阴影过硬"],
        "composition_issues": [],
        "complex_structure": True
    }

    # 生成建议参数
    params = generator.suggest_parameters(analysis)
    print("建议参数:", params)

    # 生成工作流
    workflow = generator.generate_workflow(**params)

    # 导出
    generator.export_to_file(workflow, "custom_workflow.json")
    print("\n工作流配置:")
    print(json.dumps(workflow, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
