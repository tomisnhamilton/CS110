#Function to take a comma seperated value (csv) file and return a 2D list from it's contents
def initialize(filename):
    world_map = []
    # Opens the File
    file = open(filename, "r")
    contents = file.read()
    lines = contents.split('\n')
   # Creates the Grid Locations in the File
    for line in lines:
        row = line.split(',')
        world_map.append(row)
    return world_map
