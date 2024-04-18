import time
import queue
import random
from utils import *

class map_maker:
    def __init__(self, size=8, sizeL=16, mode=1):
        self.size = size
        self.sizeL = sizeL
        self.mode = mode
        self.initialize()

    def initialize(self):
        self.map = [0] * self.sizeL * self.sizeL
        self.assigned = [False] * self.size * self.size
        self.available_pos = [(i, j) for i in range(1, self.size - 1) for j in range(1, self.size - 1)]
        if self.mode == 2:
            self.targets = []
            self.boxes = []

    def map_getter(self, x, y):
        return self.map[(x + self.size // 2) * self.sizeL + (y + self.size // 2)]
    
    def map_setter(self, x, y, value):
        self.map[(x + self.size // 2) * self.sizeL + (y + self.size // 2)] = value
        if x > 0 and x < self.size - 1 and y > 0 and y < self.size - 1 and not self.assigned[x * self.size + y]:
            self.available_pos.remove((x, y))
        self.assigned[x * self.size + y] = True

    def has_been_assigned(self, x, y):
        return self.assigned[x * self.size + y]
    
    def is_obstacle(self, x, y, moved=False, old_pos=None, new_pos=None):
        if x == 0 or x == self.size - 1 or y == 0 or y == self.size - 1:
            return True
        if moved:
            if x == old_pos[0] and y == old_pos[1]:
                return False
            if x == new_pos[0] and y == new_pos[1]:
                return True
        return self.map_getter(x, y) == map_dict["wall"] or self.map_getter(x, y) == map_dict["box"]
    
    def generate_wall(self):
        j1, j2 = 0, self.size - 1
        for i in range(0, self.size):
            changed1 = False
            if changed1:
                prob1 = 0.1
            else:
                prob1 = 0.3
            if random.random() < prob1:
                self.map_setter(i, j1, map_dict["wall"])
                j1 = 1 - j1
                self.map_setter(i, j1, map_dict["wall"])
                changed1 = True
            else:
                self.map_setter(i, j1, map_dict["wall"])
                changed1 = False

            changed2 = False
            if changed2:
                prob2 = 0.1
            else:
                prob2 = 0.3
            if random.random() < prob2:
                self.map_setter(i, j2, map_dict["wall"])
                j2 = 2 * self.size - 2 - j2
                self.map_setter(i, j2, map_dict["wall"])
                changed2 = True
            else:
                self.map_setter(i, j2, map_dict["wall"])
                changed2 = False

        i1, i2 = 0, self.size - 1
        for j in range(0, self.size):
            changed1 = False
            if changed1:
                prob1 = 0.1
            else:
                prob1 = 0.3
            if random.random() < prob1:
                self.map_setter(i1, j, map_dict["wall"])
                i1 = 1 - i1
                self.map_setter(i1, j, map_dict["wall"])
                changed1 = True
            else:
                self.map_setter(i1, j, map_dict["wall"])
                changed1 = False

            changed2 = False
            if changed2:
                prob2 = 0.1
            else:
                prob2 = 0.3
            if random.random() < prob2:
                self.map_setter(i2, j, map_dict["wall"])
                i2 = 2 * self.size - 2 - i2
                self.map_setter(i2, j, map_dict["wall"])
                changed2 = True
            else:
                self.map_setter(i2, j, map_dict["wall"])
                changed2 = False

        explore_prob = 0.4
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for i in range(0, 3):
            if random.random() < explore_prob:
                x = random.randint(1, self.size - 2)
                y = random.randint(1, self.size - 2)
                while self.has_been_assigned(x, y):
                    x = random.randint(1, self.size - 2)
                    y = random.randint(1, self.size - 2)
                self.map_setter(x, y, map_dict["wall"])
                d1, d2 = random.sample(directions, 2)
                self.map_setter(x + d1[0], y + d1[1], map_dict["wall"])
                self.map_setter(x + d2[0], y + d2[1], map_dict["wall"])

    def generate_target(self):
        self.target_cnt = 0
        while self.target_cnt < 3:
            for i in range(1, self.size - 1):
                for j in range(1, self.size - 1):
                    if not self.has_been_assigned(i, j):
                        if random.random() < 0.1:
                            self.map_setter(i, j, map_dict["target"])
                            self.target_cnt += 1
                            if self.mode == 2:
                                self.targets.append((i + self.size // 2, j + self.size // 2))

    def generate_box(self):
        box_pos = random.sample(self.available_pos, self.target_cnt)
        for pos in box_pos:
            self.map_setter(pos[0], pos[1], map_dict["box"])
            if self.mode == 2:
                actual_pos = (pos[0] + self.size // 2, pos[1] + self.size // 2)
                self.boxes.append(actual_pos)

    def generate_character(self):
        character_pos = random.choice(self.available_pos)
        self.map_setter(character_pos[0], character_pos[1], map_dict["character"])

    def check_solvable(self):
        if self.mode == 1:
            return self.check_solvable_mode1()
        elif self.mode == 2:
            return self.check_solvable_mode2()

    def check_solvable_mode1(self):
        row_to_check = []
        col_to_check = []

        for i in range(1, self.size - 1):
            for j in range(1, self.size - 1):
                if self.map_getter(i, j) == map_dict["box"]:
                    if self.map_getter(i - 1, j) == map_dict["wall"] or self.map_getter(i - 1, j - 1) == map_dict["wall"] or self.map_getter(i - 1, j + 1) == map_dict["wall"]:
                        row_to_check.append(i - 1)
                    if self.map_getter(i + 1, j) == map_dict["wall"] or self.map_getter(i + 1, j - 1) == map_dict["wall"] or self.map_getter(i + 1, j + 1) == map_dict["wall"]:
                        row_to_check.append(i + 1)
                    if self.map_getter(i, j - 1) == map_dict["wall"] or self.map_getter(i - 1, j - 1) == map_dict["wall"] or self.map_getter(i + 1, j - 1) == map_dict["wall"]:
                        col_to_check.append(j - 1)
                    if self.map_getter(i, j + 1) == map_dict["wall"] or self.map_getter(i - 1, j + 1) == map_dict["wall"] or self.map_getter(i + 1, j + 1) == map_dict["wall"]:
                        col_to_check.append(j + 1)
                    
                    if not self.movable_to_target(i, j):
                        return False
                    
                elif self.map_getter(i, j) == map_dict["target"]:
                    if not self.search_from_target_to_character(i, j):
                        return False

        for i in row_to_check:
            feasible = False
            for j in range(2, self.size - 1):
                if (not self.is_obstacle(i, j)) and (not self.is_obstacle(i, j - 1)) and self.search_towards_character(i, j):
                    feasible = True
                    break
                if self.map_getter(i + 1, j) == map_dict["target"] or self.map_getter(i - 1, j) == map_dict["target"]:
                    feasible = True
                    break
            if not feasible:
                return False
            
        for j in col_to_check:
            feasible = False
            for i in range(2, self.size - 1):
                if (not self.is_obstacle(i, j)) and (not self.is_obstacle(i - 1, j)):
                    feasible = True
                    break
                if self.map_getter(i, j + 1) == map_dict["target"] or self.map_getter(i, j - 1) == map_dict["target"]:
                    feasible = True
                    break
            if not feasible:
                return False
        
        return True
    
    def check_solvable_mode2(self):
        original_map = self.map.copy()
        res = True

        for box, target in zip(self.boxes, self.targets):
            self.map = original_map.copy()
            for i in range(1, self.size - 1):
                for j in range(1, self.size - 1):
                    if i + self.size // 2 == box[0] and j + self.size // 2 == box[1]:
                        continue
                    if i + self.size // 2 == target[0] and j + self.size // 2 == target[1]:
                        continue
                    if self.map_getter(i, j) == map_dict["box"] or self.map_getter(i, j) == map_dict["target"]:
                        self.map_setter(i, j, map_dict["background"])

            res = res and self.check_solvable_mode1()
            if not res:
                break

        self.map = original_map.copy()
        return res
    
    def generate_map(self):
        print("Generating map...")
        start_time = time.time()
        self.initialize()
        self.generate_wall()
        self.generate_target()
        self.generate_box()
        self.generate_character()
        tries = 1
        while not self.check_solvable():
            self.initialize()
            self.generate_wall()
            self.generate_target()
            self.generate_box()
            self.generate_character()
            tries += 1
        print(f"Generated map successfully after {tries} tries in {time.time() - start_time} seconds.")
        return self.map
    
    def get_targets_and_boxes(self):
        try:
            return self.targets, self.boxes
        except:
            raise Exception("Targets and boxes are not available in this mode.")
    
    def movable_to_target(self, i, j):
        obs_up = self.is_obstacle(i - 1, j)
        obs_down = self.is_obstacle(i + 1, j)
        obs_left = self.is_obstacle(i, j - 1)
        obs_right = self.is_obstacle(i, j + 1)
        if (obs_up and obs_left) or (obs_up and obs_right) or (obs_down and obs_left) or (obs_down and obs_right):
            return False
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        open = queue.Queue()
        closed = set()
        open.put((i, j))
        while not open.empty():
            x, y = open.get()
            closed.add((x, y))
            for d in directions:
                new_x, new_y = x + d[0], y + d[1]
                character_x, character_y = x - d[0], y - d[1]
                if (new_x, new_y) in closed or self.is_obstacle(new_x, new_y) or self.is_obstacle(character_x, character_y) or not self.search_towards_character(character_x, character_y, moved=True, old_pos=(i, j), new_pos=(x, y)):
                    continue
                if self.map_getter(new_x, new_y) == map_dict["target"]:
                    return True
                open.put((new_x, new_y))
    
    def search_towards_character(self, i, j, moved=False, old_pos=None, new_pos=None):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        open = queue.Queue()
        closed = set()
        open.put((i, j))
        while not open.empty():
            x, y = open.get()
            closed.add((x, y))
            for d in directions:
                new_x, new_y = x + d[0], y + d[1]
                if (new_x, new_y) in closed or self.is_obstacle(new_x, new_y, moved, old_pos, new_pos):
                    continue
                if self.map_getter(new_x, new_y) == map_dict["character"]:
                    return True
                open.put((new_x, new_y))
        return False
    
    def search_from_target_to_character(self, i, j):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        open = queue.Queue()
        open_next = queue.Queue()
        found = False
        found_next = False
        closed = set()
        open.put((i, j))
        open_next.put((i, j))
        while (not open.empty()) and (not open_next.empty()):
            if not found:
                x, y = open.get()
                closed.add((x, y))
                for d in directions:
                    new_x, new_y = x + d[0], y + d[1]
                    next_x, next_y = new_x + d[0], new_y + d[1]
                    if (new_x, new_y) in closed or self.is_obstacle(new_x, new_y) or self.is_obstacle(next_x, next_y):
                        continue
                    if self.map_getter(new_x, new_y) == map_dict["character"]:
                        found = True
                    open.put((new_x, new_y))
                    open_next.put((next_x, next_y))
            elif not found_next:
                x, y = open_next.get()
                closed.add((x, y))
                for d in directions:
                    new_x, new_y = x + d[0], y + d[1]
                    if (new_x, new_y) in closed or self.is_obstacle(new_x, new_y):
                        continue
                    if self.map_getter(new_x, new_y) == map_dict["character"]:
                        found_next = True
                    open_next.put((new_x, new_y))
            else:
                return True
        return False
