def tomita_1(word):
    return  "a" not in word

def tomita_2(word):
    return word=="ba"*(int(len(word)/2))

import re
_not_tomita_3 = re.compile("((a|b)*a)*b(bb)*(a(a|b)*b)*a(aa)*(b(a|b)*)*$") 
# *not* tomita 3: words containing an odd series of consecutive ones and then later an odd series of consecutive zeros
# tomita 3: opposite of that
def tomita_3(w): 
    return None is _not_tomita_3.match(w) #complement of _not_tomita_3

def tomita_4(word):
    return "aa" in word

def tomita_5(word):
    return (word.count("a")%2 == 0) and (word.count("b")%2 == 0)

def tomita_6(word):
    return ((word.count("a")-word.count("b"))%3) == 0

def tomita_7(word):
    return word.count("ba") >= 1

def tomita_8(word):
    return word.count("ba") < 1

def tomita_9(word):
    open_list = ["l","a"] 
    close_list = ["r",'b'] 
    
    stack = [] 
    for i in word: 
        if i in open_list: 
            stack.append(i) 
        elif i in close_list: 
            pos = close_list.index(i) 
            if ((len(stack) > 0) and
                (open_list[pos] == stack[len(stack)-1])): 
                stack.pop() 
            else: 
                return False
    if len(stack) == 0: 
        return True

def tomita_10(word):
    return not "aa" in word


