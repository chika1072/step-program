# 電卓プログラムをモジュール化して機能を追加する

#! /usr/bin/python3
import unicodedata
import sys


# 文字列のUnicode正規化 (全角の入力を半角にする)
def normalize_expression(formula):
    return unicodedata.normalize("NFKC", formula)


# 数字のtoken
def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():  # 整数を読み取る
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':  # 小数を読み取る
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


# '+'のtoken
def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

# '-'のtoken
def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

# '*'のtoken
def read_multiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1

# '/'のtoken
def read_divide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

# '('のtoken
def read_left_parenthesis(line, index):
    token = {'type': 'LEFT_PARENTHESIS'}
    return token, index + 1

# ')'のtoken
def read_right_parenthesis(line, index):
    token = {'type': 'RIGHT_PARENTHESIS'}
    return token, index + 1

# 'abs'のtoken
def read_abs(line, index):
    token = {'type': 'ABS'}
    return token, index + 3

# 'int'のtoken
def read_int(line, index):
    token = {'type': 'INT'}
    return token, index + 3

# 'round'のtoken
def read_round(line, index):
    token = {'type': 'ROUND'}
    return token, index + 5


# 入力をtokenにして格納
def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        elif line[index] == '(':
            (token, index) = read_left_parenthesis(line, index)
        elif line[index] == ')':
            (token, index) = read_right_parenthesis(line, index)
        elif line[index : index + 3] == 'abs':
            (token, index) = read_abs(line, index)
        elif line[index : index + 3] == 'int':
            (token, index) = read_int(line, index)
        elif line[index : index + 5] == 'round':
            (token, index) = read_round(line, index)
        else:
            print('Invalid character found: ' + line[index])
            sys.exit(1)
        tokens.append(token)
    return tokens


# かっこの計算
def calculate_parentheses(tokens):
    # 2(1+3)のように、かっこの前の'*'が省略されている場合に、'*'を付け加える
    for index in range(len(tokens)):
        if (tokens[index]['type'] == 'LEFT_PARENTHESIS') and (tokens[index - 1]['type'] == 'NUMBER'):
            tokens.insert(index, {'type': 'MULTIPLY'})
    
    # かっこの処理： ')'が存在したら、'('まで遡って計算する
    index = 1
    left_parentheses_index = []
    while index < len(tokens):
        # ')'が存在したなら
        if tokens[index]['type'] == 'RIGHT_PARENTHESIS':
            # ')'のindexをright_indexとする
            right_index = index
            # ')'の一つ前から読み取る
            index -= 1
            # '('が存在するまでindexを一つずつ小さくしていき、
            # 計算の順番になるようにinside_parenthesisに中身を追加する
            inside_parenthesis = []
            while tokens[index]['type'] != 'LEFT_PARENTHESIS':
                inside_parenthesis.insert(0, tokens[index])
                index -= 1
            # かっこの中身を計算する
            inside_answer = evaluate(inside_parenthesis)

            # '('の一つ前が関数なら関数を適用
            if (tokens[index - 1]['type'] in {'ABS', 'INT', 'ROUND'}):
                # indexを関数の位置に合わせる
                index -= 1
                if tokens[index]['type'] == 'ABS':
                    inside_answer = abs(inside_answer)
                elif tokens[index]['type'] == 'INT':
                    inside_answer = int(inside_answer)
                elif tokens[index]['type'] == 'ROUND':
                    inside_answer = round(inside_answer)
                # 関数から')'までをdeleteし、
                # かっこの中身の結果を新しいtokenとしてinsertする
                del tokens[index : right_index + 1]
                tokens.insert(index, {'type': 'NUMBER', 'number': inside_answer})
                
            # 関数でないなら'('から')'までをdeleteする
            else:
                del tokens[index : right_index + 1]
                tokens.insert(index, {'type': 'NUMBER', 'number': inside_answer})
        index += 1


