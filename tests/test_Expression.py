import unittest
from src.sr_fol.Expression import Expression, Var, Not, Or, And, Nand, Xor, Implies, Converse, RandomExpression
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
        self.assertEqual(self.var_1.nodes([]), [self.var_1])
        self.assertEqual(self.var_1.nodes([Var]), [self.var_1])
        self.assertEqual(self.var_1.nodes([Not]), [])
        self.assertEqual(len(self.expr.nodes([Var])), 3)
        self.assertEqual(len(self.expr.nodes([Not, Or, And])), 3)

    def test_Expression_set_child(self):
        self.not_1.set_child(self.expr)
        self.assertEqual(self.not_1.arg_1, self.expr)

    def test_Expression_new_parent(self):
        new_parent_not = self.var_1.new_parent(Var(1), [Not])
        self.assertIs(new_parent_not.__class__, Not)
        new_parent_random = self.var_1.new_parent(Var(1), [Not, Or, And])
        self.assertIn(new_parent_random.__class__, [Not, Or, And])
        new_parent_and = self.var_1.new_parent(self.var_2, [And])
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

    def test_Or_init(self):
        self.assertIs(self.or_1.__class__, Or)

    def test_Or_str(self):
        self.assertEqual(str(self.or_1), '(v_1) or (v_2)')

    def test_Or_evaluate(self):
        self.assertEqual(self.or_2.evaluate(self.matrix_or_1['a_1']), True)

    def test_Or_copy(self):
        self.assertEqual(self.or_1.copy(), self.or_1)


class TestAnd(unittest.TestCase):
    def setUp(self):
        self.and_1 = And(Var(1), Var(2))
        self.and_2 = And(Var(1), And(Var(1), Var(2)))
        self.matrix_and_1 = FormulaAssignment(self.and_1).matrix

    def test_And_init(self):
        self.assertIs(self.and_1.__class__, And)

    def test_And_str(self):
        self.assertEqual(str(self.and_1), '(v_1) and (v_2)')

    def test_And_evaluate(self):
        self.assertEqual(self.and_2.evaluate(self.matrix_and_1['a_1']), True)

    def test_And_copy(self):
        self.assertEqual(self.and_1.copy(), self.and_1)


class TestNand(unittest.TestCase):
    def setUp(self):
        self.nand_1 = Nand(Var(1), Var(2))
        self.nand_2 = Nand(Var(1), Nand(Var(1), Var(2)))
        self.matrix_nand_1 = FormulaAssignment(self.nand_1).matrix

    def test_Nand_init(self):
        self.assertIs(self.nand_1.__class__, Nand)

    def test_Nand_str(self):
        self.assertEqual(str(self.nand_1), '(v_1) nand (v_2)')

    def test_Nand_evaluate(self):
        self.assertEqual(self.nand_2.evaluate(self.matrix_nand_1['a_1']), True)

    def test_Nand_copy(self):
        self.assertEqual(self.nand_1.copy(), self.nand_1)


class TestXor(unittest.TestCase):
    def setUp(self):
        self.xor_1 = Xor(Var(1), Var(2))
        self.xor_2 = Xor(Var(1), Xor(Var(1), Var(2)))
        self.matrix_xor_1 = FormulaAssignment(self.xor_1).matrix

    def test_Xor_init(self):
        self.assertIs(self.xor_1.__class__, Xor)

    def test_Xor_str(self):
        self.assertEqual(str(self.xor_1), '(v_1) xor (v_2)')

    def test_Xor_evaluate(self):
        self.assertEqual(self.xor_2.evaluate(self.matrix_xor_1['a_1']), True)

    def test_Xor_copy(self):
        self.assertEqual(self.xor_1.copy(), self.xor_1)


class TestImplies(unittest.TestCase):
    def setUp(self):
        self.implies_1 = Implies(Var(1), Var(2))
        self.implies_2 = Implies(Var(1), Implies(Var(1), Var(2)))
        self.matrix_implies_1 = FormulaAssignment(self.implies_1).matrix

    def test_Implies_init(self):
        self.assertIs(self.implies_1.__class__, Implies)

    def test_Implies_str(self):
        self.assertEqual(str(self.implies_1), '(v_1) -> (v_2)')

    def test_Implies_evaluate(self):
        self.assertEqual(self.implies_2.evaluate(self.matrix_implies_1['a_1']), True)

    def test_Implies_copy(self):
        self.assertEqual(self.implies_1.copy(), self.implies_1)


class TestConverse(unittest.TestCase):
    def setUp(self):
        self.converse_1 = Converse(Var(1), Var(2))
        self.converse_2 = Converse(Var(1), Converse(Var(1), Var(2)))
        self.matrix_converse_1 = FormulaAssignment(self.converse_1).matrix

    def test_Converse_init(self):
        self.assertIs(self.converse_1.__class__, Converse)

    def test_Converse_str(self):
        self.assertEqual(str(self.converse_1), '(v_1) <- (v_2)')

    def test_Converse_evaluate(self):
        self.assertEqual(self.converse_2.evaluate(self.matrix_converse_1['a_1']), True)

    def test_Converse_copy(self):
        self.assertEqual(self.converse_1.copy(), self.converse_1)


class TestRandomExpression(unittest.TestCase):
    def test_RandomExpression_init(self):
        self.assertIn(RandomExpression(v_n=2).__class__.__name__, ['Var', 'Not', 'Or', 'And'])


if __name__ == '__main__':
    unittest.main()
