import matplotlib.pyplot as plt

def create_track_coordinates(num_tracks, track_width):
    coordinates = []
    for i in range(num_tracks):
        start_x = i * track_width
        end_x = start_x + track_width
        coordinates.append([(start_x, 1), (start_x, 6)])
        coordinates.append([(end_x, 1), (end_x, 6)])
    return coordinates

def plot_tracks(coordinates, route):
    fig, ax = plt.subplots()
    for i, coord in enumerate(coordinates):
        if i % 2 == 0:
            ax.plot([coord[0][0], coord[1][0]], [coord[0][1], coord[1][1]], 'b-')
        else:
            ax.plot([coord[0][0], coord[1][0]], [coord[0][1], coord[1][1]], 'r-')

    x_pos = 0
    y_pos = 3.5
    for i in route:
        if i % 2 == 0:
            ax.annotate(str(i // 2), (x_pos, y_pos), color='b', ha='center', va='center')
            x_pos += 0.5
            ax.plot([x_pos - 0.5, x_pos], [y_pos, y_pos], 'b-')
        else:
            ax.annotate(str((i + 1) // 2), (x_pos, y_pos), color='r', ha='center', va='center')
            x_pos += 0.5
            ax.plot([x_pos, x_pos - 0.5], [y_pos, y_pos], 'r-')

    ax.set_xlim(-0.5, x_pos + 0.5)
    ax.set_ylim(0, 8)
    ax.set_xlabel('Track')
    ax.set_ylabel('Position')
    ax.set_title('Truck Routing')
    ax.set_aspect('equal')
    plt.show()

# Example usage
num_tracks = 5
track_width = 2
solution = [2, 1, 3, 4, 5]

coordinates = create_track_coordinates(num_tracks, track_width)
plot_tracks(coordinates, solution)
