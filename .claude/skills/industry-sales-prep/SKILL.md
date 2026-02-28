---
name: industry-sales-prep
description: 快速生成行业销售知识库，帮助销售人员掌握专业术语、行业趋势和客户沟通话术。基于产品文档提取关键术语，结合网络搜索补充最新行业信息，输出结构化知识文档、PDF速查表和Anki记忆卡片。适用场景：(1) 销售前准备学习行业知识 (2) 从产品文档提取关键术语和话术 (3) 了解行业最新趋势和竞品动态 (4) 准备客户会议的专业知识储备。当用户提到"行业知识"、"销售准备"、"专业术语"、"客户沟通话术"、"行业学习"时触发。
---

# Industry Sales Prep - 行业销售知识库生成器

Generate comprehensive industry knowledge bases for sales professionals to quickly master domain-specific terminology, trends, and customer communication strategies.

## Workflow

Follow these steps to generate an industry sales knowledge base:

### 1. Gather Input Materials

Collect the following information from the user:

- **Industry name**: The specific industry or domain (e.g., "精密光学仪器", "工业自动化", "医疗器械")
- **Product documents**: PDF/Markdown files containing product specifications, manuals, or technical documentation
- **Optional context**: Specific customer segments, competitive landscape, or regional focus

If the user provides a document file path, read it first to understand the product domain.

### 2. Extract Core Terminology from Documents

If product documents are provided:

1. Read the document using the Read tool
2. Identify and extract:
   - **Technical terms**: Product features, specifications, parameters
   - **Industry jargon**: Domain-specific vocabulary
   - **Key metrics**: Performance indicators, standards, certifications
   - **Common abbreviations**: Acronyms frequently used
3. For each term, note:
   - Chinese name
   - English equivalent (if mentioned or can be inferred)
   - Context of usage in the document
   - Related specifications or values

Refer to `references/optics-industry-example.md` for a concrete example of terminology extraction from a polarizer detection system manual.

### 3. Supplement with Latest Industry Research

Use WebSearch to gather:

1. **Industry overview** (search: "[industry name] market size trends 2024-2026")
   - Market size and growth rate
   - Key application scenarios
   - Major players and competitive landscape

2. **Latest terminology and standards** (search: "[industry name] technical terminology glossary")
   - Industry-standard definitions
   - Emerging technical terms
   - Certification and compliance standards

3. **Sales best practices** (search: "[industry name] sales strategies customer pain points")
   - Common customer questions
   - Typical objections and responses
   - Value proposition frameworks

4. **Competitive intelligence** (search: "[industry name] leading companies product comparison")
   - Key competitors
   - Product differentiation points
   - Market positioning strategies

### 4. Generate Structured Knowledge Base

Create a comprehensive knowledge document following the template structure in `references/industry-knowledge-template.md`.

The output should include these sections:

**Section 1: Industry Overview (行业概览)**
- Market landscape and trends
- Key application scenarios
- Major players
- Target customer segments

**Section 2: Core Terminology Database (核心术语库)**

Organize terms by category:
- Product-related terms
- Technical parameters and specifications
- Process and methodology terms
- Compliance and certification terms

For each term, provide:
```markdown
### [中文术语] (English Term)
- **定义**: Clear explanation in Chinese
- **英文**: English equivalent
- **应用场景**: Where/when it's used
- **相关参数**: Related specifications or values
- **客户关注点**: Why customers care about this
```

**Section 3: Customer Communication Scripts (客户沟通话术)**

Provide ready-to-use conversation frameworks:
- Opening questions to understand customer needs
- Product advantage positioning statements
- Common objection handling scripts
- Technical explanation simplification (translating jargon to customer language)

**Section 4: FAQs and Objection Handling (常见问题与异议处理)**
- Top 10 customer questions with answers
- Competitive comparison talking points
- Price/value justification scripts

**Section 5: Latest Industry Trends (最新行业趋势)**
- Recent technology developments
- Regulatory changes
- Market opportunities
- Future outlook

### 5. Generate Additional Output Formats (Optional)

Based on user preference, generate:

**A. PDF Quick Reference Sheet**
- Single-page or double-sided cheat sheet
- Top 20 essential terms with definitions
- Key product advantages
- Common customer questions

Use the template in `assets/output-templates/quick-reference-template.md` and convert to PDF.

**B. Anki Memory Cards**
- Flashcard format for spaced repetition learning
- Front: Chinese term / English term
- Back: Definition, usage example, customer relevance

Generate a CSV file that can be imported into Anki using the script `scripts/generate_anki_cards.py`.

### 6. Review and Iterate

Present the generated knowledge base to the user and offer to:
- Add more specific terminology
- Expand certain sections
- Include company-specific product details
- Customize for specific customer segments or regions

## Output Format Requirements

- **Primary output**: Markdown document (knowledge-base-[industry]-[date].md)
- **File location**: Save to the current working directory or user-specified path
- **Language**: Bilingual (Chinese + English) for terminology, Chinese for explanations
- **Structure**: Use clear headings, bullet points, and tables for easy navigation
- **Length**: Comprehensive but concise (typically 5,000-10,000 words)

## Important Guidelines

- **Accuracy first**: Verify technical terms through multiple sources
- **Practical focus**: Prioritize information directly useful for customer conversations
- **Simplicity**: Explain complex concepts in accessible language
- **Cultural context**: Consider regional differences in terminology and business practices
- **Competitive intelligence**: Be factual, avoid speculation or unverified claims
- **Update frequency**: Note the generation date and recommend periodic updates (quarterly)

## Examples

See `references/optics-industry-example.md` for a complete example based on a polarizer detection system.

## Related Resources

- **Template**: `references/industry-knowledge-template.md` - Standard output structure
- **Example**: `references/optics-industry-example.md` - Optical instrumentation industry case
- **Scripts**:
  - `scripts/extract_terms_from_pdf.py` - Automated term extraction
  - `scripts/generate_anki_cards.py` - Flashcard generation
- **Templates**:
  - `assets/output-templates/knowledge-base-template.md` - Main document template
  - `assets/output-templates/quick-reference-template.md` - PDF cheat sheet template
