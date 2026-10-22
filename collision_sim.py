import pygame
import sys

# 初始化 Pygame
pygame.init()

# 窗口设置
WIDTH, HEIGHT = 900, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("完全弹性碰撞动画演示 (习题 2-37)")
clock = pygame.time.Clock()
FPS = 60

# 颜色定义
BG_COLOR = (240, 248, 255)  # 浅蓝色背景
TRACK_COLOR = (100, 100, 100) # 轨道颜色
COLORS = [(255, 99, 71), (60, 179, 113), (65, 105, 225), (255, 165, 0)] # 四个球的颜色
TEXT_COLOR = (0, 0, 0)

# 字体
font = pygame.font.SysFont('simhei', 24)

class Ball:
    def __init__(self, x, mass, radius, color, label, velocity=0):
        self.x = x
        self.v = velocity
        self.m = mass
        self.r = radius
        self.color = color
        self.label = label

    def update(self, dt):
        self.x += self.v * dt

    def draw(self, surface):
        # 绘制小球
        pygame.draw.circle(surface, self.color, (int(self.x), HEIGHT//2), self.r)
        pygame.draw.circle(surface, (0, 0, 0), (int(self.x), HEIGHT//2), self.r, 2) # 黑色边框
        
        # 绘制质量标签
        text = font.render(self.label, True, TEXT_COLOR)
        text_rect = text.get_rect(center=(int(self.x), HEIGHT//2))
        surface.blit(text, text_rect)

        # 绘制速度矢量线 (如果速度不为0)
        if abs(self.v) > 0.1:
            start_pos = (int(self.x + self.r), HEIGHT//2 - 40)
            end_pos = (int(self.x + self.r + self.v * 0.1), HEIGHT//2 - 40) # 缩放速度向量
            pygame.draw.line(surface, (255, 0, 0), start_pos, end_pos, 4)
            # 绘制箭头
            if self.v > 0:
                pygame.draw.polygon(surface, (255, 0, 0), [(end_pos[0], end_pos[1]), (end_pos[0]-10, end_pos[1]-5), (end_pos[0]-10, end_pos[1]+5)])
            else:
                pygame.draw.polygon(surface, (255, 0, 0), [(end_pos[0], end_pos[1]), (end_pos[0]+10, end_pos[1]-5), (end_pos[0]+10, end_pos[1]+5)])

# 参数设置
m = 1.0       # 基础质量
v0 = 150.0    # 初始速度 (像素/秒)
radius = 30   # 小球半径

# 初始化四个球 (从左到右: 2m, 2m, m, m)
# 为了动画效果明显，初始位置设定为刚好接触
b1 = Ball(x=200, mass=2*m, radius=radius, color=COLORS[0], label="2m", velocity=v0)
b2 = Ball(x=200+2*radius, mass=2*m, radius=radius, color=COLORS[1], label="2m", velocity=0)
b3 = Ball(x=200+4*radius, mass=m, radius=radius, color=COLORS[2], label="m", velocity=0)
b4 = Ball(x=200+6*radius, mass=m, radius=radius, color=COLORS[3], label="m", velocity=0)

balls = [b1, b2, b3, b4]

def resolve_collision(ball1, ball2):
    # 检查是否碰撞 (距离小于等于半径之和，且正在靠近)
    if ball1.x + ball1.r >= ball2.x - ball2.r and ball1.v > ball2.v:
        m1, m2 = ball1.m, ball2.m
        u1, u2 = ball1.v, ball2.v
        
        # 一维完全弹性碰撞速度公式
        v1 = ((m1 - m2) * u1 + 2 * m2 * u2) / (m1 + m2)
        v2 = ((m2 - m1) * u2 + 2 * m1 * u1) / (m1 + m2)
        
        ball1.v = v1
        ball2.v = v2

        # 微调位置避免卡在边界导致连续碰撞
        overlap = (ball1.x + ball1.r) - (ball2.x - ball2.r)
        if overlap > 0:
            ball1.x -= 0.5
            ball2.x += 0.5

# 主循环
running = True
dt = 1.0 / FPS

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # 按 R 键重置
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            b1.x, b1.v = 200, v0
            b2.x, b2.v = 200+2*radius, 0
            b3.x, b3.v = 200+4*radius, 0
            b4.x, b4.v = 200+6*radius, 0

    # 更新物理状态
    for ball in balls:
        ball.update(dt)

    # 检查碰撞
    resolve_collision(b1, b2)
    resolve_collision(b2, b3)
    resolve_collision(b3, b4)

    # 绘制画面
    screen.fill(BG_COLOR)
    
    # 绘制地面/光滑水平面
    pygame.draw.line(screen, TRACK_COLOR, (0, HEIGHT//2 + radius), (WIDTH, HEIGHT//2 + radius), 5)
    
    # 绘制小球
    for ball in balls:
        ball.draw(screen)

    # 绘制提示信息
    info_text = font.render("按 'R' 键重置动画", True, (100, 100, 100))
    screen.blit(info_text, (20, 20))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
