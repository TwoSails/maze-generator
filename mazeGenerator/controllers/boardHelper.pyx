def getIdx(int row, int col, int width, int height):
    if row > height or col > width or row < 0 or col < 0:
        return -1
    return row * width + col

def getNeighbourIndexes(int row, int col, int width, int height):
    cdef int neighbours[4]
    cdef int delta_row, delta_col, idx
    cdef int neighbour_row, neighbour_col, cellIdx
    cdef int relative_coords[4][2]
    cdef int coord[2]

    relative_coords[0][:] = [1, 0]
    relative_coords[1][:] = [-1, 0]
    relative_coords[2][:] = [0, 1]
    relative_coords[3][:] = [0, -1]

    for idx in range(4):
        delta_row = relative_coords[idx][0]
        delta_col = relative_coords[idx][1]
        neighbour_row = (row + delta_row) % height
        neighbour_col = (col + delta_col) % width

        if abs(neighbour_row - row) > 1 or abs(neighbour_col - col) > 1:
            neighbours[idx] = -1
            continue

        neighbours[idx] = getIdx(neighbour_row, neighbour_col, width, height)

    return neighbours