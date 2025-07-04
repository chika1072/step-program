#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <string.h>

#define ISLANDS 6
#define PATHS_IN_ISLAND 150
#define GENERATIONS 10000
#define MIGRATION_RATE 0.2

typedef struct {
    int* tour;
    double length;
} Path;

int N;
double** cities;         // [N][2]
double** dist;           // [N][N]
Path islands[ISLANDS][PATHS_IN_ISLAND];

double calc_distance(int i, int j) {
    double dx = cities[i][0] - cities[j][0];
    double dy = cities[i][1] - cities[j][1];
    return sqrt(dx * dx + dy * dy);
}

void compute_distances() {
    dist = malloc(sizeof(double*) * N);
    for (int i = 0; i < N; ++i) {
        dist[i] = malloc(sizeof(double) * N);
        for (int j = 0; j < N; ++j)
            dist[i][j] = calc_distance(i, j);
    }
}

void greedy(int* tour) {
    int* visited = calloc(N, sizeof(int));
    int current = rand() % N;
    visited[current] = 1;
    tour[0] = current;

    for (int i = 1; i < N; ++i) {
        // 最も近い未訪問都市を3つ探す
        int candidates[3] = {-1, -1, -1};
        double distances[3] = {INFINITY, INFINITY, INFINITY};

        for (int j = 0; j < N; ++j) {
            if (visited[j]) continue;
            double d = dist[current][j];

            // 値が小さい順に挿入
            for (int k = 0; k < 3; ++k) {
                if (d < distances[k]) {
                    for (int l = 2; l > k; --l) {
                        distances[l] = distances[l - 1];
                        candidates[l] = candidates[l - 1];
                    }
                    distances[k] = d;
                    candidates[k] = j;
                    break;
                }
            }
        }

        // 候補の中からランダムに1つ選ぶ
        int n_candidates = 0;
        for (int k = 0; k < 3; ++k)
            if (candidates[k] != -1) n_candidates++;
        int selected = candidates[rand() % n_candidates];

        tour[i] = selected;
        visited[selected] = 1;
        current = selected;
    }

    free(visited);
}

void two_opt(int* tour) {
    for (int i = 0; i < N - 1; ++i) {
        for (int j = i + 2; j < N; ++j) {
            int a = tour[i], b = tour[(i + 1) % N];
            int c = tour[j], d = tour[(j + 1) % N];
            double before = dist[a][b] + dist[c][d];
            double after = dist[a][c] + dist[b][d];
            if (after < before) {
                for (int k = 0; k < (j - i) / 2 + 1; ++k) {
                    int tmp = tour[i + 1 + k];
                    tour[i + 1 + k] = tour[j - k];
                    tour[j - k] = tmp;
                }
            }
        }
    }
}



double evaluate_path(int* path) {
    double length = 0;
    for (int i = 0; i < N; ++i)
        length += dist[path[i]][path[(i + 1) % N]];
    return length;
}

void copy_path(int* src, int* dest) {
    memcpy(dest, src, sizeof(int) * N);
}

void pmx_crossover(int* p1, int* p2, int* c1, int* c2) {
    int start = rand() % (N - 3) + 1;
    int end = start + rand() % (N - start - 1);

    int* map1 = malloc(sizeof(int) * N);
    int* map2 = malloc(sizeof(int) * N);
    for (int i = 0; i < N; ++i) {
        map1[i] = map2[i] = -1;
        c1[i] = p1[i];
        c2[i] = p2[i];
    }

    for (int i = start; i < end; ++i) {
        c1[i] = p2[i];
        c2[i] = p1[i];
        map1[p2[i]] = p1[i];
        map2[p1[i]] = p2[i];
    }

    for (int i = 0; i < start; ++i) {
        while (map1[c1[i]] != -1) c1[i] = map1[c1[i]];
        while (map2[c2[i]] != -1) c2[i] = map2[c2[i]];
    }
    for (int i = end; i < N; ++i) {
        while (map1[c1[i]] != -1) c1[i] = map1[c1[i]];
        while (map2[c2[i]] != -1) c2[i] = map2[c2[i]];
    }

    free(map1);
    free(map2);
}

void init_islands() {
    for (int is = 0; is < ISLANDS; ++is) {
        for (int i = 0; i < PATHS_IN_ISLAND; ++i) {
            islands[is][i].tour = malloc(sizeof(int) * N);
            greedy(islands[is][i].tour);
            two_opt(islands[is][i].tour);
            islands[is][i].length = evaluate_path(islands[is][i].tour);
        }
    }
}

void migrate() {
    int m = (int)(MIGRATION_RATE * PATHS_IN_ISLAND);
    for (int i = 0; i < ISLANDS; ++i) {
        int t = (i + 1) % ISLANDS;
        for (int j = 0; j < m; ++j)
            copy_path(islands[i][j].tour,
                      islands[t][PATHS_IN_ISLAND - m + j].tour);
    }
}

void evolve() {
    for (int gen = 0; gen < GENERATIONS; ++gen) {
        for (int is = 0; is < ISLANDS; ++is) {
            Path* new_gen = malloc(sizeof(Path) * PATHS_IN_ISLAND * 2);
            for (int i = 0; i < PATHS_IN_ISLAND * 2; ++i)
                new_gen[i].tour = malloc(sizeof(int) * N);

            int count = 0;
            while (count < PATHS_IN_ISLAND) {
                int a = rand() % PATHS_IN_ISLAND;
                int b = rand() % PATHS_IN_ISLAND;
                if (a == b) continue;
                pmx_crossover(islands[is][a].tour, islands[is][b].tour,
                              new_gen[count * 2].tour, new_gen[count * 2 + 1].tour);
                count++;
            }

            for (int i = 0; i < PATHS_IN_ISLAND * 2; ++i)
                new_gen[i].length = evaluate_path(new_gen[i].tour);

            for (int i = 0; i < PATHS_IN_ISLAND * 2 - 1; ++i)
                for (int j = i + 1; j < PATHS_IN_ISLAND * 2; ++j)
                    if (new_gen[i].length > new_gen[j].length) {
                        Path tmp = new_gen[i];
                        new_gen[i] = new_gen[j];
                        new_gen[j] = tmp;
                    }

            for (int i = 0; i < PATHS_IN_ISLAND; ++i) {
                copy_path(new_gen[i].tour, islands[is][i].tour);
                islands[is][i].length = new_gen[i].length;
            }

            for (int i = 0; i < PATHS_IN_ISLAND * 2; ++i)
                free(new_gen[i].tour);
            free(new_gen);
        }
        migrate();
    }
}

int* solve(double cities_in[][2], int num_cities) {
    N = num_cities;

    cities = malloc(sizeof(double*) * N);
    for (int i = 0; i < N; ++i) {
        cities[i] = malloc(sizeof(double) * 2);
        cities[i][0] = cities_in[i][0];
        cities[i][1] = cities_in[i][1];
    }

    srand((unsigned)time(NULL));
    compute_distances();
    init_islands();
    evolve();

    Path* best = &islands[0][0];
    for (int is = 0; is < ISLANDS; ++is)
        for (int i = 0; i < PATHS_IN_ISLAND; ++i)
            if (islands[is][i].length < best->length)
                best = &islands[is][i];

    int* result = malloc(sizeof(int) * N);
    copy_path(best->tour, result);

    for (int i = 0; i < N; ++i)
        free(cities[i]);
    free(cities);
    for (int i = 0; i < N; ++i)
        free(dist[i]);
    free(dist);

    return result;
}