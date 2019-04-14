import random
import numpy as np

# creates two half sized mazes and glues them together
def create_track_arr(height, width):
    half_height = height // 2
    arrs = []

    # creating half mazes
    for _ in range(2):
        while True:
            arr = create_maze(half_height, width)
            if check_maze(arr):
                arrs.append(arr)
                break

    # glueing
    arrs[0][0, 1] = 1
    arrs[1][0, 1] = 1
    arrs[0][0, width - 2] = 1
    arrs[1][0, width - 2] = 1
    arrs[0] = arrs[0][::-1, :]
    arr = np.vstack(arrs)
    
    # simple track test
    arr = np.zeros((height, width), dtype='int')
    arr[1, 1:-1] = 1
    arr[-2, 1:-1] = 1
    arr[1:-1, 1] = 1
    arr[1:-1, -2] = 1
    
    return arr

# modified version of depth first search algorithm
# snice walls also take up space on the grid,
# this is not quite the same as the original
# and there are some problems :V
# too lazy to come up with a proper one
def create_maze(height, width):
    arr = np.zeros((height, width), dtype='int')
    start = (1, 1)
    end = (1, width - 2)
    # taking care of edge cases
    path = [start]
    current = path[-1]
    arr[current] = 1
    while True:
        neighbors = possible_neighbors(arr, current)
        # if end is reached, terminate
        if end in neighbors:
            current = end
            path.append(current)
            arr[current] = 1
            break
        # if there is a viable step forward, take a step
        if neighbors:
            neighbor = random.choice(neighbors)
            current = neighbor
            path.append(current)
            arr[current] = 1
        # otherwise, start backtracking
        else:
            arr[current] = -1
            path.pop()
            if not path:
                break
            current = path[-1]
    return arr

def check_maze(arr):
    # due to special cases, start and end points might not connect
    # since the failure to connect rate is low, just fix this with another attempt
    # also for a track, impose that it meets another certain condition
    # although the following if can be reduced to the latter half
    # it is left like this for readability
    return arr[1][1] != -1 and any(arr[-2, :] == 1)

def is_edge(arr, idx):
    if (idx[0] == 0 or idx[0] == arr.shape[0] - 1) or (idx[1] == 0 or idx[1] == arr.shape[1] - 1):
        return True
    else:
        return False

def is_visited(arr, idx):
    return arr[idx] == 1

def is_backtracked(arr, idx):
    return arr[idx] == -1

def no_space(arr, idx):
    neighbors = [
        (idx[0] - 1, idx[1]),
        (idx[0] + 1, idx[1]),
        (idx[0], idx[1] - 1),
        (idx[0], idx[1] + 1),
    ]
    count = 0
    for neighbor in neighbors:
        if arr[neighbor] == 1 or arr[neighbor] == -1:
            count += 1
    return count > 1

def possible_neighbors(arr, idx):
    neighbors = [
        (idx[0] - 1, idx[1]),
        (idx[0] + 1, idx[1]),
        (idx[0], idx[1] - 1),
        (idx[0], idx[1] + 1),
    ]
    for neighbor in neighbors[:]:
        if is_edge(arr, neighbor):
            neighbors.remove(neighbor)
        elif is_visited(arr, neighbor):
            neighbors.remove(neighbor)
        elif is_backtracked(arr, neighbor):
            neighbors.remove(neighbor)
        elif no_space(arr, neighbor):
            neighbors.remove(neighbor)
    return neighbors
