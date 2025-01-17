import unittest
from src.sr_fol.Expression import Expression, Var, Not, Or, And, RandomExpression
from src.sr_fol.Assignment import FormulaAssignment


class TestExpression(unittest.TestCase):
    def setUp(self):
        self.var_1 = Var(1)
        self.var_2 = Var(2)
        self.matrix_var_1 = FormulaAssignment(self.var_1).matrix
        self.and_1 = And(Var(1), Var(2))
        self.expr = And(Or(Var(1), Var(2)), Not(Var(1)))
        self.not_1 = Not(Var(2))

    def test_Expression_init(self):
        self.assertIs(Expression().__class__, Expression)

    def test_Expression_eq(self):
        self.assertEqual(Var(1), Var(1))
        self.assertEqual(Var(1).copy(), Var(1))

    def test_Expression_score(self):
        self.assertEqual(self.var_1.score(self.matrix_var_1), 1.0)
        self.assertEqual(self.var_2.score(self.matrix_var_1), 0.5)
        self.assertEqual(self.and_1.score(self.matrix_var_1), 0.75)
        self.assertEqual(self.expr.score(self.matrix_var_1), 0.25)

    def test_Expression_size(self):
        self.assertEqual(self.var_1.size(), 1)
        self.assertEqual(self.and_1.size(), 3)
        self.assertEqual(self.expr.size(), 6)

    def test_Expression_depth(self):
        self.assertEqual(self.var_1.depth(), 1)
        self.assertEqual(self.and_1.depth(), 2)
        self.assertEqual(self.expr.depth(), 3)

    def test_Expression_nodes(self):
        self.assertEqual(self.var_1.nodes(), [self.var_1])
        self.assertEqual(self.var_1.nodes(('Var',)), [self.var_1])
        self.assertEqual(self.var_1.nodes(('Not',)), [])
        self.assertEqual(len(self.expr.nodes(('Var',))), 3)
        self.assertEqual(len(self.expr.nodes(('Not', 'Or', 'And'))), 3)

    def test_Expression_set_child(self):
        self.not_1.set_child(self.expr)
        self.assertEqual(self.not_1.arg_1, self.expr)

    def test_Expression_new_parent(self):
        new_parent_not = self.var_1.new_parent(Var(1), ('Not',))
        self.assertIs(new_parent_not.__class__, Not)
        new_parent_random = self.var_1.new_parent(Var(1))
        self.assertIn(new_parent_random.__class__, [Not, Or, And])
        new_parent_and = self.var_1.new_parent(self.var_2, ('And',))
        self.assertEqual(new_parent_and.arg_2, self.var_2)


class TestVar(unittest.TestCase):
    def setUp(self):
        self.var_1 = Var(1)
        self.var_2 = Var(2)
        self.matrix_var_1 = FormulaAssignment(self.var_1).matrix

    def test_Var_init(self):
        self.assertIs(self.var_1.__class__, Var)
        self.assertEqual(self.var_1.subscript, 1)

    def test_Var_str(self):
        self.assertEqual(str(self.var_1), 'v_1')
        self.assertEqual(self.var_1.__str__(), 'v_1')
        self.assertEqual(str(self.var_2), 'v_2')

    def test_Var_evaluate(self):
        self.assertEqual(self.var_2.evaluate(self.matrix_var_1['a_1']), True)

    def test_Var_copy(self):
        self.assertEqual(self.var_1.copy(), self.var_1)


class TestNot(unittest.TestCase):
    def setUp(self):
        self.not_1 = Not(Var(1))
        self.not_2 = Not(Var(2))
        self.matrix_not_1 = FormulaAssignment(self.not_1).matrix

    def test_Not_init(self):
        self.assertIs(self.not_1.__class__, Not)

    def test_Not_str(self):
        self.assertEqual(str(self.not_1), 'not (v_1)')

    def test_Not_evaluate(self):
        self.assertEqual(self.not_2.evaluate(self.matrix_not_1['a_1']), False)

    def test_Not_copy(self):
        self.assertEqual(self.not_1.copy(), self.not_1)


class TestOr(unittest.TestCase):
    def setUp(self):
        self.or_1 = Or(Var(1), Var(2))
        self.or_2 = Or(Var(1), Or(Var(1), Var(2)))
        self.matrix_or_1 = FormulaAssignment(self.or_1).matrix

    def test_Not_init(self):
        self.assertIs(self.or_1.__class__, Or)

    def test_Not_str(self):
        self.assertEqual(str(self.or_1), '(v_1) or (v_2)')

    def test_Not_evaluate(self):
        self.assertEqual(self.or_2.evaluate(self.matrix_or_1['a_1']), True)

    def test_Not_copy(self):
        self.assertEqual(self.or_1.copy(), self.or_1)


class TestAnd(unittest.TestCase):
    def setUp(self):
        self.and_1 = And(Var(1), Var(2))
        self.and_2 = And(Var(1), And(Var(1), Var(2)))
        self.matrix_and_1 = FormulaAssignment(self.and_1).matrix

    def test_Not_init(self):
        self.assertIs(self.and_1.__class__, And)

    def test_Not_str(self):
        self.assertEqual(str(self.and_1), '(v_1) and (v_2)')

    def test_Not_evaluate(self):
        self.assertEqual(self.and_2.evaluate(self.matrix_and_1['a_1']), True)

    def test_Not_copy(self):
        self.assertEqual(self.and_1.copy(), self.and_1)


class TestRandomExpression(unittest.TestCase):
    def test_RandomExpression_init(self):
        self.assertIn(RandomExpression(v_n=2).__class__.__name__, ['Var', 'Not', 'Or', 'And'])


if __name__ == '__main__':
    unittest.main()
