import numpy as np
import matplotlib.pyplot as plt
from Constants import *
from Animals import *


class GridVisualizer:
    def __init__(self, grid):
        self.grid = grid
        self.fig, self.axs = plt.subplots(2, 1, figsize=(10, 20))
        self.vegetob_density_grid = np.zeros((len(grid), len(grid[0])))
        self.animal_presence_grid = np.zeros((len(grid), len(grid[0])))
        self.day_count = 0
        self.grid_states = [{'grid': grid.copy(), 'day_count': self.day_count}]
        self.current_state_index = 0
        self.mode = 'initialization'

        self.im_vegetob_density = None
        self.im_animal_presence = None
        self.day_text = None

        self.setup_visuals()

    def setup_visuals(self):
        self.im_vegetob_density = self.axs[0].imshow(self.vegetob_density_grid, cmap='Greens', vmin=0, vmax=100)
        self.im_animal_presence = self.axs[1].imshow(self.animal_presence_grid, cmap='bwr', vmin=0, vmax=5)

        self.axs[0].set_title('Vegetob Density')
        self.axs[1].set_title('Animal Presence')

        self.fig.colorbar(self.im_vegetob_density, ax=self.axs[0], orientation='vertical')
        self.fig.colorbar(self.im_animal_presence, ax=self.axs[1], orientation='vertical')

        self.day_text = self.axs[0].text(0.45, 1.075, '', transform=self.axs[0].transAxes)

        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def update_and_visualize(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                cell = self.grid[i][j]
                if cell.type == 'ground':
                    self.vegetob_density_grid[i][j] = cell.vegetob.get_density()

                    carviz_count = sum(
                        1 for animal in cell.inhabitants if isinstance(animal, Carviz) and not animal.dead)
                    erbast_count = sum(
                        1 for animal in cell.inhabitants if isinstance(animal, Erbast) and not animal.dead)
                    total_animals = carviz_count + erbast_count

                    if total_animals > 0:
                        carviz_ratio = carviz_count / total_animals
                        erbast_ratio = erbast_count / total_animals
                        self.animal_presence_grid[i][j] = carviz_ratio + 2 * erbast_ratio
                    else:
                        self.animal_presence_grid[i][j] = 0

        self.im_vegetob_density.set_data(self.vegetob_density_grid)
        self.im_animal_presence.set_data(self.animal_presence_grid)
        self.day_text.set_text('Day: {}'.format(self.day_count))
        plt.draw()

    def visualize(self):
        plt.show()

    def on_key(self, event):
        if self.mode == 'initialization':
            if event.key == ' ':
                self.update_and_visualize()
                if self.day_count < NUM_DAYS:
                    print("-------------------------"
                          ""
                          "GIORNO NUMERO - ", self.day_count,
                          ""
                          "-------------------------")
                    # print_prides_and_herds()  # Called directly without self.
                    # age_all_animals_grow_vegetob()  # Called directly without self.
                    # print_prides_and_herds()  # Called directly without self.
                    self.day_count += 1

                    self.grid_states.append({'grid': self.grid.copy(), 'day_count': self.day_count})
                    self.current_state_index = len(self.grid_states) - 1

            elif event.key == 'n':
                self.mode = 'navigation'
                print("CAREFUL - Moving to Navigation mode")

        elif self.mode == 'navigation':
            if event.key == 'right':
                if self.current_state_index < len(self.grid_states) - 1:
                    self.current_state_index += 1
                    self.load_grid_state(self.current_state_index)

            elif event.key == 'left':
                if self.current_state_index > 0:
                    self.current_state_index -= 1
                    self.load_grid_state(self.current_state_index)

            elif event.key == 'i':
                if self.current_state_index == len(self.grid_states) - 1:
                    print("CAREFUL - Moving to initialization mode")
                    self.mode = 'initialization'
                else:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                          ""
                          "Move to the lastly stored state to move to initialization mode"
                          ""
                          "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    def load_grid_state(self, index):
        self.grid = self.grid_states[index]['grid'].copy()
        self.day_count = self.grid_states[index]['day_count']
        self.update_and_visualize()

    def on_click(self, event):
        if event.inaxes == self.axs[0] or event.inaxes == self.axs[1]:
            i = int(event.ydata + 0.5)
            j = int(event.xdata + 0.5)
            cell = self.grid[i][j]
            print(f"Cell at ({i}, {j})")
            print(f"Type: {cell.type}")
            if cell.type == 'ground':
                print(f"Vegetob density: {cell.vegetob.get_density()}")

                erbast_count = sum(1 for animal in cell.inhabitants if isinstance(animal, Erbast) and not animal.dead)
                carviz_count = sum(1 for animal in cell.inhabitants if isinstance(animal, Carviz) and not animal.dead)

                print(f"Erbast count: {erbast_count}")
                print(f"Carviz count: {carviz_count}")

                erbast_count = 0
                carviz_count = 0

                for animal in cell.inhabitants:
                    if isinstance(animal, Erbast) and not animal.dead:
                        erbast_count += 1
                        print(f"Erbast {erbast_count}, id: {animal.id} age: {animal.age}, lifetime: {animal.lifetime}")
                    elif isinstance(animal, Carviz) and not animal.dead:
                        carviz_count += 1
                        print(f"Carviz {carviz_count} age: {animal.age}, lifetime: {animal.lifetime}")
                        # print(f"Carviz {carviz_count} age: {animal.age}, lifetime: {animal.lifetime}, pride: {animal.pride.id}")


