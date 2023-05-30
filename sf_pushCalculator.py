
def pushCalculator(push):
    if push == '爆':
        push = 100
    elif pushJudge(push):
        return dislikeCalculator(push)
    else:
        push = int(push)
    return push

def dislikeCalculator(push):
    #符合噓文的規則, 噓達10次, 為X1, 以此類推, 至XX
    if push[1] != 'X':
        return -(int(push[1])*10)
    else:
        return -100

def pushJudge(push):
    # 判斷是否是X1, X2等格式
    if push[0] == 'X':
        return True

print(pushCalculator('爆'))