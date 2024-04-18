import numpy as np
from queue import PriorityQueue

map_dict = {"background": 0, "wall": 1, "target": 2, "box": 3, "character": 4, "box_inplace": 5, "character_inplace": 6}

def manhattan_distance(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])

def min_manhattan_distance_sum(x_list, y_list):
    return sum(min(manhattan_distance(x, y) for y in y_list) for x in x_list)

class numeral_map:
    def __init__(self, game_map, size):
        self.map = game_map.copy()
        self.size = size

        try:
            character_pos = self.map.index(map_dict["character"])
        except:
            character_pos = self.map.index(map_dict["character_inplace"])
        self.character_pos = [character_pos // self.size, character_pos % self.size]
        # self.boxes_pos = []
        # self.targets_pos = []
        # for i in range(self.size):
        #     for j in range(self.size):
        #         if self.map_getter(i, j) == map_dict["box"]:
        #             self.boxes_pos.append([i, j])
        #         elif self.map_getter(i, j) == map_dict["target"]:
        #             self.targets_pos.append([i, j])
        #         elif self.map_getter(i, j) == map_dict["box_inplace"]:
        #             self.boxes_pos.append([i, j])
        #             self.targets_pos.append([i, j])

    def move(self, dx, dy):
        current_pos = self.character_pos
        current_tile = self.map_getter(current_pos[0], current_pos[1])
        forward_pos = [self.character_pos[0] + dx, self.character_pos[1] + dy]
        forward_tile = self.map_getter(forward_pos[0], forward_pos[1])
        forward2_pos = [forward_pos[0] + dx, forward_pos[1] + dy]
        forward2_tile = self.map_getter(forward2_pos[0], forward2_pos[1])

        if forward_tile == map_dict["wall"]:
            return False
        elif forward_tile == map_dict["box"]:
            if forward2_tile == map_dict["wall"] or forward2_tile == map_dict["box"] or forward2_tile == map_dict["box_inplace"]:
                return False
            if forward2_tile == map_dict["target"]:
                self.map_setter(forward2_pos[0], forward2_pos[1], map_dict["box_inplace"])
            else:
                self.map_setter(forward2_pos[0], forward2_pos[1], map_dict["box"])
            self.map_setter(forward_pos[0], forward_pos[1], map_dict["character"])
            self.character_pos = forward_pos
            # box_idx = self.boxes_pos.index(forward_pos)
            # self.boxes_pos[box_idx] = forward2_pos
        elif forward_tile == map_dict["box_inplace"]:
            if forward2_tile == map_dict["wall"] or forward2_tile == map_dict["box"] or forward2_tile == map_dict["box_inplace"]:
                return False
            if forward2_tile == map_dict["target"]:
                self.map_setter(forward2_pos[0], forward2_pos[1], map_dict["box_inplace"])
            else:
                self.map_setter(forward2_pos[0], forward2_pos[1], map_dict["box"])
            self.map_setter(forward_pos[0], forward_pos[1], map_dict["character_inplace"])
            self.character_pos = forward_pos
            # box_idx = self.boxes_pos.index(forward_pos)
            # self.boxes_pos[box_idx] = forward2_pos
        elif forward_tile == map_dict["target"]:
            self.map_setter(forward_pos[0], forward_pos[1], map_dict["character_inplace"])
            self.character_pos = forward_pos
        else:
            self.map_setter(forward_pos[0], forward_pos[1], map_dict["character"])
            self.character_pos = forward_pos

        if current_tile == map_dict["character"]:
            self.map_setter(current_pos[0], current_pos[1], map_dict["background"])
        elif current_tile == map_dict["character_inplace"]:
            self.map_setter(current_pos[0], current_pos[1], map_dict["target"])

        return True

    def map_getter(self, x, y):
        return self.map[x * self.size + y]
    
    def map_setter(self, x, y, value):
        self.map[x * self.size + y] = value

    def check_win(self):
        # for box_pos in self.boxes_pos:
        #     if self.map_getter(box_pos[0], box_pos[1]) != map_dict["box_inplace"]:
        #         return False
        # return True

        for i in range(self.size):
            for j in range(self.size):
                if self.map_getter(i, j) == map_dict["box"] or self.map_getter(i, j) == map_dict["target"]:
                    return False
        return True

class state:
    step_cost = 0.001
    # step_cost = 0
    # all_states = []
    open = PriorityQueue()
    closed = set()

    def __init__(self, nmap, cost, start=False):
        # self.nmap = copy.deepcopy(nmap)
        self.nmap = numeral_map(nmap.map, nmap.size)
        self.character_pos = tuple(self.nmap.character_pos)
        self.boxes_pos = ()
        self.targets_pos = ()
        for i in range(self.nmap.size):
            for j in range(self.nmap.size):
                if self.nmap.map_getter(i, j) == map_dict["box"]:
                    self.boxes_pos += ((i, j),)
                elif self.nmap.map_getter(i, j) == map_dict["target"]:
                    self.targets_pos += ((i, j),)
                elif self.nmap.map_getter(i, j) == map_dict["box_inplace"]:
                    self.boxes_pos += ((i, j),)
                    self.targets_pos += ((i, j),)
        # self.hueristic = min_manhattan_distance_sum(self.nmap.boxes_pos, self.nmap.targets_pos)
        # self.hueristic = min_manhattan_distance_sum(nmap.boxes_pos, nmap.targets_pos)
        self.hueristic = min_manhattan_distance_sum(self.boxes_pos, self.targets_pos)
        self.cost = cost
        self.f = self.cost + self.hueristic
        self.parent = None
        self.move_from_parent = None
        self.move_to_solution = None
        self.child = None
        if start:
            # state.all_states.append(self)
            state.open.put(self)

    def __eq__(self, other):
        return self.boxes_pos == other.boxes_pos and self.character_pos == other.character_pos
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __gt__(self, other):
        return self.f > other.f
    
    def __hash__(self):
        return hash(self.boxes_pos + self.character_pos)
    
    def found_solution(self):
        return self.nmap.check_win()
    
    # @staticmethod
    # def explore():
    #     new_states = []
    #     fs = []
    #     choices = [[0, -1], [0, 1], [-1, 0], [1, 0]]
    #     found_solution = False
    #     for s in state.all_states:
    #         for choice in choices:
    #             # new_numeral_map = copy.deepcopy(s.nmap)
    #             new_numeral_map = numeral_map(s.nmap.map, s.nmap.size)
    #             if new_numeral_map.move(choice[0], choice[1]):
    #                 new_state = state(new_numeral_map, s.cost + state.step_cost)
    #                 if new_state in state.all_states:
    #                     continue
    #                 new_state.parent = s
    #                 new_state.move_from_parent = choice
    #                 if new_state.found_solution():
    #                     st = new_state
    #                     while st.parent:
    #                         st.parent.move_to_solution = st.move_from_parent
    #                         st.parent.child = st
    #                         st = st.parent
    #                     found_solution = True
    #                     return found_solution
    #                 new_states.append(new_state)
    #                 fs.append(new_state.f)
    #     fmin_idx = np.argmin(np.array(fs))
    #     state.all_states.append(new_states[fmin_idx])

    @staticmethod
    def explore():
        choices = [[0, -1], [0, 1], [-1, 0], [1, 0]]
        found_solution = False
        no_solution = False
        if state.open.empty():
            no_solution = True
            return found_solution, no_solution
        st = state.open.get()
        while st in state.closed:
            if state.open.empty():
                no_solution = True
                return found_solution, no_solution
            st = state.open.get()
        state.closed.add(st)

        for choice in choices:
            new_numeral_map = numeral_map(st.nmap.map, st.nmap.size)
            if new_numeral_map.move(choice[0], choice[1]):
                new_state = state(new_numeral_map, st.cost + state.step_cost)
                new_state.parent = st
                new_state.move_from_parent = choice
                if new_state.found_solution():
                    s = new_state
                    while s.parent:
                        s.parent.move_to_solution = s.move_from_parent
                        s.parent.child = s
                        s = s.parent
                    found_solution = True
                    return found_solution, no_solution
                state.open.put(new_state)

        return found_solution, no_solution
    
    # def generate_childs(self):
    #     choices = [[0, -1], [0, 1], [-1, 0], [1, 0]]
    #     found_solution = False
    #     for choice in choices:
    #         new_numeral_map = copy.deepcopy(self.nmap)
    #         if new_numeral_map.move(choice[0], choice[1]):
    #             new_state = state(new_numeral_map, self.cost + state.step_cost)
    #             new_state.parent = self
    #             new_state.move_from_parent = choice
    #             self.children.append(new_state)

    #             found_solution = new_state.found_solution()
    #             if found_solution:
    #                 s = new_state
    #                 while s.parent:
    #                     s.parent.move_to_solution = s.move_from_parent
    #                     s = s.parent
    #     return found_solution

if __name__ == "__main__":
    m = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 1, 1, 3, 0, 3, 2, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 2, 0, 3, 4, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 1, 1, 1, 3, 1, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    size = 16
    start_state = state(numeral_map(m, size), 0)
    print(start_state.hueristic)
  