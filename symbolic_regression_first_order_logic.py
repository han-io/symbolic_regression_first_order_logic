"""
For a matrix of variable assignments (a_1, ..., a_n) and associated evaluations (e_1, ..., e_n) find a
first-order-logic expression that validates the most pairs (a_1, e_1), ..., (a_n, e_n).
"""
from pandas import DataFrame
from random import sample
from argparse import ArgumentParser
from pickle import load
from Expression import Expression
from Population import Population
from Assignment import Assignment


def best_expression(input_df: DataFrame,
                    populations: int = 31,
                    population_size: int = 27,
                    maxdepth: int = 10,
                    niterations: int = 100,
                    verbose: bool = False) -> Expression:
    """
    Find a first-order-logic expression that evaluates the most variable assignments to their evaluations
    given in the assignment_matrix. When multiple expressions show the best performance return the shorter.

    :param input_df: uncleaned DataFrame of variable assignments and associated evaluations
    :param populations: number of populations used in the genetic algorithm
    :param population_size: number of individual expressions per population
    :param maxdepth: maximum depth of the expressions in the populations
    :param niterations: number of generations of mutation and crossover
    :param verbose: output more info to sdtout
    :return: best performing expression
    """
    assignment = Assignment(df=input_df)
    assignment.clean()
    if verbose:
        print('Input cleaned')
    assignment_matrix = assignment.matrix
    v_n = len(assignment_matrix.index) - 1
    pops = [Population(population_size, v_n, maxdepth) for _ in range(populations)]
    best_per_generation = []
    for gen in range(niterations):

        # stop if the there was no improvement in the last 10 generations
        if gen > 10 and all(i == best_per_generation[-1] for i in best_per_generation[-10:]):
            break

        if verbose:
            print(f'{gen+1}. Generation')
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
        if verbose:
            print('Best Score of Generation: ', max(best_per_population))
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


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input_df_path', type=str, help='path to a pickled DataFrame')
    parser.add_argument('--populations', type=int, help='number of populations used in the genetic algorithm')
    parser.add_argument('--population_size', type=int, help='number of individual expressions per population')
    parser.add_argument('--maxdepth', type=int, help='maximum depth of the expressions in the populations')
    parser.add_argument('--niterations', type=int, help='number of generations of mutation and crossover')
    parser.add_argument('-v', '--verbose', help='output more info to sdtout', action='store_true')
    args = parser.parse_args()

    with open(args.input_df_path, 'rb') as input_df_file:
        input_df = load(input_df_file)

    populations = args.populations if args.populations else 31
    population_size = args.population_size if args.population_size else 27
    maxdepth = args.maxdepth if args.maxdepth else 10
    niterations = args.niterations if args.niterations else 100

    result_expression = best_expression(input_df,
                                        populations=populations,
                                        population_size=population_size,
                                        maxdepth=maxdepth,
                                        niterations=niterations,
                                        verbose=args.verbose)
    print(result_expression)
