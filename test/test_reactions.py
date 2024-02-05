import unittest
import random
import reaction_systems.reactions as reactions

class TestReactions(unittest.TestCase):

    def test_equal_reactions(self):
        reactants1 = set([random.randint(0,9)])
        inhibitors1 = set([random.randint(0,9)])
        products1 = set([random.randint(0,9)])
        r1 = reactions.Reaction(reactants1,inhibitors1,products1)
        r2 = reactions.Reaction(reactants1,inhibitors1,products1)
        self.assertEqual(r1,r2)

    def test_equal_reactions(self):
        reactants1 = set([random.randint(0,9)])
        inhibitors1 = set([random.randint(0,9)])
        products1 = set([random.randint(0,9)])
        reactants2 = set([random.randint(0,9)])
        r1 = reactions.Reaction(reactants1,inhibitors1,products1)
        r2 = reactions.Reaction(reactants2,inhibitors1,products1)
        self.assertNotEqual(r1,r2)

if __name__ == '__main__':
    unittest.main()