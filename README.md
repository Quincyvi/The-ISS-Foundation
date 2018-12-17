# Before running the program:
install the libraries shown in the requirements.txt file

# Running the program:
+ For Cargo list1 and list2 run:
    - python3 space_freight.py ('Algorithm') ('List')('Spacecraft_update')
    - eg. python3 space_freight.py hill_with_outliers List2 spacecraft_update
+ for Cargo list3 run space_freight3.py

# Visualizations 
visualisation of the results (graphs) are shown in the Visualization folder

# Presentation
http://prezi.com/iqk9zoafex3u/?utm_campaign=share&utm_medium=copy

# The-ISS-Foundation
Project

State Space for:
+ Constraint relaxation:
  + CargoList1:
      4^100
  + CargoList2:
      4^100
  + max cargoList3:
      90^1000
spacecraft with least space (Cygnus)
+ Upper Bound:
  + CargoList1:
      5^100
  + CargoList2:
      5^100
  + CargoList3:
      6^1000

## Algorithms used:
+ Greedy
+ Random
+ Hill Climbing

### Max number of parcels that can be shipped with the 4 spacecrafts
#### Calculated with sum of total payload mass and sum of total payload volume minus total mass parcels and total volume parcels:
+ Cargo List1: 97 parcels
+ Cargo List2: 92 parcels
##### The max amount of parcels our algorithms calculated with the current data:
+ Cargo List1: 96 parcels (greedy)
+ Cargo List2: 88 parcels (hill climbing)

### All parcels will be shipped and multiple spacecrafts will be used
+ Cargo List3: 1000 parcels

+ Max used spacecrafts: 90 (Cygnus x 90)
+ Min used spacecrafts: 24 (Verne_ATV x 24)
