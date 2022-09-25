from collections import namedtuple
from contextlib import nullcontext
from enum import Enum
import pygame
import random
import time
import numpy as np
import math

Point = namedtuple('Point','x,y')

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Snake:
    SNAKE_BLOCK = 10
    SNAKE_BLOCK = 10
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    def __init__(self):
        self.grid_size = 40
        self.screen_size = 400
        self.grid = np.zeros((40,40),dtype=np.int32)
        self.clock =  pygame.time.Clock()
        self.reset()
        pygame.init()
        self.screen = pygame.display.set_mode([(self.grid_size*self.SNAKE_BLOCK)+300, (self.grid_size*self.SNAKE_BLOCK)])
        self.surface = pygame.display.set_mode((700,400))
    
    def reset(self):
        self.direction = Direction.RIGHT
        self.snake = [Point(random.randint(0,self.grid_size-1),random.randint(0,self.grid_size-1))]
        self.score = 0
        self.food = self.get_random_food_position()
        self.frame_iter = 0
    
    def get_random_food_position(self):
        
        rand = Point(random.randint(0,self.grid_size-1),random.randint(0,self.grid_size-1))
        if(rand in self.snake):
            return self.get_random_food_position()
        return rand
            
    def reset_grid(self):
        return np.zeros((40,40),dtype=np.int32)
    
    
    # Action
        # [1,0,0] -> Straight
        # [0,1,0] -> Right Turn 
        # [0,0,1] -> Left Turn
    def move(self,action):
        cur_dir = self.direction
        clock_dir = [Direction.RIGHT, Direction.DOWN,  Direction.LEFT,Direction.UP]
        cur_idx = clock_dir.index(cur_dir)
        new_idx = 0
        if(np.array_equal(action,[1,0,0])):
            new_idx = cur_idx
        elif(np.array_equal(action,[0,1,0])):
            new_idx = (cur_idx+1)%4
        else:
            new_idx = (cur_idx-1)%4
        new_dir = clock_dir[new_idx]
        self.direction = new_dir
        cur_head = self.snake[0]
        x = cur_head.x
        y = cur_head.y
        if(new_dir == Direction.RIGHT):
            x+=1
        elif(new_dir == Direction.LEFT):
            x-=1
        elif(new_dir == Direction.UP):
            y-=1
        else:
            y+=1
        
        self.new_head = Point(x,y)
        
    
    def insert_head(self):
        self.snake.insert(0,self.new_head)
        self.new_head = None
        
    
    def is_collision(self,pt=None):
        if(pt == None):
            head = self.snake[0]
        else:
            head = pt
        
        
        # Checking borders
        if(head.x >=self.grid_size):
            return True
        if(head.x < 0):
            return True
        if(head.y >=self.grid_size):
            return True
        if(head.y < 0):
            return True
        # Check if the snake trying to eat itself
        if(head in self.snake[1:]):
            return True

        return False


    def take_action(self, action,epochs=0):
        self.frame_iter+=1
        # 1. Collect the user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        # 2. Move
        self.move(action)
        self.insert_head()
        # 3. Check if game Over
        reward = 0  # eat food: +10 , game over: -10 , else: 0
        game_over = False 
        if(self.is_collision() or self.frame_iter > 100*len(self.snake) ):
            game_over=True
            reward = -10
            return reward,game_over,self.score
        # 4. Place new Food or just move
        if(self.food == self.snake[0]):
            self.score+=1
            reward = 10
            self.food  =  self.get_random_food_position()
        else:
            self.snake.pop()
        # 5. Update UI and clock
        
        self.render_ui(epochs)
        return reward,game_over,self.score

    def display_score(self,color):
        font_style = pygame.font.SysFont(None, 50)
        msg = font_style.render("SCORE:"+str(self.score), True, color)
        self.surface.blit(msg, [self.screen_size+10, 100])
    
    def message(self,msg,color):
        font_style = pygame.font.SysFont(None, 50)
        msg = font_style.render(msg, True, color)
        self.surface.blit(msg, [self.screen_size+100, self.screen_size/2])

    def stop_game(self):
        self.message("YOU LOST!!!",self.RED)
        self.display_score(self.RED)
        pygame.display.update()
        #time.sleep(5)
        #pygame.quit()

    def render_ui(self,epochs):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, self.WHITE, [self.screen_size,0,1, self.screen_size+1])
        for i in range(len(self.snake)):
            if(i == 0):
               pygame.draw.rect(self.surface, self.WHITE, pygame.Rect([self.snake[i].x*self.SNAKE_BLOCK,self.snake[i].y*self.SNAKE_BLOCK,10,10]))
            else:
                pygame.draw.rect(self.surface, self.RED, pygame.Rect([self.snake[i].x*self.SNAKE_BLOCK,self.snake[i].y*self.SNAKE_BLOCK,10,10]))
        pygame.draw.rect(self.surface, self.GREEN, pygame.Rect([self.food.x*self.SNAKE_BLOCK,self.food.y*self.SNAKE_BLOCK,10,10]))
        self.display_score(self.RED)
        self.message("Epochs:"+str(epochs),self.GREEN)
        pygame.display.update()
        self.clock.tick(15)

if __name__=="__main__":
    s = Snake()
    s.render_ui()
    print(s.snake[0].x,s.snake[0].y)
     # [1,0,0] -> Straight
        # [0,1,0] -> Right Turn 
        # [0,0,1] -> Left Turn
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    s.take_action([0,0,1])
                elif event.key == pygame.K_RIGHT :
                    s.take_action([0,1,0])
                elif event.key == pygame.K_UP:
                    s.take_action([1,0,0])
                
    
            



