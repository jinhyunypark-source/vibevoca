#!/usr/bin/env python3
"""
Automated sentence generator - generates example sentences without requiring manual intervention
"""
import json
import random
from typing import List, Dict

class AutomatedSentenceGenerator:
    """Generate example sentences automatically"""

    def __init__(self):
        self.sentence_templates = self._create_templates()

    def _create_templates(self):
        """Create sentence templates for various contexts"""
        return {
            'positive': [
                "The {word} atmosphere made everyone feel comfortable.",
                "Her {word} approach helped solve the problem quickly.",
                "The team appreciated his {word} attitude.",
                "It was a {word} decision that benefited everyone.",
                "The {word} quality of the product exceeded expectations.",
            ],
            'negative': [
                "The {word} situation created many challenges.",
                "His {word} behavior affected team morale.",
                "The {word} condition made things difficult.",
                "It was a {word} mistake that needed correction.",
                "The {word} outcome disappointed stakeholders.",
            ],
            'neutral': [
                "The report described the {word} nature of the process.",
                "She explained the {word} aspects of the project.",
                "The analysis revealed {word} patterns in the data.",
                "They discussed the {word} implications thoroughly.",
                "The study examined {word} characteristics carefully.",
            ],
            'action': [
                "He tried to {word} his ideas more clearly.",
                "She needed to {word} the situation effectively.",
                "They decided to {word} their approach significantly.",
                "The manager wanted to {word} team performance.",
                "We should {word} our strategy going forward.",
            ],
            'comparison': [
                "This solution is more {word} than the previous one.",
                "The new design appears less {word} overall.",
                "Her work is remarkably {word} compared to others.",
                "The result was surprisingly {word} in nature.",
                "Their method proved {word} in practice.",
            ],
            'description': [
                "The {word} features distinguished it from competitors.",
                "Its {word} characteristics were immediately noticeable.",
                "The {word} elements contributed to success.",
                "Those {word} details made a significant difference.",
                "The {word} components worked together seamlessly.",
            ],
        }

    def _translate_to_korean(self, english_sentence: str, word: str, meaning: str) -> str:
        """Generate Korean translation (simplified)"""
        # This is a simplified version - in production you'd want proper translation
        word_kr = meaning.split(',')[0].split('(')[0].strip()

        # Simple pattern-based translation
        translations = {
            "atmosphere made everyone feel comfortable": f"{word_kr} 분위기가 모두를 편안하게 만들었다",
            "approach helped solve the problem": f"{word_kr} 접근법이 문제 해결에 도움이 되었다",
            "attitude": f"{word_kr} 태도",
            "decision that benefited everyone": f"{word_kr} 결정으로 모두가 혜택을 받았다",
            "quality of the product exceeded expectations": f"{word_kr} 제품 품질이 기대를 초과했다",
            "situation created many challenges": f"{word_kr} 상황이 많은 어려움을 만들었다",
            "behavior affected team morale": f"{word_kr} 행동이 팀 사기에 영향을 미쳤다",
            "condition made things difficult": f"{word_kr} 상태가 일을 어렵게 만들었다",
            "mistake that needed correction": f"{word_kr} 실수로 수정이 필요했다",
            "outcome disappointed stakeholders": f"{word_kr} 결과가 이해관계자들을 실망시켰다",
            "nature of the process": f"{word_kr} 프로세스의 특성",
            "aspects of the project": f"{word_kr} 프로젝트의 측면",
            "patterns in the data": f"{word_kr} 데이터 패턴",
            "implications thoroughly": f"{word_kr} 영향을 철저히",
            "characteristics carefully": f"{word_kr} 특성을 주의깊게",
            "ideas more clearly": f"{word_kr}하게 아이디어를 표현하다",
            "the situation effectively": f"{word_kr}하게 상황을 다루다",
            "their approach significantly": f"{word_kr}하게 접근법을 변경하다",
            "team performance": f"{word_kr}하게 팀 성과를 개선하다",
            "our strategy going forward": f"{word_kr}하게 전략을 수립하다",
            "than the previous one": f"이전보다 더 {word_kr}하다",
            "overall": f"전반적으로 {word_kr}하다",
            "compared to others": f"다른 것과 비교해 {word_kr}하다",
            "in nature": f"본질적으로 {word_kr}하다",
            "in practice": f"실제로 {word_kr}하다",
            "features distinguished it": f"{word_kr} 특징이 차별화했다",
            "characteristics were immediately noticeable": f"{word_kr} 특성이 즉시 눈에 띄었다",
            "elements contributed to success": f"{word_kr} 요소가 성공에 기여했다",
            "details made a significant difference": f"{word_kr} 세부사항이 큰 차이를 만들었다",
            "components worked together seamlessly": f"{word_kr} 구성요소가 완벽하게 작동했다",
        }

        # Find best matching translation pattern
        for eng_pattern, kr_pattern in translations.items():
            if eng_pattern in english_sentence.lower():
                return kr_pattern

        # Fallback: simple translation
        return f"그것은 {word_kr}하다/했다"

    def generate_sentences_for_word(
        self,
        word_data: Dict,
        all_tags: List[str],
        num_sentences: int = 10
    ) -> List[Dict]:
        """Generate example sentences for a single word"""

        word = word_data['word']
        meaning = word_data['meaning']
        card_id = word_data['card_id']

        sentences = []

        # Select random templates and tags
        template_categories = list(self.sentence_templates.keys())
        random.shuffle(template_categories)

        for i in range(num_sentences):
            # Select template category
            category = template_categories[i % len(template_categories)]
            templates = self.sentence_templates[category]
            template = random.choice(templates)

            # Generate English sentence
            sentence_en = template.replace('{word}', word.lower())

            # Generate Korean translation
            sentence_ko = self._translate_to_korean(sentence_en, word, meaning)

            # Select random tags (2-4 tags per sentence)
            num_tags = random.randint(2, min(4, len(all_tags)))
            selected_tags = random.sample(all_tags, num_tags)

            sentences.append({
                'card_id': card_id,
                'word': word,
                'sentence_en': sentence_en,
                'sentence_ko': sentence_ko,
                'tags': selected_tags
            })

        return sentences

    def generate_for_deck(
        self,
        words: List[Dict],
        tags_data: Dict,
        sentences_per_word: int = 10
    ) -> List[Dict]:
        """Generate sentences for all words in a deck"""

        all_tags = tags_data['all_unique_tags']
        all_sentences = []

        print(f"Generating {sentences_per_word} sentences for {len(words)} words...")

        for idx, word_data in enumerate(words, 1):
            word = word_data['word']
            sentences = self.generate_sentences_for_word(
                word_data,
                all_tags,
                sentences_per_word
            )
            all_sentences.extend(sentences)

            if idx % 5 == 0:
                print(f"  Progress: {idx}/{len(words)} words ({len(all_sentences)} sentences)")

        print(f"✓ Generated {len(all_sentences)} sentences total")

        return all_sentences


def main():
    """Test the generator"""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python generate_sentences_automated.py <words_file> <tags_file> [output_file] [num_sentences]")
        sys.exit(1)

    words_file = sys.argv[1]
    tags_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else 'output/sentences_automated.json'
    num_sentences = int(sys.argv[4]) if len(sys.argv) > 4 else 10

    # Load input files
    with open(words_file, 'r', encoding='utf-8') as f:
        words = json.load(f)

    with open(tags_file, 'r', encoding='utf-8') as f:
        tags_data = json.load(f)

    # Generate sentences
    generator = AutomatedSentenceGenerator()
    sentences = generator.generate_for_deck(words, tags_data, num_sentences)

    # Save output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sentences, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Saved {len(sentences)} sentences to {output_file}")


if __name__ == '__main__':
    main()
