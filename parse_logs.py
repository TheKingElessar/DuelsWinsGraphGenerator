import gzip
import re
from pathlib import Path


def format_line(date, time, current_title):
    print_line = f"[{date} {time}]: {current_title}"
    return print_line


def add_wins(old_line, wins):
    print_line = f"{old_line} / {wins}\n"
    return print_line


def find_current(next_rank, next_level):
    if next_level == "":
        next_index = duels_rank_list.index(next_rank)
        if duels_rank_list[next_index - 1] == "Legend":
            return "None"
        return duels_rank_list[next_index - 1]

    else:
        next_level = duels_rank_level_list.index(next_level)
        if duels_rank_level_list[next_level - 1] == "":
            return next_rank

        return next_rank + " " + duels_rank_level_list[next_level - 1]


duels_rank_list = ["Rookie", "Iron", "Gold", "Diamond", "Master", "Legend"]
duels_rank_level_list = ["", "I", "II", "III", "IV", "V"]

output_file = Path(r"C:\Users\[name]\AppData\Roaming\.minecraft-1.8.9\title_output.txt")

legacy_logs_folder = Path(r"C:\Users\[name]\AppData\Roaming\.minecraft\logs").glob('**/*')
logs_folder = Path(r"C:\Users\[name]\AppData\Roaming\.minecraft-1.8.9\logs").glob('**/*')  # Delete if you only have one logs location

logs_list = [x for x in legacy_logs_folder if x.is_file()] + [x for x in logs_folder if x.is_file()]  # Delete everything after the + if you only have one logs location

with output_file.open("a") as opened_output_file:
    for log_file in logs_list:
        time_pattern = re.compile("\[(\d{2}:\d{2}:\d{2})] \[Client thread\/INFO]: \[CHAT] *(\w*) (I+\w*)? ?unlocked in (\d*) more wins!")
        filename_pattern = re.compile("(\d*-\d*-\d*)-\d*.log.*")

        date = filename_pattern.search(log_file.name)
        # note that it doesn't take latest.log because that makes it harder to get the date

        if date:
            date = date.group(1)

            if log_file.suffix == ".gz":
                with gzip.open(log_file, 'rt') as unzipped_log:

                    skip_lines = 0
                    waiting = False
                    earlier_line = ""
                    total_wins = 0
                    for line in unzipped_log:

                        if waiting and skip_lines == 1:
                            total_wins_pattern = re.compile("(\d*) \/ (\d*) \(\d*\.\d*%\)")
                            found_pattern = total_wins_pattern.search(line)
                            if not found_pattern:
                                print(line)

                            total_wins = found_pattern.group(1)

                        if waiting and skip_lines == 4:
                            if "skywars" in line.lower():
                                earlier_line = add_wins(earlier_line, total_wins)
                                opened_output_file.write(earlier_line)

                            earlier_line = ""
                            skip_lines = 0
                            waiting = False

                        if waiting:
                            skip_lines += 1

                        found_string = time_pattern.search(line)

                        if found_string:
                            waiting = True
                            group3 = found_string.group(3)
                            if group3 is None:
                                group3 = ""

                            earlier_line = format_line(date, found_string.group(1), find_current(found_string.group(2), group3))

            else:
                skip_lines = 0
                waiting = False
                earlier_line = ""
                total_wins = 0
                for line in log_file.read_text():

                    if waiting and skip_lines == 1:
                        total_wins_pattern = re.compile("(\d*) \/ (\d*) \(\d*\.\d*%\)")
                        found_pattern = total_wins_pattern.search(line)
                        if not found_pattern:
                            print(line)

                        total_wins = found_pattern.group(1)

                    if waiting and skip_lines == 4:
                        if "skywars" in line.lower():
                            earlier_line = add_wins(earlier_line, total_wins)
                            opened_output_file.write(earlier_line)

                        earlier_line = ""
                        skip_lines = 0
                        waiting = False

                    if waiting:
                        skip_lines += 1

                    found_string = time_pattern.search(line)

                    if found_string:
                        waiting = True
                        group3 = found_string.group(3)
                        if group3 is None:
                            group3 = ""

                        earlier_line = format_line(date, found_string.group(1), find_current(found_string.group(2), group3))
