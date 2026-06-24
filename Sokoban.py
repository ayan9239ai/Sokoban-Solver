import os
import time
import sys
from collections import deque

def print_final_solution(solution):
    print("\nFinal Solution Path:")
    print(" -> ".join(solution))

class Sokoban:
    def __init__(self, level_str):
        width_part, data = level_str.split(':')
        self.width = int(width_part)
        self.initial_grid = list(data)
        self.grid = list(data)
        self.height = len(self.grid) // self.width

    def get_pos(self, index):
        return index % self.width, index // self.width

    def get_idx(self, x, y):
        return y * self.width + x

    def find_player(self, grid_state):
        for i, tile in enumerate(grid_state):
            if tile in ('@', '+'):
                return i % self.width, i // self.width
        return None

    def is_win_a(self, grid_state):
        return '.' not in grid_state and '+' not in grid_state
    
    def is_win(self):
        # Win if no goals (.) and no player-on-goals (+) remain uncovered by boxes
        return '.' not in self.grid and '+' not in self.grid


    def move(self, grid, dx, dy):
        """Returns a NEW grid state after a move, or None if move is impossible."""
        new_grid = list(grid)
        px, py = self.find_player(new_grid)
        nx, ny = px + dx, py + dy
        bx, by = px + 2*dx, py + 2*dy

        curr_idx = self.get_idx(px, py)
        next_idx = self.get_idx(nx, ny)
        
        # if not (0 <= nx < self.width and 0 <= ny < self.height): return None
        # target = new_grid[next_idx]
        if (next_idx > len(self.grid)):
            return None# Out of bounds
        target = new_grid[next_idx]

        if target in (' ', '.'):
            new_grid[next_idx] = '+' if target == '.' else '@'
            new_grid[curr_idx] = '.' if grid[curr_idx] == '+' else ' '
            return new_grid

        elif target in ('$', '*'):
            if not (0 <= bx < self.width and 0 <= by < self.height): return None
            behind_idx = self.get_idx(bx, by)
            behind_target = new_grid[behind_idx]
            
            if behind_target in (' ', '.'):
                new_grid[behind_idx] = '*' if behind_target == '.' else '$'
                new_grid[next_idx] = '+' if target == '*' else '@'
                new_grid[curr_idx] = '.' if grid[curr_idx] == '+' else ' '
                return new_grid
        return None

    def solve(self):
        start_state = tuple(self.initial_grid)
        queue = deque([(start_state, "")])
        visited = {start_state}
        
        dirs = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}

        while queue:
            curr_state, path = queue.popleft()
            if self.is_win_a(curr_state): return path

            for char, (dx, dy) in dirs.items():
                next_state = self.move(curr_state, dx, dy)
                if next_state:
                    t_state = tuple(next_state)
                    if t_state not in visited:
                        visited.add(t_state)
                        queue.append((t_state, path + char))
        return None

    def draw(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for y in range(self.height):
            print("".join(self.grid[y * self.width : (y + 1) * self.width]))
        
        if self.is_win():
            print("\nLevel Clear!")
            print_final_solution(solution)
            sys.exit()

    def playback(self, lurd):
        for move_char in lurd:
            self.draw()
            print(f"\nExecuting: {move_char}  | Full Path: {lurd}")
            time.sleep(0.4)
            dirs = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}
            dx, dy = dirs[move_char]
            self.grid = self.move(self.grid, dx, dy)
        self.draw()
        # print(f"Solution found: {lurd}")
        # print("\nLevel Clear!")


    def get_input():
        if os.name == 'nt':
            import msvcrt
            key = msvcrt.getch().decode('utf-8').lower()
            return key
        else:
            import tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch.lower()

# --- EXECUTION ---
# if __name__ == "__main__":
# Example 1 Level
# level = "7:#  ####@ $ #. # $  .####   #"
level = input("Enter the Sokoban level (format: width:data): ")
game = Sokoban(level)

if input("Do you want to solve the level automatically? (y/n): ").lower() == 'y':
    solution = game.solve()
    if solution:
        game.playback(solution)
    else:
        print("No solution found.")
else:
    solution = []  # Clear solution path for manual play
    while True:
        game.draw()
        cmd = Sokoban.get_input()
        # if cmd == 'w': game.grid = game.move(game.grid, 0, -1) or game.grid
        # elif cmd == 's': game.grid = game.move(game.grid, 0, 1) or game.grid
        # elif cmd == 'a': game.grid = game.move(game.grid, -1, 0) or game.grid
        # elif cmd == 'd': game.grid = game.move(game.grid, 1, 0) or game.grid
        # elif cmd == 'q': break
        if cmd == 'w' :
            game.grid = game.move(game.grid, 0, -1) or game.grid
            solution.append('U')
        elif (cmd == 's') :
            game.grid = game.move(game.grid, 0, 1) or game.grid
            solution.append('D')
        elif cmd == 'a':
            game.grid = game.move(game.grid, -1, 0) or game.grid
            solution.append('L')
        elif cmd == 'd':
            game.grid = game.move(game.grid, 1, 0) or  game.grid
            solution.append('R')
        elif cmd == 'q':
            break
        else:
            game.grid = game.grid  # No change for invalid input, just redraw