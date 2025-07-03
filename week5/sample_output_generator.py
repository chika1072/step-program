#!/usr/bin/env python3

from common import format_tour, read_input

import solver_ga

CHALLENGES = 7


def generate_sample_output():
    for i in range(CHALLENGES):
        cities = read_input(f'input_{i}.csv')
        solver, name = solver_ga, "output"
        tour = solver.solve(cities)
        with open(f'{name}_{i}.csv', 'w') as f:
            f.write(format_tour(tour) + '\n')


if __name__ == '__main__':
    generate_sample_output()
