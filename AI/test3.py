from copy import deepcopy
from timeit import default_timer as timer

class puzzle:
    def __init__(self, starting, parent):
        self.board = starting
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0

    def manhattan(self):
        h = 0
        for i in range(3):
            for j in range(3):
                x, y = divmod(self.board[i][j], 3)
                h += abs(x - i) + abs(y - j)
        return h

    def goal(self):
        inc = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != inc:
                    return False
                inc += 1
        return True

    def __eq__(self, other):
        return self.board == other.board


def move_function(curr):
    curr = curr.board
    for i in range(3):
        for j in range(3):
            if curr[i][j] == 0:
                x, y = i, j
                break
    q = []
    if x - 1 >= 0:
        b = deepcopy(curr)
        b[x][y] = b[x - 1][y]
        b[x - 1][y] = 0
        succ = puzzle(b, curr)
        q.append(succ)
    if x + 1 < 3:
        b = deepcopy(curr)
        b[x][y] = b[x + 1][y]
        b[x + 1][y] = 0
        succ = puzzle(b, curr)
        q.append(succ)
    if y - 1 >= 0:
        b = deepcopy(curr)
        b[x][y] = b[x][y - 1]
        b[x][y - 1] = 0
        succ = puzzle(b, curr)
        q.append(succ)
    if y + 1 < 3:
        b = deepcopy(curr)
        b[x][y] = b[x][y + 1]
        b[x][y + 1] = 0
        succ = puzzle(b, curr)
        q.append(succ)
    print(len(q))
    return q



def best_fvalue(openList):
    f = openList[0].f
    index = 0
    for i, item in enumerate(openList):
        if i == 0:
            continue
        if (item.f < f):
            f = item.f
            index = i
    return openList[index], index


def AStar(start): #1
    openList = []#2
    closedList = []#3
    openList.append(start)#4

    while openList:
        current, index = best_fvalue(openList)
        if current.goal():
            return current
        print(index)
        openList.pop(index)
        print(openList.__sizeof__())
        closedList.append(current)
        print(closedList.__sizeof__())
        X = move_function(current)
        for move in X:
            ok = False  # checking in closedList
            for i, item in enumerate(closedList):
                if item == move:
                    ok = True
                    break
            if not ok:  # not in closed list
                newG = current.g + 1
                present = False

                # openList includes move
                for j, item in enumerate(openList):
                    if item == move:
                        present = True
                        if newG < openList[j].g:
                            openList[j].g = newG
                            openList[j].f = openList[j].g + openList[j].h
                            openList[j].parent = current
                if not present:
                    move.g = newG
                    move.h = move.manhattan()
                    move.f = move.g + move.h
                    move.parent = current
                    openList.append(move)

    return None

tart= timer()
#start = puzzle([[1,2,3],[4,0,5],[6,7,8]], None)
start = puzzle([[7, 2, 4], [5, 0, 6], [8, 3, 1]], None)
#start = puzzle([[0,1,2],[3,4,5],[6,7,8]], None)
#start = puzzle([[1,2,0],[3,4,5],[6,7,8]], None)
result = AStar(start)
end = timer()

noofMoves = 0

if (not result):
    print("No solution")
else:
    print(result.board)
    t = result.parent
    while t:
        noofMoves += 1
        print(t.board)
        t = t.parent
print("Length: " + str(noofMoves))
print(end-tart)