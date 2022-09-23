import pygame
import random
import time


from pygame.locals import (

    K_UP,

    K_DOWN,

    K_LEFT,

    K_RIGHT,

    K_ESCAPE,

    KEYDOWN,

    QUIT,

)

class snake:
    SNAKE_BLOCK = 10
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    def __init__(self,height,width):
        self.screen_height = height
        self.screen_width = width
        self.snake_pos_x = [200]
        self.snake_pos_y = [150]
        self.food_x, self.food_y =  self.get_random_food_position()
        self.score = 0
        pygame.init()
        self.screen = pygame.display.set_mode([self.screen_height+300, self.screen_width])
        self.surface = pygame.display.set_mode((700,400))



    def get_random_food_position(self):
        while True:
            rand_x = random.randint(0,(self.screen_height-self.SNAKE_BLOCK)/self.SNAKE_BLOCK) * self.SNAKE_BLOCK
            rand_y = random.randint(0,(self.screen_width-self.SNAKE_BLOCK)/self.SNAKE_BLOCK) * self.SNAKE_BLOCK
            flag = False
            for i in range(len(self.snake_pos_x)):
                if(rand_x == self.snake_pos_x[i] and rand_y == self.snake_pos_y[i]):
                    flag=True
                    break
            if(~flag):
                return rand_x,rand_y

    
    def add_length(self,x1_change,y1_change):
        snake_pos_x = self.snake_pos_x
        snake_pos_y = self.snake_pos_y
        if(x1_change == -self.SNAKE_BLOCK):
            snake_pos_x.append(snake_pos_x[-1]+self.SNAKE_BLOCK)
            snake_pos_y.append(snake_pos_y[-1])
        elif(x1_change == self.SNAKE_BLOCK):
            snake_pos_x.append(snake_pos_x[-1]-self.SNAKE_BLOCK)
            snake_pos_y.append(snake_pos_y[-1])
        elif(y1_change == -self.SNAKE_BLOCK):
            snake_pos_x.append(snake_pos_x[-1])
            snake_pos_y.append(snake_pos_y[-1]+self.SNAKE_BLOCK)
        elif(y1_change == self.SNAKE_BLOCK):
            snake_pos_x.append(snake_pos_x[-1])
            snake_pos_y.append(snake_pos_y[-1]-self.SNAKE_BLOCK)
        return snake_pos_x, snake_pos_y
    
    def gameover_check(self,snake_pos_x, snake_pos_y):
        '''
        This is to check if the snake game is game over by checking if it touched the border or its tail
        '''
        head_x = snake_pos_x[0]
        head_y = snake_pos_y[0]
        # Checking borders
        if(head_x >=self.screen_width):
            return True
        if(head_x <= -self.SNAKE_BLOCK):
            return True
        if(head_y >= self.screen_height):
            return True
        if(head_y <= -self.SNAKE_BLOCK):
            return True
        # Check if the snake trying to eat itself
        for i in range(1,len(self.snake_pos_x)):
            if(head_x == self.snake_pos_x[i] and head_y == self.snake_pos_y[i]):
                return True
    
    def message(self,msg,color):
        font_style = pygame.font.SysFont(None, 50)
        msg = font_style.render(msg, True, color)
        self.surface.blit(msg, [self.screen_height+100, self.screen_width/2])

    def print_snake(self,x1_change, y1_change):
        prev_x = 0
        prev_y = 0
        for i in range(len(self.snake_pos_x)):
            if(i == 0):
                prev_x = self.snake_pos_x[i]
                prev_y = self.snake_pos_y[i]
                self.snake_pos_x[i] = self.snake_pos_x[i] + x1_change
                self.snake_pos_y[i] = self.snake_pos_y[i] + y1_change
            else:
                cur_x = self.snake_pos_x[i]
                cur_y = self.snake_pos_y[i]
                self.snake_pos_x[i] = prev_x
                self.snake_pos_y[i] = prev_y
                prev_x = cur_x
                prev_y = cur_y
            pygame.draw.rect(self.surface, self.RED, pygame.Rect([self.snake_pos_x[i],self.snake_pos_y[i],10,10]))
    
    def display_score(self,color):
        font_style = pygame.font.SysFont(None, 50)
        msg = font_style.render("SCORE:"+str(self.score), True, color)
        self.surface.blit(msg, [self.screen_height+10, 100])
    def run(self):
        
        running = True
        
        x1_change = 0
        y1_change = 0
        clock = pygame.time.Clock()
        game_over = False
        while running:

            self.screen.fill((0, 0, 0))
           #pygame.draw.rect(self.screen, self.WHITE, [400,0,5, 405])

           #pygame.draw.rect(self.screen, self.WHITE, [0,0,self.screen_width,1])
           #pygame.draw.rect(self.screen, self.WHITE, [0,self.screen_height,self.screen_width,1])
# left line
            #pygame.draw.rect(self.screen, self.WHITE, [0,0,1, self.screen_height])
# right line
            pygame.draw.rect(self.screen, self.WHITE, [self.screen_width,0,1, self.screen_height+1])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and x1_change != 10:
                        x1_change = -10
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT and x1_change != -10 :
                        x1_change = 10
                        y1_change = 0
                    elif event.key == pygame.K_UP and y1_change != 10:
                        x1_change = 0
                        y1_change = -10
                    elif event.key == pygame.K_DOWN and y1_change != -10:
                        x1_change = 0
                        y1_change = 10
            if(self.snake_pos_x[0] == self.food_x and self.snake_pos_y[0] == self.food_y):
                self.snake_pos_x, self.snake_pos_y = self.add_length(x1_change, y1_change)
                self.food_x,self.food_y = self.get_random_food_position()
                self.score+=1
            
            self.print_snake(x1_change,y1_change)
            if(self.gameover_check(self.snake_pos_x, self.snake_pos_y)):
                game_over = True
                break
            pygame.draw.rect(self.surface, self.GREEN, pygame.Rect([self.food_x,self.food_y,10,10]))
            self.display_score(self.RED)
            pygame.display.update()
            clock.tick(15)

        if(game_over):
            self.message("YOU LOST!!!",self.RED)
            self.display_score(self.RED)
            pygame.display.update()
            time.sleep(5)

    pygame.quit()
        
if __name__=="__main__":
    s = snake(400,400)
    s.run()