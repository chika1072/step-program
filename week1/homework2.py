from collections import Counter

SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]

# wordのscoreを計算する
def score(word):
    score = 0
    for char in word:
        score += SCORES[ord(char) - ord('a')]
    return score


# wordをscoreの大きい順に格納する
def sorted_words(words):
    word_score = [[word, score(word)] for word in words]
    sort_word_score = sorted(word_score, key = lambda x: x[1], reverse = True)   # scoreの大きい順に並べる
    sorted_words = [item[0] for item in sort_word_score]   # wordだけ取り出す
    return sorted_words

# wordがlineの中に含まれるか判定
def word_in_line(word, line):
    for chr in set(word):
        if chr not in set(line):
            return False
    # wordに含まれる全ての文字がlineにも含まれていたら、
    # (文字のwordに含まれる数) <= (文字のlineに含まれる数) を確認する
    counter_word = Counter(word)
    counter_line = Counter(line)
    for chr in counter_word:
        if counter_word[chr] > counter_line.get(chr, 0):
            return False
    return True


def main():
    # ファイルを開く
    with open('week1/words.txt','r') as f:   # words.txtを開く -> 変更しない
        words = f.read().splitlines()

    with open('week1/large.txt','r') as f:   # 開きたいファイルを指定
        lines = f.read().splitlines()

    biggest_score_words = []   # lineごとに最も大きいスコアの単語を格納するリスト
    sorted_word_list = sorted_words(words)
    for line in lines:
        for word in sorted_word_list:
            if word_in_line(word, line) == True:
                biggest_score_words.append(word)
                break
    
    with open ('week1/large_answer.txt', mode = 'w') as f:   # 作成したいファイル名を指定
        f.write('\n'.join(biggest_score_words))   # 改行して、一単語ずつ出力
    print('large_answer.txt is generated')

if __name__ == '__main__':
    main()