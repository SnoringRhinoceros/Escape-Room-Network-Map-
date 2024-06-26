import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Submit delay
submit_delay = 10000  # milliseconds
code = "1345"
imgPath = ""


# Screen dimensions
screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Drag and Drop Text")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BORDER_COLOR = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 36)
unlocked_font = pygame.font.SysFont(None, 72)


class Box:
    def __init__(self, text, rect):
        self.text = text
        self.rect = rect
        self.assigned_text = None
        self.correct = None  # None means unchecked, True means correct, False means incorrect

    def draw(self, surface):
        pygame.draw.rect(surface, BORDER_COLOR, self.rect, 3)
        pygame.draw.rect(surface, GRAY, self.rect)
        if self.assigned_text:
            text_surface = font.render(self.assigned_text, True, BLACK)
            surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))
        if self.correct is not None:
            mark_surface = font.render("Y" if self.correct else "N", True, GREEN if self.correct else RED)
            surface.blit(mark_surface, (self.rect.right + 10, self.rect.centery - mark_surface.get_height() // 2))

class DraggableText:
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.rect = font.render(text, True, BLACK).get_rect(topleft=pos)
        self.assigned_box = None

    def draw(self, surface):
        text_surface = font.render(self.text, True, BLACK)
        surface.blit(text_surface, self.pos)

    def update_position(self, new_pos):
        # Ensure the text does not go off the screen
        max_x = screen_width - self.rect.width
        max_y = screen_height - self.rect.height
        self.pos = (max(0, min(new_pos[0], max_x)), max(0, min(new_pos[1], max_y)))
        self.rect.topleft = self.pos

def main():
    texts = ["Internet", "Internet Edge", "Security Edge", "Network Core", "Application Edge", "Wireless Network", "Printer", "Tablet"]
    
    # Load images
    imgs = [pygame.image.load(imgPath + x + ".png") for x in texts]

    # Relative positions and sizes of the boxes based on screen dimensions
    boxes = [
        Box(texts[0], pygame.Rect((500, 29), (screen_width * 0.22, screen_height * 0.04))),
        Box(texts[1], pygame.Rect((480, 221), (screen_width * 0.22, screen_height * 0.04))),
        Box(texts[2], pygame.Rect((328, screen_height * 0.359), (screen_width * 0.22, screen_height * 0.04))),
        Box(texts[3], pygame.Rect((700, screen_height * 0.359), (screen_width * 0.22, screen_height * 0.04))),
        Box(texts[4], pygame.Rect((screen_width * 0.012, screen_height * 0.61), (screen_width * 0.22, screen_height * 0.04))),
        Box(texts[5], pygame.Rect((screen_width * 0.46, 468), (screen_width * 0.22, screen_height * 0.04))),
        Box(texts[6], pygame.Rect((750, 468), (screen_width * 0.22, screen_height * 0.04))),
        Box(texts[7], pygame.Rect((760, 700), (screen_width * 0.22, screen_height * 0.04)))
    ]
    
    random.shuffle(texts)
    draggable_texts = [DraggableText(text, (screen_width * 0.05, screen_height * (0.05 + i * 0.07))) for i, text in enumerate(texts)]

    # Relative position of the submit button based on screen dimensions
    submit_button_rect = pygame.Rect(screen_width * 0.05, screen_height * 0.93, screen_width * 0.2, screen_height * 0.05)
    last_submit_time = -submit_delay

    dragging_text = None
    dragging_offset = (0, 0)
    unlocked = False

    def check_correctness():
        all_correct = True
        for box in boxes:
            if box.assigned_text == box.text:
                box.correct = True
            else:
                box.correct = False
                all_correct = False
        return all_correct

    def draw_screen():
        if unlocked:
            screen.fill(BLACK)
            unlocked_text_surface = unlocked_font.render("Unlocked! Your code is: " + code, True, GREEN)
            screen.blit(unlocked_text_surface, (screen_width // 2 - unlocked_text_surface.get_width() // 2, screen_height // 2 - unlocked_text_surface.get_height() // 2))
        else:
            screen.fill(WHITE)
            screen.blit(imgs[0], (524, 8))
            screen.blit(imgs[1], (519, 138))
            screen.blit(imgs[2], (353, 316))
            screen.blit(imgs[3], (718, 310))
            screen.blit(imgs[4], (11, 504))
            screen.blit(imgs[5], (500, 504))
            screen.blit(imgs[6], (800, 504))
            screen.blit(imgs[7], (640, 620))
            
            for box in boxes:
                box.draw(screen)
            for draggable in draggable_texts:
                if not draggable.assigned_box:
                    draggable.draw(screen)
            pygame.draw.rect(screen, BORDER_COLOR, submit_button_rect, 3)
            pygame.draw.rect(screen, GRAY, submit_button_rect)
            submit_text_surface = font.render("Submit", True, BLACK)
            screen.blit(submit_text_surface, (submit_button_rect.x + 10, submit_button_rect.y + 10))

            # Calculate and draw the time left
            current_time = pygame.time.get_ticks()
            time_left = max((submit_delay - (current_time - last_submit_time)) // 1000, 0)
            text_surface = font.render(f"Wait {time_left} sec", True, BLACK)
            screen.blit(text_surface, (screen_width * 0.252, screen_height * 0.942))
        
        pygame.display.update()

    running = True
    while running:
        # print(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                current_time = pygame.time.get_ticks()
                if submit_button_rect.collidepoint(pos) and current_time - last_submit_time >= submit_delay:
                    if check_correctness():
                        unlocked = True
                    last_submit_time = current_time
                else:
                    for draggable in draggable_texts:
                        if draggable.rect.collidepoint(pos):
                            dragging_text = draggable
                            dragging_offset = (draggable.rect.x - pos[0], draggable.rect.y - pos[1])
                            if draggable.assigned_box:
                                draggable.assigned_box.assigned_text = None
                                draggable.assigned_box = None
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_text:
                    pos = pygame.mouse.get_pos()
                    for box in boxes:
                        if box.rect.collidepoint(pos) and box.assigned_text is None:
                            box.assigned_text = dragging_text.text
                            dragging_text.update_position((box.rect.x + 10, box.rect.y + 10))
                            dragging_text.assigned_box = box
                            break
                    dragging_text = None
            elif event.type == pygame.MOUSEMOTION and dragging_text:
                pos = pygame.mouse.get_pos()
                new_pos = (pos[0] + dragging_offset[0], pos[1] + dragging_offset[1])
                dragging_text.update_position(new_pos)

        draw_screen()

if __name__ == "__main__":
    main()
