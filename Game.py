
import pygame

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
class Screen:

    def __init__(self, height, width, name):

        self.height = height
        self.width = width
        self.name = name
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        self.events = pygame.event.get()
        Input.startListening()

class GameLoop:

    screen = None
    def __init__(self, frameRateCap=60):
        pygame.init()
        self.frameRateCap = frameRateCap

    def run(self):
        while True:
            GameLoop.screen.events = pygame.event.get()
            Input.keysPressed = pygame.key.get_pressed()

            # Your game logic update function
            self.update()
            GameLoop.screen.screen.fill((0,0,0))

            Input.keysPressedLastFrame = pygame.key.get_pressed()
            for event in GameLoop.screen.events:
                if event.type == pygame.QUIT:
                    pygame.quit()

    def update(self):
        ActionObj.runUpdates()

class Input:
    keys = {}
    numberOfKeys = 0
    keysPressed = []
    keysPressedLastFrame = []

    @staticmethod
    def startListening():
        Input.numberOfKeys = len(pygame.key.get_pressed())
        Input.keysPressed = pygame.key.get_pressed()
        Input.keysPressedLastFrame = pygame.key.get_pressed()
        for key in range(Input.numberOfKeys - 1):
            Input.keys[pygame.key.name(key)] = key

    @staticmethod
    def isKeyPressed(key,pressed = None):
        if pressed == None:
            return pygame.key.get_pressed()[Input.keys[key]]
        return pressed[Input.keys[key]]

    @staticmethod
    def getKeyDown(key):
        for event in GameLoop.screen.events:
            if event.type == pygame.KEYDOWN and Input.isKeyPressed(key):
                return True
        return False

    @staticmethod
    def getKeyUp(key):
        for event in GameLoop.screen.events:
            if event.type == pygame.KEYUP and Input.isKeyPressed(key,Input.keysPressedLastFrame):
                return True
        return False
class ActionObj:
    actionObjs = []
    def __init__(self):
        ActionObj.actionObjs.append(self)
    @staticmethod
    def runUpdates():
        for obj in ActionObj.actionObjs:
            obj.update()


def plot3dArray(array, show=False):
    try:
        # Ensure the input is a numpy array
        array = np.asarray(array)

        # Check if the array is 3D
        if array.ndim != 3:
            raise ValueError("Input array must be 3-dimensional")

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Define vertices for a unit cube
        cube_vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 1],
            [1, 1, 1],
            [0, 1, 1]
        ])

        # Define the 6 faces of a cube
        faces = [
            [cube_vertices[j] for j in [0, 1, 2, 3]],
            [cube_vertices[j] for j in [4, 5, 6, 7]],
            [cube_vertices[j] for j in [0, 1, 5, 4]],
            [cube_vertices[j] for j in [2, 3, 7, 6]],
            [cube_vertices[j] for j in [1, 2, 6, 5]],
            [cube_vertices[j] for j in [4, 7, 3, 0]]
        ]

        # Iterate through the array and plot blocks
        X, Y, Z = array.shape
        for x in range(X):
            for y in range(Y):
                for z in range(Z):
                    if not show:
                        if array[x, y, z] == 1:
                            translated_faces = [[vertex + [x, y, z] for vertex in face] for face in faces]
                            ax.add_collection3d(Poly3DCollection(translated_faces, facecolors='green', edgecolors='k'))
                        if array[x, y, z] == 2:
                            translated_faces = [[vertex + [x, y, z] for vertex in face] for face in faces]
                            ax.add_collection3d(Poly3DCollection(translated_faces, facecolors='purple', edgecolors='k'))
                        if array[x, y, z] == 4:
                            translated_faces = [[vertex + [x, y, z] for vertex in face] for face in faces]
                            ax.add_collection3d(Poly3DCollection(translated_faces, facecolors='blue', edgecolors='k'))
                        if array[x, y, z] == 5:
                            translated_faces = [[vertex + [x, y, z] for vertex in face] for face in faces]
                            ax.add_collection3d(Poly3DCollection(translated_faces, facecolors='red', edgecolors='k'))
                    if array[x, y, z] == 6:
                        translated_faces = [[vertex + [x, y, z] for vertex in face] for face in faces]
                        ax.add_collection3d(Poly3DCollection(translated_faces, facecolors='yellow', edgecolors='k'))
                    if array[x, y, z] == 3:
                        translated_faces = [[vertex + [x, y, z] for vertex in face] for face in faces]
                        ax.add_collection3d(Poly3DCollection(translated_faces, facecolors='black', edgecolors='k'))

        # Set plot limits
        ax.set_xlim(0, X)
        ax.set_ylim(0, Y)
        ax.set_zlim(0, Z)

        # Set labels
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        #ax.view_init(elev=30, azim=190)
        ax.view_init(elev=45, azim=-10)
        plt.show()
    except ValueError as e:
        print(f"Error: {e}")
def c(x):
    return x

class PriorityQueue():
    def __init__(self, fx=c):
        self.queue = []
        self.length = 0
        self.fx = fx

    def add(self, node):
        self.queue.append(node)
        self.queue.sort(key=self.fx)  # Sort the queue based on the fx value
        self.length = len(self.queue)

    def peak(self):
        return self.queue[0]

    def pop(self):
        self.length -= 1
        return self.queue.pop(0)  # Pop the first element (lowest fx value)
