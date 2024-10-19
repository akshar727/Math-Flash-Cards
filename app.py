import pygame, sys, random, json, os, math, time, pyperclip

icon = pygame.image.load("assets/icon.png")

if not os.path.exists("assets/data.json"):
    with open('assets/data.json', 'w') as f:
        f.write('{"max":10,"op":["+","-"]}')

pygame.init()


if os.path.exists("assets/data.json"):
    try:
        with open('assets/data.json', 'r') as f:
            x = json.load(f)
    except:
        with open('assets/data.json', 'w') as f:
            f.write('{"max":10,"op":["+","-"]}')

pygame.display.set_icon(icon)
with open('assets/data.json', 'r') as f:
    r = json.load(f)

if r["max"] <= 0:
    r["max"] = 1


clock = pygame.time.Clock()


operations = r["op"]
_max = r["max"]
correct_answers = 0
correct_amt = r["corr_amt"]
correct_in_row = r["corr_row"]
bad_input = False
bad_zero = False

temp = r["op"]
question_screen = False
title_screen = False
started = False
ran_show = False
splash= True
viewed = False
ups = False
prev = ""
settings_screen_2 = False
play_button_delay = int(90*clock.tick(600))
splash_delay = int(450*clock.tick(600))
song_screen = False
next_question_button_delay = -1
ci = 0
ic = 0
added = False
playing = False
settings_screen = False
a = 0
b = 0
c = 0
d = 0
custom_title = ""
correct = ""
cor = None
downloading = False
num_a, num_b, op, ans, question_text, quesRect, question_up,= None, None, None, None, None, None, False

def save_data():
    r["op"] = temp
    r["max"] = _max
    with open('assets/data.json', 'w') as f:
        json.dump(r, f)



