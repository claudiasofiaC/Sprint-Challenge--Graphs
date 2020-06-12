from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# dft seems best
class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def check(self):
        if self.size() > 0:
            return self.stack[-1]
        else: return None
    def size(self):
        return len(self.stack)

# dict: opposite directions
# used to leave the current room we are in
new_entry = {'n' : 's', 's' : 'n', 'w' : 'e', 'e' : 'w'}


# new stack to keep track of rooms visited and direction taken
stackity = Stack()
# visited rooms and direction
visited = {}
# push first element in stack
stackity.push((player.current_room, None))
while stackity.size() > 0:
    # check element on top of stack
    current = stackity.check()
    room = current[0]
    direction_taken = current[1]
    # if not in visited, add a new set for new entry
    if room.id not in visited:
        visited[room.id] = set()
    # if direction already taken, add to visited
    if direction_taken:
        visited[room.id].add(direction_taken)
    # visited all rooms!
    if len(visited) == len(room_graph):
        break
    # available directions, not yet add to visited
    unexplored_paths = [i for i in room.get_exits() if i not in visited[room.id]]
    # if ther are still unexplored directions from current room
    if len(unexplored_paths) > 0:
        # picks a random unexplored direction from current room
        direction = random.choice(unexplored_paths)
        # add that to room.id in visited
        visited[room.id].add(direction)
        # push to stack
        # add direction to new room from previous room
        stackity.push((room.get_room_in_direction(direction), new_entry[direction]))
        # add direction to traversal_path
        traversal_path.append(direction)
    else:
        # when there are no more unexplored paths, we go in reverse (dft)
        traversal_path.append(direction_taken)
        # remove last element from stack 
        stackity.pop()


#print(traversal_path)

# got as low as 986 moves!

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
#player.current_room.print_room_description(player)
#while True:
#    cmds = input("-> ").lower().split(" ")
#    if cmds[0] in ["n", "s", "e", "w"]:
#        player.travel(cmds[0], True)
#    elif cmds[0] == "q":
#        break
#    else:
#        print("I did not understand that command.")
