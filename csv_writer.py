import csv
import re
from pathlib import Path

output_file = Path(r"C:\Users\[name]\AppData\Roaming\.minecraft-1.8.9\skywars_ranks.csv")


def get_color(level):
    color_dict = {"None": "#AAAAAA", "Rookie": "#555555", "Iron": "#FFFFFF", "Gold": "#FFAA00", "Diamond": "#55FFFF", "Master": "#00AA00", "Legend": "#AA0000"}
    return color_dict[level]


with open(output_file, mode = 'w', newline = "") as output_scv_file:
    rank_writer = csv.writer(output_scv_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)

    rank_writer.writerow(['Date', 'Level', 'Color', 'Number of Wins'])

    input_file = Path(r"C:\Users\[name]\AppData\Roaming\.minecraft-1.8.9\title_output.txt")

    pattern = re.compile("\[(.*)]: ([a-zA-Z ]*) \/ (\d*)")
    level_pattern = re.compile("(\w*) ?(I+\w*)?")

    with open(input_file, mode = 'r') as input_read:
        for line in input_read:
            parsed_line = pattern.search(line)
            searched_level = level_pattern.search(parsed_line.group(2))
            rank_writer.writerow([parsed_line.group(1), parsed_line.group(2), get_color(searched_level.group(1)), parsed_line.group(3)])
