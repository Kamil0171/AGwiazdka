# Wizualizacja algorytmu A* za pomocą Pygame
# Ten skrypt implementuje algorytm A* do wyznaczania ścieżki i wizualizuje jego działanie za pomocą Pygame.
# Na ekranie wyświetlany jest siatka, z przeszkodami zaznaczonymi na czarno, punktem startowym na niebiesko, a końcowym na czerwono.
# Algorytm dynamicznie oblicza optymalną ścieżkę i animuje ruch wzdłuż niej.

import numpy as np
import pygame

# Stałe dotyczące rozmiaru siatki i kolorów
GRID_SIZE = 20  # Liczba komórek w każdym wierszu i kolumnie siatki
CELL_SIZE = 40  # Rozmiar komórki w pikselach
SCREEN_SIZE = GRID_SIZE * CELL_SIZE  # Całkowity rozmiar ekranu

# Definicje kolorów do wizualizacji
WHITE = (255, 255, 255)  # Białe tło
BLACK = (0, 0, 0)  # Czarny kolor dla przeszkód
RED = (255, 0, 0)  # Czerwony kolor dla punktu końcowego
GREEN = (0, 255, 0)  # Zielony kolor dla ruchu po ścieżce
DARK_BLUE = (0, 0, 128)  # Ciemny niebieski dla wartości f
GRAY = (200, 200, 200)  # Szary kolor dla linii siatki

# Pozycje punktów startowego i końcowego
START = (19, 0)
END = (0, 19)

# Inicjalizacja Pygame i ekranu
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Wizualizacja A*")

# Ładowanie obrazków dla startu, końca i reprezentacji postaci
start_img = pygame.image.load("start.jpg")
end_img = pygame.image.load("koniec.jpg")
ludzik_img = pygame.image.load("ludzik.jpg")

# Zmiana rozmiaru obrazków, aby pasowały do komórek siatki
start_img = pygame.transform.scale(start_img, (CELL_SIZE, CELL_SIZE))
end_img = pygame.transform.scale(end_img, (CELL_SIZE, CELL_SIZE))
ludzik_img = pygame.transform.scale(ludzik_img, (CELL_SIZE, CELL_SIZE))

# Klasa Node reprezentująca każdy węzeł w siatce podczas obliczeń A*
class Node:
    def __init__(self, position, parent=None):
        self.position = position  # Pozycja węzła (wiersz, kolumna)
        self.parent = parent  # Rodzic węzła do rekonstrukcji ścieżki
        self.g = 0  # Koszt dojścia do węzła startowego
        self.h = 0  # Szacunkowa odległość do węzła końcowego
        self.f = 0  # Całkowity koszt (g + h)

# Funkcja do obliczenia heurystyki (odległość euklidesowa)
def euclidean_distance(node1, node2):
    # Oblicza odległość w linii prostej między dwoma węzłami
    return ((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2) ** 0.5

# Funkcja do obliczenia wartości f dla wszystkich węzłów w siatce
def calculate_all_f_values(grid):
    nodes_dict = {}
    end_node = Node(END)  # Tworzymy węzeł dla punktu końcowego

    console_grid = np.copy(grid)  # Kopia siatki do debugowania

    # Przechodzimy po siatce i obliczamy wartości f dla każdego węzła
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 5:  # Pomijamy przeszkody
                continue
            node = Node((row, col))  # Tworzymy nowy węzeł
            node.h = euclidean_distance((row, col), END)  # Obliczamy heurystykę
            node.f = node.g + node.h  # Całkowita wartość f
            nodes_dict[(row, col)] = node  # Dodajemy węzeł do słownika

            # Rysujemy siatkę i aktualizujemy ekran
            draw_grid(grid, nodes_dict)
            pygame.display.flip()
        pygame.time.delay(100)  # Opóźnienie dla wizualizacji

    # Wypisujemy siatkę w konsoli
    for row in console_grid:
        print(" ".join(map(str, row)))

    return nodes_dict, console_grid

# Implementacja algorytmu A*
def astar_algorithm(grid, start, end, nodes_dict, console_grid):
    open_list = []  # Lista węzłów do oceny
    closed_list = set()  # Zbiór węzłów już ocenionych
    start_node = nodes_dict[start]  # Węzeł startowy
    open_list.append(start_node)  # Dodajemy węzeł startowy do listy otwartych

    while open_list:
        # Sortujemy listę otwartą według wartości f
        open_list.sort(key=lambda node: node.f)
        current_node = open_list.pop(0)  # Pobieramy węzeł z najniższą wartością f
        closed_list.add(current_node.position)  # Oznaczamy bieżący węzeł jako oceniony

        # Jeśli osiągnięto punkt końcowy, rekonstruujemy ścieżkę
        if current_node.position == end:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            path.reverse()  # Odwracamy ścieżkę, aby zaczynała się od punktu startowego

            # Oznaczamy ścieżkę w siatce
            for pos in path[1:-1]:
                console_grid[pos] = 3  # Komórki na ścieżce
            return path

        # Sprawdzamy sąsiadów bieżącego węzła (góra, dół, lewo, prawo)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor_pos = (current_node.position[0] + dx, current_node.position[1] + dy)
            # Pomijamy komórki spoza siatki lub przeszkody
            if 0 <= neighbor_pos[0] < GRID_SIZE and 0 <= neighbor_pos[1] < GRID_SIZE:
                if grid[neighbor_pos] == 5 or neighbor_pos in closed_list:
                    continue
                neighbor_node = nodes_dict[neighbor_pos]
                new_g = current_node.g + 1  # Obliczamy nową wartość g

                # Aktualizujemy wartość g i f sąsiada, jeśli znaleźliśmy lepszą ścieżkę
                if neighbor_node.g == 0 or new_g < neighbor_node.g:
                    neighbor_node.g = new_g
                    neighbor_node.f = neighbor_node.g + neighbor_node.h
                    neighbor_node.parent = current_node
                    if neighbor_node not in open_list:
                        open_list.append(neighbor_node)

    return None  # Brak ścieżki

# Funkcja generująca losową siatkę z przeszkodami
def generate_random_grid(obstacle_chance=0.3):
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)  # Inicjalizujemy pustą siatkę
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if (row, col) != START and (row, col) != END:  # Pomijamy komórki startowe i końcowe
                if np.random.rand() < obstacle_chance:  # Dodajemy losowe przeszkody
                    grid[row, col] = 5
    return grid

