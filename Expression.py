from random import sample
from pandas import DataFrame, Series


class Expression:
    """
    Parent class to provide common functions for the child classes of first-order-logic operators and variables.
    Logical expressions are implemented as binary trees with operators as branches and variables as leaves.
    """

    def __init__(self, arg_1=None, arg_2=None) -> None:
        self.arg_1 = arg_1
        self.arg_2 = arg_2

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    def score(self, assignment_matrix: DataFrame) -> float:
        """
        Calculate the fraction of assignments this expression correctly evaluates.

        :param assignment_matrix: DataFrame of variable assignments and associated evaluations
        :return: fraction of correct assignments
        """
        score_total = 0
        for assignment in assignment_matrix.columns:
            score_total += self.evaluate(assignment_matrix[assignment]) == assignment_matrix[assignment]['e']
        return score_total / len(assignment_matrix.columns)

    def size(self) -> int:
        """
        Return the amount of nodes below this node, including this node.

        :return: amount of nodes
        """
        if self.arg_1 is None and self.arg_2 is None:
            return 1
        elif self.arg_1 is None:
            return self.arg_2.size() + 1
        elif self.arg_2 is None:
            return self.arg_1.size() + 1
        else:
            return self.arg_1.size() + self.arg_2.size() + 1

    def depth(self) -> int:
        """
        Return the amount of steps between this node and the deepest leaf below it.

        :return: level of depth
        """
        if self.arg_1 is None and self.arg_2 is None:
            return 1
        elif self.arg_1 is None:
            return self.arg_2.depth() + 1
        elif self.arg_2 is None:
            return self.arg_1.depth() + 1
        else:
            return max(self.arg_1.depth(), self.arg_2.depth()) + 1

    def nodes(self, node_types: tuple[str, ...] = ()) -> list['Expression']:
        """
        Get a list of all specified node types in an expression.
        If no node types are specified return all nodes.

        :param node_types: types of nodes to be returned
        :return: all nodes of specified type
        """
        nodes = []
        if node_types == () or self.__class__.__name__ in node_types:
            nodes.append(self)
        if self.arg_2 is not None:
            nodes = nodes + self.arg_1.nodes(node_types) + self.arg_2.nodes(node_types)
        elif self.arg_1 is not None:
            nodes = nodes + self.arg_1.nodes(node_types)
        return nodes

    def set_child(self, child_expression: 'Expression') -> None:
        """
        Incorporate child_expression as an argument for this expression.

        :param child_expression: expression to include
        """
        if self.__class__.__name__ == 'Not':
            self.arg_1 = child_expression
        else:
            if sample([1, 2], k=1).pop() == 1:
                self.arg_1 = child_expression
            else:
                self.arg_2 = child_expression

    def new_parent(self,
                   sibling_expression: 'Expression',
                   node_types: tuple[str, ...] = ('Not', 'Or', 'And')) -> 'Expression':
        """
        Expand this expression with a node randomly chosen from node_types above this expression.
        Use sibling_expression as the second argument of the parent node if necessary.

        :param sibling_expression: second argument for the new parent node
        :param node_types: allowed types for the parent node
        :return: parent node
        """
        node_type = sample(node_types, k=1).pop()
        if node_type == 'Not':
            return Not(self)
        elif node_type == 'Or':
            return Or(self, sibling_expression)
        elif node_type == 'And':
            return And(self, sibling_expression)
        else:
            return self


class Var(Expression):
    """
    Class to fulfill the role of a variable in first-order-logic.
    """

    def __init__(self, subscript: int) -> None:
        self.subscript = subscript
        super().__init__()

    def __str__(self) -> str:
        return 'v_' + str(self.subscript)

    def copy(self) -> 'Var':
        """
        Create a copy of this node and recursively copy the expression tree below this node.
        This generates a logically equivalent expression composed of entirely different instances.

        :return: deep copied expression
        """
        return Var(self.subscript)

    def evaluate(self, assignment: Series) -> bool | None:
        """
        Evaluate the logical value of this expression by assigning the variable.

        :param assignment: values for variables
        :return: evaluation of expression
        """
        eval_variable = assignment['v_' + str(self.subscript)]
        if eval_variable is None:
            return None
        return assignment['v_' + str(self.subscript)]


