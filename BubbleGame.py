from distutils.command.check import check
from random import randint
import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((850, 650))
clock = pygame.time.Clock()

ball_WIDTH = 30
ball_HEIGHT = 30
row_space = 4
arrow_length = 150
left_edge = 20
right_edge = 600
top_edge = 20
bottom_edge = 550

def pick_a_color():
    colors = ['red', 'yellow', 'green', 'aqua', 'blue', 'magenta']
    return random.choice(colors)

class Ball(pygame.Rect):
    def __init__(self, x, y, color):
        super().__init__(x, y, ball_WIDTH, ball_HEIGHT)
        self.check_neighbors = None
        self.color = pick_a_color()
        self.vx = 0
        self.vy = 0
        self.is_moving = False

    def draw(self):
        pygame.draw.ellipse(screen, self.color, self, 0)
        pygame.draw.ellipse(screen, 'black', self, 1)

    def update(self):
        if self.is_moving:
            self.x += self.vx
            self.y += self.vy

            # Check for wall collisions (gray area)
            if self.left < 30 or self.right > screen.get_width() - 200:
                self.vx = -self.vx  # Reverse horizontal direction

    def __eq__(self, other):
        if isinstance(other, Ball):
            return self.x == other.x and self.y == other.y and self.color == other.color
        return False

    def __hash__(self):
        return hash((self.x, self.y, self.color))

    def neighbor_color(self):
        for b in balls:
            # Calculate the distance between the centers
            distance = math.sqrt((self.x + ball_WIDTH // 2 - (b.x + ball_WIDTH // 2)) ** 2 +
                                 (self.y + ball_HEIGHT // 2 - (b.y + ball_HEIGHT // 2)) ** 2)
            if distance < 40:  # Check within 40 pixels
                return b.color  # Return the color of the neighbor if found
        return None  # No neighbor found

    def has_neighbors(self):
        neighbors = [
            (-ball_WIDTH - row_space, 0),  # Left
            (ball_WIDTH + row_space, 0),  # Right
            (0, -ball_HEIGHT - row_space),  # Above
            (0, ball_HEIGHT + row_space),  # Below
            (-ball_WIDTH - row_space, ball_HEIGHT + row_space),  # Bottom-left
            (ball_WIDTH + row_space, ball_HEIGHT + row_space)  # Bottom-right
        ]

        for dx, dy in neighbors:
            neighbor_x = self.x + dx
            neighbor_y = self.y + dy

            for b in balls:
                if (abs(b.x - neighbor_x) < ball_WIDTH and
                        abs(b.y - neighbor_y) < ball_HEIGHT):
                    return True  # A neighboring ball is found

        return False  # No neighboring balls found

balls = []
for x in range(25, screen.get_width() - 250, ball_WIDTH + row_space):
    for y in range(25, (screen.get_height() - 100) // 2 + ball_HEIGHT, (ball_HEIGHT + row_space) * 2):
        balls.append(Ball(x, y, pick_a_color()))

for x in range(25 + ball_WIDTH // 2, screen.get_width() - 250, ball_WIDTH + row_space):
    for y in range(25 + ball_HEIGHT + row_space, (screen.get_height() - 100) // 2, (ball_HEIGHT + row_space) * 2):
        balls.append(Ball(x, y, pick_a_color()))

current = Ball((screen.get_width() - 250) // 2, screen.get_height() - 50, pick_a_color())

def draw_arrow(start, end):
    direction = (end[0] - start[0], end[1] - start[1])
    length = math.sqrt(direction[0] ** 2 + direction[1] ** 2)

    if length != 0:
        # Normalize the direction
        direction = (direction[0] / length, direction[1] / length)

    # Calculate the endpoint of the arrow based on the fixed length
    arrow_end = (start[0] + direction[0] * arrow_length, start[1] + direction[1] * arrow_length)

    # Draw the arrow line
    pygame.draw.line(screen, 'white', start, arrow_end, 2)

    # Drawing the arrowhead:
    angle = math.atan2(direction[1], direction[0])
    p1 = (arrow_end[0] - 10 * math.cos(angle - math.pi / 6),
          arrow_end[1] - 10 * math.sin(angle - math.pi / 6))
    p2 = (arrow_end[0] - 10 * math.cos(angle + math.pi / 6),
          arrow_end[1] - 10 * math.sin(angle + math.pi / 6))
    pygame.draw.polygon(screen, 'white', [arrow_end, p1, p2])

shooting_ball = None

def bubble_main():
    global shooting_ball  # Declare shooting_ball as a global variable
    global current  # Declare current as a global variable
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            # Check for the "E" key to exit the BubbleGame
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                return  # Exit the bubble_main function to return to the map

            elif event.type == pygame.MOUSEBUTTONDOWN and (shooting_ball is None):
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if the mouse click is within the gray area
                if left_edge < mouse_x < right_edge and top_edge < mouse_y < bottom_edge:
                    dx = mouse_x - (current.x + ball_WIDTH // 2)
                    dy = mouse_y - current.y

                    # Calculate angle and speed
                    angle = math.atan2(dy, dx)
                    shooting_ball = current  # Use the current ball for shooting
                    shooting_ball.vx = 10 * math.cos(angle)  # Adjust speed as necessary
                    shooting_ball.vy = 10 * math.sin(angle)
                    shooting_ball.is_moving = True  # Set the ball to moving state
                    current = Ball(current.x, current.y, pick_a_color())

        def find_target_position(ball):
            for b in balls:
                if abs(ball.x - b.x) <= ball_WIDTH and abs(ball.y - b.y) <= ball_HEIGHT:
                    # Calculate target position based on proximity to another ball
                    offset_x = (ball_WIDTH + row_space) // 2 * (-1 if ball.x < b.x else 1)
                    offset_y = (ball_HEIGHT + row_space) * (-1 if ball.y < b.y else 1)

                    # Ensure target position is within bounds
                    target_x = max(left_edge, min(b.x + offset_x, right_edge - ball_WIDTH))
                    target_y = max(top_edge, min(b.y + offset_y, bottom_edge - ball_HEIGHT))

                    return target_x, target_y

            return ball.x, ball.y  # Return original position if no nearby balls are found

        def check_neighbors(ball, connected_balls=None):
            if connected_balls is None:
                connected_balls = set()

            if ball in connected_balls:
                return

            target_color = shooting_ball.color
            connected_balls.add(ball)

            neighbors = [
                (-17, -34), (17, -34),  # Top-left, Top-right
                (-34, 0), (34, 0),  # Left, Right
                (-17, 34), (17, 34)  # Bottom-left, Bottom-right
            ]

            for dx, dy in neighbors:
                neighbor_x = ball.x + dx
                neighbor_y = ball.y + dy

                for b in balls:
                    if abs(b.x - neighbor_x) <= ball_WIDTH and abs(b.y - neighbor_y) <= ball_HEIGHT:
                        if b.color == target_color:
                            check_neighbors(b, connected_balls)  # Recursively check neighbors

            if len(connected_balls) > 2:
                for b in connected_balls:
                    if b in balls:
                        balls.remove(b)

        # Update and handle collision for shooting ball
        if shooting_ball:
            shooting_ball.update()

            for b in balls:
                if shooting_ball.colliderect(b):
                    # Freeze the shooting ball and find its target position
                    shooting_ball.is_moving = False
                    shooting_ball.x, shooting_ball.y = find_target_position(shooting_ball)

                    # Add to the balls list
                    balls.append(shooting_ball)  # Add to the balls list
                    check_neighbors(shooting_ball, connected_balls=None)  # Check for matching neighbors
                    shooting_ball = None  # Reset reference
                    break  # Exit loop after the first collision

        balls_to_remove = []
        for x in balls:
            if not x.has_neighbors():
                balls_to_remove.append(x)

        for b in balls_to_remove:
            balls.remove(b)

        screen.fill('purple')
        pygame.draw.rect(screen, 'gray', pygame.Rect(left_edge, top_edge, right_edge, bottom_edge))


        current.draw()
        if shooting_ball:
            shooting_ball.draw()
        for b in balls:
            b.draw()

        draw_arrow((current.x + ball_WIDTH // 2, current.y), pygame.mouse.get_pos())

        # Draw the exit instruction note
        font = pygame.font.Font(None, 36)
        text_surface = font.render('Press "e" twice to exit', True, 'black')
        screen.blit(text_surface, (500, 600))

        pygame.display.flip()
        clock.tick(60)