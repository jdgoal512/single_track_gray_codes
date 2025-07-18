#!/usr/bin/env python3
from typing import List, Union, Iterator
import itertools


def is_monotonic(a, b, n) -> int:
    mask = 1
    difference = a & mask != b & mask
    for _ in range(1, n):
        mask = mask << 1
        if a & mask != b & mask:
            if difference:
                return False
            difference = True
    return difference


def is_sequential(a, b, n) -> int:
    return (a ^ b).bit_count() == 1

class GrayCode:
    def __init__(self, sensor_positions: List[int], track: int, n: int):
        self.track = track
        for s in sensor_positions:
            assert 0 <= s, "Negative sensor position"
            assert s < n, "Sensor is outside track range"
        self.sensor_positions = sensor_positions
        self.n_track = n
        self.n_sensors = len(self.sensor_positions)

    def _check_sensor(self, sensor_position: int, offset: int) -> bool:
        index = (sensor_position + offset) % self.n_track
        return self.track & 1<<index != 0

    def get_reading(self, offset: int) -> int:
        value = 0
        for i, sensor_index in enumerate(self.sensor_positions[::-1]):
            if self.track & 1 << ((sensor_index+offset)%self.n_track):
                value += 1 << i
        return value

    def check_silent(self) -> bool:
        values = []
        last_value = self.get_reading(self.n_track-1)
        for i in range(self.n_track):
            v = self.get_reading(i)
            if not is_sequential(v, last_value, self.n_sensors):
                return False
            last_value = v
            if v in values:
                return False
            values.append(self.get_reading(i))
        return True

    def check(self):
        print(f"Precision: {360/self.n_track:.2f}\u00B0")
        print(f"Not single track precision: {360/(1<<len(self.sensor_positions)):.2f}\u00B0")
        values = []
        for i in range(self.n_track):
            values.append(self.get_reading(i))

        last_value = self.get_reading(self.n_track-1)
        for i, v in enumerate(values):
            display_track = f"{self.track:0{self.n_track}b}"[::-1]
            display_track = display_track[i:] + display_track[:i]
            display_track = "".join(f"\033[93m{j}\033[0m" if i in self.sensor_positions else f"{j}" for i, j in enumerate(display_track))

            if values.count(v) == 1:
                if is_sequential(v, last_value, self.n_sensors):
                    print(f'\033[92m{v:0{self.n_sensors}b}\033[0m {display_track}')
                else:
                    print(f'\033[91m{v:0{self.n_sensors}b}\033[0m {display_track}')
            else:
                print(f'\033[91m{v:0{self.n_sensors}b}\033[0m {display_track}')
            last_value = v


def unique_permutations(elements):
    if len(elements) == 1:
        yield (elements[0],)
    else:
        unique_elements = set(elements)
        for first_element in unique_elements:
            remaining_elements = list(elements)
            remaining_elements.remove(first_element)
            for sub_permutation in unique_permutations(remaining_elements):
                yield (first_element,) + sub_permutation


def next_gray_code(sensors: List[int], n: int) -> Iterator[GrayCode]:
    """Find a Gray Code based on the a sensor configuration and track length"""
    # There cannot be a Gray Code with an odd track length
    if n % 2:
        return
    track_sequence = "1"*int(n/2) + "0"*int(n/2)
    for track in unique_permutations(track_sequence):
        track = int("".join(track), 2)
        g = GrayCode(sensors, track, n)
        if g.check_silent():
            yield g
    return


def find_gray_code(sensors: List[int], n: int) -> Union[GrayCode, None]:
    """Find a Gray Code based on the a sensor configuration and track length"""
    # There cannot be a Gray Code with an odd track length
    gray_code_generator = next_gray_code(sensors, n)
    try:
        return next(gray_code_generator)
    except StopIteration:
        return None

def find_sensor_gray_codes(n_sensors, n_track, first_only=True) -> List[GrayCode]:
    solutions = []
    for sensors in itertools.combinations(range(1, n_track), n_sensors-1):
        sensors = [0, *sensors] # Always have the first sensor be the first index to avoid duplicates
        #print(f'Trying {sensors}')
        g = find_gray_code(sensors, n_track)
        if g:
            print("Success")
            print(f"Sensors: {g.sensor_positions}")
            print(f"Track: {g.track:0{n_track}b}")
            g.check()
            solutions.append(g)
            if first_only:
                return [g]
    return solutions

