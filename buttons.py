import pygame

# button class inherite from the block class the check_clicked and draw functions
# buttons are used to create the text box for the game windows
# buttons are used to create the text box to display info

class Button():
    def __init__(self, x_pos, y_pos, width, height, color, label, text_color, font_size):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.label = label
        self.text_color = text_color
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x_pos, self.y_pos,self.width, self.height)
        self.font = pygame.font.SysFont('ebrima', font_size)
        self.text = self.font.render(self.label, True, self.text_color)

    # draw used to draw the block
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text, (self.x_pos, self.y_pos))

    # check_clicked checks if the mouse click was on the block
    def check_clicked(self, x_clicked, y_clicked):
        if(x_clicked >= self.x_pos
                and x_clicked < self.x_pos + self.width
                and y_clicked >= self.y_pos
                and y_clicked < self.y_pos + self.height):
            return True
