import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt, QTimer

class TacticsGameGrid(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tactics Game Grid")
        self.setGeometry(100, 100, 600, 600)

        # Create a central widget and set the layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a grid layout with reduced spacing and margins
        grid_layout = QGridLayout()
        grid_layout.setSpacing(1)  # Reduce spacing between tiles
        grid_layout.setContentsMargins(1, 1, 1, 1)  # Reduce margins around the grid
        central_widget.setLayout(grid_layout)

        # Create a 12x12 grid of tiles
        self.tiles = []
        for row in range(12):
            for col in range(12):
                tile = QPushButton()
                tile.setFixedSize(40, 40)  # Set the size of each tile
                tile.setStyleSheet("background-color: lightgray; border: 1px solid black;")  # Default tile appearance
                grid_layout.addWidget(tile, row, col)
                self.tiles.append(tile)

        # Connect the button click event to a slot
        for tile in self.tiles:
            tile.clicked.connect(self.on_tile_click)

        # Track unit positions
        self.unit_positions = {}  # Key: (row, col), Value: dict with unit data

        # Create the first Warrior (Team A)
        self.place_unit("Warrior A", "red", 100, 0, 0)  # Place at (0, 0)

        # Create the second Warrior (Team B)
        self.place_unit("Warrior B", "blue", 100, 11, 11)  # Place at (11, 11)

        # Initialize turn system
        self.current_turn = "Team A"  # Start with Team A's turn
        self.selected_unit = None  # Track the currently selected unit
        self.update_status_bar()

        # Timer for enemy AI
        self.ai_timer = QTimer(self)
        self.ai_timer.timeout.connect(self.enemy_turn)
        self.ai_timer.start(1000)  # Trigger enemy AI every 1 second

    def place_unit(self, name, color, hp, row, col):
        """Place a unit on the grid at the specified row and column."""
        # Check if the tile is already occupied
        if (row, col) in self.unit_positions:
            print(f"Tile ({row}, {col}) is already occupied!")
            return

        # Update the tile to display the unit
        tile = self.tiles[row * 12 + col]
        tile.setText(f"{name}\n{hp} HP")
        tile.setStyleSheet(f"background-color: {color}; font-size: 10px; color: white; border: 1px solid black;")

        # Store unit data
        self.unit_positions[(row, col)] = {"name": name, "color": color, "hp": hp, "team": "A" if color == "red" else "B"}

    def on_tile_click(self):
        """Handle tile click events."""
        if self.current_turn != "Team A":  # Only allow Team A to click
            return

        button = self.sender()
        index = self.tiles.index(button)
        row = index // 12
        col = index % 12

        # Check if the clicked tile is occupied
        if (row, col) in self.unit_positions:
            unit = self.unit_positions[(row, col)]
            if unit["team"] == "A":
                # Select the unit if it belongs to Team A
                self.selected_unit = (row, col)
                self.highlight_valid_tiles()  # Highlight valid movement and attack tiles
                print(f"Selected {self.current_turn}'s {unit['name']} at ({row}, {col})")
            elif self.selected_unit:
                # If an enemy unit is clicked and a friendly unit is selected, attack it
                if self.is_within_attack_range(self.selected_unit, row, col):
                    self.attack_unit(self.selected_unit, (row, col))
                    self.clear_highlights()  # Clear highlights after attacking
                    self.end_turn()  # End the turn after attacking
                else:
                    print(f"Enemy unit is out of attack range!")
            else:
                print(f"Cannot select {self.current_turn}'s opponent's unit!")
            return

        # If a unit is selected, try to move it
        if self.selected_unit:
            if self.is_within_move_range(self.selected_unit, row, col):
                # Check if the target tile is occupied
                if (row, col) in self.unit_positions:
                    print(f"Tile ({row}, {col}) is already occupied!")
                    return

                # Move the unit to the new tile
                self.move_unit(self.selected_unit, (row, col))
                self.clear_highlights()  # Clear highlights after moving
                self.end_turn()  # End the turn after moving
            else:
                print(f"Tile ({row}, {col}) is out of movement range!")
        else:
            print("No unit selected!")

    def enemy_turn(self):
        """Handle the enemy team's turn."""
        if self.current_turn != "Team B":  # Only proceed if it's Team B's turn
            return

        print("Enemy team's turn...")

        # Find all Team B units
        team_b_units = [pos for pos, unit in self.unit_positions.items() if unit["team"] == "B"]

        for unit_pos in team_b_units:
            # Find the nearest enemy unit
            nearest_enemy_pos = self.find_nearest_enemy(unit_pos)
            if not nearest_enemy_pos:
                print("No enemy units found!")
                continue

            # Move towards the nearest enemy unit
            self.move_towards(unit_pos, nearest_enemy_pos)

            # Attack if the enemy is within range
            if self.is_within_attack_range(unit_pos, nearest_enemy_pos[0], nearest_enemy_pos[1]):
                self.attack_unit(unit_pos, nearest_enemy_pos)

        # End the enemy team's turn
        self.end_turn()

    def find_nearest_enemy(self, unit_pos):
        """Find the nearest enemy unit for the given unit."""
        unit_row, unit_col = unit_pos
        nearest_enemy_pos = None
        min_distance = float("inf")

        for pos, unit in self.unit_positions.items():
            if unit["team"] != self.unit_positions[unit_pos]["team"]:  # Find enemy units
                row, col = pos
                distance = abs(unit_row - row) + abs(unit_col - col)  # Manhattan distance
                if distance < min_distance:
                    min_distance = distance
                    nearest_enemy_pos = pos

        return nearest_enemy_pos

    def move_towards(self, unit_pos, target_pos):
        """Move the unit towards the target position."""
        unit_row, unit_col = unit_pos
        target_row, target_col = target_pos

        # Calculate the direction to move
        row_diff = target_row - unit_row
        col_diff = target_col - unit_col

        # Determine the new position
        new_row = unit_row + (1 if row_diff > 0 else -1 if row_diff < 0 else 0)
        new_col = unit_col + (1 if col_diff > 0 else -1 if col_diff < 0 else 0)

        # Check if the new position is valid and within movement range
        if self.is_within_move_range(unit_pos, new_row, new_col):
            # Check if the target tile is occupied
            if (new_row, new_col) in self.unit_positions:
                print(f"Tile ({new_row}, {new_col}) is already occupied!")
                return

            # Move the unit
            self.move_unit(unit_pos, (new_row, new_col))
            print(f"Moved {self.unit_positions[(new_row, new_col)]['name']} to ({new_row}, {new_col})")

    def move_unit(self, old_pos, new_pos):
        """Move a unit from old_pos to new_pos."""
        old_row, old_col = old_pos
        new_row, new_col = new_pos

        # Get unit data
        unit = self.unit_positions[old_pos]

        # Update the old tile
        old_tile = self.tiles[old_row * 12 + old_col]
        old_tile.setText("")
        old_tile.setStyleSheet("background-color: lightgray; border: 1px solid black;")

        # Update the new tile
        new_tile = self.tiles[new_row * 12 + new_col]
        new_tile.setText(f"{unit['name']}\n{unit['hp']} HP")
        new_tile.setStyleSheet(f"background-color: {unit['color']}; font-size: 10px; color: white; border: 1px solid black;")

        # Update unit positions
        del self.unit_positions[old_pos]
        self.unit_positions[new_pos] = unit

    def attack_unit(self, attacker_pos, defender_pos):
        """Attack the target unit."""
        attacker = self.unit_positions[attacker_pos]
        defender = self.unit_positions[defender_pos]

        damage = 20  # Fixed damage value
        defender["hp"] -= damage
        print(f"{attacker['name']} attacked {defender['name']} for {damage} damage!")

        # Update the defender's HP display
        defender_tile = self.tiles[defender_pos[0] * 12 + defender_pos[1]]
        defender_tile.setText(f"{defender['name']}\n{defender['hp']} HP")

        # Check if the defender is defeated
        if defender["hp"] <= 0:
            print(f"{defender['name']} has been defeated!")
            self.remove_unit(defender_pos)

    def remove_unit(self, pos):
        """Remove a unit from the grid."""
        tile = self.tiles[pos[0] * 12 + pos[1]]
        tile.setText("")
        tile.setStyleSheet("background-color: lightgray; border: 1px solid black;")  # Reset to default
        del self.unit_positions[pos]
        print(f"Unit at {pos} has been removed.")

    def end_turn(self):
        """End the current turn and switch to the other team."""
        self.selected_unit = None  # Deselect the unit
        self.current_turn = "Team B" if self.current_turn == "Team A" else "Team A"  # Switch turns
        self.update_status_bar()
        print(f"It is now {self.current_turn}'s turn.")

    def update_status_bar(self):
        """Update the status bar to show whose turn it is."""
        self.statusBar().showMessage(f"{self.current_turn}'s turn")

    def highlight_valid_tiles(self):
        """Highlight valid movement and attack tiles for the selected unit."""
        if not self.selected_unit:
            return

        # Clear previous highlights
        self.clear_highlights()

        # Get the selected unit's position
        current_row, current_col = self.selected_unit

        # Highlight movement tiles (within 3 tiles)
        for row in range(12):
            for col in range(12):
                if self.is_within_move_range(self.selected_unit, row, col):
                    tile = self.tiles[row * 12 + col]
                    tile.setStyleSheet("background-color: lightgreen; border: 1px solid black;")  # Movement highlight

        # Highlight attack tiles (within 1 tile)
        for row in range(12):
            for col in range(12):
                if self.is_within_attack_range(self.selected_unit, row, col):
                    tile = self.tiles[row * 12 + col]
                    tile.setStyleSheet("background-color: pink; border: 1px solid black;")  # Attack highlight

    def clear_highlights(self):
        """Clear all tile highlights."""
        for tile in self.tiles:
            if (self.tiles.index(tile) // 12, self.tiles.index(tile) % 12) not in self.unit_positions:
                tile.setStyleSheet("background-color: lightgray; border: 1px solid black;")  # Reset to default

    def is_within_move_range(self, unit_pos, target_row, target_col):
        """Check if the target tile is within 3 tiles of the unit's current position."""
        current_row, current_col = unit_pos
        distance = abs(current_row - target_row) + abs(current_col - target_col)  # Manhattan distance
        return distance <= 3  # Allow movement up to 3 tiles away

    def is_within_attack_range(self, unit_pos, target_row, target_col):
        """Check if the target tile is within 1 tile of the unit's current position."""
        current_row, current_col = unit_pos
        distance = abs(current_row - target_row) + abs(current_col - target_col)  # Manhattan distance
        return distance == 1  # Allow attacking only adjacent tiles

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TacticsGameGrid()
    window.show()
    sys.exit(app.exec_())