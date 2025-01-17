import unittest
from src.sr_fol.__main__ import best_expression
from src.sr_fol.Expression import Not, Var
from src.sr_fol.Assignment import FormulaAssignment


class TestSrFol(unittest.TestCase):

    def test_best_expression(self):
        expr = Not(Not(Var(1)))
        assign_matrix = FormulaAssignment(expr, 2).matrix
        result_scores = []
        for _ in range(100):
            result_expr = best_expression(assign_matrix, verbose=True)
            result_scores.append(result_expr.score(assign_matrix))
        self.assertGreater(sum(result_scores)/float(len(result_scores)), 0.95)


if __name__ == '__main__':
    unittest.main()
