#!/usr/bin/env python3
"""
Extract technical terms from PDF documents for industry knowledge base.

Usage:
    python extract_terms_from_pdf.py <pdf_file> [--output <output_file>]

Requirements:
    pip install pypdf2 or pip install pdfplumber
"""

import sys
import re
import argparse
from collections import Counter
from pathlib import Path

def extract_terms_from_pdf(pdf_path):
    """
    Extract potential technical terms from PDF.

    This is a basic implementation. For production use, consider:
    - Using NLP libraries like spaCy or jieba for better term extraction
    - Adding domain-specific dictionaries
    - Implementing TF-IDF for term importance ranking
    """
    try:
        import pdfplumber
    except ImportError:
        print("Error: pdfplumber not installed. Install with: pip install pdfplumber")
        sys.exit(1)

    terms = []
    english_terms = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            # Extract Chinese technical terms (typically 2-6 characters)
            chinese_pattern = r'[\u4e00-\u9fa5]{2,6}'
            chinese_terms = re.findall(chinese_pattern, text)
            terms.extend(chinese_terms)

            # Extract English terms (capitalized words or acronyms)
            english_pattern = r'\b[A-Z][A-Za-z]{2,}|\b[A-Z]{2,}\b'
            english_matches = re.findall(english_pattern, text)
            english_terms.extend(english_matches)

    # Count term frequency
    term_freq = Counter(terms)
    english_freq = Counter(english_terms)

    return term_freq, english_freq

def format_term_output(term_freq, english_freq, top_n=50):
    """Format extracted terms as Markdown."""
    output = []
    output.append("# 提取的技术术语\n")
    output.append("## 中文术语（按频率排序）\n")
    output.append("| 排名 | 术语 | 出现次数 | 英文 | 定义 | 应用场景 |")
    output.append("|------|------|----------|------|------|----------|")

    for i, (term, count) in enumerate(term_freq.most_common(top_n), 1):
        output.append(f"| {i} | {term} | {count} | [待补充] | [待补充] | [待补充] |")

    output.append("\n## 英文术语（按频率排序）\n")
    output.append("| 排名 | 术语 | 出现次数 | 中文 | 定义 | 应用场景 |")
    output.append("|------|------|----------|------|------|----------|")

    for i, (term, count) in enumerate(english_freq.most_common(top_n), 1):
        output.append(f"| {i} | {term} | {count} | [待补充] | [待补充] | [待补充] |")

    output.append("\n---\n")
    output.append("*注：以上术语通过频率分析自动提取，需要人工审核和补充定义*\n")

    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description='Extract technical terms from PDF')
    parser.add_argument('pdf_file', help='Path to PDF file')
    parser.add_argument('--output', '-o', help='Output markdown file (default: terms.md)',
                       default='extracted-terms.md')
    parser.add_argument('--top', '-t', type=int, default=50,
                       help='Number of top terms to extract (default: 50)')

    args = parser.parse_args()

    if not Path(args.pdf_file).exists():
        print(f"Error: File not found: {args.pdf_file}")
        sys.exit(1)

    print(f"Extracting terms from {args.pdf_file}...")
    term_freq, english_freq = extract_terms_from_pdf(args.pdf_file)

    print(f"Found {len(term_freq)} unique Chinese terms")
    print(f"Found {len(english_freq)} unique English terms")

    output_content = format_term_output(term_freq, english_freq, args.top)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(output_content)

    print(f"\nTerms extracted to {args.output}")
    print(f"Please review and manually add definitions, English equivalents, and usage contexts.")

if __name__ == '__main__':
    main()
