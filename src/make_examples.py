#!/usr/bin/env python3
import glob

from gray_code import GrayCode, from_json
from plot import plot


def main():
    files = glob.glob("examples/*.json")
    print(files)
    gray_codes = []
    for f in files:
        print(f)
        with open(f, "r", encoding="utf-8") as json_file:
            g = from_json(json_file.read())
            output_file = f.removesuffix(".json") + ".gif"
            gray_codes.append((g, output_file.removeprefix("examples").strip("\/"))) # Remove current directory from filename
            plot(g, output_file)
    with open("examples/README.md", "w", encoding="utf-8") as md_file:
        md_file.write("# Example Single Track Gray Codes\n")
        md_file.write("| Visualization | Sensor Positions | Track | Position Lookup Table |\n")
        md_file.write("| ---- | ---- | ---- | ---- |\n")
        for (g, visualization) in gray_codes:
            sensors = ', '.join(str(i) for i in g.sensor_positions)
            track = f"{g.track:0{g.n_track}b}"
            lookup = "TODO"
            image = f'<img src="{visualization}" alt="Animation" width="400" height="400">'
            md_file.write(f"| {image} | {sensors} | {track} | {lookup} |\n")



if __name__ == "__main__":
    main()