class PlayButton:
    def __init__(self, text, width, height, pos, elevation, top_color, bottom_color, clicked_color, font):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.font = font

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color
        self.top_color_1 = top_color

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = bottom_color

        # clicked color
        self.clicked_color = clicked_color
        # text
        self.text_surf = self.font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(win, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(win, self.top_color, self.top_rect, border_radius=12)
        win.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        global question_screen, title_screen
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.clicked_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    question_screen = True
                    title_screen = False
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.top_color_1


class SettingsButton:
    def __init__(self, text, width, height, pos, elevation, top_color, bottom_color, clicked_color, font):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.font = font

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color
        self.top_color_1 = top_color

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = bottom_color

        # clicked color
        self.clicked_color = clicked_color
        # text
        self.text_surf = self.font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(win, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(win, self.top_color, self.top_rect, border_radius=12)
        win.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        global settings_screen, title_screen
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.clicked_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    settings_screen = True
                    title_screen = False
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.top_color_1


class SettingNextPage:
    def __init__(self, text, width, height, pos, elevation, top_color, bottom_color, clicked_color, font):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.font = font

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color
        self.top_color_1 = top_color

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = bottom_color

        # clicked color
        self.clicked_color = clicked_color
        # text
        self.text_surf = self.font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(win, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(win, self.top_color, self.top_rect, border_radius=12)
        win.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        global settings_screen, title_screen, settings_screen_2
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.clicked_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    settings_screen = False
                    settings_screen_2 = True
                    title_screen = False
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.top_color_1


class BackButton:
    def __init__(self, text, width, height, pos, elevation, top_color, bottom_color, clicked_color, font):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.font = font

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color
        self.top_color_1 = top_color

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = bottom_color

        # clicked color
        self.clicked_color = clicked_color
        # text
        self.text_surf = self.font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(win, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(win, self.top_color, self.top_rect, border_radius=12)
        win.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        global settings_screen, title_screen, question_screen, play_button_delay, playing, settings_screen_2
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.clicked_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    settings_screen = False
                    question_screen = False
                    play_button_delay = 0
                    settings_screen_2 = False
                    title_screen = True
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.top_color_1


class BackButton1:
    def __init__(self, text, width, height, pos, elevation, top_color, bottom_color, clicked_color, font):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.font = font

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color
        self.top_color_1 = top_color

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = bottom_color

        # clicked color
        self.clicked_color = clicked_color
        # text
        self.text_surf = self.font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(win, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(win, self.top_color, self.top_rect, border_radius=12)
        win.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        global settings_screen, title_screen, question_screen, play_button_delay, playing, settings_screen_2, question_up
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.clicked_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    settings_screen = True
                    question_screen = False
                    question_up = False
                    play_button_delay = 0
                    settings_screen_2 = False
                    title_screen = False
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.top_color_1


class ExitButton:
    def __init__(self, text, width, height, pos, elevation, top_color, bottom_color, clicked_color, font):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.font = font

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color
        self.top_color_1 = top_color

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = bottom_color

        # clicked color
        self.clicked_color = clicked_color
        # text
        self.text_surf = self.font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(win, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(win, self.top_color, self.top_rect, border_radius=12)
        win.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        global question_screen, title_screen
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.clicked_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    pygame.quit()
                    sys.exit()
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.top_color_1


class AnswerA:
    def __init__(self, width, height, pos, elevation, top_color, bottom_color, clicked_color, font):
        global a
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.font = font

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color
        self.top_color_1 = top_color

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = bottom_color

        # clicked color
        self.clicked_color = clicked_color
        # text
        self.text_surf = self.font.render(f"A: {a}", True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(win, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(win, self.top_color, self.top_rect, border_radius=12)
        win.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        global correct, cor, ci, ic, added, correct_answers
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.clicked_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    if correct == "a" and cor != False:
                        cor = True
                        if added == False:
                            ci += 1
                            correct_answers += 1
                            added = True
                    elif cor != True:
                        cor = False
                        if added == False:
                            ic += 1
                            added = True
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.top_color_1


class AnswerB:
    def __init__(self, width, height, pos, elevation, top_color, bottom_color, clicked_color, font):
        global b
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.font = font

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color
        self.top_color_1 = top_color

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = bottom_color

        # clicked color
        self.clicked_color = clicked_color
        # text
        self.text_surf = self.font.render(f"B: {b}", True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(win, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(win, self.top_color, self.top_rect, border_radius=12)
        win.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        global correct, cor, ci, ic, added, correct_answers
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.clicked_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    if correct == "b" and cor != False:
                        cor = True
                        if added == False:
                            ci += 1
                            correct_answers += 1
                            added = True
                    elif cor != True:
                        cor = False
                        if added == False:
                            ic += 1
                            added = True
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.top_color_1


class AnswerC:
    def __init__(self, width, height, pos, elevation, top_color, bottom_color, clicked_color, font):
        global c
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.font = font

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color
        self.top_color_1 = top_color

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = bottom_color

        # clicked color
        self.clicked_color = clicked_color
        # text
        self.text_surf = self.font.render(f"C: {c}", True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(win, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(win, self.top_color, self.top_rect, border_radius=12)
        win.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        global correct, cor, ci, ic, added, correct_answers
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.clicked_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    if correct == "c" and cor != False:
                        cor = True
                        if added == False:
                            ci += 1
                            correct_answers += 1
                            added = True
                    elif cor != True:
                        cor = False
                        if added == False:
                            ic += 1
                            added = True
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.top_color_1


class AnswerD:
    def __init__(self, width, height, pos, elevation, top_color, bottom_color, clicked_color, font):
        global d
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.font = font

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color
        self.top_color_1 = top_color

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = bottom_color

        # clicked color
        self.clicked_color = clicked_color
        # text
        self.text_surf = self.font.render(f"D: {d}", True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(win, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(win, self.top_color, self.top_rect, border_radius=12)
        win.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.clicked_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                global correct, cor, ci, ic, added, correct_answers
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    if correct == "d" and cor != False:
                        cor = True
                        if added == False:
                            ci += 1
                            correct_answers += 1
                            added = True
                    elif cor != True:
                        cor = False
                        if added == False:
                            ic += 1
                            added = True
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.top_color_1


class NextQuestion:
    def __init__(self, width, height, pos, elevation, top_color, bottom_color, clicked_color, font):
        global a
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.font = font

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color
        self.top_color_1 = top_color

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = bottom_color

        # clicked color
        self.clicked_color = clicked_color
        # text
        self.text_surf = self.font.render(f"Next Question", True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(win, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(win, self.top_color, self.top_rect, border_radius=12)
        win.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        global correct, cor, question_up, next_question_button_delay, added, correct_answers, song_screen, question_screen, started, ran_show, operations, temp, ups,correct_amt, correct_in_row
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.clicked_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    if temp != []:
                        operations = temp
                        save_data()
                    if correct_answers < correct_amt:
                        cor = None
                        ups = False
                        next_question_button_delay = -1
                        added = False
                        question_up = False
                        song_screen = False
                        question_screen = True
                        ran_show = False
                        started = False
                    elif correct_answers == correct_amt:
                        cor = None
                        next_question_button_delay = -1
                        ups = False
                        added = False
                        question_up = False
                        correct_answers = 0
                        song_screen = True
                        question_screen = False
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.top_color_1


class Mode:
    def __init__(self,text ,width, height, pos, elevation, top_color, bottom_color, clicked_color, font, mode):
        global a
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.font = font
        self.text = text
        self.mode = mode

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color
        self.top_color_1 = top_color

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = bottom_color

        # clicked color
        self.clicked_color = clicked_color
        # text
        self.text_surf = self.font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(win, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(win, self.top_color, self.top_rect, border_radius=12)
        win.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        global temp, operations
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.clicked_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    temp = self.mode
                    save_data()
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.top_color_1


class Song:
    def __init__(self,text ,width, height, pos, elevation, top_color, bottom_color, clicked_color, font, song):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.font = font
        self.text = text
        self.mode = song

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color
        self.top_color_1 = top_color

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = bottom_color

        # clicked color
        self.clicked_color = clicked_color
        # text
        self.text_surf = self.font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(win, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(win, self.top_color, self.top_rect, border_radius=12)
        win.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        global song, question_screen, song_screen, started
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.clicked_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    if started == False:
                        if self.mode == "shark":
                            baby_shark.play()
                            started = True
                        elif self.mode == "taco":
                            tacos.play()
                            started = True
                        elif self.mode == "yakko":
                            yakko.play()
                            started = True
                        elif self.mode == "dogs":
                            who_let_the_dogs_out.play()
                            started = True
                        elif self.mode == "e":
                            rush_e.play()
                            started = True
                        elif self.mode == "hand":
                            handclap.play()
                            started = True
                        elif self.mode == "a":
                            rush_all.play()
                            started = True
                        else:
                            song = None
                            question_screen = True
                            song_screen = False


                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.top_color_1




res = (1080, 720)
win = pygame.display.set_mode(res)
pygame.display.set_caption('Math Flash Cards!')
title_font = pygame.font.Font("assets/freesansbold.ttf", 70)
play_font = pygame.font.Font("assets/freesansbold.ttf", 30)
question_font = pygame.font.Font("assets/freesansbold.ttf", 20)
answer_font = pygame.font.Font("assets/freesansbold.ttf" ,30)
correct_font = pygame.font.Font("assets/freesansbold.ttf", 75)
score_font = pygame.font.Font("assets/freesansbold.ttf", 30)
box_font = pygame.font.Font("assets/freesansbold.ttf", 27)
setting_font = pygame.font.Font("assets/freesansbold.ttf", 20)

baby_shark = pygame.mixer.Sound("assets/baby_shark.mp3")
tacos = pygame.mixer.Sound("assets/tacos.mp3")
yakko = pygame.mixer.Sound("assets/yakko.mp3")

rush_e = pygame.mixer.Sound("assets/e.mp3")
who_let_the_dogs_out = pygame.mixer.Sound("assets/dogs.mp3")
handclap = pygame.mixer.Sound("assets/clap.mp3")
rush_all = pygame.mixer.Sound("assets/rush_all.mp3")



def get_random_equation():
    global num_a, num_b, op, ans, question_text, quesRect, question_up, a, b, c, d, a_, b_, c_, d_, correct, ups
    num_a = random.randint(0,_max)
    num_b = random.randint(0,_max)
    op = random.choice(operations)
    if op == "/" and num_b == 0:
        get_random_equation()
        return
    ans = eval(str(num_a)+str(op).replace("x", "*")+str(num_b))
    if int(ans) < 0:
        get_random_equation()
        return
    if str(ans).replace('.0','') != str(int(ans)):
        get_random_equation()
        return
    correct = random.choice(["a","b","c","d"])
    a = 0
    b = 0
    c = 0
    d = 0
    if correct == "a":
        a = ans
        try:
            b = a + random.randint(1, a)
            c = a - random.randint(1, a)
            d = a + random.randint(1, a)
        except:
            get_random_equation()
            return
    if correct == "b":
        b = ans
        try:
            a = b - random.randint(1, b)
            c = b + random.randint(1, b)
            d = b - random.randint(1, b)
        except:
            get_random_equation()
            return
    if correct == "c":
        c = ans
        try:
            b = c + random.randint(1, c)
            d = c - random.randint(1, c)
            a = b + random.randint(1, c)
        except:
            get_random_equation()
            return
    if correct == "d":
        d = ans
        try:
            a = d - random.randint(1, d)
            b = d + random.randint(1, d)
            c = d - random.randint(1, d)
        except:
            get_random_equation()
            return
    if a == b or a ==c or a == d or b == c or b ==d or c == d:
        get_random_equation()
        return
    if op == "/" and str(ans).replace('.0','') == str(int(ans)):
        a = int(a)
        b = int(b)
        c = int(c)
        d = int(d)
    question_text = title_font.render(f'What is {num_a} {op} {num_b}?', True, (0, 0, 0))
    quesRect = question_text.get_rect()
    quesRect.center = (res[0] // 2, res[1] // 2 - 190)
    a_ = AnswerA(300, 60, (res[0] / 2 - 145, res[1] / 2 + 40), 5, (140, 255, 0), (0,255,0), (190, 255, 50),
                 answer_font)
    b_ = AnswerB(300, 60, (res[0] / 2 - 145, res[1] / 2 + 120), 5, (140, 255, 0), (0,255,0), (190, 255, 50),
                 answer_font)
    c_ = AnswerC(300, 60, (res[0] / 2 - 145, res[1] / 2 + 200), 5, (140, 255, 0), (0,255,0), (190, 255, 50),
                 answer_font)
    d_ = AnswerD(300, 60, (res[0] / 2 - 145, res[1] / 2 + 280), 5, (140, 255, 0), (0,255,0), (190, 255, 50),
                 answer_font)
    question_up = True
    ups = True


def get_random_greater_less():
    global num_a, num_b, correct, ans,a ,b ,c, a_, b_, c_,d_, question_up, question_text, quesRect, ups
    ops = ["<",">","="]
    num_1 = random.randint(0,_max)
    num_2 = random.randint(0, _max)
    correct = random.choice(["a", "b", "c"])
    if num_1 == num_2:
        ans = "="
    if num_1 > num_2:
        ans = ">"
    if num_2 > num_1:
        ans = "<"
    if correct == "a":
        a = ans
        choice_b = random.choice(["b","c"])
        if choice_b == "b":
            ops.remove(ans)
            b = random.choice(ops)
            ops.remove(b)
            c = ops[0]
        if choice_b == "c":
            ops.remove(ans)
            c = random.choice(ops)
            ops.remove(c)
            b = ops[0]

    if correct == "b":
        b = ans
        choice_b = random.choice(["a","c"])
        if choice_b == "a":
            ops.remove(ans)
            a = random.choice(ops)
            ops.remove(a)
            c = ops[0]
        if choice_b == "c":
            ops.remove(ans)
            c = random.choice(ops)
            ops.remove(c)
            a = ops[0]

    if correct == "c":
        c = ans
        choice_b = random.choice(["b","a"])
        if choice_b == "b":
            ops.remove(ans)
            b = random.choice(ops)
            ops.remove(b)
            a = ops[0]
        if choice_b == "a":
            ops.remove(ans)
            a = random.choice(ops)
            ops.remove(a)
            b = ops[0]

    question_text = title_font.render(f'{num_1} _ {num_2}', True, (0, 0, 0))
    quesRect = question_text.get_rect()
    quesRect.center = (res[0] // 2, res[1] // 2 - 190)

    a_ = AnswerA(300, 60, (res[0] / 2 - 145, res[1] / 2 + 40), 5, (140, 255, 0), (0, 255, 0), (190, 255, 50),
                 answer_font)
    b_ = AnswerB(300, 60, (res[0] / 2 - 145, res[1] / 2 + 120), 5, (140, 255, 0), (0, 255, 0), (190, 255, 50),
                 answer_font)
    c_ = AnswerC(300, 60, (res[0] / 2 - 145, res[1] / 2 + 200), 5, (140, 255, 0), (0, 255, 0), (190, 255, 50),
                 answer_font)
    d_ = AnswerD(300, 60, (res[0] / 2 - 145, res[1] / 2 + 280), 5, (140, 255, 0), (0, 255, 0), (190, 255, 50),
                 answer_font)
    question_up = True
    ups = True

def get_random_geometry():
    global correct, ans, a, b, c,d, a_, b_, c_, d_, question_up, question_text, quesRect, ups,prev
    shapes = ["circle","square","triangle", "rectangle", "pentagon", "hexagon", "heptagon", "octagon", "nonagon", "decagon"]
    shape = random.choice(shapes)
    attributes = {"circle":0,"square":4,"triangle":3,"rectangle":4,"pentagon":5,"hexagon":6,"heptagon":7,"octagon":8,"nonagon":9,"decagon":10}
    ans = attributes[shape]
    correct = random.choice(["a", "b", "c", "d"])
    if shape == prev:
        return get_random_geometry()
    else:
        prev = shape
    a = 0
    b = 0
    c = 0
    d = 0
    if correct == "a":
        a = ans
        try:
            b = ans + random.randint(1,int(ans))
            c = ans - random.randint(1,int(ans))
            d = ans + random.randint(1,int(ans))
        except:
            return get_random_geometry()
    elif correct == "b":
        b = ans
        try:
            a = ans + random.randint(1,int(ans))
            c = ans - random.randint(1,int(ans))
            d = ans + random.randint(1,int(ans))
        except:
            return get_random_geometry()
    elif correct == "c":
        c = ans
        try:
            a = ans + random.randint(1,int(ans))
            b = ans - random.randint(1,int(ans))
            d = ans + random.randint(1,int(ans))
        except:
            return get_random_geometry()
    elif correct == "d":
        d = ans
        try:
            a = ans + random.randint(1,int(ans))
            b = ans - random.randint(1,int(ans))
            c = ans + random.randint(1,int(ans))
        except:
            return get_random_geometry()
    if a == b or a == c or a == d or b == c or b == d or c == d:
        return get_random_geometry()

    question_text = pygame.font.Font("assets/freesansbold.ttf", 40).render(f'How many sides does a {shape.capitalize()} have?', True, (0, 0, 0))
    quesRect = question_text.get_rect()
    quesRect.center = (res[0] // 2, res[1] // 2 - 190)
    a_ = AnswerA(300, 60, (res[0] / 2 - 145, res[1] / 2 + 40), 5, (140, 255, 0), (0, 255, 0), (190, 255, 50),
                 answer_font)
    b_ = AnswerB(300, 60, (res[0] / 2 - 145, res[1] / 2 + 120), 5, (140, 255, 0), (0, 255, 0), (190, 255, 50),
                 answer_font)
    c_ = AnswerC(300, 60, (res[0] / 2 - 145, res[1] / 2 + 200), 5, (140, 255, 0), (0, 255, 0), (190, 255, 50),
                 answer_font)
    d_ = AnswerD(300, 60, (res[0] / 2 - 145, res[1] / 2 + 280), 5, (140, 255, 0), (0, 255, 0), (190, 255, 50),
                 answer_font)

    question_up = True
    ups = True
    






title_text = title_font.render('Math Flash Cards', True, (0,0,0))
playRect = title_text.get_rect()
playRect.center = (res[0] // 2, res[1] // 2-80+math.sin(time.time()*5)*5 - 25)


settings_text = title_font.render('Settings', True, (0,0,0))
sRect = settings_text.get_rect()
sRect.center = (res[0] // 2, res[1] // 2-180)


song_text = title_font.render('Choose a song!', True, (0,0,0))
__sRect = song_text.get_rect()
__sRect.center = (res[0] // 2, res[1] // 2-180)


settings_text_2 = title_font.render('Settings 2', True, (0,0,0))
_sRect = settings_text_2.get_rect()
_sRect.center = (res[0] // 2, res[1] // 2-180)

correct_text = correct_font.render('Correct!', True, (72, 196, 0))
correctRect = correct_text.get_rect()
correctRect.center = (res[0] // 2, res[1] // 2-90)

incorrect_text = correct_font.render('Incorrect.', True, (255,0,0))
incorrectRect = incorrect_text.get_rect()
incorrectRect.center = (res[0] // 2, res[1] // 2-90)


splash_text = title_font.render('Made by Akshar Desai.', True, (0,0,0))
splashRect = splash_text.get_rect()
splashRect.center = (res[0] // 2, res[1]//2)


_bad_input = pygame.font.Font("assets/freesansbold.ttf", 17).render('Invalid Number!', True, (255, 56, 56))
bRect = _bad_input.get_rect()
bRect.center = (res[0]/2, res[1]/2-40)

_bad_input_1 = pygame.font.Font("assets/freesansbold.ttf", 17).render('Cannot be 0 or less!', True, (255, 56, 56))
_bRect = _bad_input_1.get_rect()
_bRect.center = (res[0]/2, res[1]/2-40)






play = PlayButton('Play!', 300, 60, (res[0]/2-145, res[1]/2+40), 5,(140, 255, 0),(0,255,0),(190,255,50), play_font)
settings = SettingsButton('Settings', 300, 60, (res[0]/2-145, res[1]/2+120), 5,(71, 154, 255),(0, 73, 161),(138, 191, 255), play_font)
exit = ExitButton('Exit', 300, 60, (res[0]/2-145, res[1]/2+200), 5,(212, 35, 4),(120, 18, 0),(255, 92, 64), play_font)
back_1 = BackButton('Back To Main Menu', 300, 60, (res[0]/2-145, res[1]/2+280), 5,(212, 35, 4),(120, 18, 0),(255, 92, 64), play_font)
back_2 = BackButton('Back', 300, 60, (50, res[1]/2 + 280), 5,(212, 35, 4),(120, 18, 0),(255, 92, 64), play_font)
back_3 = BackButton1('Back', 300, 60, (res[0]/2-145, res[1]/2+280), 5,(212, 35, 4),(120, 18, 0),(255, 92, 64), play_font)

setting_2 = SettingNextPage('Next Page', 300, 60, (res[0]/2-145, res[1]/2+200), 5,(59, 7, 245),(23, 0, 105),(116, 77, 255), play_font)

# modes
plus_minus = Mode('Addition & Subtraction', 300, 60, (50, res[1]/2 + 100), 5,(59, 7, 245),(23, 0, 105),(116, 77, 255), setting_font, ['+','-'])
x_divide = Mode("Multiplication & Division", 300, 60, (365, res[1]/2 + 100), 5,(59, 7, 245),(23, 0, 105),(116, 77, 255), setting_font,['x','/'])
all = Mode('All', 300, 60, (680, res[1]/2 + 100), 5,(59, 7, 245),(23, 0, 105),(116, 77, 255), setting_font,['+','-','/','x'])

greater_less = Mode('Greater and Less than', 300, 60, (50, res[1]/2 + 100), 5,(59, 7, 245),(23, 0, 105),(116, 77, 255), setting_font, ['<','>'])
geometry = Mode("2D Geometry", 300, 60, (365, res[1]/2 + 100), 5,(59, 7, 245),(23, 0, 105),(116, 77, 255), setting_font,['triangle'])




# Songs
shark = Song('Baby Shark', 300, 60, (50, res[1]/2 + 60), 5,(59, 7, 245),(23, 0, 105),(116, 77, 255), setting_font, "shark")
taco = Song("Raining Tacos", 300, 60, (365, res[1]/2 + 60), 5,(59, 7, 245),(23, 0, 105),(116, 77, 255), setting_font,"taco")
yakk = Song('''Yakko's World''', 300, 60, (680, res[1]/2 + 60), 5,(59, 7, 245),(23, 0, 105),(116, 77, 255), setting_font,"yakko")
none = Song('''None''', 300, 60, (365, res[1]/2+220), 5,(59, 7, 245),(23, 0, 105),(116, 77, 255), setting_font,None)

dog = Song("Who Let The Dogs Out", 300, 60, (50, res[1]/2 + 140), 5,(59, 7, 245),(23, 0, 105),(116, 77, 255), setting_font,"dogs")
hand = Song('''Handclap''', 300, 60, (365, res[1]/2 + 140), 5,(59, 7, 245),(23, 0, 105),(116, 77, 255), setting_font,"hand")
rush_ee = Song('''Rush E''', 300, 60, (680, res[1]/2+140), 5,(59, 7, 245),(23, 0, 105),(116, 77, 255), setting_font,"e")
rush_al = Song('''Rush All''', 300, 60, (50, res[1]/2+220), 5,(59, 7, 245),(23, 0, 105),(116, 77, 255), setting_font,"a")


next = NextQuestion(300, 60, (res[0]/2-145, res[1]/2-40), 5,(48, 242, 233),(0, 122, 117),(107, 255, 248), answer_font)
next_1 = NextQuestion(300, 60, (365, res[1]/2-40), 5,(48, 242, 233),(0, 122, 117),(107, 255, 248), answer_font)

input_box = pygame.Rect(res[0]/2-100, res[1]/2-20, 140, 32)
link_box = pygame.Rect(res[0]/2-100, res[1]/2-20, 140, 32)
color_inactive = (0, 161, 0)
color_active = (0,255,0)
color = color_inactive
color_1 = color_inactive
active = False
_active = False
text = ''
lin = ''
done = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if song_screen:
            keys = pygame.key.get_pressed()
            if _active:
                if keys[pygame.K_LMETA] and keys[pygame.K_v]:
                    if _active:
                        if len(lin) <= 30:
                            lin += pyperclip.paste()
                if keys[pygame.K_LMETA] and keys[pygame.K_BACKSPACE]:
                    if _active:
                        lin = ""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if input_box.collidepoint(event.pos):
                # Toggle the active variable.
                active = not active
            else:
                active = False

            if link_box.collidepoint(event.pos):
                # Toggle the active variable.
                _active = not _active
            else:
                _active = False
            # Change the current color of the input box.
            color = color_active if _active else color_inactive
            color_1 = color_active if _active else color_inactive
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    if settings_screen:
                        try:
                            _max = int(text)
                            if _max <= 0:
                                bad_zero = True
                                _max = r["max"]
                            else:
                                save_data()
                        except:
                            bad_input = True
                        text = ''
            if _active:
                if event.key == pygame.K_RETURN:
                    if song_screen and downloading == False:
                        link = lin
                        downloading = True
                        lin = 'Downloading Song...'
                elif keys[pygame.K_BACKSPACE]:
                    lin = lin[:-1]
                else:
                    keys = pygame.key.get_pressed()
                    if song_screen:
                        if not keys[pygame.K_LMETA] and keys[pygame.K_v]:
                            lin += event.unicode
                    else:
                        text += event.unicode
                    
    correct_score = score_font.render(f'Correct: {ci}', True, (23, 230, 0))
    csRect = correct_score.get_rect()
    csRect.left = 10
    csRect.centery = 30
    incorrect_score = score_font.render(f'Incorrect: {ic}', True, (214, 19, 9))
    icsRect = incorrect_score.get_rect()
    icsRect.left = 10
    icsRect.centery = 60
    total = int(ci) + int(ic)
    per = None
    try:
        per = f"{str(round(float(int(ci)/total)*100, 2))}%"
    except:
        per = "0.0%"
    percent = score_font.render(f'Percent Correct: {per}', True, (234, 255, 94))
    pRect = percent.get_rect()
    pRect.left = 10
    pRect.centery = 90
    if play_button_delay >= 1 and title_screen == True:
        play_button_delay -= 1
    if splash_delay >= 1:
        splash_delay -= 1
    if next_question_button_delay >= 1:
        next_question_button_delay -= 1
    if splash:
        win.fill('#e68883')
        if splash_delay != 0:
            win.blit(splash_text, splashRect)
        if splash_delay == 0:
            splash_delay = -1
            splash = False
            title_screen = True

    if settings_screen:
        max_text = setting_font.render(f'Change Max Number In Math Problems (Currently {_max}) [Press enter to update]', True, (0, 0, 0))
        mRect = max_text.get_rect()
        mRect.center = (res[0] // 2, res[1] // 2-60)
        mode_text = None

        if "+" in temp and "-" in temp and "/" not in temp:
            mode_text = setting_font.render(f'Change Mode (Currently Addition & Subtraction)', True, (0, 0, 0))
        if "/" in temp and "x" in temp and "+" not in temp:
            mode_text = setting_font.render(f'Change Mode (Currently Multiplication & Division)', True, (0, 0, 0))
        if "+" in temp and "-" in temp and "/" in temp and "x" in temp:
            mode_text = setting_font.render(f'Change Mode (Currently All Operations)', True, (0, 0, 0))
        if "<" in temp and ">" in temp:
            mode_text = setting_font.render(f'Change Mode (Currently Greater & Less than)', True, (0, 0, 0))

        if "triangle" in temp:
            mode_text = setting_font.render(f'Change Mode (Currently 2D Geometry)', True, (0, 0, 0))
        moRect = mode_text.get_rect()
        moRect.center = (res[0] // 2, res[1] // 2 + 60)
        win.fill('#c800cf')
        txt_surface = box_font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        win.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(win, color, input_box, 2, border_radius=12)
        win.blit(settings_text, sRect)
        win.blit(max_text, mRect)
        win.blit(mode_text, moRect)
        back_1.draw()
        plus_minus.draw()
        all.draw()
        x_divide.draw()
        setting_2.draw()
        if bad_input:
            win.blit(_bad_input, bRect)
        elif bad_zero:
            win.blit(_bad_input_1, _bRect)

    if settings_screen_2:
        mode_text = None
        if "+" in temp and "-" in temp and "/" not in temp:
            mode_text = setting_font.render(f'Change Mode (Currently Addition & Subtraction)', True, (0, 0, 0))
        if "/" in temp and "x" in temp and "+" not in temp:
            mode_text = setting_font.render(f'Change Mode (Currently Multiplication & Division)', True, (0, 0, 0))
        if "+" in temp and "-" in temp and "/" in temp and "x" in temp:
            mode_text = setting_font.render(f'Change Mode (Currently All Operations)', True, (0, 0, 0))
        if "<" in temp and ">" in temp:
            mode_text = setting_font.render(f'Change Mode (Currently Greater & Less than)', True, (0, 0, 0))

        if "triangle" in temp:
            mode_text = setting_font.render(f'Change Mode (Currently 2D Geometry)', True, (0, 0, 0))
        moRect = mode_text.get_rect()
        moRect.center = (res[0] // 2, res[1] // 2 + 60)
        win.fill('#c800cf')
        back_3.draw()
        win.blit(settings_text_2, _sRect)
        greater_less.draw()
        geometry.draw()
        win.blit(mode_text, moRect)

    if song_screen:
        win.fill('#c800cf')
        win.blit(song_text, __sRect)
        if downloading == None:
            lin = "Successfuly Downloaded Song!"
        taco.draw()
        shark.draw()
        yakk.draw()
        none.draw()
        dog.draw()
        rush_ee.draw()
        hand.draw()
        rush_al.draw()
        if not pygame.mixer.Channel(0).get_busy() and started == True and ran_show == False:
            next_1.draw()

        # txt_surface_1 = box_font.render(lin, True, color_1)
        # width_1 = max(200, txt_surface_1.get_width() + 10)
        # link_box.w = width_1
        # win.blit(txt_surface_1, (link_box.x + 5, link_box.y + 5))
        # pygame.draw.rect(win, color, link_box, 2, border_radius=12)
    if title_screen:
        win.fill('#c800cf')
        playRect.center = (res[0] // 2, res[1] // 2 - 80 + math.sin(time.time() * 5) * 20 - 25)
        if play_button_delay == 0:
            play.draw()
            settings.draw()
            exit.draw()
        if not question_screen:
            win.blit(title_text, playRect)

    if question_screen:
        global a_, b_, c_, d_
        if question_up == False and cor == None and ups == False:
            if temp != operations and viewed == False:
                operations = temp
                viewed = True
            if "+" in operations or "x" in operations:
                get_random_equation()
            elif "<" in operations:
                get_random_greater_less()
            elif "triangle" in operations:
                get_random_geometry()
        win.fill('#89e0df')
        play_button_delay = -1
        win.blit(correct_score, csRect)
        win.blit(incorrect_score, icsRect)
        win.blit(question_text,quesRect)
        win.blit(percent, pRect)
        if "+" in operations or "x" in operations or "triangle" in operations:
            a_.draw()
            b_.draw()
            c_.draw()
            d_.draw()
        elif ">" in operations:
            a_.draw()
            b_.draw()
            c_.draw()
        back_2.draw()
        if cor == True:
            win.blit(correct_text, correctRect)
            if next_question_button_delay == -1:
                next_question_button_delay = int(30*clock.tick(600))
        if cor == False:
            if correct_in_row == True:
                correct_answers = 0
            win.blit(incorrect_text, incorrectRect)
            incorrect_text_1 = pygame.font.Font("assets/freesansbold.ttf",23).render(f'The Correct Answer was {correct.upper()}.', True, (255, 0, 0))
            incorrectRect1 = incorrect_text_1.get_rect()
            incorrectRect1.center = (res[0] // 2 - 355, res[1] // 2 + 120)
            win.blit(incorrect_text_1, incorrectRect1)
            if next_question_button_delay == -1:
                next_question_button_delay = int(30*clock.tick(600))
        if next_question_button_delay == 0:
           next.draw()

    pygame.display.update()
    clock.tick(600)

