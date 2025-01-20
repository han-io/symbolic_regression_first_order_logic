import unittest
from src.sr_fol.Expression import Var, Not, Or, And
from src.sr_fol.Population import Population
from src.sr_fol.Assignment import FormulaAssignment


class TestPopulation(unittest.TestCase):
    def setUp(self):
        and_ = And(Var(1), Var(2))
        self.f_a = FormulaAssignment(and_)

    def test_population_init(self):
        self.assertIs(Population(population_size=10,
                                 v_n=2,
                                 maxdepth=10,
                                 binary_operators=(Or, And),
                                 unary_operators=(Not,)).__class__, Population)

    def test_population_contain(self):
        p = Population(population_size=10,
                       v_n=2,
                       maxdepth=10,
                       binary_operators=(Or, And),
                       unary_operators=(Not,))
        expr = p.expressions[0]
        self.assertTrue(expr in p)

    def test_population_scores(self):
        p = Population(population_size=3,
                       v_n=2,
                       maxdepth=10,
                       binary_operators=(Or, And),
                       unary_operators=(Not,))
        p.expressions[0] = And(Var(1), Var(2))
        p.expressions[1] = Or(Var(1), Var(2))
        p.expressions[2] = Not(And(Var(1), Var(2)))

        scores = p.scores(self.f_a.matrix)

        self.assertEqual(len(p.expressions), 3)
        self.assertEqual(scores[0][1], 0.0)
        self.assertEqual(scores[1][1], 0.5)
        self.assertEqual(scores[2][1], 1.0)

    def test_population_cull(self):
        p = Population(population_size=10,
                       v_n=2,
                       maxdepth=10,
                       binary_operators=(Or, And),
                       unary_operators=(Not,))
        p.cull(self.f_a.matrix, percent=0.9)
        self.assertEqual(len(p.expressions), 1)

    def test_population_mutation(self):
        p = Population(population_size=10,
                       v_n=2,
                       maxdepth=10,
                       binary_operators=(Or, And),
                       unary_operators=(Not,))
        p.cull(self.f_a.matrix)
        p.mutation()
        self.assertEqual(len(p.expressions), 10)

    def test_population_crossover(self):
        p_1 = Population(population_size=10,
                         v_n=2,
                         maxdepth=10,
                         binary_operators=(Or, And),
                         unary_operators=(Not,))
        p_2 = Population(population_size=10,
                         v_n=2,
                         maxdepth=10,
                         binary_operators=(Or, And),
                         unary_operators=(Not,))
        p_1.cull(self.f_a.matrix)
        p_1.crossover(p_2)
        self.assertEqual(len(p_1.expressions), 10)


if __name__ == '__main__':
    unittest.main()
