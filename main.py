import pygame


class StartScreen:
    def __init__(self):
        pygame.init()
        self.display_info = pygame.display.Info()
        self.screen = pygame.display.set_mode(
            size=(int(self.display_info.current_w * 1), int(self.display_info.current_h * 1)),
            flags=pygame.DOUBLEBUF | pygame.HWSURFACE
        )
        self.clock = pygame.time.Clock()
        self.player_name = ""
        self.current_score = -1

    def scale_width(self, width):
        return int(width * (self.screen.get_width() / 1280))

    def scale_height(self, height):
        return int(height * (self.screen.get_height() / 720))

    def open(self):
        font = pygame.font.Font("seguisym.ttf", self.scale_height(27))
        start_button = Button("start", pygame.font.Font('freesansbold.ttf', self.scale_height(15)),
                              self.scale_width(1040), self.scale_height(538), self.scale_width(133),
                              self.scale_height(67), self.launch_game,
                              self.player_name_not_entered)
        player_input_box = InputBox(self.scale_width(667), self.scale_height(550), self.scale_width(133),
                                    self.scale_height(43), pygame.font.Font(None, self.scale_height(40)), "",
                                    self.record_player)
        while True:

            # --- events ---

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_RETURN and not self.player_name_not_entered():
                        self.launch_game()

                # --- objects events ---

                start_button.handle_event(event)
                player_input_box.handle_event(event)

            # --- updates ---

            start_button.update()
            player_input_box.update()

            # --- draws ---

            self.screen.fill((255, 255, 255))

            instructions_x_position = self.scale_width(107)
            instructions_y_position = self.scale_height(443)
            instructions_line_spacing = self.scale_height(40)
            text = font.render("How to play:", True, (0, 0, 0))
            self.screen.blit(text, [instructions_x_position, instructions_y_position])
            text = font.render(" - use a/d or ←/→ to turn", True, (0, 0, 0))
            self.screen.blit(text, [instructions_x_position, instructions_y_position + instructions_line_spacing])
            text = font.render(" - use w/s or ↑/↓ to control speed", True, (0, 0, 0))
            self.screen.blit(text, [instructions_x_position, instructions_y_position + 2 * instructions_line_spacing])
            text = font.render(" - slow down to a stop to pause", True, (0, 0, 0))
            self.screen.blit(text, [instructions_x_position, instructions_y_position + 3 * instructions_line_spacing])
            text = font.render(" - use esc to exit", True, (0, 0, 0))
            self.screen.blit(text, [instructions_x_position, instructions_y_position + 4 * instructions_line_spacing])

            start_button.draw(self.screen)
            player_input_box.draw(self.screen)

            if self.current_score != -1:
                text = font.render("Your score was: " + str(self.current_score), True, (0, 0, 0))
                self.screen.blit(text, [self.scale_width(667), self.scale_height(493)])

            pygame.display.update()

    def launch_game(self):
        self.current_score = GameScreen(self.clock, self.screen, self.player_name).open()

    def record_player(self, name):
        self.player_name = name

    def player_name_not_entered(self):
        return len(self.player_name) == 0


class InputBox:

    def __init__(self, left, top, width, height, font, text='', callback=None):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(left, top, width, height)
        self.input_box_color_inactive = pygame.Color('lightskyblue3')
        self.input_box_color_active = pygame.Color('dodgerblue2')
        self.color = self.input_box_color_inactive
        self.font = font
        self.text = text
        self.callback = callback
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            self.active = self.rect.collidepoint(event.pos)

            # Change the current color of the input box.
            self.color = self.input_box_color_active if self.active else self.input_box_color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                if self.callback:
                    self.callback(self.text)
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.width, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + int(self.width / 26), self.rect.y + int(self.height / 8)))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Button:

    def __init__(self, text, font, x=0, y=0, width=100, height=50,
                 command=None, is_disabled=None):

        self.text = text
        self.command = command
        self.is_disabled = is_disabled

        self.image_normal = pygame.Surface((width, height))
        self.image_normal.fill((0, 153, 0))

        self.image_hovered = pygame.Surface((width, height))
        self.image_hovered.fill((79, 153, 69))

        self.image_disabled = pygame.Surface((width, height))
        self.image_disabled.fill((127, 127, 127))

        self.image = self.image_normal
        self.rect = self.image.get_rect()

        text_image = font.render(text, True, (255, 255, 255))
        text_rect = text_image.get_rect(center=self.rect.center)

        self.image_normal.blit(text_image, text_rect)
        self.image_hovered.blit(text_image, text_rect)
        self.image_disabled.blit(font.render(text, True, (191, 191, 191)), text_rect)

        # you can't use it before `blit`
        self.rect.topleft = (x, y)

        self.hovered = False

    def update(self):

        if self.is_disabled and self.is_disabled():
            self.image = self.image_disabled
        elif self.hovered:
            self.image = self.image_hovered
        else:
            self.image = self.image_normal

    def draw(self, surface):

        surface.blit(self.image, self.rect)

    def handle_event(self, event):

        if not (self.is_disabled and self.is_disabled()):
            if event.type == pygame.MOUSEMOTION:
                self.hovered = self.rect.collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.hovered:
                    if self.command:
                        self.command()


class GameScreen:
    def __init__(self, clock, screen, player_name):
        self.clock = clock
        self.screen = screen
        self.player_name = player_name
        self.score = 0

    def open(self):
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.score
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return self.score
            backround_image = pygame.image.load("backround_test.jpg")
            self.screen.blit(backround_image, backround_image.get_rect())
            pygame.display.update()


def main():
    StartScreen().open()


if __name__ == "__main__":
    main()
    pygame.quit()

