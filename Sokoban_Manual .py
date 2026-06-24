import os
import sys

# Tile Constants
WALL = '#'
PLAYER = '@'
PLAYER_ON_GOAL = '+'
BOX = '$'
BOX_ON_GOAL = '*'
GOAL = '.'
EMPTY = ' '

class Sokoban:
    def __init__(self, level_str):
        # Parse format "Width:Data"
        width_part, data = level_str.split(':')
        self.width = int(width_part)
        self.grid = list(data)
        self.height = len(self.grid) // self.width

    def get_pos(self, index):
        return index % self.width, index // self.width

    def get_idx(self, x, y):
        return y * self.width + x

    def find_player(self):
        for i, tile in enumerate(self.grid):
            if tile in (PLAYER, PLAYER_ON_GOAL):
                return self.get_pos(i)
        return None

    def draw(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for y in range(self.height):
            line = "".join(self.grid[y * self.width : (y + 1) * self.width])
            print(line)
        
        if self.is_win():
            print("\nLevel Clear!")
            sys.exit()

    def is_win(self):
        # Win if no goals (.) and no player-on-goals (+) remain uncovered by boxes
        return GOAL not in self.grid and PLAYER_ON_GOAL not in self.grid

    def move(self, dx, dy):
        px, py = self.find_player()
        nx, ny = px + dx, py + dy  # Next position
        bx, by = px + 2*dx, py + 2*dy  # Position behind a box

        curr_idx = self.get_idx(px, py)
        next_idx = self.get_idx(nx, ny)
        behind_idx = self.get_idx(bx, by)

        if (next_idx > len(self.grid)):
            return  # Out of bounds
        target = self.grid[next_idx]

        # 1. Logic for walking into empty space or goal
        if target in (EMPTY, GOAL):
            self._update_tile(next_idx, PLAYER)
            self._update_tile(curr_idx, EMPTY, is_move_off=True)

        # 2. Logic for pushing a box
        elif target in (BOX, BOX_ON_GOAL):
            behind_target = self.grid[behind_idx]
            if behind_target in (EMPTY, GOAL):
                # Move Box
                self._update_tile(behind_idx, BOX)
                # Move Player
                self._update_tile(next_idx, PLAYER)
                # Clear old Player spot
                self._update_tile(curr_idx, EMPTY, is_move_off=True)

    def _update_tile(self, idx, type, is_move_off=False):
        """Handles the transformation of tiles (e.g., @ becomes + on goal)."""
        current = self.grid[idx]
        
        if is_move_off:
            self.grid[idx] = GOAL if current in (PLAYER_ON_GOAL, BOX_ON_GOAL) else EMPTY
        else:
            if type == PLAYER:
                self.grid[idx] = PLAYER_ON_GOAL if current in (GOAL, BOX_ON_GOAL) else PLAYER
            elif type == BOX:
                self.grid[idx] = BOX_ON_GOAL if current == GOAL else BOX

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

def main():
    # Example 1: 7 wide
    lvl = "7:#  ####@ $ #. # $  .####   #"
    max_len=len(lvl);
    game = Sokoban(lvl)
    
    while True:
        game.draw()
        cmd = get_input()
        if cmd == 'w': game.move(0, -1)
        elif cmd == 's': game.move(0, 1)
        elif cmd == 'a': game.move(-1, 0)
        elif cmd == 'd': game.move(1, 0)
        elif cmd == 'q': break

if __name__ == "__main__":
    main()