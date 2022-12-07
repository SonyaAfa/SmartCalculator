

import re

from collections import deque

import string


class InvExpressionError(Exception):
    def __str__(self):
        return "Invalid expression"


class UnkownVariableError(Exception):
    def __str__(self):
        return "Unknown variable"


def minus_counter(word):
    return word.count("-")


def is_signs(word):
    for s in word:
        if s not in ["+", "-"]:
            return False
    return True


def cut_empty_boarders(word):
    word_without_empty_board = word
    while word_without_empty_board[-1] == " ":
        word_without_empty_board = word_without_empty_board[:-1]
    while word_without_empty_board[0] == " ":
        word_without_empty_board = word_without_empty_board[1:]
    return word_without_empty_board


def check_latin(word):
    """"checks wehether the word contain only Latin letters"""
    latin = string.ascii_letters
    word_without_empty_board = cut_empty_boarders(word)
    for l in word_without_empty_board:
        if l not in latin:
            return False

    return True


def check_int_or_in_dictionary(word, dictionary):
    word_without_empty_board = cut_empty_boarders(word)
    if not (word_without_empty_board.isdigit() or dictionary.get(word_without_empty_board)):
        return False
    return True

def remove_the_blanks(list):
    """"Remove ' ' from a list"""
    while "" in list:
        list.remove("")
    return list


def priopity(chr:string)->int:
    if chr in ["+","-"]:
        return 1
    elif chr in ['*',"/"]:
        return 2
    elif chr in ["(",")"]:
        return 0



def postfix_expression(infix_expr:list)->deque:
    if len(infix_expr)== 0:
        return deque()


    my_stack=deque()
    postfix_expr=deque()

    for i in range(len(infix_expr)):

        word=infix_expr[i]
        if re.match("[0-9]+",word) or re.match("\w+",word):

            postfix_expr.append(word)

        elif word=="(" or len(my_stack)==0:
            my_stack.append(word)

        elif word==")" :
            last_in_my_stack = my_stack.pop()
            while last_in_my_stack!="(":
                postfix_expr.append(last_in_my_stack)
                try:
                    last_in_my_stack = my_stack.pop()
                except:  #InvExpressionError:
                    raise InvExpressionError


        else:
            last_in_my_stack = my_stack.pop()

            if last_in_my_stack=="(":
                my_stack.append(last_in_my_stack)
                my_stack.append(word)

            elif priopity(word)>priopity(last_in_my_stack):
                my_stack.append(last_in_my_stack)
                my_stack.append(word)

            else:

                empt=False #True when my_stack is empty
                while (priopity(word) <= priopity(last_in_my_stack)) and not empt:

                    postfix_expr.append(last_in_my_stack)
                    if len(my_stack)>0:
                        last_in_my_stack = my_stack.pop()
                    else:
                        empt=True
                if not empt:
                    my_stack.append(last_in_my_stack)

                my_stack.append(word)

    while len(my_stack)>0:
        postfix_expr.append(my_stack.pop())

    return postfix_expr

def calculate_the_result(postfix_expr:deque,dictionary:dict)->int:
    my_stack=deque() # stack for calculations
    while len(postfix_expr)>0:
        word=postfix_expr.popleft()
        if re.match("[0-9]+",word):
            my_stack.append(word)

        elif re.match("\w+",word):
            if dictionary.get(word) or dictionary.get(word) == 0:
                my_stack.append(dictionary.get(word))
            else:
                raise UnkownVariableError
        elif word == "/error":
            return "error"
        else:
            operand2=int(my_stack.pop())
            operand1=int(my_stack.pop())
            if re.match("[+-]+",word):
                result = operand1 + (-1)**minus_counter(word)*operand2

            elif word == "*":
                result = operand1 * operand2
            elif word in ["(",")"]:
                raise InvExpressionError
            elif word == "/":
                try:
                    result = operand1 / operand2
                except ZeroDivisionError:
                    print('Zero div')
                    result='Zero Division'
                    break
            my_stack.append(result)


    return my_stack.pop()

def check_valid(str):
    for i in str:
        if i not in ["0","1","2","3","4","5","6","7","8","9","+","-","*","/","(",")"," "] and not re.match("\w",i):
            return False
    return True

if __name__ == '__main__':

    read = True
    names_dictionary = {}
    ne_nuzno=0
    while read:
        str = input()
        if len(str) == 0:
            continue
        elif str == '/exit':
           print("Bye!")
           read = False
        elif str == '/help':
            print('The program calculates the value of expression,using +,-,* and')
        elif str[0] == '/':
            print("Unknown command")
        elif "=" in str:
            word_left = str[:str.index("=")]
            word_right = str[str.index("="):][1:]
            #print(word_left,word_right)
            if not check_latin(word_left):

               print("Invalid identifier")
            elif check_int_or_in_dictionary(word_right, names_dictionary):
                # print('gg',cut_empty_boarders(word_right))
              if cut_empty_boarders(word_right).isdigit():
                  names_dictionary[cut_empty_boarders(word_left)] = int(cut_empty_boarders(word_right))
              else:
                  names_dictionary[cut_empty_boarders(word_left)] = names_dictionary.get(cut_empty_boarders(word_right))
            else:
                print("Invalid expression")

        elif re.findall("\*{2}", str) or re.findall("/{2}", str):
            print("Invalid expression")
            #print("***")
        elif not check_valid(str):
            print("Invalid expression")
            #print("check")

        else:
            if str[0] == "-":
                str = "0" + str
            pattern = r"[+-]+|[0-9]+|\*+|\(|\)|/|=|\w+"
            list = remove_the_blanks(re.findall(pattern, str))


            try:
                postfix_expr = postfix_expression(list)
                print(calculate_the_result(postfix_expr, names_dictionary))
            except InvExpressionError as err:
                print(err)


            except UnkownVariableError as err:

                print(err)












