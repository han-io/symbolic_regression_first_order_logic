from itertools import product, combinations
from pandas import DataFrame, concat
from numpy.random import rand
from numpy import ndarray
from .Expression import Expression


class Assignment:
    """
    An Assignment is an incomplete truth table realized as a pandas DataFrame containing boolean or None.
    Rows represent the values for variables per assignment, depicted as columns. The output of an evaluation
    of a logical expression given the assignment is concatenated as the last row 'e' in the matrix.
    """

    def __init__(self, df: DataFrame) -> None:
        self.matrix = df

    def clean(self) -> None:
        """
        Sanitize the matrix by making the values bool or None, uniform index and column names
        and remove useless columns.
        """

        # 1. all values are True, False or NaN
        self.matrix = self.matrix.map(lambda x: bool(x), na_action='ignore')

        # 2. index labels are v_1, ..., v_n, e
        self.matrix.index = ['v_' + str(i + 1) for i in range(len(self.matrix.index) - 1)] + ['e']

        # 3. column are labeled a_1, ..., a_n
        self.matrix.columns = ['a_' + str(i + 1) for i in range(len(self.matrix.columns))]

        # 4. columns with the same values are removed
        assignments_to_drop = set()
        for assignment_x, assignment_y in combinations(self.matrix.columns, r=2):
            if self.matrix[assignment_x][:-1].equals(self.matrix[assignment_y][:-1]):
                assignments_to_drop.add(assignment_y)
        for assignment in assignments_to_drop:
            self.matrix = self.matrix.drop(assignment, axis=1)

        # 5. columns with a None-value in the e row are removed
        self.matrix = self.matrix.drop(self.matrix.loc[:, self.matrix.loc['e'].isna()], axis=1)


class RandomAssignment(Assignment):

    def __new__(cls, v_n: int = 2, a_n: int = 4) -> Assignment:
        """
        Generate an Assignment filled with random boolean values.

        :param v_n: number of variables
        :param a_n: number of assignments
        :return: Assignment with random assignments
        """
        matrix = DataFrame(data=rand(v_n + 1, a_n),
                           index=['v_' + str(i + 1) for i in range(v_n)] + ['e'],
                           columns=['a_' + str(i + 1) for i in range(a_n)])
        return Assignment(df=matrix.ge(0.5))


class FormulaAssignment(Assignment):

    def __new__(cls, expression: Expression, v_n: int = 2) -> Assignment:
        """
        Generate a matrix with all the assignments and evaluations as produced by a
        first-order-logic expression

        :param expression: expression to produce the evaluation row of the Assignment
        :param v_n: number of variables
        :return: Assignment with all assignments
        """
        matrix = DataFrame(data=list(product([True, False], repeat=v_n)),
                           index=['a_' + str(i + 1) for i in range(2**v_n)],
                           columns=['v_' + str(i + 1) for i in range(v_n)]).T
        e_row = DataFrame(data=[expression.evaluate(matrix[a_i]) for a_i in matrix.columns],
                          index=['a_' + str(i + 1) for i in range(2**v_n)],
                          columns=['e']).T
        matrix = concat([matrix, e_row])
        return Assignment(df=matrix)
