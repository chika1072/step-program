# answer.txtのscoreの和を求める

SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]

# wordのscoreを計算する
def score(word):
    score = 0
    for char in word:
        score += SCORES[ord(char) - ord('a')]
    return score


def main():
    total_score = 0
    with open ('week1/large_answer.txt', mode = 'r') as f:   # 開きたいファイルを指定
        words = f.read().splitlines()
    for word in words:
        total_score += score(word)
    print(total_score)

if __name__ == '__main__':
    main()