import math
from timeit import default_timer as timer
class Node:
    # Node constructor includes the board state as well as a link to the parent Node
    # has additional attributes for calculating score of board.
    def __init__(self, board, parent):
        self.board = board
        self.parent = parent
        self.total_cost = 0
        self.node_cost = 0
        self.h_cost = 0

    # check equivalance of board states
    def __eq__(self, other):
        return self.board == other.board   

    # heristics function calls the specific
    def heruistic_choice(self, choice,goal):
        if (choice == 1):
            return self.manhattan(goal)
        if (choice == 2):
            return self.euclid(goal)
        else:
            print("enter valid choice")
    # manhattan heuristic to find the distance of each cell
    def manhattan(self,other):       
        h_cost = 0
        for i in range(3):
            for j in range(3):
                if(self.board[i][j] != 0):
                    pos = find_position(other.board, self.board[i][j])
                    h_cost += abs(pos[0]-i) + abs(pos[1]-j)       
        return h_cost
     #euclidean heuristic to find the distance of each cell
    def euclid(self,other):
        h_cost = 0
        for i in range(3):
            for j in range(3):
                if(self.board[i][j] != 0):
                    pos = find_position(other.board, self.board[i][j])
                    wt = abs(pos[0]-i)
                    ht = abs(pos[1]-j)
                    h_cost += math.floor(math.sqrt(wt * wt + ht * ht))        
        return h_cost     
                   
# finds x and y coordinate of the given board and element to find
def find_position(state,target):
    for i in range(3):
        if target in state[i]:
            return i,state[i].index(target)

# finds the board state with the least total cost value
def min_node(open_list):
    total_cost = open_list[0].total_cost
    index = 0
    for i, item in enumerate(open_list):
        if i == 0:
            continue
        if (item.total_cost < total_cost):
            total_cost = item.total_cost
            index = i
    return open_list[index], index

# returns a list of valid board moves by checking and not returning invalid ones
def board_moves(state):
    moves = []
    board = state.board
    x = find_position(state.board,0)[0]
    y = find_position(state.board,0)[1]
    
    if (x + 1 < 3):
        move = list(map(list,board))
        move[x][y] = move[x + 1][y]
        move[x + 1][y] = 0
        next_move = Node(move, board)
        moves.append(next_move)
    if (x - 1 >= 0):
        move = list(map(list,board))
        move[x][y] = move[x - 1][y]
        move[x - 1][y] = 0
        next_move = Node(move, board)
        moves.append(next_move)
    if (y + 1 < 3):
        move = list(map(list,board))
        move[x][y] = move[x][y + 1]
        move[x][y + 1] = 0
        next_move = Node(move, board)
        moves.append(next_move)
    if (y - 1 >= 0):
        move = list(map(list,board))
        move[x][y] = move[x][y - 1]
        move[x][y - 1] = 0
        next_move = Node(move, board)
        moves.append(next_move)
    return moves

# main A* algorithm
def algo(start,goal,choice):
    open_list = []
    closed_list = []
    open_list.append(start) #adds the intial start state

    while open_list:
        (state, index) = min_node(open_list)
        if state.__eq__(goal): # checks if goal state has been reached
            return state
        open_list.pop(index) #removes state before evaluating
        closed_list.append(state) # adds state into closed list
        moves = board_moves(state) 
        for move in moves:
            previous = False  # checking in closed list
            for i, closdmv in enumerate(closed_list):
                if closdmv == move:
                    previous = True # if in closed list the move is repeated hence it breaks
                    break
            if(not previous):  # not in closed list
                newBoard = state.node_cost + 1
                present = False

                # open list includes move
                for j, openmv in enumerate(open_list):
                    if openmv == move:
                        present = True
                        if newBoard < open_list[j].node_cost: 
                            open_list[j].node_cost = newBoard
                            open_list[j].total_cost = open_list[j].node_cost + open_list[j].h_cost
                            open_list[j].parent = state
                if(not present):
                    move.node_cost = newBoard
                    move.h_cost = move.heruistic_choice(choice,goal)
                    move.total_cost = move.node_cost + move.h_cost
                    move.parent = state
                    open_list.append(move)
    return False
start = timer()
#result = algo(Node(start,None),Node(stop,None),option)
#result = algo(Node([[6,4,7],[8,5,0],[3,2,1]],None), Node([[0,1,2],[3,4,5],[6,7,8]],None),1)
#result = algo(Node([[8,6,7],[2,5,4],[3,0,1]],None), Node([[0,1,2],[3,4,5],[6,7,8]],None),1)
#result = algo(Node([[1,2,3],[4,5,0],[6,7,8]],None), Node([[0,1,2],[3,4,5],[6,7,8]],None),1)
result = algo(Node([[7,2,4],[5,0,6],[8,3,1]],None), Node([[0,1,2],[3,4,5],[6,7,8]],None),1)
end = timer()

TotalMoves = 0

if (not result):
    print("Error")
else:
    print(result.board[0])
    print(result.board[1])
    print(result.board[2])
    print("\n")
    z = result.parent
    while z:
        TotalMoves += 1
        print(z.board[0])
        print(z.board[1])
        print(z.board[2])
        print("\n")
        z = z.parent
print("Moves " + str(TotalMoves))
print(end-start)


'''
LEGACY CODE that took forever to run 
    # calculates with manhattan distance
    def manhattan(self,other):
        h_cost = 0
        for i in range(3):
            for j in range(3):
                if(self.board[i][j] != 0):
                    found = False
                    for x in range(3):
                        for y in range(3):
                            if (self.board[i][j].__eq__(self.board[x][y])):
                                h_cost += abs(x-i) + abs(y-j)
                                found = True
                                break
                        if(found):
                            break
        return h_cost
    
    #calculates with euclidean distance
    def euclid(self,other):
        h_cost = 0
        for i in range(3):
            for j in range(3):
                found = False
                for x in range(3):
                    for y in range(3):
                        if(self.board[i][j].__eq__(other.board[x][y])):
                            ht = abs(y-j)
                            wt = abs(x-i)
                            h_cost += math.floor(math.sqrt(wt * wt + ht * ht))
                            found = True
                            break
                    if(found):
                        break           
        return h_cost'''
