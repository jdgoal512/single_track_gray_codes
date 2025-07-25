#!/usr/bin/env python3
import itertools
import math
import sys

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib import animation

from gray_code import GrayCode, from_json

def plot(g: GrayCode, output_filename: str="", color: str="#202020", show: bool=False):
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    center = (0.5, 0.5)
    radius = 0.362

    # center_circle
    center_circle = mpatches.Circle(center, 0.3, fill=True, color=color)
    ax.add_patch(center_circle)

    display_track = [(value=="1", len(list(group))) for value, group in itertools.groupby(f"{g.track:0{g.n_track}b}")][::-1]
    angle_index = 0
    arc_size = 360/g.n_track
    start = 180 + arc_size/2 # Start at left side
    frame = 0
    track_arcs = []
    for (track_value, length) in display_track:
        print(length, angle_index, arc_size)
        if track_value:
            track_section = mpatches.Wedge(
                center,
                radius,
                theta1=start - angle_index - (frame+length)*arc_size,
                theta2=start - angle_index - frame*arc_size,
                fill=True,
                color=color)
            track_arcs.append((angle_index, length, track_section))
            ax.add_patch(track_section)
        angle_index += length*arc_size
    sensor_radius = 0.38
    print(g.sensor_positions)
    sensor_circles = {}
    for sensor in g.sensor_positions:
        sensor_angle = 180 - sensor*360/g.n_track
        sensor_x = sensor_radius*math.cos(math.radians(sensor_angle)) + 0.5
        sensor_y = sensor_radius*math.sin(math.radians(sensor_angle)) + 0.5
        print((sensor_x, sensor_y))
        color = "#0000FF"
        if g.check_sensor(sensor, frame):
            color = "#FF0000"
        sensor_circle = mpatches.Circle((sensor_x, sensor_y), 0.01, fill=True, color=color)
        sensor_circles[sensor] = sensor_circle
        ax.add_patch(sensor_circle)
    # frame = 0
    display_track = f"{g.track:0{g.n_track}b}"[::-1]
    display_track = display_track[frame:] + display_track[:frame]
    display_track = "".join(f"\033[93m{j}\033[0m" if i in g.sensor_positions else f"{j}" for i, j in enumerate(display_track))
    print(display_track)
    def update(frame):
        for (angle_index, length, track_section) in track_arcs:
            # track_section.set_theta1(start + angle_index - frame*arc_size)
            # track_section.set_theta2(start + angle_index - (length+frame)*arc_size)

            track_section.set_theta1(start - angle_index - (frame + length)*arc_size)
            track_section.set_theta2(start - angle_index - frame*arc_size)
        frame = (g.n_track - frame)%g.n_track # We go backwards to go clockwise
        for sensor, sensor_circle in sensor_circles.items():
            color = "#0000FF"
            if g.check_sensor(sensor, frame):
                color = "#FF0000"
            sensor_circle.set_color(color)

        display_track = f"{g.track:0{g.n_track}b}"[::-1]
        display_track = display_track[frame:] + display_track[:frame]
        display_track = "".join(f"\033[93m{j}\033[0m" if i in g.sensor_positions else f"{j}" for i, j in enumerate(display_track))
        print(display_track)
    plt.axis('off')
    plt.tight_layout()
    ani = animation.FuncAnimation(fig=fig, func=update, frames=g.n_track, interval=300)
    if output_filename:
        ani.save(output_filename)
    if show:
        plt.show()

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} GRAY_CODE_JSON")
        sys.exit()
    json_filename = sys.argv[1]
    with open(json_filename) as json_file:
        json_text = json_file.read()
        g = from_json(json_text)
        output_file = json_filename.removesuffix(".json") + ".gif"
        plot(g, output_file, show=True)


if __name__ == "__main__":
    main()