class Not(Expression):
    """
    Class to fulfill the role of the 'not' operator in first-order-logic.
    """

    def __str__(self) -> str:
        return 'not (' + str(self.arg_1) + ')'

    def copy(self) -> 'Not':
        """
        Create a copy of this node and recursively copy the expression tree below this node.
        This generates a logically equivalent expression composed of entirely different instances.

        :return: deep copied expression
        """
        return Not(arg_1=self.arg_1.copy())

    def evaluate(self, assignment: Series) -> bool | None:
        """
        Evaluate the logical value of this expression by recursively evaluating its arguments.

        :param assignment: values for variables
        :return: evaluation of expression
        """
        eval_arg_1 = self.arg_1.evaluate(assignment)
        if eval_arg_1 is None:
            return None
        return not self.arg_1.evaluate(assignment)


class Or(Expression):
    """
    Class to fulfill the role of the 'or' operator in first-order-logic.
    """

    def __str__(self) -> str:
        return '(' + str(self.arg_1) + ') or (' + str(self.arg_2) + ')'

    def copy(self) -> 'Or':
        """
        Create a copy of this node and recursively copy the expression tree below this node.
        This generates a logically equivalent expression composed of entirely different instances.

        :return: deep copied expression
        """
        return Or(arg_1=self.arg_1.copy(), arg_2=self.arg_2.copy())

    def evaluate(self, assignment: Series) -> bool | None:
        """
        Evaluate the logical value of this expression by recursively evaluating its arguments.

        :param assignment: values for variables
        :return: evaluation of expression
        """
        eval_arg_1 = self.arg_1.evaluate(assignment)
        eval_arg_2 = self.arg_2.evaluate(assignment)
        if eval_arg_1 is None or eval_arg_2 is None:
            return None
        return eval_arg_1 or eval_arg_2


class And(Expression):
    """
    Class to fulfill the role of the 'and' operator in first-order-logic.
    """

    def __str__(self) -> str:
        return '(' + str(self.arg_1) + ') and (' + str(self.arg_2) + ')'

    def copy(self) -> 'And':
        """
        Create a copy of this node and recursively copy the expression tree below this node.
        This generates a logically equivalent expression composed of entirely different instances.

        :return: deep copied expression
        """
        return And(arg_1=self.arg_1.copy(), arg_2=self.arg_2.copy())

    def evaluate(self, assignment: Series) -> bool | None:
        """
        Evaluate the logical value of this expression by recursively evaluating its arguments.

        :param assignment: values for variables
        :return: evaluation of expression
        """
        eval_arg_1 = self.arg_1.evaluate(assignment)
        eval_arg_2 = self.arg_2.evaluate(assignment)
        if eval_arg_1 is None or eval_arg_2 is None:
            return None
        return eval_arg_1 and eval_arg_2


class RandomExpression(Expression):

    def __new__(cls, v_n: int, maxdepth: int = 10) -> Expression:
        """
        Generate a random Expression.

        :param v_n: number of variables
        :param maxdepth: maximum depth of the expression
        """
        node_options = [i + 1 for i in range(v_n)]
        if maxdepth > 0:
            node_options += ['Not', 'Or', 'And']
        node_type = sample(node_options, k=1).pop()
        if node_type == 'Not':
            return Not(RandomExpression(v_n, maxdepth-1))
        elif node_type == 'Or':
            return Or(RandomExpression(v_n, maxdepth-1), RandomExpression(v_n, maxdepth-1))
        elif node_type == 'And':
            return And(RandomExpression(v_n, maxdepth-1), RandomExpression(v_n, maxdepth-1))
        else:
            return Var(node_type)
