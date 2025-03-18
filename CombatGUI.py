import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QListWidget, QComboBox
from PyQt5.QtCore import Qt, QRect, QTimer
from PyQt5.QtGui import QColor, QPainter, QPixmap, QFont

import Combat


class CombatGrid(QWidget):

    def __init__(self):
        super().__init__()


        self.tile_size = 80 # in pixels
        self.grid_width = 12
        self.grid_height = 12

        self.screen_width = self.tile_size * self.grid_width
        self.screen_height = self.tile_size * self.grid_height

        self.setGeometry(100, 100, self.screen_width, self.screen_height)
        self.setFixedSize(self.screen_width, self.screen_height)

        self.setMouseTracking(True)

        self.selected_unit = None
        self.current_turn_unit = None

        self.unitlist = Combat.create_unitlist()

        self.game_tick()


    def game_tick(self):
        while self.current_turn_unit == None:
            self.unitlist, turnup = Combat.initiative_tick(self.unitlist)
            # for unit in self.unitlist:
            #     print(unit['name'], unit['initiative'])
            if turnup == True:
                self.current_turn_unit = self.unitlist[0]
                self.current_turn_unit['move_points'] = 1
                self.current_turn_unit['action_points'] = 2
                print(f"It is {self.current_turn_unit['name']}'s Turn!")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.draw_grid(painter)
        self.draw_units(painter)

        if self.selected_unit:
            self.draw_possible_moves(painter)

    def draw_units(self, painter):
        for unit in self.unitlist:
            rect = QRect(unit['pos_x'] * self.tile_size, unit['pos_y'] * self.tile_size, self.tile_size, self.tile_size)
            color = QColor(255, 0, 0) if unit['team'] >= 1 else QColor(0, 0, 255)
            painter.setBrush(color)
            painter.drawRect(rect)

            ### add an if to check their team color so we can draw black text on the red team and white text on the blue team
            ### also maybe a way to highlight whose turn it is?
            font = QFont("Arial", 10, QFont.Bold)
            painter.setFont(font)
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(rect, 5, f"{unit['name']}\nHP: {unit['current_hp']}")

            if unit == self.selected_unit:
                select_rect = QRect(unit['pos_x'] * self.tile_size + 30, unit['pos_y'] * self.tile_size + 30, self.tile_size // 4, self.tile_size // 4)
                select_color = QColor(255, 255, 255)
                painter.setBrush(select_color)
                painter.drawRect(select_rect)
    def draw_grid(self, painter):
        for x in range(0, self.screen_width, self.tile_size):
            for y in range(0, self.screen_height, self.tile_size):
                rect = QRect(x, y, self.tile_size, self.tile_size)
                painter.setPen(QColor(0, 0, 0))
                painter.drawRect(rect)

    def draw_possible_moves(self, painter):
        x, y = self.selected_unit['pos_x'], self.selected_unit['pos_y']
        possible_moves = self.calculate_possible_moves(self.selected_unit)

        for move in possible_moves:
            rect = QRect(move[0] * self.tile_size, move[1] * self.tile_size, self.tile_size, self.tile_size)
            painter.setPen(QColor(0, 255, 0))
            painter.setBrush(QColor(0, 255, 0, 100))
            painter.drawRect(rect)

    def mousePressEvent(self, event):
        x, y = event.x() // self.tile_size, event.y() // self.tile_size
        #print(x, y)

        if self.selected_unit == self.current_turn_unit:
            possible_moves = self.calculate_possible_moves(self.selected_unit)
            self.update()
            if (x, y) in possible_moves:
                self.selected_unit['pos_x'], self.selected_unit['pos_y'] = x, y
                self.selected_unit['move_points'] = self.selected_unit['move_points'] - 1
                self.update()
                
                if self.current_turn_unit['move_points'] == 0:
                    self.current_turn_unit['wait'] = True
                    self.current_turn_unit['initiative'] = Combat.end_initiative(self.current_turn_unit)
                    print(self.current_turn_unit['initiative'])
                    self.current_turn_unit = None
                    self.selected_unit = None
                    self.game_tick()
            else:
                if self.is_tile_occupied(x, y):
                    print("Tile is occupied!")
                else:
                    print("Tile is out of range!")
        elif self.selected_unit is not None and self.selected_unit is not self.current_turn_unit:
            print(f"Not {self.selected_unit['name']}'s Turn!")
            self.selected_unit = None
            self.update()
        else:
            for unit in self.unitlist:
                if unit['pos_x'] == x and unit['pos_y'] == y:
                    self.selected_unit = unit
                    self.update()
                    break
    
    def calculate_possible_moves(self, unit):
        possible_moves = []

        ### Need to add unit base movement distance
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if abs(dx) + abs(dy) <= 3:
                    nx, ny = unit['pos_x'] + dx, unit['pos_y'] + dy

                    if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height and not self.is_tile_occupied(nx, ny):
                        possible_moves.append((nx, ny))
        return possible_moves
    
    def is_tile_occupied(self, x, y):
        for unit in self.unitlist:
            if unit['pos_x'] == x and unit['pos_y'] == y:
                return True
        return False

                


class CombatGUITest(QWidget):

    def __init__(self):
        super().__init__()
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = CombatGrid()
    window.show()

    sys.exit(app.exec_())