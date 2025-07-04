#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <string.h>

#define MAX_N 1000
#define ISLANDS 4
#define PATHS_IN_ISLAND 100
#define GENERATIONS 500
#define MIGRATION_RATE 0.2

int N;
double cities[MAX_N][2];
double dist[MAX_N][MAX_N];

typedef struct {
    int tour[MAX_N];
    double length;
} Path;

Path islands[ISLANDS][PATHS_IN_ISLAND];

double calc_distance(int i, int j) {
    double dx = cities[i][0] - cities[j][0];
    double dy = cities[i][1] - cities[j][1];
    return sqrt(dx*dx + dy*dy);
}

void compute_distances() {
    for (int i = 0; i < N; ++i)
        for (int j = i; j < N; ++j)
            dist[i][j] = dist[j][i] = calc_distance(i, j);
}

double evaluate_path(const int *path) {
    double length = 0;
    for (int i = 0; i < N; ++i)
        length += dist[path[i]][path[(i + 1) % N]];
    return length;
}

void copy_path(const int *src, int *dest) {
    memcpy(dest, src, sizeof(int) * N);
}

void greedy(int *tour) {
    int visited[MAX_N] = {0};
    int current = rand() % N;
    visited[current] = 1;
    tour[0] = current;
    for (int i = 1; i < N; ++i) {
        int candidates[3], count = 0;
        double min_d = 1e9;
        for (int j = 0; j < N; ++j) {
            if (!visited[j]) {
                double d = dist[current][j];
                if (count < 3) {
                    candidates[count++] = j;
                } else {
                    for (int k = 0; k < 3; ++k) {
                        if (d < dist[current][candidates[k]]) {
                            candidates[k] = j;
                            break;
                        }
                    }
                }
            }
        }
        int next = candidates[rand() % count];
        tour[i] = next;
        visited[next] = 1;
        current = next;
    }
}

void two_opt(int *tour) {
    for (int i = 0; i < N - 3; ++i) {
        for (int j = i + 2; j < N - 1; ++j) {
            double before = dist[tour[i]][tour[i+1]] + dist[tour[j]][tour[j+1]];
            double after  = dist[tour[i]][tour[j]]   + dist[tour[i+1]][tour[j+1]];
            if (after < before) {
                for (int k = 0; k < (j - i) / 2; ++k) {
                    int tmp = tour[i+1+k];
                    tour[i+1+k] = tour[j-k];
                    tour[j-k] = tmp;
                }
            }
        }
    }
}

void init_islands() {
    for (int is = 0; is < ISLANDS; ++is) {
        for (int i = 0; i < PATHS_IN_ISLAND; ++i) {
            greedy(islands[is][i].tour);
            two_opt(islands[is][i].tour);
            islands[is][i].length = evaluate_path(islands[is][i].tour);
        }
    }
}

void pmx_crossover(int *parent1, int *parent2, int *child1, int *child2) {
    int start = rand() % (N - 3) + 1;
    int end = start + rand() % (N - start - 1);

    int map1[MAX_N], map2[MAX_N];
    for (int i = 0; i < N; ++i) map1[i] = map2[i] = -1;

    for (int i = 0; i < N; ++i) {
        child1[i] = parent1[i];
        child2[i] = parent2[i];
    }

    for (int i = start; i < end; ++i) {
        child1[i] = parent2[i];
        child2[i] = parent1[i];
        map1[parent2[i]] = parent1[i];
        map2[parent1[i]] = parent2[i];
    }

    for (int i = 0; i < start; ++i) {
        while (map1[child1[i]] != -1)
            child1[i] = map1[child1[i]];
        while (map2[child2[i]] != -1)
            child2[i] = map2[child2[i]];
    }

    for (int i = end; i < N; ++i) {
        while (map1[child1[i]] != -1)
            child1[i] = map1[child1[i]];
        while (map2[child2[i]] != -1)
            child2[i] = map2[child2[i]];
    }
}

void evaluate_and_select(Path *population) {
    for (int i = 0; i < PATHS_IN_ISLAND; ++i)
        population[i].length = evaluate_path(population[i].tour);

    for (int i = 0; i < PATHS_IN_ISLAND-1; ++i)
        for (int j = i+1; j < PATHS_IN_ISLAND; ++j)
            if (population[i].length > population[j].length) {
                Path tmp = population[i];
                population[i] = population[j];
                population[j] = tmp;
            }
}

void migrate() {
    int num_migrants = (int)(MIGRATION_RATE * PATHS_IN_ISLAND);
    for (int i = 0; i < ISLANDS; ++i) {
        int target = (i + 1) % ISLANDS;
        for (int j = 0; j < num_migrants; ++j)
            islands[target][PATHS_IN_ISLAND - num_migrants + j] = islands[i][j];
    }
}

void evolve() {
    for (int gen = 0; gen < GENERATIONS; ++gen) {
        for (int is = 0; is < ISLANDS; ++is) {
            Path new_gen[PATHS_IN_ISLAND * 2];
            int count = 0;
            while (count < PATHS_IN_ISLAND) {
                int a = rand() % PATHS_IN_ISLAND;
                int b = rand() % PATHS_IN_ISLAND;
                if (a == b) continue;
                pmx_crossover(islands[is][a].tour, islands[is][b].tour,
                              new_gen[count*2].tour, new_gen[count*2+1].tour);
                count++;
            }
            for (int i = 0; i < PATHS_IN_ISLAND*2; ++i)
                new_gen[i].length = evaluate_path(new_gen[i].tour);

            // select best PATHS_IN_ISLAND individuals
            for (int i = 0; i < PATHS_IN_ISLAND*2-1; ++i)
                for (int j = i+1; j < PATHS_IN_ISLAND*2; ++j)
                    if (new_gen[i].length > new_gen[j].length) {
                        Path tmp = new_gen[i];
                        new_gen[i] = new_gen[j];
                        new_gen[j] = tmp;
                    }

            for (int i = 0; i < PATHS_IN_ISLAND; ++i)
                islands[is][i] = new_gen[i];
        }
        migrate();
    }
}

void print_tour(int *tour) {
    for (int i = 0; i < N; ++i)
        printf("%d\n", tour[i]);
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: ./tsp input.txt\n");
        return 1;
    }

    FILE *fp = fopen(argv[1], "r");
    fscanf(fp, "%d", &N);
    for (int i = 0; i < N; ++i)
        fscanf(fp, "%lf %lf", &cities[i][0], &cities[i][1]);
    fclose(fp);

    srand((unsigned)time(NULL));
    compute_distances();
    init_islands();
    evolve();

    Path *best = &islands[0][0];
    for (int is = 0; is < ISLANDS; ++is)
        for (int i = 0; i < PATHS_IN_ISLAND; ++i)
            if (islands[is][i].length < best->length)
                best = &islands[is][i];

    print_tour(best->tour);
    return 0;
}
