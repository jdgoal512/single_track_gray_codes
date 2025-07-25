#!/usr/bin/env python3
import glob
import os

from gray_code import GrayCode, from_json, DEGREE
from plot import plot


def main():
    files = glob.glob("examples/*.json")
    print(files)
    gray_codes_by_n_sensors = {}
    for f in files:
        print(f)
        with open(f, "r", encoding="utf-8") as json_file:
            g = from_json(json_file.read())
            output_file = f.removesuffix(".json") + ".gif"
            if g.n_sensors not in gray_codes_by_n_sensors:
                gray_codes_by_n_sensors[g.n_sensors] = []
            gray_codes_by_n_sensors[g.n_sensors].append((g, output_file.removeprefix("examples").strip("\/"))) # Remove current directory from filename
            if not os.path.exists(output_file):
                plot(g, output_file)
    with open("examples/README.md", "w", encoding="utf-8") as md_file:
        md_file.write("# Example Single Track Gray Codes\n")
        for i, gray_codes in gray_codes_by_n_sensors.items():
            if i == 1:
                md_file.write("## 1 Sensor\n")
            else:
                md_file.write(f"## {i} Sensors\n")
            md_file.write("| Visualization | Number of Positions | Resolution | Sensor Positions | Track | Position Lookup Table |\n")
            md_file.write("| ---- | ---- | ---- | ---- | ---- | ---- |\n")
            for (g, visualization) in gray_codes:
                resolution = f"{360/g.n_track:0.2f}{DEGREE}"
                sensors = ', '.join(str(i) for i in g.sensor_positions)
                track = f"{g.track:0{g.n_track}b}"
                track = "<br>".join([track[i:i+15] for i in range(0, len(track), 15)])  # Split long tracks into groups of 15 character lines
                lookup_values = []
                for j in range(g.n_track):
                    lookup_values.append(f"{g.get_reading(j):0{g.n_sensors}b}")
                lookup = f"[{', '.join(lookup_values)}]"
                image = f'<img src="{visualization}" alt="Animation" width="400" height="400">'
                md_file.write(f"| {image} | {g.n_track} | {resolution} | {sensors} | {track} | {lookup} |\n")



if __name__ == "__main__":
    main()