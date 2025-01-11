import unittest
from pandas import DataFrame
from numpy import concatenate
from math import isnan
from Expression import Var, Not, Or, And
from Assignment import Assignment, RandomAssignment, FormulaAssignment


class TestAssignment(unittest.TestCase):
    def test_Assignment_init(self):
        df = DataFrame([[0, 1], [2, 3]])
        self.assertIs(Assignment(df).__class__, Assignment)

    def test_Assignment_clean(self):
        a = Assignment(DataFrame([[None, 0, 1, True], [1, '2', 0, False], ['right', None, 10, 20]]))
        a.clean()

        # 1. all values are True, False or NaN
        expected_values = [None, True,
                           True, False,
                           True, True]
        matrix_list = concatenate(a.matrix.values).tolist()
        self.assertListEqual(matrix_list, expected_values)

        # 2. index labels are v_1, ..., v_n, e
        self.assertListEqual(list(a.matrix.index), ['v_1', 'v_2', 'e'])

        # 3. column are labeled a_1, ..., a_n
        self.assertListEqual(list(a.matrix.columns), ['a_1', 'a_3'])

        # 4. columns with the same values are removed
        self.assertTrue('a_4' not in a.matrix.columns)

        # 5. columns with a None-value in the e row are removed
        self.assertTrue('a_2' not in a.matrix.columns)

    def test_Assignment_RandomAssignment(self):
        self.assertIs(RandomAssignment().__class__, Assignment)

    def test_Assignment_FormulaAssignment(self):
        expr_1 = Or(And(Var(1), Var(2)), Not(Var(2)))
        f_a_1 = FormulaAssignment(expr_1)
        expected_values_1 = [True, True, False, False,
                           True, False, True, False,
                           True, True, False, True]
        self.assertListEqual(concatenate(f_a_1.matrix.values).tolist(), expected_values_1)

        expr_2 = Var(1)
        f_a_2 = FormulaAssignment(expr_2, v_n=1)
        expected_values_2 = [True, False,
                             True, False]
        self.assertListEqual(concatenate(f_a_2.matrix.values).tolist(), expected_values_2)


if __name__ == '__main__':
    unittest.main()
