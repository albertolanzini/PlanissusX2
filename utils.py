import numpy as np

def get_neighboring_cells(grid, cell, radius=2):
    current_x, current_y = cell.position
    neighboring_cells = []
    # Getting the dimensions using np.shape
    grid_shape = np.shape(grid)
    for i in range(max(0, current_x - radius), min(grid_shape[0], current_x + radius + 1)):
        for j in range(max(0, current_y - radius), min(grid_shape[1], current_y + radius + 1)):
            if (i, j) != (current_x, current_y) and grid[i][j].type != 'water':
                neighboring_cells.append(grid[i][j])
    return neighboring_cells

def count_ground_cells(grid):
    count = 0
    for row in grid:
        for cell in row:
            if cell.type == 'ground':
                count += 1
    return count