import copy
import math
import queue
import random

from entities.Tile import Tile


class StateTree:

    def __init__(self, depth, start_state, player):
        self.depth = depth
        self.start_state = start_state
        self.player = player

    def minimax(self, node, depth, alpha, beta, minmax):
        if depth == 0 or not node.generate_children(self.player):
            return node.get_static_evaluation()

        if not minmax:
            max_eva = -math.inf

            for child in node.children:
                eva = self.minimax(child, depth - 1, alpha, beta, True)

                max_eva = max(max_eva, eva)
                alpha = max(alpha, max_eva)

                if beta <= alpha:
                    break

            return max_eva
        else:
            min_eva = math.inf
            for child in node.children:
                eva = self.minimax(child, depth - 1, alpha, beta, False)
                min_eva = min(min_eva, eva)
                beta = min(beta, eva)
                if beta <= alpha:
                    break
            return min_eva

    def get_next(self):
        if self.start_state.count_available_places() == 0:
            return None

        if not self.start_state.generate_children(self.player):
            return None

        if self.start_state.minmax:
            return min(self.start_state.children,
                       key=lambda child: self.minimax(child, self.depth, -math.inf, math.inf, not self.start_state.minmax))
        else:
            return max(self.start_state.children,
                       key=lambda child: self.minimax(child, self.depth, -math.inf, math.inf, not self.start_state.minmax))


class State:

    def __init__(self, parent, cells, minmax):
        self.parent = parent
        self.cells = cells
        self.minmax = minmax
        self.children = []
        self.alpha = -math.inf
        self.beta = math.inf
        self.cells_number = len(self.cells)
        self.processed = False

    def generate_children(self, player):
        if self.count_available_places() == 0:
            return False

        self.children.clear()

        blocked_coords = []

        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                if j != len(self.cells[i]) - 1 and self.cells[i][j].tile is None and self.cells[i][j + 1].tile is None:
                    if (i == 3 and j == 2) or (i == 3 and j == 3):
                        continue

                    if self.cells[i][j].blocked or self.cells[i][j + 1].blocked:
                        blocked_coords.append([(j, i), (j + 1, i)])
                        continue

                    self.children.append(self.generate_to((j, i), (j + 1, i), Tile.RED))
                    self.children.append(self.generate_to((j, i), (j + 1, i), Tile.GREEN))
                    self.children.append(self.generate_to((j, i), (j + 1, i), Tile.BLUE))
                    self.children.append(self.generate_to((j, i), (j + 1, i), Tile.YELLOW))

                if i != len(self.cells[i]) - 1 and self.cells[i][j].tile is None and self.cells[i + 1][j].tile is None:
                    if (i == 2 and j == 3) or (i == 3 and j == 3):
                        continue

                    if self.cells[i][j].blocked or self.cells[i + 1][j].blocked:
                        blocked_coords.append([(j, i), (j, i + 1)])
                        continue

                    self.children.append(self.generate_to((j, i), (j, i + 1), Tile.RED))
                    self.children.append(self.generate_to((j, i), (j, i + 1), Tile.GREEN))
                    self.children.append(self.generate_to((j, i), (j, i + 1), Tile.BLUE))
                    self.children.append(self.generate_to((j, i), (j, i + 1), Tile.YELLOW))

        if len(self.children) > 50:
            self.children = random.sample(self.children, 50)
        elif len(self.children) == 0:
            if player.blocked:
                for blocked_coord in blocked_coords:
                    self.children.append(self.generate_to(blocked_coord[0], blocked_coord[1], Tile.RED))
                    self.children.append(self.generate_to(blocked_coord[0], blocked_coord[1], Tile.GREEN))
                    self.children.append(self.generate_to(blocked_coord[0], blocked_coord[1], Tile.BLUE))
                    self.children.append(self.generate_to(blocked_coord[0], blocked_coord[1], Tile.YELLOW))
            else:
                return False

        return True

    def generate_to(self, pos1, pos2, color):
        new_sheet = copy.deepcopy(self.cells)

        new_sheet[pos1[1]][pos1[0]].tile = color
        new_sheet[pos2[1]][pos2[0]].tile = color

        return State(self, new_sheet, not self.minmax)

    def get_min(self):
        return min(map(lambda state: state.get_static_value(), self.children))

    def get_max(self):
        return max(map(lambda state: state.get_static_value(), self.children))

    def count_available_places(self):
        available_places = 0

        for i in range(self.cells_number):
            for j in range(self.cells_number - 1):
                if (i == 3 and j == 2) or (i == 3 and j == 3):
                    continue

                if self.cells[i][j].tile is None and self.cells[i][j + 1].tile is None:
                    available_places += 1

                if self.cells[j][i].tile is None and self.cells[j + 1][i].tile is None:
                    available_places += 1
        return available_places

    def count_sections(self):
        processed = set()
        section_count = 0

        for y in range(self.cells_number):
            for x in range(self.cells_number):
                if self.cells[y][x] in processed:
                    continue

                processed.add(self.cells[y][x])

                if self.cells[y][x].tile is None:
                    continue

                section_count += 1
                section_queue = queue.Queue()
                section_queue.put(self.cells[y][x])

                while not section_queue.empty():
                    cell = section_queue.get()
                    processed.add(cell)

                    if cell.pos[0] != 0:
                        left_cell = self.cells[cell.pos[1]][cell.pos[0] - 1]

                        if left_cell.tile is not None and left_cell not in processed and cell.tile == left_cell.tile:
                            section_queue.put(left_cell)

                    if cell.pos[1] != 0:
                        top_cell = self.cells[cell.pos[1] - 1][cell.pos[0]]

                        if top_cell.tile is not None and top_cell not in processed and cell.tile == top_cell.tile:
                            section_queue.put(top_cell)

                    if cell.pos[0] != self.cells_number - 1:
                        right_cell = self.cells[cell.pos[1]][cell.pos[0] + 1]

                        if right_cell.tile is not None and right_cell not in processed and cell.tile == right_cell.tile:
                            section_queue.put(right_cell)

                    if cell.pos[1] != self.cells_number - 1:
                        bottom_cell = self.cells[cell.pos[1] + 1][cell.pos[0]]

                        if bottom_cell.tile is not None and bottom_cell not in processed and cell.tile == bottom_cell.tile:
                            section_queue.put(bottom_cell)

        return section_count

    def get_static_evaluation(self):
        return self.count_sections() + self.count_available_places()

