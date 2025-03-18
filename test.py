from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QRect
import sys

class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.tile_size = 80
        self.grid_size = 12
        self.units = [
            {'x': 2, 'y': 3, 'team': 'red', 'type': 'Archer', 'has_moved': False},
            {'x': 4, 'y': 5, 'team': 'red', 'type': 'Swordsman', 'has_moved': False},
            {'x': 7, 'y': 6, 'team': 'blue', 'type': 'Archer', 'has_moved': False},
            {'x': 8, 'y': 2, 'team': 'blue', 'type': 'Swordsman', 'has_moved': False},
        ]
        self.selected_unit = None
        self.setWindowTitle("Strategy Game")
        self.setGeometry(100, 100, self.tile_size * self.grid_size, self.tile_size * self.grid_size)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_grid(painter)
        self.draw_units(painter)
        if self.selected_unit:
            self.draw_possible_moves(painter)

    def draw_grid(self, painter):
        painter.setPen(QColor(200, 200, 200))
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                rect = QRect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                painter.drawRect(rect)

    def draw_units(self, painter):
        for unit in self.units:
            rect = QRect(unit['x'] * self.tile_size, unit['y'] * self.tile_size, self.tile_size, self.tile_size)
            color = QColor(255, 0, 0) if unit['team'] == 'red' else QColor(0, 0, 255)
            painter.setBrush(color)
            painter.drawRect(rect)
            painter.drawText(rect, 0, unit['type'])

    def draw_possible_moves(self, painter):
        x, y = self.selected_unit['x'], self.selected_unit['y']
        possible_moves = self.calculate_possible_moves(x, y)

        for move in possible_moves:
            rect = QRect(move[0] * self.tile_size, move[1] * self.tile_size, self.tile_size, self.tile_size)
            painter.setPen(QColor(0, 255, 0))
            painter.setBrush(QColor(0, 255, 0, 100))
            painter.drawRect(rect)

    def calculate_possible_moves(self, x, y):
        moves = []
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if abs(dx) + abs(dy) <= 3:  # Manhattan distance
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
                        if not any(unit['x'] == new_x and unit['y'] == new_y for unit in self.units):
                            moves.append((new_x, new_y))
        return moves

    def mousePressEvent(self, event):
        x, y = event.x() // self.tile_size, event.y() // self.tile_size

        if self.selected_unit:
            possible_moves = self.calculate_possible_moves(self.selected_unit['x'], self.selected_unit['y'])
            if (x, y) in possible_moves:
                # Move the selected unit
                self.selected_unit['x'], self.selected_unit['y'] = x, y
                self.selected_unit['has_moved'] = True
                self.update()
                self.selected_unit = None  # Deselect after move

                # Check if all units have moved
                if all(unit['has_moved'] for unit in self.units):
                    self.next_turn()
        else:
            # Select a unit if none is currently selected
            for unit in self.units:
                if unit['x'] == x and unit['y'] == y and not unit['has_moved']:
                    self.selected_unit = unit
                    self.update()
                    break

    def next_turn(self):
        # Reset all units to allow movement in the next turn
        for unit in self.units:
            unit['has_moved'] = False
        self.update()  # Refresh the grid to reflect any changes

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec_())
