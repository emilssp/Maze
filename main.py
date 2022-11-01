class Node():

    def __init__(self,state,parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():

    def __init__(self):
        self.frontier = []

    def add(self,node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier)==0

    def remove(self):
        if self.empty():
            raise Exception("Empty")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("Empty")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Astar_frontier(StackFrontier):

    def remove(self,end,start):
        if self.empty():
            raise Exception("Empty")
        else:
            node = self.frontier
            a_star=[]
            for i in range(0,len(node)):
                a_star.append(abs(node[i].state[0]-start[0])+abs(node[i].state[1]-start[1])+abs(node[i].state[0]-end[0])+abs(node[i].state[1]-end[1]))
            node = self.frontier[a_star.index(min(a_star))]
            self.frontier.remove(self.frontier[a_star.index(min(a_star))])
            return node



class Maze():

    def __init__(self, filename):
        with open(f"mazes/{filename}") as f:
            contents = f.read()
        if contents.count("A") != 1:
            raise Exception ("Only one start point allowed!")
        if contents.count("B") != 1:
            raise Exception ("Only one end point allowed!")

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []
        for i in range (self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j]=="A":
                        self.start = (i,j)
                        row.append(False)
                    elif contents[i][j]=="B":
                        self.end = (i,j)
                        row.append(False)
                    elif contents[i][j]==" ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        if self.solution != None:
            solution = self.solution[1]
        else:
            solution = None
        print()
        for i, row in enumerate(self.walls):
            for j,col in enumerate(row):
                if col:
                    print("#", end="")
                elif (i,j)==self.start:
                    print("A", end="")
                elif (i,j)==self.end:
                    print("B", end="")
                elif solution is not None and (i,j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state

        tries = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1)),
        ]

        result = []

        for action,(r,c) in tries:
            try:
                if not self.walls[r][c]:
                    result.append((action,(r,c)))
            except IndexError:
                continue
        return result

    def solve(self):
        self.number_explored = 0

        start = Node(state=self.start, parent=None, action=None)
        frontier =  Astar_frontier()
        frontier.add(start)

        self.explored = set() #empty explored set

        while True:

            if frontier.empty():
                raise Exception("No solution")

            node = frontier.remove(start=self.start,end=self.end)
            self.number_explored += 1

            if node.state == self.end:
                actions = []
                cells = []

                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


mzn = input("Choose a maze from 1 to 3: ")

m = Maze(f'maze{mzn}.txt')
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.number_explored)
print("Solution:")
m.print()