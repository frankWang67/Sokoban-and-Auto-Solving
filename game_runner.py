import pygame
import time
from map_list import map_list
from map_maker import map_maker
from utils import *

class game_runner:
    def __init__(self, level=0, mode="human"):
        self.level = level
        self.size = 16
        self.map_dict = map_dict
        # self.nmap = numeral_map(map_list[self.level], self.size)
        self.nmap = numeral_map(map_maker().generate_map(), self.size)

        self.tile_size = 56
        self.background_texture = pygame.image.load('./texture/ground.jpg')
        self.wall_texture = pygame.image.load('./texture/wall.jpg')
        self.target_texture = pygame.image.load('./texture/target.jpg')
        self.box_texture = pygame.image.load('./texture/box.jpg')
        self.box_inplace_texture = pygame.image.load('./texture/box_inplace.jpg')
        self.character_texture_list = [pygame.image.load('./texture/pika_right.jpg'), pygame.image.load('./texture/pika_left.jpg')]
        self.character_inplace_texture = pygame.image.load('./texture/pika_inplace.jpg')

        self.background_texture = pygame.transform.scale(self.background_texture, (self.tile_size, self.tile_size))
        self.wall_texture = pygame.transform.scale(self.wall_texture, (self.tile_size, self.tile_size))
        self.target_texture = pygame.transform.scale(self.target_texture, (self.tile_size, self.tile_size))
        self.box_texture = pygame.transform.scale(self.box_texture, (self.tile_size, self.tile_size))
        self.box_inplace_texture = pygame.transform.scale(self.box_inplace_texture, (self.tile_size, self.tile_size))
        self.character_texture_list = [pygame.transform.scale(character_texture, (self.tile_size, self.tile_size)) for character_texture in self.character_texture_list]
        self.character_inplace_texture = pygame.transform.scale(self.character_inplace_texture, (self.tile_size, self.tile_size))

        self.character_left = True

        pygame.init()
        self.window_width = self.size * self.tile_size + 200
        self.window_height = self.size * self.tile_size
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.mode = mode
        self.start = True
        state.open = PriorityQueue()
        state.closed = set()

    def run(self):
        idx = 0
        length = -1
        while self.running:
            self.draw_map()
            pygame.display.flip()

            if self.mode == "human":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.character_left = True
                            self.nmap.move(0, -1)
                        elif event.key == pygame.K_RIGHT:
                            self.character_left = False
                            self.nmap.move(0, 1)
                        elif event.key == pygame.K_UP:
                            self.nmap.move(-1, 0)
                        elif event.key == pygame.K_DOWN:
                            self.nmap.move(1, 0)
                        elif event.key == pygame.K_r:
                            self.nmap = numeral_map(map_list[self.level], self.size)

                        if self.nmap.check_win():
                            self.draw_map()
                            self.next_level()
            elif self.mode == "auto":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                if self.start:
                    self.start = False
                    steps = self.solve()
                    if steps is None:
                        self.notice_no_solution()
                        continue
                    idx = 0
                    length = len(steps)
                else:
                    if idx == length:
                        self.next_level()
                        continue
                    step = steps[idx]
                    if step == [0, -1]:
                        self.character_left = True
                    elif step == [0, 1]:
                        self.character_left = False
                    self.nmap.move(step[0], step[1])
                    idx += 1
                    time.sleep(0.3)

        pygame.quit()
    
    def next_level(self):
        time.sleep(0.5)
        # self.level += 1
        # if self.level == len(map_list):
        #     self.running = False
        # else:
        #     self.nmap = numeral_map(map_list[self.level], self.size)
        #     self.start = True
        #     # state.all_states = []
        #     state.open = PriorityQueue()
        #     state.closed = set()
        self.nmap = numeral_map(map_maker().generate_map(), self.size)
        self.start = True
        state.open = PriorityQueue()
        state.closed = set()

    def draw_map(self):
        for row in range(self.size):
            for col in range(self.size):
                tile = self.nmap.map_getter(row, col)
                x = col * self.tile_size
                y = row * self.tile_size

                if tile == self.map_dict["background"]:
                    self.window.blit(self.background_texture, (x, y))
                elif tile == self.map_dict["wall"]:
                    self.window.blit(self.wall_texture, (x, y))
                elif tile == self.map_dict["target"]:
                    self.window.blit(self.target_texture, (x, y))
                elif tile == self.map_dict["box"]:
                    self.window.blit(self.box_texture, (x, y))
                elif tile == self.map_dict["character"]:
                    self.window.blit(self.character_texture_list[self.character_left], (x, y))
                elif tile == self.map_dict["box_inplace"]:
                    self.window.blit(self.box_inplace_texture, (x, y))
                elif tile == self.map_dict["character_inplace"]:
                    self.window.blit(self.character_inplace_texture, (x, y))

        pygame.draw.rect(self.window, (128, 128, 128), (self.size * self.tile_size, 0, 200, self.size * self.tile_size))
        mode_text = self.font.render('Mode: ' + self.mode, True, (255, 255, 255))
        self.window.blit(mode_text, (self.size * self.tile_size + 10, 10))
        if self.mode == 'human':
            # 在交互区显示按键操作提示
            control_text = self.font.render('press dir key', True, (255, 255, 255))
            self.window.blit(control_text, (self.size * self.tile_size + 10, 80))
            control_text = self.font.render('to move', True, (255, 255, 255))
            self.window.blit(control_text, (self.size * self.tile_size + 10, 110))
            control_text = self.font.render('press R', True, (255, 255, 255))
            self.window.blit(control_text, (self.size * self.tile_size + 10, 160))
            control_text = self.font.render('to restart', True, (255, 255, 255))
            self.window.blit(control_text, (self.size * self.tile_size + 10, 190))
    
    def solve(self):
        return self.Astar()

    def Astar(self):
        max_step = int(1e8)
        start_state = state(self.nmap, 0, start=True)
        found = False
        start_time = time.time()
        for i in range(max_step):
            found, no_solution = start_state.explore()
            if found or no_solution:
                break
        text = self.font.render(f'Explored {i} states', True, (255, 255, 255))
        self.window.blit(text, (self.size * self.tile_size + 10, 200))
        text = self.font.render(f'in {time.time() - start_time} s', True, (255, 255, 255))
        self.window.blit(text, (self.size * self.tile_size + 10, 220))
        print("Explored", i, "states in", time.time() - start_time, "seconds")

        if found:
            steps = []
            st = start_state
            while st.move_to_solution is not None:
                steps.append(st.move_to_solution)
                st = st.child
            text = self.font.render('Found solution with', True, (255, 255, 255))
            self.window.blit(text, (self.size * self.tile_size + 10, 250))
            text = self.font.render(f'{len(steps)} steps', True, (255, 255, 255))
            self.window.blit(text, (self.size * self.tile_size + 10, 270))
            print("Found solution with", len(steps), "steps")
            return steps
        else:
            return None
        
    def notice_no_solution(self):
        print("No solution found")
        print(self.nmap.map)
        text = self.font.render('No solution found', True, (255, 255, 255))
        self.window.blit(text, (self.size * self.tile_size + 10, 200))
        self.running = False
    
if __name__ == "__main__":
    # runner = game_runner(level=50, mode="human")
    runner = game_runner(level=0, mode="auto")
    runner.run()