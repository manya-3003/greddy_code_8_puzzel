import heapq

GOAL_STATE = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)

INITIAL_STATE = (0, 1, 3,
                 4, 2, 5,
                 7, 8, 6)

def misplaced_tiles(state, goal=GOAL_STATE):
    """Heuristic h(n): number of tiles not in their goal position."""
    return sum(1 for i in range(9) if state[i] != 0 and state[i] != goal[i])

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

def greedy_best_first_search(start, goal):
    counter = 0
    frontier = [(misplaced_tiles(start, goal), counter, start, [start])]
    heapq.heapify(frontier)
    visited = set()
    nodes_expanded = 0

    while frontier:
        h, _, current, path = heapq.heappop(frontier)

        if current in visited:
            continue
        visited.add(current)
        nodes_expanded += 1

        if current == goal:
            return path, nodes_expanded

        for _, neighbor in get_neighbors(current):
            if neighbor not in visited:
                counter += 1
                heapq.heappush(
                    frontier,
                    (misplaced_tiles(neighbor, goal), counter, neighbor, path + [neighbor])
                )
    return None, nodes_expanded

if __name__ == "__main__":
    print("=========================================")
    print(" 8-TILE PROBLEM : GREEDY BEST FIRST SEARCH")
    print("=========================================\n")

    print("Initial State:")
    print_state(INITIAL_STATE)

    print("Goal State:")
    print_state(GOAL_STATE)

    solution_path, expanded = greedy_best_first_search(INITIAL_STATE, GOAL_STATE)

    if solution_path:
        print(f"Solution found in {len(solution_path) - 1} moves")
        print(f"Nodes expanded: {expanded}\n")
        print("Path from Initial State to Goal State:\n")
        for step, state in enumerate(solution_path):
            print(f"Step {step}:")
            print_state(state)
        print(f"PATH COST (Total number of moves) = {len(solution_path) - 1}")
    else:
        print("No solution found.")

