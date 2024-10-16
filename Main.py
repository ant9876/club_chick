import os
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 800))

clock = pygame.time.Clock()

master_list = []
house_list = []
is_touching = False
first_draw = True
game_state = "map"  # Game state to track what screen you're on
entered_game = False  # Flag to track if we entered the game screen
space_pressed = False  # Flag to track if the space bar is pressed

# Load assets
chick_left = os.path.expanduser("chick_left.png")
chick_right = os.path.expanduser("chick_right.png")
chick_front = os.path.expanduser("chick_front.png")
chick_back = os.path.expanduser("chick_back.png")
tree_one = os.path.expanduser("tree_one.png")
bush_one = os.path.expanduser("bush_one.png")


class Player(pygame.Rect):
    def __init__(self, image_path1, image_path2, image_path3, image_path4):
        super().__init__(325, 325, 20, 20)
        self.image1 = pygame.image.load(image_path1)
        self.image2 = pygame.image.load(image_path2)
        self.image3 = pygame.image.load(image_path3)
        self.image4 = pygame.image.load(image_path4)
        self.current_image = self.image1

    def draw(self):
        screen.blit(self.current_image, (self.x, self.y))


class Object(pygame.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.vx = 0
        self.vy = 0

    def update(self):
        self.x += self.vx
        self.y += self.vy


class Tree(Object):
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path)
        super().__init__(x, y, self.image.get_width(), self.image.get_height())

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Bush(Object):
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path)
        super().__init__(x, y, self.image.get_width(), self.image.get_height())

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class House(Object):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height)
        self.image = pygame.image.load(image_path)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x + 133, self.y + 188, 35, 51)


player = Player(chick_front, chick_back, chick_right, chick_left)

# Add objects to master list
master_list.append(Tree(500, 300, tree_one))
master_list.append(Tree(-50, 300, tree_one))

house_1 = os.path.expanduser("house1.png")
house_list.append(House(300, 200, 300, 300, house_1))

for i in range(0, 40):
    master_list.append(Bush(-600 + i * 110, 900, bush_one))

show_popup = None  # Flag to indicate if the pop-up should be shown

def show_collision_popup():
    if is_touching:
        popup_width, popup_height = 250, 150
        popup_rect = pygame.Rect(screen.get_width()/2 - popup_width/2, screen.get_height()/2 - popup_height/2, popup_width, popup_height)

        popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        popup_surface.fill((200, 200, 200, 200))  # Light gray with 50% opacity

        screen.blit(popup_surface, popup_rect.topleft)

        font = pygame.font.SysFont('Courier New', 24)
        text1_surface = font.render("Welcome to:", True, (0, 0, 0))
        text2_surface = font.render("House!", True, (0, 0, 0))
        text3_surface = font.render("Type 'A' if you", True, (0, 0, 0))
        text4_surface = font.render("wish to enter.", True, (0, 0, 0))

        text1_rect = text1_surface.get_rect(center=(popup_rect.centerx, popup_rect.centery - 50))
        text2_rect = text2_surface.get_rect(center=(popup_rect.centerx, popup_rect.centery - 20))
        text3_rect = text3_surface.get_rect(center=(popup_rect.centerx, popup_rect.centery + 10))
        text4_rect = text4_surface.get_rect(center=(popup_rect.centerx, popup_rect.centery + 40))

        screen.blit(text1_surface, text1_rect)
        screen.blit(text2_surface, text2_rect)
        screen.blit(text3_surface, text3_rect)
        screen.blit(text4_surface, text4_rect)


# Function to stop the player's movement
def stop_movement():
    for obj in master_list:
        obj.vx = 0
        obj.vy = 0
    for house in house_list:
        house.vx = 0
        house.vy = 0

# Function to show the game screen text
def show_game_screen():
    font = pygame.font.SysFont('Courier New', 20)
    text_surface = font.render("Welcome to house game! Press 'space' continue or 'e' to exit.", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
    screen.blit(text_surface, text_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if game_state == "map":
                if event.key == pygame.K_LEFT:
                    player.current_image = player.image4
                    for obj in master_list:
                        obj.vx = 3
                    for house in house_list:
                        house.vx = 3

                elif event.key == pygame.K_RIGHT:
                    player.current_image = player.image3
                    for obj in master_list:
                        obj.vx = -3
                    for house in house_list:
                        house.vx = -3

                elif event.key == pygame.K_UP:
                    player.current_image = player.image2
                    for obj in master_list:
                        obj.vy = 3
                    for house in house_list:
                        house.vy = 3

                elif event.key == pygame.K_DOWN:
                    player.current_image = player.image1
                    for obj in master_list:
                        obj.vy = -3
                    for house in house_list:
                        house.vy = -3

                elif event.key == pygame.K_a and is_touching:
                    game_state = "blank"  # Enter the blank screen if 'A' is pressed when touching the door
                    entered_game = True  # Mark that we've entered the game
                    space_pressed = False  # Reset the space bar flag when entering the game

            elif game_state == "blank":
                if event.key == pygame.K_e:
                    game_state = "map"  # Return to the original map if 'E' is pressed
                    entered_game = False  # Reset the flag when exiting
                elif event.key == pygame.K_SPACE:
                    space_pressed = True  # Mark that the space bar has been pressed

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                stop_movement()  # Stop movement when arrow keys are released

    if game_state == "map":
        inside_rect = pygame.Rect(player.x + player.width // 4 + 64, player.y + player.height // 4 + 56, player.width // 2, player.height // 2)
        is_touching = False  # Reset the flag at the start of each frame

        for obj in master_list:
            obj.update()
        for house in house_list:
            house.update()

        for house in house_list:
            door_rect = house.get_rect()
            if door_rect.colliderect(inside_rect):
                is_touching = True
                show_popup = (player.x, player.y)
            else:
                show_popup = None

        screen.fill((123, 191, 98))

        for house in house_list:
            house.draw()
        player.draw()
        for obj in master_list:
            obj.draw()

        if show_popup:
            show_collision_popup()

    elif game_state == "blank":
        screen.fill((255, 255, 255))  # Blank white screen
        if entered_game and not space_pressed:
            show_game_screen()  # Display welcome text if space is not yet pressed

    pygame.display.update()
    clock.tick(30)
