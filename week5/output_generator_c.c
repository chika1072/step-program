#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CHALLENGES 7
#define MAX_N 1000

typedef struct {
    double x, y;
} City;

// 仮のツアー生成（順番通りに並べるだけ）
void simple_solver(int *tour, int n) {
    for (int i = 0; i < n; ++i) {
        tour[i] = i;
    }
}

// CSV入力（ヘッダー付き）を読み込む
int read_input(const char *filename, City cities[]) {
    FILE *fp = fopen(filename, "r");
    if (!fp) {
        fprintf(stderr, "ファイルが開けません: %s\n", filename);
        return -1;
    }

    char line[100];
    fgets(line, sizeof(line), fp); // ヘッダー読み飛ばし

    int count = 0;
    while (fgets(line, sizeof(line), fp) && count < MAX_N) {
        sscanf(line, "%lf,%lf", &cities[count].x, &cities[count].y);
        count++;
    }

    fclose(fp);
    return count;
}

// ツアーをoutput_{i}.csv に書き出す（format_tourと同様）
void write_output(const char *filename, int *tour, int n) {
    FILE *fp = fopen(filename, "w");
    if (!fp) {
        fprintf(stderr, "出力ファイルが作成できません: %s\n", filename);
        return;
    }

    fprintf(fp, "index\n");
    for (int i = 0; i < n; ++i) {
        fprintf(fp, "%d\n", tour[i]);
    }

    fclose(fp);
}

int main() {
    for (int i = 0; i < CHALLENGES; ++i) {
        char input_filename[64], output_filename[64];
        snprintf(input_filename, sizeof(input_filename), "input_%d.csv", i);
        snprintf(output_filename, sizeof(output_filename), "output_%d.csv", i);

        City cities[MAX_N];
        int n = read_input(input_filename, cities);
        if (n <= 0) continue;

        int tour[MAX_N];
        simple_solver(tour, n); // solver_homework.solve(cities) に相当

        write_output(output_filename, tour, n);
    }

    return 0;
}