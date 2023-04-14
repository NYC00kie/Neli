import pygame


class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text: str,  pos: list, font: int, commonmemdict, bg="black", feedback=""):
        self.commonmemdict = commonmemdict
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)

    def change_text(self, text: str, bg="black"):
        """Change the text whe you click"""
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(
            self.x-0.5*self.size[0], self.y, self.size[0], self.size[1])

    def show(self, screen):
        screen.blit(self.surface, (self.x-(0.5*self.size[0]), self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.change_text(self.feedback, bg="red")
                    # do smth
                    self.commonmemdict["pressed_uno"] = True

    def hover(self, screen):
        # do nothing on hover
        pass


class Buetton:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text: str,  pos: list, font: int, assignedfunc: object, bg="black", feedback=""):
        self.bg = bg
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        self.assignedfunc = assignedfunc
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)

    def change_text(self, text: str, bg="black"):
        """Change the text whe you click"""
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        print(self.size)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(
            self.x-0.5*self.size[0], self.y, self.size[0], self.size[1])

    def show(self, screen):
        screen.blit(self.surface, (self.x-(0.5*self.size[0]), self.y))

    def click(self, event, pygame):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.change_text(self.feedback, bg=self.bg)
                    self.assignedfunc()

    def hover(self, screen):
        pass
