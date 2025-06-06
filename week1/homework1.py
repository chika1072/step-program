# 与えられた文字列のAnagramを辞書ファイルから探して、「見つかったアナグラム全部」を答えるプログラムを作る

# 二分探索
def binary_search(sorted_dict, w):
    anagram = []
    left, right = 0, len(sorted_dict) - 1
    while left <= right:
        mid = (left + right) // 2
        if sorted_dict[mid][0] == ''.join(sorted(w)):
            anagram.append(sorted_dict[mid][1])
            #anagramが複数あるか確認する
            i = 1
            while mid + i < len(sorted_dict) and sorted_dict[mid + i][0] == ''.join(sorted(w)):
                anagram.append(sorted_dict[mid + i][1])
                i += 1
            i = 1
            while mid - i < len(sorted_dict) and sorted_dict[mid - i][0] == ''.join(sorted(w)):
                anagram.append(sorted_dict[mid - i][1])
                i += 1
            return anagram
        elif sorted_dict[mid][0] < ''.join(sorted(w)):
            left = mid + 1
        else:
            right = mid - 1


def main():
    # words.txtを開く
    f = open('week1/words.txt','r')
    words = f.read().splitlines()
    f.close()


    sorted_words = []
    sorted_dict = []

    # wordsの単語をそれぞれsortする
    for word in words:
        sorted_words.append([''.join(sorted(word)), word])

    # wordsの単語をそれぞれsortする
    sorted_dict = sorted(sorted_words, key=lambda x:x[0])

    print('Input a word: ')
    input_word = input()
    print('Anagram: ')

    anagram = binary_search(sorted_dict, input_word)
    print(anagram)


if __name__ == "__main__":
    main()
