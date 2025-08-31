import numpy as np
import pygame

GRID_SIZE = 20
CELL_SIZE = 40
SCREEN_SIZE = GRID_SIZE * CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_BLUE = (0, 0, 128)
GRAY = (200, 200, 200)

START = (19, 0)
END = (0, 19)

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Wizualizacja A*")

start_img = pygame.image.load("start.jpg")
end_img = pygame.image.load("koniec.jpg")
ludzik_img = pygame.image.load("ludzik.jpg")

start_img = pygame.transform.scale(start_img, (CELL_SIZE, CELL_SIZE))
end_img = pygame.transform.scale(end_img, (CELL_SIZE, CELL_SIZE))
ludzik_img = pygame.transform.scale(ludzik_img, (CELL_SIZE, CELL_SIZE))

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

def euclidean_distance(node1, node2):
    return ((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2) ** 0.5

def calculate_all_f_values(grid):
    nodes_dict = {}
    end_node = Node(END)

    console_grid = np.copy(grid)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 5:
                continue
            node = Node((row, col))
            node.h = euclidean_distance((row, col), END)
            node.f = node.g + node.h
            nodes_dict[(row, col)] = node

            draw_grid(grid, nodes_dict)
            pygame.display.flip()
        pygame.time.delay(100)

    for row in console_grid:
        print(" ".join(map(str, row)))

    return nodes_dict, console_grid

def astar_algorithm(grid, start, end, nodes_dict, console_grid):
    open_list = []
    closed_list = set()
    start_node = nodes_dict[start]
    open_list.append(start_node)

    while open_list:
        open_list.sort(key=lambda node: node.f)
        current_node = open_list.pop(0)
        closed_list.add(current_node.position)

        if current_node.position == end:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            path.reverse()

            for pos in path[1:-1]:
                console_grid[pos] = 3
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor_pos = (current_node.position[0] + dx, current_node.position[1] + dy)
            if 0 <= neighbor_pos[0] < GRID_SIZE and 0 <= neighbor_pos[1] < GRID_SIZE:
                if grid[neighbor_pos] == 5 or neighbor_pos in closed_list:
                    continue
                neighbor_node = nodes_dict[neighbor_pos]
                new_g = current_node.g + 1

                if neighbor_node.g == 0 or new_g < neighbor_node.g:
                    neighbor_node.g = new_g
                    neighbor_node.f = neighbor_node.g + neighbor_node.h
                    neighbor_node.parent = current_node
                    if neighbor_node not in open_list:
                        open_list.append(neighbor_node)

    return None

def generate_random_grid(obstacle_chance=0.3):
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if (row, col) != START and (row, col) != END:
                if np.random.rand() < obstacle_chance:
                    grid[row, col] = 5
    return grid

def draw_grid(grid, nodes_dict):
    font = pygame.font.Font(None, 16)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = WHITE
            if grid[row][col] == 5:
                color = BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

            if (row, col) in nodes_dict:
                f_value = nodes_dict[(row, col)].f
                f_text = font.render(f"{f_value:.2f}", True, DARK_BLUE)
                text_rect = f_text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(f_text, text_rect)

def animate_path(path):
    for pos in path[1:-1]:
        screen.fill(WHITE)
        draw_grid(grid, nodes_dict)
        screen.blit(start_img, (START[1] * CELL_SIZE, START[0] * CELL_SIZE))
        screen.blit(end_img, (END[1] * CELL_SIZE, END[0] * CELL_SIZE))

        for previous_pos in path[1:path.index(pos) + 1]:
            pygame.draw.rect(screen, GREEN,
                             (previous_pos[1] * CELL_SIZE, previous_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        screen.blit(ludzik_img, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE))

        pygame.display.flip()
        pygame.time.delay(300)

    screen.fill(WHITE)
    draw_grid(grid, nodes_dict)
    screen.blit(start_img, (START[1] * CELL_SIZE, START[0] * CELL_SIZE))
    screen.blit(end_img, (END[1] * CELL_SIZE, END[0] * CELL_SIZE))
    for previous_pos in path[1:-1]:
        pygame.draw.rect(screen, GREEN,
                         (previous_pos[1] * CELL_SIZE, previous_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

def main():
    global grid, nodes_dict
    grid = generate_random_grid()

    nodes_dict, console_grid = calculate_all_f_values(grid)

    path = astar_algorithm(grid, START, END, nodes_dict, console_grid)

    if path:
        print("\nŚcieżka znaleziona!")
        font = pygame.font.Font(None, 36)
        message = "Ścieżka znaleziona!"
        text = font.render(message, True, GREEN)
        text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))

        screen.fill(WHITE)
        draw_grid(grid, nodes_dict)
        screen.blit(start_img, (START[1] * CELL_SIZE, START[0] * CELL_SIZE))
        screen.blit(end_img, (END[1] * CELL_SIZE, END[0] * CELL_SIZE))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)

        animate_path(path)
    else:
        print("\nNie znaleziono ścieżki!")
        font = pygame.font.Font(None, 36)
        message = "Nie znaleziono ścieżki!"
        text = font.render(message, True, RED)
        text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))

        screen.fill(WHITE)
        draw_grid(grid, nodes_dict)
        screen.blit(start_img, (START[1] * CELL_SIZE, START[0] * CELL_SIZE))
        screen.blit(end_img, (END[1] * CELL_SIZE, END[0] * CELL_SIZE))
        screen.blit(text, text_rect)
        pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()

