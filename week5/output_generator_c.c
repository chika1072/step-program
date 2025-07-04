#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "solver.h"

#define CHALLENGES 7

typedef struct {
    int x;
    int y;
} City;

// 入力読み込み関数
City* read_input(const char* filename, int* num_cities) {
    FILE* f = fopen(filename, "r");
    if (!f) return NULL;

    int capacity = 128;
    City* cities = malloc(sizeof(City) * capacity);
    *num_cities = 0;

    char line[256];
    fgets(line, sizeof(line), f);  // 1行目スキップ

    while (fgets(line, sizeof(line), f)) {
        if (*num_cities >= capacity) {
            capacity *= 2;
            cities = realloc(cities, sizeof(City) * capacity);
        }
        char* token = strtok(line, ",");
        double x = atof(token);
        token = strtok(NULL, ",");
        double y = atof(token);
        cities[*num_cities].x = x;
        cities[*num_cities].y = y;
        (*num_cities)++;
    }

    fclose(f);
    return cities;
}

// City → double[ ][2] 変換関数
double (*convert_city_array(City* cities, int num_cities))[2] {
    double (*converted)[2] = malloc(sizeof(double[2]) * num_cities);
    for (int i = 0; i < num_cities; ++i) {
        converted[i][0] = (double)cities[i].x;
        converted[i][1] = (double)cities[i].y;
    }
    return converted;
}

// ツアー配列 → CSV形式文字列に変換
char* format_tour(int* tour, int num_cities) {
    char* buffer = malloc(16 * num_cities + 16);
    strcpy(buffer, "index\n");

    for (int i = 0; i < num_cities; i++) {
        char line[16];
        snprintf(line, sizeof(line), "%d\n", tour[i]);
        strcat(buffer, line);
    }

    return buffer;
}

// 入力 → 出力ファイル生成ループ
void generate_sample_output() {
    for (int i = 0; i < CHALLENGES; i++) {
        char input_filename[64];
        snprintf(input_filename, sizeof(input_filename), "input_%d.csv", i);

        int num_cities;
        City* cities = read_input(input_filename, &num_cities);
        if (!cities) {
            fprintf(stderr, "Failed to read %s\n", input_filename);
            continue;
        }

        double (*city_array)[2] = convert_city_array(cities, num_cities);
        int* tour = solve(city_array, num_cities);

        char* tour_str = format_tour(tour, num_cities);

        char output_filename[64];
        snprintf(output_filename, sizeof(output_filename), "output_%d.csv", i);
        FILE* f = fopen(output_filename, "w");
        if (f) {
            fprintf(f, "%s\n", tour_str);
            fclose(f);
        } else {
            fprintf(stderr, "Failed to write %s\n", output_filename);
        }

        free(city_array);
        free(cities);
        free(tour);
        free(tour_str);
    }
}

int main() {
    generate_sample_output();
    return 0;
}