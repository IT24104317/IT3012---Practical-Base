"""Self-evaluation tests for the Lab 07 forward-chaining engine."""

from logic_engine import KnowledgeBase


def test_forward_chaining():
    kb = KnowledgeBase()
    kb.tell_rule(['TargetVisible', 'HasDust'], 'SafeToEngage')
    kb.tell_rule(['SafeToEngage', 'BloodseekerMissing'], 'Retreat')

    # Test case 1: the first rule fires, but the retreat rule cannot fire.
    kb.clear_facts()
    kb.tell_fact('TargetVisible')
    kb.tell_fact('HasDust')
    kb.forward_chain()
    assert 'SafeToEngage' in kb.facts
    assert 'Retreat' not in kb.facts

    # Test case 2: chained inference derives Retreat.
    kb.clear_facts()
    kb.tell_fact('TargetVisible')
    kb.tell_fact('HasDust')
    kb.tell_fact('BloodseekerMissing')
    kb.forward_chain()
    assert 'Retreat' in kb.facts


if __name__ == '__main__':
    test_forward_chaining()
    print('All Logic Engine Test Cases Passed!')