def find_sensor_gray_code(n_sensors, n_track, first_only=True):
    solution = None
    for sensors in itertools.combinations(range(1, n_track), n_sensors-1):
        sensors = [0, *sensors] # Always have the first sensor be the first index to avoid duplicates
        #print(f'Trying {sensors}')
        g = find_gray_code(sensors, n_track)
        if g:
            print("Success")
            print(f"Sensors: {g.sensor_positions}")
            print(f"Track: {g.track:0{n_track}b}")
            g.check()
            solution = g
            if first_only:
                return g
    if solution == None:
        print("Failed to find match")
    return solution

def find_minimum_gray_code_by_track(n_track, first_only=True):
    for n_sensors in range(1, n_track):
        # Skip checking when there are not enough sensors
        if n_track > 1<<n_sensors:
            continue
        print(f"Checking {n_sensors} sensors")
        g = find_sensor_gray_code(n_sensors, n_track, first_only)
        if g:
            return g
    return None

def find_max_gray_code_by_sensors(n_sensors, first_only=True):
    for n_track in range((1<<n_sensors), 0, -1):
        print(f"Checking {n_track} length track")
        g = find_sensor_gray_code(n_sensors, n_track, first_only)
        if g:
            return g
    return None

# g = GrayCode([0, 2, 9], 0b100110011110000, 15)
# g.check()

# for i in [8, 15, 16, 17]:
#     print(i)
#     find_sensor_gray_code(3, i)

# find_sensor_gray_code(5, 20)


# find_minimum_gray_code_by_track(8, first_only=False)
# find_minimum_gray_code_by_track(6, first_only=False)
# find_max_gray_code_by_sensors(3)

# g = find_gray_code([1, 2, 3], 6)
# if g:
#     g.check()


# sensor_readings = [
#     0b011,
#     0b010,
#     0b000,
#     0b100,
#     0b101,
#     0b111,
# ]

# track = [
#     0b000111,
#     0b001110,
#     0b011100,
#     0b111000,
#     0b110001,
#     0b100011,
# ]

# n_track = 6
# n_sensors = 3
# long_track = 0
# for s in sensor_readings:
#     # print(s)
#     # long_track = (long_track << n_sensors) + s
#     for t in track:
#         long_track = long_track << (n_sensors + n_track)
#         long_track += (s << n_track) + t
# print(f'{long_track:0{len(sensor_readings)*len(track)}b}')

# find_gray_code([i for i in range(0, 30, 5)], 30)


# 30 segment, 5 sensors
# g = GrayCode([i for i in range(0, 30, 5)], 0b1111111111111111111111111111111111111111111111111111110000000000000000011110000001111111000000000000000000000000001111100011111111111111111110000000000000000000000000000000011000011, 30)
# g.check()

# 360 segments, 9 sensors (original)
# g = GrayCode([i for i in range(0, 360, 40)], 0b111111111111111111111111111111111111111111111111111111000000000000000001111000000111111100000000000000000000000000111110001111111111111111111000000000000000000000000000000001100001111111110000000000000000001111111111111111100011110000000000000001111110000011111100111001111000000000001110011111111000111110000000111110000001111111001111110000000000000000001100, 360)
# g.check()

for n in range(2, 60, 2):
    find_minimum_gray_code_by_track(n)
#for factor in range(2, 1<<6):
#    print(f"##### Finding {6*factor}")
#    g =  find_gray_code([i for i in range(0, 6*factor, factor)], 6*factor)
#    if g:
#        g.check()
#g = find_gray_code([i for i in range(0, 504, 56)], 504)
#if g:
#    g.check()

# g = GrayCode([0, 4, 8, 12, 16], 0b11111110001110000000, 20)



# g = GrayCode([0, 1, 2, 3, 4, 5, 6, 7, 8], 0b011000111011001110011011100011111000011110001011100011010000111010001110010011100010111000010110001010100011000000111000001110000011100000111000000110001000100011100000111100001110100011100100111000100110001100100011101000111101001110101011100101111000101110001101100011111000111111001110111011100111111000111110001111100011, 324)

# 360 segments, 9 sensors (not original)
# g = GrayCode([x for x in range(0, 360, 40)], 0b001100000000000000000011111100111111100000011111000000011111000111111110011100000000000111100111001111110000011111100000000000000011110001111111111111111100000000000000000011111111100001100000000000000000000000000000000111111111111111111100011111000000000000000000000000001111111000000111100000000000000000111111111111111111111111111111111111111111111111111111, 360)
# g.check()

