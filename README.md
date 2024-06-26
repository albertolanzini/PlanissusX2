This simulation involves a grid with two types of animals, Erbasts and Carvizs, which are grouped into herds
and prides respectively. The simulation is visualized using matplotlib and can be interacted with in various
ways.

The simulation is initialized with a grid of cells, each of which can contain animals and vegetation. 
The animals are grouped into herds and prides at the start of the simulation using the groupAnimalsStart 
function in dailyOperations.py.

The animals in the simulation are instances of the Animal class, with Erbast and Carviz as subclasses. 
Each animal has energy, a lifetime, and a social attitude. Animals can join or leave groups, expend energy, 
age, and die. When an animal dies, it may spawn offspring.

Groups of animals are represented by the Group class, with Herd and Pride as subclasses. 
Each group has a maximum size, a threshold, and a list of members. Animals can join or leave groups.

It is possible to change the values of the simulation, such as grid dimension, number of animals, etc. 
through the Constants.py file.

When you run the main.py script a UI will open up that lets you choose between interactive and automatic mode:
- Choose interactve mode for a deep analysis of the ecosystem. In interactive mode the user will manually 
  progress the simulation during initialization mode (by pressing the space bar). The user can also check
  the content of single cells just by clicking on them.
- Choose automatic mode to see the natural development of the ecosystem. It must be noted that, while in
  automatic mode, the user can pause the simulation and check the content of the cells or join god mode.

While in God Mode, the user can select a different animal type to generate:
- By pressing 'h', the user will be able to generate herds by clicking on a ground cell in the grid
- By pressing 'p', the user will be able to generate prides by clicking on a ground cell in the grid.

During the simulation, directions on how to use the god mode, or information about the current mode the 
user is in, as well as the information about the cells the user is clicking on, or about the herds/prides
they are generating while in god mode, will be printed out through the terminal. Keep a look on that!

The plots shown are:
1. Vegetob density plot that shows the vegetation density within a range 0-100.
2. Animal presence plot that shows the Erbast to Carviz ratio.
3. A population plot that shows the total population of the simulation over time.
4. An energy plot that shows the average energy of the animals in the simulation over time.

Start the simulation by running the main.py file from the terminal.

Make sure to stop the simulation by pressing the stop simulation button in the top left of the window.
