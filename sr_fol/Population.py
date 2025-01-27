from random import sample
from pandas import DataFrame
from sr_fol.Expression import Expression, RandomExpression


class Population:
    """
    The Population class contains expressions and provides functions to access their performance,
    remove the worst performing expressions and repopulate through changes.
    """

    def __init__(self,
                 population_size: int,
                 v_n: int,
                 maxdepth: int,
                 binary_operators: tuple[type[Expression], ...],
                 unary_operators: tuple[type[Expression], ...]) -> None:
        """
        Initialize a Population with population_size of random expressions.

        :param population_size: target amount of expressions in a population
        :param v_n: number of variables
        :param maxdepth: maximum depth of the expressions in the population
        :param binary_operators: only use these binary operators
        :param unary_operators: only use these unary operators
        """
        self.population_size = population_size
        self.v_n = v_n
        self.maxdepth = maxdepth
        self.binary_operators = binary_operators
        self.unary_operators = unary_operators
        self.expressions = []
        populating_tries = 500
        while len(self.expressions) < population_size and populating_tries > 0:
            populating_tries -= 1
            expression = RandomExpression(v_n, binary_operators, unary_operators, maxdepth)
            if expression not in self.expressions:
                self.expressions.append(expression)

    def __contains__(self, item: Expression) -> bool:
        return item in self.expressions

    def scores(self, assignment_matrix: DataFrame) -> list[tuple[Expression, float]]:
        """
        Calculate the fitness of all expressions in the population.

        :param assignment_matrix: DataFrame of variable assignments and associated evaluations
        :return: the expressions and scores
        """
        fitness = [(expr, expr.score(assignment_matrix)) for expr in self.expressions]
        fitness.sort(key=lambda x: x[1])
        return fitness

    def cull(self, assignment_matrix: DataFrame, percent: float = 0.5) -> None:
        """
        Remove the percentage of worst performing expression from the population.

        :param assignment_matrix:
        :param percent: percentage of expressions to be removed
        """
        fitness = [(expr, expr.score(assignment_matrix)) for expr in self.expressions]
        fitness.sort(key=lambda x: x[1])
        for i in range(round(len(fitness) * percent)):
            self.expressions.remove(fitness[i][0])

    def mutation(self) -> None:
        """
        Fill the population back up to population_size by choosing a random expression from the population,
        introducing random changes and adding it to the population.
        """
        populating_tries = 500
        while len(self.expressions) < self.population_size and populating_tries > 0:
            populating_tries -= 1
            mutant_expression = sample(self.expressions, k=1).pop().copy()
            mutation_maxdepth = self.maxdepth - mutant_expression.depth()

            # for small expression containing only a single variable, nodes above are added
            if mutant_expression.size() < 2:
                random_expression = RandomExpression(self.v_n,
                                                     self.binary_operators,
                                                     self.unary_operators,
                                                     mutation_maxdepth)
                mutant_expression = mutant_expression.new_parent(random_expression,
                                                                 list(self.binary_operators) + list(self.unary_operators))

            # for larger expressions randomize an argument in the expression
            else:
                branch_node = sample(mutant_expression.nodes(list(self.binary_operators) + list(self.unary_operators)),
                                     k=1).pop()
                branch_node.set_child(RandomExpression(self.v_n,
                                                       self.binary_operators,
                                                       self.unary_operators,
                                                       mutation_maxdepth))

            if mutant_expression not in self.expressions:
                self.expressions.append(mutant_expression)

    def crossover(self, guest_population: 'Population') -> None:
        """
        Fill the population back up to population_size by choosing a random expression from the population
        and splicing part of a random expression from a different population into it.

        :param guest_population: population to take expression splices from
        """
        populating_tries = 500
        while len(self.expressions) < self.population_size and populating_tries > 0:
            populating_tries -= 1
            crossover_expression = sample(self.expressions, k=1).pop().copy()

            # for small expression containing only a single variable, nodes above are added
            if crossover_expression.size() < 2:
                guest_expression = sample(guest_population.expressions, k=1).pop().copy()
                if guest_expression.size() < 2:
                    crossover_expression.new_parent(guest_expression,
                                                    list(self.binary_operators) + list(self.unary_operators))
                else:
                    guest_branch_nodes = guest_expression.nodes(list(self.binary_operators) + list(self.unary_operators))
                    guest_branch_node = sample(guest_branch_nodes, k=1).pop()
                    guest_branch_node.set_child(crossover_expression)
                    crossover_expression = guest_branch_node

            # for larger expressions take a random node from the guest expression and place it as a random branch
            else:
                guest_expression = sample(guest_population.expressions, k=1).pop()
                guest_subexpression = sample(guest_expression.nodes([]), k=1).pop().copy()

                branch_nodes = crossover_expression.nodes(list(self.binary_operators) + list(self.unary_operators))
                branch_node = sample(branch_nodes, k=1).pop()
                branch_node.set_child(guest_subexpression)

            if crossover_expression not in self.expressions and crossover_expression.depth() <= self.maxdepth:
                self.expressions.append(crossover_expression)
