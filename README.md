# Tower Defense utilizing BF DF A* search algorithms

Self playing tower defense game that shows the different solutions created by different search algorithms.

The algorithms are used to decide the optimal tower to place at any given time given multiple types of towers with different parameters.

Since every configuration represents a turn passing, the problem turns into a search one, where we generate every possible placement of towers and search for the shortest road that gets us to the goal(defeating all the enemies)

![input](https://i.imgur.com/3c7Q06m.png)

The input file contains:
  - General game data(enemy hitpoints, number of enemies, starting points, points per turn, points per kill)
  - Tower data(identifier, cost, damage, life, range and firing cooldown)
  - The map(with "*" representing the road and "#" representing walls on which towers may be built)
  - Start and end points of the road

The program can do only one of 3 actions each turn:
  1. It can wait a turn
  2. It can build a tower
  3. Or it can sell a tower for half of its price
  

The program also calculates solution cost assuming:
  - Waiting a turn has a cost of 1
  - Building a tower has a cost equal to the tower's price
  - Selling a tower has a cost equal to half the tower's price
  
Since every iteration where an enemy reaches the end point of the road is considered a failure, waiting a turn is usually the worst move, despite it's small cost.

Additionally, the outermost tiles do not allow towers being built on them (however there is no limitation on the enemy path made out of star symbols "*")

![text](https://i.imgur.com/TAHj9kJ.png)
The program outputs a turn breakdown for every solution of every algorithm which contains:

The number of enemies left, the number of currently owned points, a vector representing the enemy path showing the current enemies and their health values, as well as a vector containing all possible spots for towers and the tower currently placed there with its parameters.
