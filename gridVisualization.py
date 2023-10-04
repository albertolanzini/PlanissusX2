import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.widgets import Button
from rich import print
import sys
import time

from Constants import *
from Animals import *
from main import daily_actions
from dailyOperations import *

def normalize_rgb(rgb):
    return tuple(color/255 for color in rgb)

class GridVisualizer:
    def __init__(self, grid):
        self.grid = grid
        self.fig, self.axs = plt.subplots(2, 2, figsize=(15, 10))
        self.vegetob_density_grid = np.zeros((len(grid), len(grid[0])))
        self.animal_presence_grid = np.zeros((len(grid), len(grid[0])))
        self.day_count = 1
        self.mode = 'initialization'
        self.interactive = False
        self.delay = 1

        self.im_vegetob_density = None
        self.im_animal_presence = None

        self.erbast_population = []
        self.carviz_population = []

        self.erbast_energy = []
        self.carviz_energy = []

        self.new_animal_type = None

        self.paused = False
        self.pause_button_ax = self.fig.add_axes([0.8, 0.025, 0.1, 0.04])
        self.pause_button = Button(self.pause_button_ax, 'Pause/Resume')
        self.pause_button.color = normalize_rgb((173, 216, 230))
        self.pause_button.on_clicked(self.toggle_pause)

        self.god_mode_button_ax = self.fig.add_axes([0.7, 0.025, 0.1, 0.04]) 
        self.god_mode_button = Button(self.god_mode_button_ax, 'God Mode')
        self.god_mode_button.color = normalize_rgb((255, 255, 0))
        self.god_mode_button.on_clicked(self.enter_god_mode)

        self.init_mode_button_ax = self.fig.add_axes([0.6, 0.025, 0.1, 0.04]) 
        self.init_mode_button = Button(self.init_mode_button_ax, 'Initialization Mode')
        self.init_mode_button.color = normalize_rgb((0, 175, 0))
        self.init_mode_button.on_clicked(self.enter_init_mode)

        self.stop_button_ax = self.fig.add_axes([0.1, 0.95, 0.1, 0.04])  
        self.stop_button = Button(self.stop_button_ax, 'Stop Simulation')
        self.stop_button.color = normalize_rgb((242, 24, 90))
        self.stop_button.on_clicked(self.stop_simulation)

        self.speed_up_button_ax = self.fig.add_axes([0.1, 0.025, 0.1, 0.04])  
        self.speed_up_button = Button(self.speed_up_button_ax, 'Speed Up')
        self.speed_up_button.color = normalize_rgb((7, 232, 116))
        self.speed_up_button.on_clicked(self.speed_up)

        self.slow_down_button_ax = self.fig.add_axes([0.2, 0.025, 0.1, 0.04]) 
        self.slow_down_button = Button(self.slow_down_button_ax, 'Slow Down')
        self.slow_down_button.color = normalize_rgb((255, 80, 80))
        self.slow_down_button.on_clicked(self.slow_down)

        self.setup_visuals()

    def speed_up(self, event):
        # Decrease delay, but don't let it go below 0.02
        self.delay = max(self.delay - 0.1, 0.02) 
    
    def slow_down(self, event):
        self.delay += 0.05

    def stop_simulation(self, event):
        plt.close(self.fig)
        time.sleep(0.2)
        sys.exit()

    def toggle_pause(self, event):
        self.paused = not self.paused
        if self.paused:
            print("[bold blue]Simulation paused.[/bold blue]")
        else:
            self.mode = 'initialization'
            print("[bold blue]Simulation resumed. Switching back to initialization mode.[/bold blue]")

    def enter_god_mode(self, event):
        if (not self.interactive and self.paused) or self.interactive:
            self.mode = 'god mode'
            print("""[bold yellow]Switching to god mode.[/bold yellow]
        [bold]Generate herds[/bold] by pressing [bold]h[/bold] and clicking on the desidered cell.
        [bold]Generate prides[/bold] by pressing [bold]p[/bold] and clicking on the desidered cell.
      """)

    def enter_init_mode(self, event):
        if (not self.interactive and self.paused) or self.interactive:
            self.mode = 'initialization'
            print("[bold green]Switching to initialization mode.[/bold green]")

    def get_animal_presence_grid(self):
        animal_presence_grid = np.zeros((len(self.grid), len(self.grid[0])))
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                cell = self.grid[i][j]
                if cell.type == 'ground':
                    cell_carviz_count = sum(1 for animal in cell.inhabitants if isinstance(animal, Carviz) and not animal.dead)
                    cell_erbast_count = sum(1 for animal in cell.inhabitants if isinstance(animal, Erbast) and not animal.dead)
                    total_animals = cell_carviz_count + cell_erbast_count

                    if total_animals > 0:
                        carviz_ratio = cell_carviz_count / total_animals
                        erbast_ratio = cell_erbast_count / total_animals
                        animal_presence_grid[i][j] = carviz_ratio + 2 * erbast_ratio
                    else:
                        animal_presence_grid[i][j] = 0
        return animal_presence_grid

    def setup_visuals(self):
        self.axs[0, 0].set_title('Erbast and Carviz Population')
        self.axs[0, 0].set_xlabel('Day')
        self.axs[0, 0].set_ylabel('Population')

        cmap = mcolors.LinearSegmentedColormap.from_list(
        "Custom", [(0, 'purple'), (0.5, 'white'), (1, 'green')], N=256
        )

        self.im_vegetob_density = self.axs[0, 1].imshow(self.vegetob_density_grid, cmap=cmap, vmin=-100, vmax=100)
        self.axs[0, 1].set_title('Vegetob Density')

        self.im_animal_presence = self.axs[1, 1].imshow(self.animal_presence_grid, cmap='bwr', vmin=0, vmax=2)
        self.axs[1, 1].set_title('Animal Presence')

        self.fig.colorbar(self.im_vegetob_density, ax=self.axs[0, 1], orientation='vertical')
        cbar = self.fig.colorbar(self.im_animal_presence, ax=self.axs[1, 1], ticks=[0, 1, 2], orientation='vertical')
        cbar.ax.set_yticklabels(['0', '1', '2'])

        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def update_and_visualize(self):
        erbast_count = 0
        carviz_count = 0

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                cell = self.grid[i][j]
                if cell.type == 'ground':
                    density = cell.vegetob.get_density()
                    self.vegetob_density_grid[i][j] = -density if cell.vegetob.poisonous else density


                    cell_carviz_count = sum(1 for animal in cell.inhabitants if isinstance(animal, Carviz) and not animal.dead)
                    cell_erbast_count = sum(1 for animal in cell.inhabitants if isinstance(animal, Erbast) and not animal.dead)

                    carviz_count += cell_carviz_count
                    erbast_count += cell_erbast_count

                    total_animals = cell_carviz_count + cell_erbast_count

                    if total_animals > 0:
                        carviz_ratio = cell_carviz_count / total_animals
                        erbast_ratio = cell_erbast_count / total_animals
                        self.animal_presence_grid[i][j] = carviz_ratio + 2 * erbast_ratio
                    else:
                        self.animal_presence_grid[i][j] = 0

        self.erbast_population.append(erbast_count)
        self.carviz_population.append(carviz_count)

        self.axs[0, 0].clear()
        self.axs[0, 0].set_title('Erbast and Carviz Population')
        self.axs[0, 0].plot(self.erbast_population, color='blue', label='Erbast')
        self.axs[0, 0].plot(self.carviz_population, color='red', label='Carviz')
        self.axs[0, 0].legend()

        window_size = 10  # size of the sliding window
        recent_erbast_population = self.erbast_population[-window_size:] if len(self.erbast_population) > window_size else self.erbast_population
        recent_carviz_population = self.carviz_population[-window_size:] if len(self.carviz_population) > window_size else self.carviz_population
        max_recent_population = max(max(recent_erbast_population), max(recent_carviz_population))
        self.axs[0, 0].set_ylim([0, max_recent_population * 2.5])


        erbast_energy = sum(animal.energy for row in self.grid for cell in row for animal in cell.inhabitants if isinstance(animal, Erbast) and not animal.dead)
        carviz_energy = sum(animal.energy for row in self.grid for cell in row for animal in cell.inhabitants if isinstance(animal, Carviz) and not animal.dead)

        self.erbast_energy.append(erbast_energy / erbast_count if erbast_count > 0 else 0)
        self.carviz_energy.append(carviz_energy / carviz_count if carviz_count > 0 else 0)

        self.axs[1, 0].clear()
        self.axs[1, 0].plot(self.erbast_energy, color='blue', label='Erbast')
        self.axs[1, 0].plot(self.carviz_energy, color='red', label='Carviz')
        self.axs[1, 0].set_title('Average Energy')
        self.axs[1, 0].set_xlabel('Day')
        self.axs[1, 0].set_ylabel('Energy')
        self.axs[1, 0].legend()

        self.im_vegetob_density.set_data(self.vegetob_density_grid)
        self.axs[0, 1].set_title('Vegetob Density')

        self.im_animal_presence.set_data(self.animal_presence_grid)
        self.axs[1, 1].set_title('Animal Presence')

        plt.draw()

    def visualize(self, delay, interactive):
        self.interactive = interactive
        self.speed_up_button_ax.set_visible(not interactive)
        self.slow_down_button_ax.set_visible(not interactive)
        self.pause_button_ax.set_visible(not interactive)
        self.delay = delay
        if interactive:
            plt.show()
        else:
            while self.day_count <= NUM_DAYS:
                if not self.paused:
                    daily_actions(self.grid)
                    self.update_and_visualize()
                    self.day_count += 1
                    plt.pause(self.delay)
                else:
                    # Wait for a short period before checking the paused state again
                    plt.pause(0.2)
            plt.show()
                


    def on_key(self, event):
        if self.mode == 'initialization' and not self.interactive:
            return

        if self.mode == 'initialization':

            if event.key == ' ':
        
                if self.day_count <= NUM_DAYS:
                        
                    daily_actions(self.grid)
                        
                    self.update_and_visualize()
                    self.day_count += 1
                    
        elif (self.mode == 'god mode' and self.paused and not self.interactive) or (self.mode == 'god mode' and not self.paused and self.interactive):
            if event.key == 'h':
                self.new_animal_type = 'herd'
                print("Ready to add a new herd. Click on a cell.")
            elif event.key == 'p':
                self.new_animal_type = 'pride'
                print("Ready to add a new pride. Click on a cell.")
            elif event.key == 'i':
                self.mode = 'initialization'
                print("Switching back to initialization mode.")

    def on_click(self, event):
        if event.inaxes == self.axs[0, 1] or event.inaxes == self.axs[1, 1]:
            i = int(event.ydata + 0.5)
            j = int(event.xdata + 0.5)
            cell = self.grid[i][j]


            if self.mode == 'god mode':

                if cell.type == 'ground':
                    # Generate a random number of animals
                    num_animals = np.random.randint(1, MAX_SIZE)

                    if self.new_animal_type == 'herd':
                        actual_n = 0
                        new_herd = Herd()
                        new_herd.setThreshold(0)
                        new_herd.cell = cell
                        for i in range(num_animals):
                            # Make sure the newly generated animals do not exceed the max number per cell
                            if cell.count_erbast() >= 20:
                                if not new_herd.members and new_herd in cell.herds:
                                    cell.herds.remove(new_herd)
                                return
                            
                            energy = random.randint(50, 80)
                            lifetime = random.randint(50, 100)
                            social_attitude = random.random()
                            new_animal = Erbast(energy, lifetime, social_attitude, cell)
                            new_animal.join_group(new_herd)

                            actual_n += 1

                            cell.inhabitants.add(new_animal)

                        print(f"[bold green]Added a new herd with {num_animals} Erbasts at ({i}, {j})[/bold green]")

                    elif self.new_animal_type == 'pride':
                        actual_n = 0
                        new_pride = Pride()
                        new_pride.setThreshold(0)
                        new_pride.cell = cell
                        for i in range(num_animals):
                            # Make sure the newly generated animals do not exceed the max number per cell
                            if cell.count_carviz() >= 20:
                                if not new_pride.members:
                                    cell.prides.remove(new_pride)
                                return
                            
                            energy = random.randint(50, 80)
                            lifetime = random.randint(50, 100)
                            social_attitude = random.random()
                            new_animal = Carviz(energy, lifetime, social_attitude, cell)
                            new_animal.join_group(new_pride)

                            cell.inhabitants.add(new_animal)

                            actual_n += 1
                        
                        print(f"[bold yellow]Added a new pride with {actual_n} Carvizs at ({i}, {j})[/bold yellow]")

                else:
                    print("In God Mode [bold red]you can only add Animals to a Ground cell[/bold red], not to a water cell")
                
            elif self.mode == 'initialization':

                print(f"Cell at ({i}, {j})")
                print(f"Type: {cell.type}")
                if cell.type == 'ground':
                    print(f"Vegetob density: {cell.vegetob.get_density()}")
                    print(f"Vegetob is poisonous: {'Yes' if cell.vegetob.poisonous else 'No'}")

                    erbast_count = sum(1 for animal in cell.inhabitants if isinstance(animal, Erbast) and not animal.dead)
                    carviz_count = sum(1 for animal in cell.inhabitants if isinstance(animal, Carviz) and not animal.dead)

                    print(f"Erbast count: {erbast_count}")
                    print(f"Carviz count: {carviz_count}")

                    erbast_count = 0
                    carviz_count = 0

                    for animal in cell.inhabitants:
                        if isinstance(animal, Erbast) and not animal.dead:
                            erbast_count += 1
                            print(f"Erbast {erbast_count}, ID: {animal.id}, age: {animal.age}, lifetime: {animal.lifetime}, herd: {animal.herd.id}, energy: {animal.energy}")
                        elif isinstance(animal, Carviz) and not animal.dead:
                            carviz_count += 1
                            print(f"Carviz {carviz_count},ID: {animal.id}, age: {animal.age}, lifetime: {animal.lifetime}, pride: {animal.pride.id}, energy: {animal.energy}")