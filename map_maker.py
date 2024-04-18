import numpy as np
import random
from utils import *

class map_maker:
    def __init__(self, size=8, sizeL=16):
        self.size = size
        self.sizeL = sizeL
        self.map = [0] * sizeL * sizeL
        self.assigned = [False] * size * size
        self.available_pos = [(i, j) for i in range(1, size - 1) for j in range(1, size - 1)]
        state.open = PriorityQueue()
        state.closed = set()

    def map_getter(self, x, y):
        return self.map[(x + self.size // 2) * self.sizeL + (y + self.size // 2)]
    
    def map_setter(self, x, y, value):
        self.map[(x + self.size // 2) * self.sizeL + (y + self.size // 2)] = value
        if x > 0 and x < self.size - 1 and y > 0 and y < self.size - 1 and not self.assigned[x * self.size + y]:
            self.available_pos.remove((x, y))
        self.assigned[x * self.size + y] = True

    def has_been_assigned(self, x, y):
        return self.assigned[x * self.size + y]
    
    def is_obstacle(self, x, y):
        if x == 0 or x == self.size - 1 or y == 0 or y == self.size - 1:
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

    def generate_box(self):
        box_pos = random.sample(self.available_pos, self.target_cnt)
        for pos in box_pos:
            self.map_setter(pos[0], pos[1], map_dict["box"])

    def generate_character(self):
        character_pos = random.choice(self.available_pos)
        self.map_setter(character_pos[0], character_pos[1], map_dict["character"])

    def check_solvable(self):
        max_step = int(1e6)
        nmap = numeral_map(self.map, self.sizeL)
        start_state = state(nmap, 0, start=True)
        found = False
        for i in range(max_step):
            found, no_solution = start_state.explore()
            if found or no_solution:
                break
        if not found:
            print("Unsolvable map, regenerating...")
        return found

        # row_to_check = []
        # col_to_check = []

        # for i in range(1, self.size - 1):
        #     for j in range(1, self.size - 1):
        #         if self.map_getter(i, j) == map_dict["box"]:
        #             if self.map_getter(i - 1, j) == map_dict["wall"]:
        #                 row_to_check.append(i - 1)
        #             if self.map_getter(i + 1, j) == map_dict["wall"]:
        #                 row_to_check.append(i + 1)
        #             if self.map_getter(i, j - 1) == map_dict["wall"]:
        #                 col_to_check.append(j - 1)
        #             if self.map_getter(i, j + 1) == map_dict["wall"]:
        #                 col_to_check.append(j + 1)
                    
        #             obs_up = self.is_obstacle(i - 1, j)
        #             obs_down = self.is_obstacle(i + 1, j)
        #             obs_left = self.is_obstacle(i, j - 1)
        #             obs_right = self.is_obstacle(i, j + 1)
        #             if (obs_up and obs_left) or (obs_up and obs_right) or (obs_down and obs_left) or (obs_down and obs_right):
        #                 return False
        #         elif self.map_getter(i, j) == map_dict["target"]:
        #             pass

        # for i in row_to_check:
        #     feasible = False
        #     for j in range(2, self.size - 1):
        #         if (not self.is_obstacle(i, j)) and (not self.is_obstacle(i, j - 1)):
        #             feasible = True
        #             break
        #     if not feasible:
        #         return False
            
        # for j in col_to_check:
        #     feasible = False
        #     for i in range(2, self.size - 1):
        #         if (not self.is_obstacle(i, j)) and (not self.is_obstacle(i - 1, j)):
        #             feasible = True
        #             break
        #     if not feasible:
        #         return False
        
        # return True
    
    def generate_map(self):
        print("Generating map...")
        self.generate_wall()
        self.generate_target()
        self.generate_box()
        self.generate_character()
        while not self.check_solvable():
            self.map = [0] * self.sizeL * self.sizeL
            self.assigned = [False] * self.size * self.size
            self.available_pos = [(i, j) for i in range(1, self.size - 1) for j in range(1, self.size - 1)]
            self.generate_wall()
            self.generate_target()
            self.generate_box()
            self.generate_character()
        print("Generated map successfully!")
        return self.map

if __name__ == "__main__":
    m = map_maker()
    m.generate_map()
    for i in range(m.size):
        for j in range(m.size):
            print(m.map_getter(i, j), end=" ")
        print()
