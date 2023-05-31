
def pushCalculator(push):
    if push == '':
        return 0
    else:
        if push == '爆':
            push = 100
        elif __pushJudge(push):
            return __dislikeCalculator(push)
        else:
            push = int(push)
        return push


#符合噓文的規則, 噓達10次, 為X1, 以此類推, 至XX
def __dislikeCalculator(push):
    if push[1] != 'X':
        return -(int(push[1])*10)
    else:
        return -100

# 判斷是否是X1, X2等格式
def __pushJudge(push):
    if push[0] == 'X':
        return True