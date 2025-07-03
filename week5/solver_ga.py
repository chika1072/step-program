#!/usr/bin/env python3

import sys
import math
import random
from tqdm import tqdm
import time


# "common.py" ファイルから print_tour と read_input を import
from common import print_tour, read_input


# city1 と city2 の距離を求める関数
def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def solve(cities):

    """ パラメータ """
    island_number = 4      # 島の数
    paths_in_island = 100   # 島に含まれるpathの数
    migration_rate = 0.2   # 各世代の生成後に、他の島に移動させるpathの割合
    generations = 500       # 世代数   

    N = len(cities)

    # distanceをあらかじめ計算する
    # dist[i][j] = city(i)からcity(j)への距離
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])


    """ 貪欲法と2-optを、初めからある程度短距離のpathを用意するために使う """ 
    # greedy法(ランダム性あり)
    def greedy(tour):
        current_city = random.randint(0, N-1)
        unvisited_cities = set(range(0, N))
        unvisited_cities.remove(current_city)  #  unvisited_citiesから、current_cityだけ除外
        tour = [current_city]

        while unvisited_cities:
            next_city = min(unvisited_cities,
                            key=lambda city: dist[current_city][city])
            # 距離の短い3個のcityの中からランダムに1つ選ぶ
            nearest_3 = sorted(unvisited_cities, key=lambda city: dist[current_city][city])[:3]
            next_city = random.choice(nearest_3)
            unvisited_cities.remove(next_city)
            tour.append(next_city)
            current_city = next_city
        return tour
    
    # 2-opt
    def two_opt(tour):
        for i in range(N-3):
            for j in range(i+2, N-1):
                # もしi->i+1, j->j+1の長さよりも、i->j, i+1->j+1のほうが短いなら
                if dist[tour[i]][tour[i+1]] + dist[tour[j]][tour[j+1]] > dist[tour[i]][tour[j]] + dist[tour[i+1]][tour[j+1]]:
                    # pathを入れ替える
                    tour = tour[:i+1] + tour[j:i:-1] + tour[j+1:]
        return tour


    def initialization(cities):
        """ 初代を生成 """
        sequence = list(range(N))   # 0, 1, ... , N-1
        generation_zero = [[] for _ in range(island_number)]
        # それぞれの島に対して
        for island in range(island_number):
            # 各島に含まれるpathの数だけ貪欲法で生成し、2-optで改善しておく
            for _ in range(paths_in_island):
                initial_list = greedy(cities)          # 貪欲法
                initial_list = two_opt(initial_list)   # 2-opt
                generation_zero[island].append(initial_list)
        
        return generation_zero
    

    def selection(parent_generation: list[list[int]]) -> list[list[list[int]]]:
        """ トーナメント方式で親となるpathの組を paths_in_island 個作成し、重複しないものだけを選択 """
        parents = []        # 生成した親を一旦保持
        parents_pool = []   # 生成した親の組み合わせを保持
        while (len(parents_pool) < paths_in_island):   # paths_in_island 個作成
            selection = random.sample(parent_generation, 6)   # 全てのpathの中から6つをランダムで選択
            tournament = [[], []]   # [[ここから親1のtounament], [ここから親2のtounament]]
            tournament[0] = selection[:3]   # 3つのpathに分ける -> ここから親1のtournament
            tournament[1] = selection[3:]   # ここから親2のtournament
            min_length = float('inf')
            # 親1と親2に対して、3つのpathの内、距離が最小のものをmin_length_pathとする
            for i in range(2):
                for path in tournament[i]:
                    path_length = sum(dist[path[j]][path[(j + 1) % N]] for j in range(N))
                    if  path_length < min_length:
                        min_length = path_length
                        min_length_path = path
                parents.append(min_length_path)
            parents_pool.append(parents)
        return parents_pool

    
    def crossover(parents: list[list[int]]) -> tuple[list[int], list[int]]:
        """ 
        Partially Mapped Crossover を用いて交叉 
        1. 交叉点を2つ選ぶ
        2. 子に親1(親2)の中間部分をコピーし、そのほかを親2(親1)のcitiesで埋める
        3. マッピング関係を作る
        4. 子の中で重複したcityをマッピングを使って修正する

        """
        parent1 = parents[0]
        parent2 = parents[1]

        # 1. 交叉点を2つ選ぶ
        start, end = sorted(random.sample(range(1, N-2), 2))   # 最初と最後を除いてrandomに2つ選ぶ

        # 2. 子に親1(親2)の中間部分をコピーし、そのほかを親2(親1)のcitiesで埋める
        child1 = parent1[:start] + parent2[start:end] + parent1[end:]
        child2 = parent2[:start] + parent1[start:end] + parent2[end:]

        # 3. マッピング関係を作る
        map1 = {parent2[i]:parent1[i] for i in range(start, end)}   # parent1の修正に用いる
        map2 = {parent1[i]:parent2[i] for i in range(start, end)}   # parent2の修正に用いる

        # 4. 子の中で重複したcityをマッピングを使って修正する
        # 最初 ~ start-1 まで
        for i in range(start):
            # 1. mapにcityが存在すれば、そのcityは重複しているので、keyに対応するitemを取得
            # 2. そのitemがさらにkeyになっているならば、keyでなくなるまでitemを取得
            while child1[i] in map1:
                child1[i] = map1[child1[i]]
            while child2[i] in map2:
                child2[i] = map2[child2[i]]
        # end+1 ~ 最後 まで
        for i in range(end, N):
            while child1[i] in map1:
                child1[i] = map1[child1[i]]
            while child2[i] in map2:
                child2[i] = map2[child2[i]]

        return child1, child2


    def evaluation(generation_in_island: list[list[int]]) -> list[list[int]]:
        """ ルートの短い順にpaths_in_islandの数だけ選択 """
        length = []   # pathとその距離を格納
        next_generation = []
        for path in generation_in_island:
            path_length = sum(dist[path[i]][path[(i + 1) % N]] for i in range(N))
            length.append((path_length, path))
        sorted_paths = [path for _, path in sorted(length)]
        next_generation = sorted_paths[:paths_in_island]
        return next_generation
        

    def immigration(islands: list[list[list[int]]]) -> list[list[list[int]]]:
        for i in range(island_number):
            # migrating_pathsに、島ごとに移動するpathを格納する
            migrating_paths = [[] for _ in range(island_number)]
            # islandに含まれるpathの内migration_rateの割合だけ抽出
            migrating_paths[i] = random.sample(islands[i], int(migration_rate * paths_in_island))
            # 移動するpathは元の島から削除
            for path in migrating_paths[i]:
                islands[i].remove(path)
            
        for i in range(island_number):
            # 次のindexの島に移動させる
            index = (i + 1) % island_number
            islands[index] += migrating_paths[i]
        return islands


    generation = initialization(cities)
    for _ in range(generations):
        new_generation = []
        for i in range(island_number):
            parents_pool = selection(generation[i])
            children = []
            for parents in parents_pool:
                child1, child2 = crossover(parents)
                children.extend([child1, child2])
            evaluated = evaluation(children)
            new_generation.append(evaluated)
        generation = immigration(new_generation)


    tour = min((path for island in generation for path in island),
    key=lambda path: sum(dist[path[i]][path[(i + 1) % N]] for i in range(N)))

    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)

