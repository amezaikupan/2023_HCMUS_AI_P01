import pygame
from enum import Enum
from graphic.util import readMap
from algorithm.search import handleLv1, handleLv2, handleLv3, handleLv4

#Declare roation direction for pacman
class Direction(Enum):
    Right = 0
    Left = 180
    Up = 90
    Down = -90
    Unchanged = 360

class PathFinder:
    def __init__(self, map, pacmanPos):
        self._map = map
        self._pacmanPos = pacmanPos
    def get_path(self, level):
        if (level == '1'):
            pacman_path, monster_path, status = handleLv1(self._map, self._pacmanPos)
            return pacman_path, monster_path, status
        elif (level == '2'):
            pacman_path, monster_path, status = handleLv2(self._map, self._pacmanPos)
            return pacman_path, monster_path, status
        elif (level == '3'):
            pacman_path, monster_path, status = handleLv3(self._map, self._pacmanPos)
            return pacman_path, monster_path, status
        elif (level == '4'):
            pacman_path, monster_path, status = handleLv4(self._map, self._pacmanPos)
            return pacman_path, monster_path, status
        
class GameController:
    def __init__(self, path):
        self._size, self._map, self._pacmanPos = readMap(path)
        self._status = None
        self._food_positions = []
        self._reachable_positions = []
        self._monster_spawns = []
        self._wall_positions = []
        self.getPosFromMap()
        self._pathFinder = PathFinder(self._map, self._pacmanPos)
        
    def set_status(self, status):
        self._status = status

    def getPosFromMap(self):
        for row in range(self._size[0]):
            for column in range(self._size[1]):
                if self._map[row][column] == 0:
                    self._reachable_positions.append((row, column))
                if self._map[row][column] == 1:
                    self._wall_positions.append((row, column))
                if self._map[row][column] == 2:
                    self._food_positions.append((row, column))
                    self._reachable_positions.append((row, column))
                if self._map[row][column] == 3:
                    self._monster_spawns.append((row, column))

class GameObject:
    def __init__(self, x, y, size, game_environment):
        self._x = x
        self._y = y
        self._size = size
        self._environment: Environment = game_environment
        self._surface = game_environment._screen
        
    def getShape(self):
        return pygame.Rect(self._x, self._y, self._size, self._size)
    
    def setPosition(self, x, y):
        self._x = x
        self._y = y
        
    def move(self):
        pass
    
    def getPosition(self):
        return self._x, self._y
    
    def draw(self):
        pass
    
class MovableGameObject(GameObject):
    def __init__(self, x, y, size, game_environment, image_path, object_path, controller):
        super().__init__(x, y, size, game_environment)
        self._curDirection = Direction.Unchanged
        self._positions = object_path
        self._image = pygame.image.load(image_path)
        self._nextPosition = None
        self._controller = controller
        self._surface = game_environment._screen
        
    def getNextPosition(self):
        #If there is no position left
        if (len(self._positions) == 0):
            return None
        else:
            return self._positions.pop(0)
        
    def setDirection(self, direction):
        self._curDirection = direction
    
    def getDirectionToTarget(self):
        #No valid move
        if self._nextPosition is None:
            self._nextPosition = self.getNextPosition()
            if (self._nextPosition is None and self._controller._status == "block"):
                self._environment.endGame()
            return Direction.Unchanged

        diff_x = self._nextPosition[0] - self._x
        diff_y = self._nextPosition[1] - self._y

        if diff_x == 0:
            return Direction.Down if diff_y > 0 else Direction.Up
        if diff_y == 0:
            return Direction.Left if diff_x < 0 else Direction.Right
        
        #If pacman continues to move straight
        self._nextPosition = self.getNextPosition()
        return self._curDirection
    
    def reachTarget(self):
        #check if Pacman has reached its target => get the next position
        if (self._x, self._y) == self._nextPosition:
            self._nextPosition = self.getNextPosition()
            if isinstance(self, Pacman):
                self._environment.calculateStepScore()
        self._curDirection = self.getDirectionToTarget()
        
    def updatePositionOnDirectionChange(self, direction):
        if direction == Direction.Up:
            self.setPosition(self._x, self._y - 1)
        elif direction == Direction.Down:
            self.setPosition(self._x, self._y + 1)
        elif direction == Direction.Left:
            self.setPosition(self._x - 1, self._y)
        elif direction == Direction.Right:
            self.setPosition(self._x + 1, self._y)
    
    def move(self):
        pass
    
    def draw(self):
        self._image = pygame.transform.scale(self._image, (self._size, self._size)) #rescale the image to fit
        self._surface.blit(self._image, self.getShape()) #blit the image on the screen
             
class Wall(GameObject):
    def __init__(self, x, y, size, game_environment, image_path):
        super().__init__(x*size, y*size, size, game_environment)
        self._image = pygame.image.load(image_path)
        self._surface = game_environment._screen
    
    def draw(self):
        self._image = pygame.transform.scale(self._image, (self._size, self._size)) #rescale the image to fit
        self._surface.blit(self._image, self.getShape()) #blit the image on the screen
        
