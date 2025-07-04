#!/usr/bin/env python3

import sys
import math
import random

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def solve(cities):
    # greedy法
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    shortest_length = float('inf')
    # startを10個randomに設定し、greedy法を行い、shortest_lengthを更新していく
    for _ in range(10):
        start = random.randint(0, N-1)

        current_city = start
        unvisited_cities = set(range(0, N))  # unvisited_citiesに、0からNまで追加
        unvisited_cities.remove(start)  #  unvisited_citiesから、startだけ除外
        temporary_tour = [current_city]

        # citiesの内、90%のパスを短い順につなぐ
        while len(unvisited_cities) / N >= 0.1:
            next_city = min(unvisited_cities,
                            key=lambda city: dist[current_city][city])
            unvisited_cities.remove(next_city)
            temporary_tour.append(next_city)
            current_city = next_city
        
        # 残りのcitiesを最小となるような区間に挿入する
        while unvisited_cities:  # unvisited_citiesに残っている全てのcityに対して
            city = unvisited_cities.pop()
            # shortest_insertの初期値を、(tourの初め)->city + city->(tourの終わり) に設定
            shortest_insert = dist[city][start] + dist[city][temporary_tour[-1]]
            # すべてのパスに挿入して最小値を記録する
            for i in range(len(temporary_tour)-2):
                if dist[city][temporary_tour[i]] + dist[city][temporary_tour[i+1]] < shortest_insert:
                    shortest_insert = dist[city][temporary_tour[i]] + dist[city][temporary_tour[i+1]]
                    to_be_inserted = i+1  # insertしたい場所を記録
            # 挿入し、tourを更新
            temporary_tour.insert(to_be_inserted, city)


        # pathの長さを計算
        path_length = sum(distance(cities[temporary_tour[i]], cities[temporary_tour[(i + 1) % N]])
                              for i in range(N))
        # 最短であればtourを更新
        if path_length < shortest_length:
            shortest_length = path_length
            tour = temporary_tour

    # 2-opt
    while True:
        cnt = 0
        for i in range(N-3):
            for j in range(i+2, N-1):
                # もしi->i+1, j->j+1の長さよりも、i->j, i+1->j+1のほうが短いなら
                if dist[tour[i]][tour[i+1]] + dist[tour[j]][tour[j+1]] > dist[tour[i]][tour[j]] + dist[tour[i+1]][tour[j+1]]:
                    # pathを入れ替える
                    tour = tour[:i+1] + tour[j:i:-1] + tour[j+1:]
                    cnt += 1
        if cnt == 0:  #改善がみられなかったら終了
            break
 
    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)

