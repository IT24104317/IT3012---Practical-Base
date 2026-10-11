"""A minimal propositional-logic knowledge base for Lab 07.

Rules are Horn clauses represented as a collection of premise strings and one
conclusion string.  ``forward_chain`` repeatedly applies Modus Ponens until a
fixed point is reached.
"""


class KnowledgeBase:
    """Store facts and derive conclusions using forward chaining."""

    def __init__(self):
        self.facts = set()
        self.rules = []

    def tell_fact(self, fact_string):
        """Add one atomic fact to the knowledge base."""
        self.facts.add(fact_string)

    def tell_rule(self, premise_list, conclusion_string):
        """Add a rule of the form premises => conclusion."""
        self.rules.append((tuple(premise_list), conclusion_string))

    def clear_facts(self):
        """Remove percept-specific facts while preserving the domain rules."""
        self.facts.clear()

    def forward_chain(self):
        """Infer every conclusion supported by the current facts and rules."""
        new_facts_added = True
        while new_facts_added:
            new_facts_added = False
            for premises, conclusion in self.rules:
                if conclusion not in self.facts and all(
                    premise in self.facts for premise in premises
                ):
                    self.facts.add(conclusion)
                    new_facts_added = True