class Food(GameObject):
    def __init__(self, x, y, size, game_environment, image_path):
        super().__init__(x, y, size, game_environment)
        self._image = pygame.image.load(image_path)
        self._surface = game_environment._screen
    
    def draw(self):
        self._image = pygame.transform.scale(self._image, (self._size, self._size)) #rescale the image to fit
        self._surface.blit(self._image, self.getShape()) #blit the image on the screen
        
class Pacman(MovableGameObject):
    def __init__(self, x, y, size, environment, image_path, object_path, controller):
        super().__init__(x, y, size, environment, image_path, object_path, controller)

    def move(self):
        self.reachTarget()
        self.updatePositionOnDirectionChange(self._curDirection)
        self.handleFoodPickUp()
        self.handleMonsterCollision()
        
    def handleFoodPickUp(self):
        foods = self._environment.getFood() 
        pacman = self._environment.getPacman()
        gameObjects = self._environment.getGameObject()
        food_to_remove = None
        
        for food in foods:
            if pacman.getShape().colliderect(food.getShape()):
                food_to_remove = food
                gameObjects.remove(food)
                self._environment.calculateFoodScore()
        
        if (food_to_remove is not None):
            foods.remove(food_to_remove)
        if (len(foods) == 0):
            self._environment.setWinCondition()
            
    def handleMonsterCollision(self):
        monsters = self._environment.getMonster()
        pacman = self._environment.getPacman()
        for monster in monsters:
            if pacman.getPosition() == monster.getPosition():
                self._environment.endGame()
    
    def draw(self):
        #self._image = pygame.transform.rotate(self._image, self._curDirection.value)
        super(Pacman, self).draw()
                        
class Monster(MovableGameObject):
    def __init__(self, x, y, size, environment, image_path, object_path, controller):
        super().__init__(x, y, size, environment, image_path, object_path, controller)
        
    def move(self):
        self.reachTarget()
        self.updatePositionOnDirectionChange(self._curDirection)
        
    def draw(self):
        super(Monster, self).draw()
        
class Environment:
    def __init__(self, width, height):
        pygame.init()
        self._level = 1
        self._mapNumber = 1
        self._height = height
        self._width = width
        self._hasWon = False
        self._score = 0
        self._walls = []
        self._foods = []
        self._monsters = []
        self._pacman: Pacman = None
        self._foodScore = 20
        self._gameObjects = []
        self._isEnded = False
        self._screen = pygame.display.set_mode([width, height])
        pygame.display.set_caption("PACMAN")
        self._clock = pygame.time.Clock()
        
    def setLevel(self, level):
        self._level = level   
    def setMap(self, map):
        self._mapNumber = map 
    def setWinCondition(self):
        self._hasWon = True
    def hasWon(self):
        return self._hasWon
    def setGameObject(self, object):
        self._gameObjects.append(object)
    def getGameObject(self):
        return self._gameObjects
    def setWall(self, object: Wall):
        self.setGameObject(object)
        self._walls.append(object)
    def setPacman(self, object: Pacman):
        self.setGameObject(object)
        self._pacman = object
    def getPacman(self):
        return self._pacman
    def setFood(self, object: Food):
        self.setGameObject(object)
        self._foods.append(object)
    def getFood(self):
        return self._foods
    def setMonster(self, object: Monster):
        self.setGameObject(object)
        self._monsters.append(object)
    def getMonster(self):
        return self._monsters
    def calculateStepScore(self):
        self._score += -1
    def calculateFoodScore(self):
        self._score += 20
    def endGame(self):
        if self._pacman:
            self._pacman._positions.clear()
            self._pacman._nextPosition = None
            self._pacman._curDirection = Direction.Unchanged
        if self._pacman in self._gameObjects:
            self._gameObjects.remove(self._pacman)
        self._pacman = None
    def display_text(self, text, position=(40, 0), size=25):
        font = pygame.font.SysFont("Arial", size)
        text_surface = font.render(text, True, (0, 0, 0))
        self._screen.blit(text_surface, position)
    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._isEnded = True
                pygame.quit()
                
        if self._pacman is None:
            return
    def start(self):
        while not self._isEnded:
            for object in self._gameObjects:
                object.move()
                object.draw()
                
            self.display_text(f"Score: {self._score}  Level: {self._level} Map: {self._mapNumber}")
            if self._pacman is None:
                font = pygame.font.SysFont("Helvetica", 100)
                text = font.render("LOSE", True, (255, 0, 0))
                text_rect = text.get_rect(center=(self._width / 2, self._height / 2))
                self._screen.blit(text, text_rect)
            if self.hasWon():
                font = pygame.font.SysFont("Helvetica", 100)
                text = font.render("WIN", True, (255, 0, 0))
                text_rect = text.get_rect(center=(self._width / 2, self._height / 2))
                self._screen.blit(text, text_rect)
            pygame.display.flip()
            self._clock.tick(390)
            self._screen.fill((0,0,0))
            self.handleEvent()
        print("Score:", self._score)