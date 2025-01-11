"""
For a matrix of variable assignments (a_1, ..., a_n) and associated evaluations (e_1, ..., e_n) find a
first-order-logic expression that validates the most pairs (a_1, e_1), ..., (a_n, e_n).
"""
from pandas import DataFrame
from random import sample
from Expression import Expression, RandomExpression
from Population import Population
from Assignment import RandomAssignment, FormulaAssignment


def best_expression(assignment_matrix: DataFrame,
                    populations: int = 31,
                    population_size: int = 27,
                    maxdepth: int = 10,
                    niterations: int = 100) -> Expression:
    """
    Find a first-order-logic expression that evaluates the most variable assignments to their evaluations
    given in the assignment_matrix. When multiple expressions show the best performance return the shorter.

    :param assignment_matrix: DataFrame of variable assignments and associated evaluations
    :param populations: number of populations used in the genetic algorithm
    :param population_size: number of individual expressions per population
    :param maxdepth: maximum depth of the expressions in the populations
    :param niterations: number of generations of mutation and crossover
    :return: best performing expression
    """
    v_n = len(assignment_matrix.index) - 1
    pops = [Population(population_size, v_n, maxdepth) for _ in range(populations)]
    best_per_generation = []
    for gen in range(niterations):

        # stop if the there was no improvement in the last 10 generations
        if gen > 10 and all(i == best_per_generation[-1] for i in best_per_generation[-10:]):
            break

        # print(f'{gen+1}. Generation')
        best_per_population = []

        # remove the worst expressions in the population
        for pop in pops:
            pop.cull(assignment_matrix)

        # crossover half the populations back up to population_size
        for crossover in range(populations//2):
            host, guest = sample(pops, k=2)
            host.crossover(guest_population=guest)

        # mutate the remaining populations back up to population_size
        for pop in pops:
            pop.mutation()
            scores = pop.scores(assignment_matrix)
            best_per_population.append(round(scores[-1][1], 2))
        # print('Best Score of Generation: ', max(best_per_population))
        best_per_generation.append(max(best_per_population))

    # retrieve the best expression from the current populations
    best_expr_score_size = (Expression(), 0.0, 0)
    for pop in pops:
        for score in pop.scores(assignment_matrix):
            if round(score[1], 2) > best_expr_score_size[1]:
                best_expr_score_size = (score[0], round(score[1], 2), score[0].size())
            elif round(score[1], 2) == best_expr_score_size[1] and score[0].size() < best_expr_score_size[2]:
                best_expr_score_size = (score[0], round(score[1], 2), score[0].size())
    return best_expr_score_size[0]
