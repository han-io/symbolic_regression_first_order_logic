import unittest
from symbolic_regression_first_order_logic import best_expression
from Expression import Not, Var
from Assignment import FormulaAssignment


class TestSymbolicRegressionFol(unittest.TestCase):

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
