import heapq

GOAL_STATE = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)

INITIAL_STATE = (0, 1, 3,
                 4, 2, 5,
                 7, 8, 6)

def manhattan_distance(state, goal=GOAL_STATE):
    """Heuristic h(n): total Manhattan grid distances of misplaced tiles."""
    distance = 0
    for index, tile in enumerate(state):
        if tile == 0:
            continue
        goal_index = goal.index(tile)
        row1, col1 = divmod(index, 3)
        row2, col2 = divmod(goal_index, 3)
        distance += abs(row1 - row2) + abs(col1 - col2)
    return distance

def get_neighbors(state):
    """Generate all adjacent states by shifting tiles into the blank space."""
    neighbors = []
    zero_index = state.index(0)
    row, col = divmod(zero_index, 3)

    moves = {
        'UP': (row - 1, col),
        'DOWN': (row + 1, col),
        'LEFT': (row, col - 1),
        'RIGHT': (row, col + 1)
    }

    for move, (r, c) in moves.items():
        if 0 <= r < 3 and 0 <= c < 3:
            new_index = r * 3 + c
            new_state = list(state)
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
            neighbors.append((move, tuple(new_state)))
    return neighbors

def print_state(state):
    for i in range(0, 9, 3):
        row = state[i:i + 3]
        print(" ".join(str(x) if x != 0 else "_" for x in row))
    print()

def a_star_search(start, goal):
    counter = 0
    g_score = {start: 0}
    f_start = manhattan_distance(start, goal)
    frontier = [(f_start, counter, start, [start])]
    heapq.heapify(frontier)
    visited = set()
    nodes_expanded = 0

    while frontier:
        f, _, current, path = heapq.heappop(frontier)

        if current in visited:
            continue
        visited.add(current)
        nodes_expanded += 1

        if current == goal:
            return path, g_score[current], nodes_expanded

        for _, neighbor in get_neighbors(current):
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score = tentative_g + manhattan_distance(neighbor, goal)
                counter += 1
                heapq.heappush(frontier, (f_score, counter, neighbor, path + [neighbor]))
    return None, None, nodes_expanded

if __name__ == "__main__":
    print("=========================================")
    print(" 8-TILE PROBLEM : A* SEARCH")
    print("=========================================\n")

    print("Initial State:")
    print_state(INITIAL_STATE)

    print("Goal State:")
    print_state(GOAL_STATE)

    solution_path, cost, expanded = a_star_search(INITIAL_STATE, GOAL_STATE)

    if solution_path:
        print(f"Solution found in {cost} moves")
        print(f"Nodes expanded: {expanded}\n")
        print("Path from Initial State to Goal State:\n")
        for step, state in enumerate(solution_path):
            print(f"Step {step}:")
            print_state(state)
        print(f"PATH COST g(n) (Total number of moves) = {cost}")
    else:
        print("No solution found.")
