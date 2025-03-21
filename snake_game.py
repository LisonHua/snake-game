import pygame
import random
import sys
import os

# 初始化 Pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 设置游戏窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20
BASE_SPEED = 5  # 降低基础速度
MAX_SPEED = 25   # 最大速度
SPEED_INCREMENT = 0.5  # 每增加一个长度增加的速度

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('贪吃蛇游戏')

# 初始化时钟
clock = pygame.time.Clock()

# 设置字体
def get_font(size):
    # 尝试使用系统中文字体
    system_fonts = [
        "Microsoft YaHei",  # Windows
        "PingFang SC",     # macOS
        "WenQuanYi Micro Hei",  # Linux
        "SimHei",         # Windows
        "SimSun",         # Windows
        "NSimSun",        # Windows
        "FangSong",       # Windows
        "KaiTi"           # Windows
    ]
    
    for font_name in system_fonts:
        try:
            return pygame.font.SysFont(font_name, size)
        except:
            continue
    
    # 如果找不到中文字体，使用默认字体
    return pygame.font.Font(None, size)

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = get_font(36)
        self.is_hovered = False

    def draw(self, surface):
        color = (min(self.color[0] + 30, 255), min(self.color[1] + 30, 255), min(self.color[2] + 30, 255)) if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        self.speed = BASE_SPEED
        self.is_alive = True

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new_x = cur[0] + (x*BLOCK_SIZE)
        new_y = cur[1] + (y*BLOCK_SIZE)
        
        # 检查是否撞到边界
        if (new_x < 0 or new_x >= WINDOW_WIDTH or 
            new_y < 0 or new_y >= WINDOW_HEIGHT):
            self.is_alive = False
            return False
            
        new = (new_x, new_y)
        if new in self.positions[3:]:
            self.is_alive = False
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

    def reset(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.speed = BASE_SPEED
        self.is_alive = True

    def render(self):
        for p in self.positions:
            pygame.draw.rect(screen, self.color, (p[0], p[1], BLOCK_SIZE, BLOCK_SIZE))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WINDOW_WIDTH-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE,
                        random.randint(0, (WINDOW_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE)

    def render(self):
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

# 定义方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def show_game_over(screen, score):
    font = get_font(74)
    text = font.render(f'游戏结束! 得分: {score}', True, WHITE)
    text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)  # 等待2秒

def show_start_screen():
    start_button = Button(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 - 25, 200, 50, "开始游戏", BLUE)
    title_font = get_font(74)
    title_text = title_font.render("贪吃蛇游戏", True, WHITE)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/4))

    while True:
        screen.fill(BLACK)
        screen.blit(title_text, title_rect)
        start_button.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if start_button.handle_event(event):
                return True

def main():
    while True:
        if not show_start_screen():
            break

        snake = Snake()
        food = Food()
        font = get_font(36)

        while snake.is_alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == pygame.K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT

            # 更新蛇的位置
            if not snake.update():
                show_game_over(screen, snake.score)
                break

            # 检查是否吃到食物
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                # 增加速度，但不超过最大速度
                snake.speed = min(BASE_SPEED + (snake.length - 1) * SPEED_INCREMENT, MAX_SPEED)
                food.randomize_position()

            # 绘制游戏界面
            screen.fill(BLACK)
            snake.render()
            food.render()
            
            # 显示分数和速度
            score_text = font.render(f'得分: {snake.score}', True, WHITE)
            speed_text = font.render(f'速度: {int(snake.speed)}', True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(speed_text, (10, 50))

            pygame.display.update()
            clock.tick(snake.speed)

if __name__ == '__main__':
    main() 