#!/usr/bin/env python3
"""
Generate Anki flashcards from product catalog.

Usage:
    python generate_product_anki.py <catalog.md> [--output <anki_import.csv>]

Output format: CSV file with Front, Back, Tags columns for Anki import
"""

import sys
import re
import csv
import argparse
from pathlib import Path


def parse_product_catalog(md_file):
    """
    Parse product catalog markdown and extract products for flashcards.

    Expected format:
        #### {产品名称} ({型号})
        **一句话描述**: ...
        **核心特点**:
        - 特点1
        - 特点2
        **应用场景**:
        - 场景1
    """
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    products = []
    current_category = "uncategorized"

    # Find category headers (### 大类: xxx)
    lines = content.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i]

        # Match category header
        cat_match = re.match(r'^###\s*(?:大类\d*[：:]?\s*)?(.+)$', line)
        if cat_match and '产品名称' not in line:
            current_category = cat_match.group(1).strip()
            i += 1
            continue

        # Match product header
        prod_match = re.match(r'^####\s*(.+?)(?:\s*\(([^)]+)\))?$', line)
        if prod_match:
            product_name = prod_match.group(1).strip()
            model = prod_match.group(2).strip() if prod_match.group(2) else ""

            # Collect product details
            i += 1
            description = ""
            features = []
            scenarios = []

            while i < len(lines) and not lines[i].startswith('####') and not lines[i].startswith('###'):
                detail_line = lines[i].strip()

                # One-line description
                if detail_line.startswith('**一句话描述**'):
                    desc_match = re.search(r'\*\*一句话描述\*\*[：:]\s*(.+)', detail_line)
                    if desc_match:
                        description = desc_match.group(1).strip()

                # Features
                elif '核心特点' in detail_line or (features and detail_line.startswith('-')):
                    if detail_line.startswith('-'):
                        feature = detail_line.lstrip('- ').strip()
                        if feature and not feature.startswith('**'):
                            features.append(feature)

                # Scenarios
                elif '应用场景' in detail_line:
                    # Start collecting scenarios
                    pass
                elif scenarios is not None and detail_line.startswith('-') and '特点' not in ''.join(lines[max(0,i-3):i]):
                    scenario = detail_line.lstrip('- ').strip()
                    if scenario and not scenario.startswith('**'):
                        scenarios.append(scenario)

                i += 1

            products.append({
                'name': product_name,
                'model': model,
                'category': current_category,
                'description': description,
                'features': features[:5],  # Max 5 features
                'scenarios': scenarios[:3]  # Max 3 scenarios
            })
            continue

        i += 1

    return products


def generate_cards(products):
    """
    Generate multiple types of flashcards for each product.

    Card types:
    1. Product identification: Name -> Description + Features
    2. Feature recall: "What are features of X?" -> Feature list
    3. Scenario matching: "For scenario Y, which product?" -> Product + reason
    """
    cards = []

    for product in products:
        name = product['name']
        model = f" ({product['model']})" if product['model'] else ""
        category = product['category']
        desc = product['description'] or "暂无描述"
        features = product['features']
        scenarios = product['scenarios']

        # Tag for organization
        tag = f"product::{category.replace(' ', '_')}"

        # Card Type 1: Product identification
        front1 = f"{name}{model}"
        back1_parts = [f"<b>描述:</b> {desc}"]
        if features:
            back1_parts.append("<b>核心特点:</b><br>" + "<br>".join([f"• {f}" for f in features]))
        back1 = "<br><br>".join(back1_parts)
        cards.append((front1, back1, tag))

        # Card Type 2: Feature recall
        if features:
            front2 = f"{name} 的核心特点是什么？"
            back2 = "<br>".join([f"• {f}" for f in features])
            cards.append((front2, back2, tag))

        # Card Type 3: Scenario matching (one card per scenario)
        for scenario in scenarios:
            front3 = f"客户需要「{scenario}」，推荐什么产品？"
            back3 = f"<b>{name}</b>{model}<br><br>{desc}"
            cards.append((front3, back3, tag + "::scenario"))

    return cards


def main():
    parser = argparse.ArgumentParser(description='Generate Anki flashcards from product catalog')
    parser.add_argument('catalog', help='Path to product catalog markdown file')
    parser.add_argument('--output', '-o', help='Output CSV file for Anki import (default: anki_cards.csv)',
                       default='anki_cards.csv')

    args = parser.parse_args()

    if not Path(args.catalog).exists():
        print(f"Error: File not found: {args.catalog}")
        sys.exit(1)

    print(f"Parsing product catalog from {args.catalog}...")
    products = parse_product_catalog(args.catalog)

    if not products:
        print("Warning: No products extracted. Check the markdown format.")
        sys.exit(1)

    print(f"Found {len(products)} products")

    cards = generate_cards(products)

    # Write CSV
    with open(args.output, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Front', 'Back', 'Tags'])
        for card in cards:
            writer.writerow(card)

    print(f"\nAnki cards saved to {args.output}")
    print(f"Total cards: {len(cards)}")
    print("\nTo import into Anki:")
    print("  1. Open Anki")
    print("  2. File -> Import")
    print("  3. Select the generated CSV file")
    print("  4. Set 'Allow HTML in fields'")
    print("  5. Map columns: Field 1 -> Front, Field 2 -> Back, Field 3 -> Tags")
    print("  6. Import")


if __name__ == '__main__':
    main()
