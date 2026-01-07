#!/usr/bin/env python3
"""
English Verb Conjugator for Template System

Handles:
- 3rd person singular (-s, -es, -ies)
- Irregular verbs
- Template placeholder parsing
"""

from typing import Optional
import re


# ============================================
# Irregular Verbs
# ============================================

IRREGULAR_3S = {
    # be/have/do
    'be': 'is',
    'have': 'has',
    'do': 'does',

    # Modal verbs (no change)
    'can': 'can',
    'could': 'could',
    'will': 'will',
    'would': 'would',
    'shall': 'shall',
    'should': 'should',
    'may': 'may',
    'might': 'might',
    'must': 'must',
}

IRREGULAR_PAST = {
    'be': 'was/were',
    'have': 'had',
    'do': 'did',
    'go': 'went',
    'see': 'saw',
    'come': 'came',
    'take': 'took',
    'make': 'made',
    'know': 'knew',
    'think': 'thought',
    'feel': 'felt',
    'find': 'found',
    'give': 'gave',
    'tell': 'told',
    'say': 'said',
    'get': 'got',
    'put': 'put',
    'keep': 'kept',
    'let': 'let',
    'begin': 'began',
    'seem': 'seemed',
    'leave': 'left',
    'bring': 'brought',
    'write': 'wrote',
    'sit': 'sat',
    'stand': 'stood',
    'lose': 'lost',
    'meet': 'met',
    'run': 'ran',
    'pay': 'paid',
    'hear': 'heard',
    'grow': 'grew',
    'spend': 'spent',
    'win': 'won',
    'teach': 'taught',
    'buy': 'bought',
    'send': 'sent',
    'build': 'built',
    'fall': 'fell',
    'cut': 'cut',
    'drive': 'drove',
    'break': 'broke',
    'speak': 'spoke',
    'read': 'read',
    'sleep': 'slept',
}


# ============================================
# Conjugation Functions
# ============================================

def to_3rd_singular(verb: str) -> str:
    """
    Convert base verb to 3rd person singular present tense.

    Examples:
        work -> works
        watch -> watches
        study -> studies
        go -> goes
        have -> has
    """
    verb = verb.lower().strip()

    # Check irregular first
    if verb in IRREGULAR_3S:
        return IRREGULAR_3S[verb]

    # Regular rules
    if verb.endswith(('s', 'sh', 'ch', 'x', 'z')):
        return verb + 'es'
    elif verb.endswith('o'):
        return verb + 'es'
    elif verb.endswith('y'):
        if len(verb) > 1 and verb[-2] not in 'aeiou':
            return verb[:-1] + 'ies'
        else:
            return verb + 's'
    else:
        return verb + 's'


def to_past_tense(verb: str) -> str:
    """
    Convert base verb to past tense.

    Examples:
        work -> worked
        study -> studied
        stop -> stopped
        go -> went
    """
    verb = verb.lower().strip()

    # Check irregular first
    if verb in IRREGULAR_PAST:
        return IRREGULAR_PAST[verb]

    # Regular rules (-ed)
    if verb.endswith('e'):
        return verb + 'd'
    elif verb.endswith('y'):
        if len(verb) > 1 and verb[-2] not in 'aeiou':
            return verb[:-1] + 'ied'
        else:
            return verb + 'ed'
    elif verb.endswith(('b', 'd', 'g', 'm', 'n', 'p', 't')):
        # Double consonant for CVC pattern (simplified)
        if len(verb) >= 2 and verb[-2] in 'aeiou' and verb[-3] not in 'aeiou' if len(verb) >= 3 else True:
            return verb + verb[-1] + 'ed'
        return verb + 'ed'
    else:
        return verb + 'ed'


def to_progressive(verb: str) -> str:
    """
    Convert base verb to -ing form.

    Examples:
        work -> working
        make -> making
        run -> running
        lie -> lying
    """
    verb = verb.lower().strip()

    if verb.endswith('ie'):
        return verb[:-2] + 'ying'
    elif verb.endswith('e') and not verb.endswith('ee'):
        return verb[:-1] + 'ing'
    elif len(verb) >= 3 and verb[-1] not in 'aeiouwxy' and verb[-2] in 'aeiou' and verb[-3] not in 'aeiou':
        # CVC pattern - double consonant
        return verb + verb[-1] + 'ing'
    else:
        return verb + 'ing'


# ============================================
# Template Processing
# ============================================

# Pattern: {verb:conjugation} or {placeholder:verb:conjugation}
VERB_PATTERN = re.compile(r'\{(\w+):(\w+)\}')


