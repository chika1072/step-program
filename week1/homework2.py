from collections import Counter

SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]

# wordのscoreを計算する
def score(word):
    score = 0
    for chr in word:
        score += SCORES[ord(chr) - ord('a')]
    return score


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
        if counter_word[chr] > counter_line.get(chr, 0):  # Prevents KeyError
            return False
    return True


def main():
    # ファイルを開く
    with open('week1/words.txt','r') as f:
        words = f.read().splitlines()

    with open('week1/small.txt','r') as f:
        lines = f.read().splitlines()
    
    counter_word = {}
    counter_line = {}
    for word in words:
        counter_word[word] = score(word)
    for line in lines:
        counter_line[word] = score(line)

    for i in range(len(words)):
        biggest_score_line
        anagrams = counter_word
        for line in lines:
            if word_in_line(biggest_score_line, line) == True:
                return score(biggest_score_line)
        i += 1
    
if __name__ == '__main__':
    print(main())