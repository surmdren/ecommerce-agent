#!/usr/bin/env python3
"""
Generate Anki flashcards from industry knowledge base.

Usage:
    python generate_anki_cards.py <knowledge_base.md> [--output <anki_import.txt>]

Output format: Tab-separated text file that can be imported into Anki
"""

import sys
import re
import argparse
from pathlib import Path

def parse_knowledge_base(md_file):
    """
    Parse knowledge base markdown and extract terms for flashcards.

    Expected format:
        ### [中文术语] (English Term)
        - **定义**: Definition
        - **英文**: English equivalent
        - **应用场景**: Usage context
        - **客户关注点**: Customer concern
    """
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    cards = []

    # Pattern to match term sections
    pattern = r'###\s*([^(]+)\s*\(([^)]+)\)\s*\n(.*?)(?=\n###|\n##|\Z)'

    matches = re.finditer(pattern, content, re.DOTALL)

    for match in matches:
        chinese_term = match.group(1).strip()
        english_term = match.group(2).strip()
        details = match.group(3)

        # Extract definition
        definition_match = re.search(r'\*\*定义\*\*[：:]\s*([^\n]+)', details)
        definition = definition_match.group(1).strip() if definition_match else ""

        # Extract usage context
        usage_match = re.search(r'\*\*应用场景\*\*[：:]\s*([^\n]+)', details)
        usage = usage_match.group(1).strip() if usage_match else ""

        # Extract customer concern
        concern_match = re.search(r'\*\*客户关注点\*\*[：:]\s*([^\n]+)', details)
        concern = concern_match.group(1).strip() if concern_match else ""

        if definition:  # Only create card if definition exists
            cards.append({
                'chinese': chinese_term,
                'english': english_term,
                'definition': definition,
                'usage': usage,
                'concern': concern
            })

    return cards

def format_anki_cards(cards, card_type='basic'):
    """
    Format cards for Anki import.

    Anki import format: tab-separated values
    Basic format: Front TAB Back
    Cloze format: Text with {{c1::cloze}}
    """
    output_lines = []

    if card_type == 'basic':
        # Front: Chinese term + English
        # Back: Definition + Usage + Concern
        for card in cards:
            front = f"{card['chinese']} ({card['english']})"
            back_parts = [
                f"<b>定义:</b> {card['definition']}" if card['definition'] else "",
                f"<b>应用:</b> {card['usage']}" if card['usage'] else "",
                f"<b>客户关注:</b> {card['concern']}" if card['concern'] else ""
            ]
            back = "<br><br>".join([p for p in back_parts if p])

            output_lines.append(f"{front}\t{back}")

    elif card_type == 'reverse':
        # Create two cards: CN->EN and EN->CN
        for card in cards:
            # Card 1: Chinese -> English + Definition
            front1 = card['chinese']
            back1 = f"<b>English:</b> {card['english']}<br><br><b>定义:</b> {card['definition']}"
            output_lines.append(f"{front1}\t{back1}")

            # Card 2: English -> Chinese + Definition
            front2 = card['english']
            back2 = f"<b>中文:</b> {card['chinese']}<br><br><b>Definition:</b> {card['definition']}"
            output_lines.append(f"{front2}\t{back2}")

    elif card_type == 'comprehensive':
        # More detailed cards with usage and customer concern
        for card in cards:
            front = f"<b>{card['chinese']}</b><br>({card['english']})"
            back = f"""
<b>定义:</b> {card['definition']}<br><br>
<b>应用场景:</b> {card['usage']}<br><br>
<b>客户关注点:</b> {card['concern']}
            """.strip()
            output_lines.append(f"{front}\t{back}")

    return output_lines

def main():
    parser = argparse.ArgumentParser(description='Generate Anki flashcards from knowledge base')
    parser.add_argument('knowledge_base', help='Path to knowledge base markdown file')
    parser.add_argument('--output', '-o', help='Output file for Anki import (default: anki-cards.txt)',
                       default='anki-cards.txt')
    parser.add_argument('--type', '-t', choices=['basic', 'reverse', 'comprehensive'],
                       default='comprehensive',
                       help='Card type: basic (CN+EN -> details), reverse (bidirectional), comprehensive (all info)')

    args = parser.parse_args()

    if not Path(args.knowledge_base).exists():
        print(f"Error: File not found: {args.knowledge_base}")
        sys.exit(1)

    print(f"Parsing knowledge base from {args.knowledge_base}...")
    cards = parse_knowledge_base(args.knowledge_base)

    if not cards:
        print("Warning: No cards extracted. Check the markdown format.")
        print("Expected format:")
        print("  ### [中文术语] (English Term)")
        print("  - **定义**: ...")
        sys.exit(1)

    print(f"Found {len(cards)} terms")

    output_lines = format_anki_cards(cards, args.type)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print(f"\nAnki cards saved to {args.output}")
    print(f"Card type: {args.type}")
    print(f"Total cards: {len(output_lines)}")
    print("\nTo import into Anki:")
    print("  1. Open Anki")
    print("  2. File -> Import")
    print("  3. Select the generated .txt file")
    print("  4. Set 'Fields separated by: Tab'")
    print("  5. Set 'Allow HTML in fields'")
    print("  6. Import")

if __name__ == '__main__':
    main()