def conjugate_in_template(template: str, verb: str, subject_type: str = '3s') -> str:
    """
    Process verb conjugation markers in template.

    Markers:
        {verb:3s}   -> 3rd person singular (works, has)
        {verb:past} -> past tense (worked, had)
        {verb:ing}  -> progressive (working, having)
        {verb:base} -> base form (work, have)

    Args:
        template: Template string with markers
        verb: Base verb to conjugate
        subject_type: '1s', '2s', '3s', '1p', '2p', '3p' (for context)

    Returns:
        Template with conjugated verb
    """
    result = template

    # Find all verb markers
    matches = VERB_PATTERN.findall(template)

    for placeholder, conjugation in matches:
        if placeholder == 'verb':
            if conjugation == '3s':
                conjugated = to_3rd_singular(verb)
            elif conjugation == 'past':
                conjugated = to_past_tense(verb)
            elif conjugation == 'ing':
                conjugated = to_progressive(verb)
            elif conjugation == 'base':
                conjugated = verb
            else:
                conjugated = verb

            result = result.replace(f'{{{placeholder}:{conjugation}}}', conjugated)

    return result


def get_subject_type(subject: str) -> str:
    """
    Determine subject type for verb conjugation.

    Returns: '1s', '2s', '3s', '1p', '2p', '3p'
    """
    subject_lower = subject.lower().strip()

    # 1st person singular
    if subject_lower in ('i', 'i am'):
        return '1s'

    # 2nd person
    if subject_lower in ('you', 'you are'):
        return '2s'

    # 1st person plural
    if subject_lower in ('we', 'we are'):
        return '1p'

    # 3rd person plural
    if subject_lower in ('they', 'they are', 'the team', 'my colleagues', 'people'):
        return '3p'

    # Default: 3rd person singular (most common in templates)
    # "The developer", "He", "She", "It", etc.
    return '3s'


# ============================================
# Subject-Verb Agreement Helper
# ============================================

class SubjectVerbPair:
    """
    Pre-conjugated subject-verb pairs for common patterns.
    """

    PAIRS = {
        # 1st person
        ('I', 'feel'): 'I feel',
        ('I', 'work'): 'I work',
        ('I', 'have'): 'I have',
        ('I', 'am'): 'I am',

        # 3rd person singular
        ('The developer', 'feel'): 'The developer feels',
        ('The developer', 'work'): 'The developer works',
        ('The developer', 'have'): 'The developer has',
        ('The designer', 'feel'): 'The designer feels',
        ('The student', 'feel'): 'The student feels',
        ('He', 'feel'): 'He feels',
        ('She', 'feel'): 'She feels',

        # 3rd person plural
        ('The team', 'feel'): 'The team feels',  # collective noun = singular
        ('They', 'feel'): 'They feel',
        ('We', 'feel'): 'We feel',
    }

    @classmethod
    def get(cls, subject: str, verb: str) -> str:
        """Get pre-conjugated subject-verb pair or generate one."""
        key = (subject, verb)
        if key in cls.PAIRS:
            return cls.PAIRS[key]

        # Generate dynamically
        subject_type = get_subject_type(subject)
        if subject_type == '3s':
            return f"{subject} {to_3rd_singular(verb)}"
        else:
            return f"{subject} {verb}"


# ============================================
# Test
# ============================================

if __name__ == '__main__':
    print("=== 3rd Person Singular ===")
    test_verbs = ['work', 'watch', 'study', 'go', 'have', 'be', 'play', 'try', 'fix', 'do']
    for v in test_verbs:
        print(f"  {v} -> {to_3rd_singular(v)}")

    print("\n=== Past Tense ===")
    for v in test_verbs:
        print(f"  {v} -> {to_past_tense(v)}")

    print("\n=== Progressive ===")
    for v in test_verbs:
        print(f"  {v} -> {to_progressive(v)}")

    print("\n=== Template Processing ===")
    template = "The developer {verb:3s} {word} after debugging."
    result = conjugate_in_template(template, 'feel', '3s')
    print(f"  Template: {template}")
    print(f"  Result:   {result}")

    template2 = "Yesterday, I {verb:past} the issue."
    result2 = conjugate_in_template(template2, 'fix', '1s')
    print(f"  Template: {template2}")
    print(f"  Result:   {result2}")

    print("\n=== Subject-Verb Pairs ===")
    print(f"  {SubjectVerbPair.get('The developer', 'feel')}")
    print(f"  {SubjectVerbPair.get('They', 'feel')}")
    print(f"  {SubjectVerbPair.get('I', 'have')}")