# 掛け算と割り算の計算
def multiply_divide(tokens):
    index = 1
    while index < len(tokens):
        # 掛け算の計算
        if tokens[index]['type'] == 'MULTIPLY':
            # 一つ前のtokenと、一つ後のtokenを掛ける
            multiplied_num = tokens[index - 1]['number'] * tokens[index + 1]['number']
            # 一つ前のtokenから、一つ後のtokenまでをdeleteする
            del tokens[index - 1 : index + 2]
            # 掛け算の結果を新しいtokenとしてinsertする
            tokens.insert(index - 1, {'type': 'NUMBER', 'number': multiplied_num})
            # insertしたtokenを指すようにindexを調整
            index -= 1
        # 割り算の計算
        elif tokens[index]['type'] == 'DIVIDE':
            # 0での割り算が発生したら、exitする
            if tokens[index + 1]['number'] == 0:
                print("You cannot divide by zero.")
                sys.exit(1)
            else:
                # 一つ前のtokenを、一つ後のtokenで割る
                divided_num = tokens[index - 1]['number'] / tokens[index + 1]['number']
                # 一つ前のtokenから、一つ後のtokenまでをdeleteする
                del tokens[index - 1 : index + 2]
                # 割り算の結果を新しいtokenとしてinsertする
                tokens.insert(index - 1, {'type': 'NUMBER', 'number': divided_num})
                # insertしたtokenを指すようにindexを調整
                index -= 1
        index += 1
    return tokens


# tokensの計算
def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1  # dummy tokenの次から読み取る
    # かっこの計算を行う
    calculate_parentheses(tokens)
    # 掛け算と割り算を行う
    multiply_divide(tokens)
    # 足し算と引き算を行う
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                sys.exit(1)
        index += 1
    return answer


def test(line):
    line = normalize_expression(line)
    line = line.replace(' ', '')  # スペースがあれば除く
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print(f"PASS! ({line} = {expected_answer})")
    else:
        print(f"FAIL! ({line} should be {expected_answer} but was {actual_answer})")


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1")  # 数字
    test("1+2")  # 加
    test("1-2")  # 減
    test("1+2-3")  # 整数の加減
    test("1.1+2.2-3.3")  # 小数の加減
    test("1.-2.2+3")  # 整数と小数の加減
    test("1*2")  # 乗
    test("1/2")  # 徐
    test("1/2*3")  # 整数の乗除
    test("1.1*2.2/3.3")  # 小数の乗除
    test("1./2*3.3*4")  # 整数と小数の乗除
    test("1+2*3-4/5")  # 整数の加減乗除
    test("1.1+2.2/3.3-4.4*5.5")  # 小数の加減乗除
    test("1.1*2-3+4.4/5")  # 整数と小数の加減乗除
    test("2*(3+4)")  # かっこ
    test("(1+2*(3-4))/5")  # 複数かっこ
    test("(1)")  # かっこの中に数字
    test("abs(-1)")  # absの中に数字
    test("int(1.5)")  # intの中に数字
    test("round(1.5)")  # roundの中に数字
    test("abs(1-2)")  # absの中に式
    test("int(1.2-3.4)")  # intの中に式
    test("round(1.1*2.2)")  # roundの中に式
    test("1+abs(-2*int(1.2+3.4))")  # 関数の二重構造
    test("12+abs(int(round(-1.55)+abs(int(-2.3+4))))")  # 関数の多重構造
    test("１＋２")  # 全角の入力
    test("1 / (2 - 3) + 4 * 5")  # スペースを含む入力
    print("==== Test finished! ====\n")

run_test()


while True:
    print('> ', end="")
    line = input()
    line = normalize_expression(line)  # 規格化
    line = line.replace(' ', '')  # スペースがあれば除く
    tokens = tokenize(line)
    print(tokens)
    answer = evaluate(tokens)
    print(f"answer = {answer}\n")