# Funkcja rysująca siatkę i węzły na ekranie
def draw_grid(grid, nodes_dict):
    font = pygame.font.Font(None, 16)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = WHITE  # Domyślny kolor dla pustych komórek
            if grid[row][col] == 5:  # Kolor przeszkód
                color = BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

            if (row, col) in nodes_dict:  # Wyświetlamy wartość f dla każdego węzła
                f_value = nodes_dict[(row, col)].f
                f_text = font.render(f"{f_value:.2f}", True, DARK_BLUE)
                text_rect = f_text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(f_text, text_rect)

# Funkcja animująca ruch wzdłuż ścieżki
def animate_path(path):
    for pos in path[1:-1]:
        screen.fill(WHITE)  # Czyszczenie ekranu
        draw_grid(grid, nodes_dict)  # Ponowne rysowanie siatki
        screen.blit(start_img, (START[1] * CELL_SIZE, START[0] * CELL_SIZE))  # Wyświetlanie obrazu startowego
        screen.blit(end_img, (END[1] * CELL_SIZE, END[0] * CELL_SIZE))  # Wyświetlanie obrazu końcowego

        # Rysowanie ścieżki na zielono
        for previous_pos in path[1:path.index(pos) + 1]:
            pygame.draw.rect(screen, GREEN,
                             (previous_pos[1] * CELL_SIZE, previous_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        screen.blit(ludzik_img, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE))  # Wyświetlanie postaci

        pygame.display.flip()  # Aktualizacja wyświetlania
        pygame.time.delay(300)  # Opóźnienie dla efektu animacji

    screen.fill(WHITE)  # Ostateczne czyszczenie ekranu
    draw_grid(grid, nodes_dict)
    screen.blit(start_img, (START[1] * CELL_SIZE, START[0] * CELL_SIZE))
    screen.blit(end_img, (END[1] * CELL_SIZE, END[0] * CELL_SIZE))
    for previous_pos in path[1:-1]:
        pygame.draw.rect(screen, GREEN,
                         (previous_pos[1] * CELL_SIZE, previous_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

# Główna funkcja inicjująca i uruchamiająca wizualizację A*
def main():
    global grid, nodes_dict
    grid = generate_random_grid()  # Generowanie siatki z przeszkodami

    nodes_dict, console_grid = calculate_all_f_values(grid)  # Obliczanie wartości f dla wszystkich węzłów

    path = astar_algorithm(grid, START, END, nodes_dict, console_grid)  # Uruchamianie algorytmu A*

    # Jeśli ścieżka została znaleziona, animujemy ją
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

        animate_path(path)  # Animowanie ruchu wzdłuż ścieżki
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

# Uruchomienie głównej funkcji, jeśli skrypt jest wykonywany
if __name__ == "__main__":
    main()
