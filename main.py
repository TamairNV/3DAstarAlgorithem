import math
import time as t
import Game

class Node():
    def __init__(self, pos, endNode, state=0, ):
        self.pos = pos
        self.g = 0
        self.h = 0
        # 0 = undiscovered
        # 1 = unvisited
        # 2 = discovered
        # 3 = wall
        # 4 = start
        # 5 = end
        # 6 = path
        self.state = state
        self.parent = None
        self.endNode = endNode

    def findF(self):
        return self.g + self.h

    def absDistance(self, position2):
        x = position2[0] - self.pos[0]
        y = position2[1] - self.pos[1]
        z = position2[2] - self.pos[2]

        return math.sqrt(x ** 2 + y ** 2 + z ** 2)

    def traceBack(self):
        currentNode = self
        path = [self.endNode]
        self.endNode.state = 6
        while currentNode != None:
            path.append(currentNode)
            currentNode.state = 6
            currentNode = currentNode.parent

        path.reverse()
        return path

    def discover(self, grid, queue):
        x, y, z = self.pos[0], self.pos[1], self.pos[2]

        adjacent = self.getAdjacentCells(grid, x, y, z)
        if self.state != 4:
            self.state = 2
        for node in adjacent:
            if node[0].state == 5:
                path = self.traceBack()
                return path

            if node[0] != self and node[0].state == 0:
                node[0].g = self.g + node[1]
                node[0].h = node[0].absDistance(self.endNode.pos)
                node[0].state = 1
                node[0].parent = self
                queue.add(node[0])
            elif node[0] != self and node[0].state == 1 and node[0].parent.g >= self.g:
                node[0].g = self.g + node[1]
                node[0].parent = self

        return None

    def getAdjacentCells(self, grid, x, y, z):
        adjacent_cells = []
        directions = [(dx, dy, dz) for dx in range(-1, 2) for dy in range(-1, 2) for dz in range(-1, 2)]

        directions.remove((0, 0, 0))  # Remove the current cell

        for dx, dy, dz in directions:
            new_x, new_y, new_z = x + dx, y + dy, z + dz
            if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and 0 <= new_z < len(grid[0][0]):
                distance = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

                adjacent_cells.append((grid[new_x][new_y][new_z], distance))

        return adjacent_cells

    @staticmethod
    def getF(node):
        return node.findF()


class Grid():
    def __init__(self, gridSize, startPos, endPos):
        self.queue = Game.PriorityQueue(fx=Node.getF)
        self.end = Node(endPos, None, state=5)
        self.start = Node(startPos, self.end, state=4)

        self.queue.add(self.start)
        self.grid = self.createGrid(gridSize)
        self.gridSize = gridSize

        self.grid[endPos[0]][endPos[1]][endPos[2]] = self.end
        self.grid[startPos[0]][startPos[1]][startPos[2]] = self.start

        pass

    def run(self):
        return self.queue.pop().discover(self.grid, self.queue)

    def createGrid(self, gridSize):
        grid = [[[Node([z, y, x], self.end) for x in range(gridSize[0])] for y in range(gridSize[1])] for z in
                range(gridSize[2])]
        return grid




class pathFinder(Game.ActionObj):
    def __init__(self):
        super().__init__()
        self.pathing = Grid([10, 10, 10], [0, 0, 0], [0, 9, 0])
        for i in range(10):
            self.pathing.grid[4][i][4].state = 3
            for j in range(5):
                self.pathing.grid[4][i][j].state = 3

        for i in range(5):
            self.pathing.grid[i][4][4].state = 3
            for j in range(10):
                self.pathing.grid[i][4][j].state = 3

        for i in range(5):
            self.pathing.grid[8 - i][4][4].state = 3
            for j in range(5):
                self.pathing.grid[8 - i][9 - j][4].state = 3

        for i in range(5):
            self.pathing.grid[i+5][4][4].state = 3
            for j in range(5):
                self.pathing.grid[i+5][4][j-5].state = 3


        self.done = False
        self.Display()
    def update(self):
        #time = t.time()
        if Game.Input.getKeyDown("space"):
            if not self.done:
                while True:
                    #t.sleep(0.05)
                    #self.Display(show=self.done)
                    for i in range(1):
                        path = self.pathing.run()
                        if path != None:
                            self.done = True
                            self.Display(show=True)
                            return

            self.Display(show=self.done)
    def Display(self, show=False):
        newGrid = [[[self.pathing.grid[z][y][x].state for x in range(self.pathing.gridSize[0])] for y in
                    range(self.pathing.gridSize[1])] for z in range(self.pathing.gridSize[2])]
        Game.plot3dArray(newGrid, show=show)


game = Game.GameLoop(frameRateCap=10)
Game.GameLoop.screen = Game.Screen(300, 300, "Pathfinding")
obj = pathFinder()
game.run()

