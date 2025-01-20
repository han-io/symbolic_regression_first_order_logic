import unittest
from src.sr_fol.__main__ import best_expression
from src.sr_fol.Expression import RandomExpression, Not, Or, And, Nand, Xor, Implies, Converse
from src.sr_fol.Assignment import FormulaAssignment, RandomAssignment, Assignment


class TestSrFol(unittest.TestCase):

    def test_best_expression(self):
        expr = Not(Not(Var(1)))
        assign_matrix = FormulaAssignment(expr, 2).matrix
        result_scores = []
        for _ in range(3):
            result_expr = best_expression(assign_matrix, verbose=True)
            result_scores.append(result_expr.score(assign_matrix))
        self.assertGreater(sum(result_scores)/float(len(result_scores)), 0.95)

    def test_best_expression_random(self):
        result_scores = []
        for _ in range(10):
            assign_matrix = RandomAssignment(4, 100).matrix
            a = Assignment(assign_matrix)
            a.clean()
            result_expr = best_expression(assign_matrix, verbose=True)
            result_scores.append(result_expr.score(a.matrix))
        self.assertGreater(sum(result_scores)/float(len(result_scores)), 0.84)

    def test_best_expression_random_all_operators(self):
        result_scores = []
        for _ in range(10):
            assign_matrix = RandomAssignment(4, 100).matrix
            a = Assignment(assign_matrix)
            a.clean()
            result_expr = best_expression(assign_matrix, binary_operators=(Or, And, Nand, Xor, Implies, Converse), verbose=True)
            result_scores.append(result_expr.score(a.matrix))
        self.assertGreater(sum(result_scores)/float(len(result_scores)), 0.84)

    def test_best_expression_random_nand(self):
        result_scores = []
        for _ in range(10):
            assign_matrix = RandomAssignment(4, 100).matrix
            a = Assignment(assign_matrix)
            a.clean()
            result_expr = best_expression(assign_matrix, binary_operators=(Nand,), unary_operators=(), verbose=True)
            result_scores.append(result_expr.score(a.matrix))
        self.assertGreater(sum(result_scores)/float(len(result_scores)), 0.84)


if __name__ == '__main__':
    unittest.main()
