#!/usr/bin/env python3

from common import format_tour, read_input

import solver_ga

CHALLENGES = 7


def generate_sample_output():
    for i in range(CHALLENGES):
        cities = read_input('input_2.csv')
        solver, name = solver_ga, "output"
        tour = solver.solve(cities)
        with open(f'{name}_2.csv', 'w') as f:
            f.write(format_tour(tour) + '\n')


if __name__ == '__main__':
    generate_sample_output()
