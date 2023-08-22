import re
file_path = "자막파일"


def check_string_pattern(file_path):
    print("check#1\n시간표시형식에 맞지 않는 line이 있는지 확인합니다\n ex) 00:01:24,2    00:01;24,200")
    with open(file_path, 'r') as file:
        lines = file.readlines()

    pattern = r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}"
    violation_lines = []

    for i, line in enumerate(lines):
        if "-->" in line and not re.match(pattern, line):
            print(line)
            violation_lines.append(i + 1)  # 라인 번호는 1부터 시작하므로 1을 더해줍니다.

    if violation_lines:
        print(" 규칙이 지켜지지 않은 라인:")
        for line_number in violation_lines:
            print(f"Line {line_number}")
        print("\n")
    else:
        print(" 문제가 되는 line이 없습니다.\n")


check_string_pattern(file_path)



def find_triple_newlines(filename):
    print("check#2\n줄바꿈이 세 번 이상 있는 부분을 찾습니다.")
    with open(filename, 'r') as file:
        content = file.read()

    triple_newline_indices = []
    prev_char = ''
    count = 0
    for index, char in enumerate(content):
        if char == '\n':
            if prev_char == '\n':
                count += 1
            else:
                count = 1
        else:
            count = 0

        if count == 3:
            triple_newline_indices.append(index - 2)

        prev_char = char

    return triple_newline_indices

triple_newline_indices = find_triple_newlines(file_path)

with open(file_path, 'r') as file:
        content = file.read()

if triple_newline_indices:
    print(" 연속으로 세 번의 줄바꿈이 있는 부분을 찾았습니다:")
    for index in triple_newline_indices:
        context_start = max(0, index - 20)  # 인덱스 앞의 20문자까지 표시
        context_end = min(index + 40, len(content))  # 인덱스 뒤의 40문자까지 표시
        context = content[context_start:context_end]
        print(f" {index}: ...{context}...")
    print("\n")
else:
    print(" 연속으로 세 번의 줄바꿈이 있는 부분이 없습니다.\n")




def check_subtitle_timing(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    print("check#3\n시간표시 줄에서 끝나는 시간이 시작 시간보다 빠르거나 같은 line이 있는 지 확인합니다")

    problematic_lines = []

    for line in lines:
        match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})', line)

        if match:
            start_time = match.group(1)
            end_time = match.group(2)

            start_time_parts = re.split(r'[:,]', start_time)
            end_time_parts = re.split(r'[:,]', end_time)

            start_hours, start_minutes, start_seconds, start_milliseconds = map(int, start_time_parts)
            end_hours, end_minutes, end_seconds, end_milliseconds = map(int, end_time_parts)

            if (start_hours * 3600000 + start_minutes * 60000 + start_seconds * 1000 + start_milliseconds) >= \
                    (end_hours * 3600000 + end_minutes * 60000 + end_seconds * 1000 + end_milliseconds):
                problematic_lines.append(line.strip())

    if not problematic_lines:
        print(" 문제가 되는 line이 없습니다.")
    else:
        print(" 다음 line들에 문제가 있습니다:")
        for line in problematic_lines:
            print(" ", line)

    print("\n")


check_subtitle_timing(file_path)




def extract_timestamps_from_txt(filename):
    timestamps = []

    print("check#4\n앞 줄의 시간표시줄에서 끝나는 시간보다 뒷 줄의 시간표시줄에서 시작하는 시간이 더 빠른 line이 있는지 확인합니다.")

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        timestamp_pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')

        for line in lines:
            match = timestamp_pattern.search(line)
            if match:
                start_time = match.group(1)
                end_time = match.group(2)
                timestamps.append((start_time, end_time))

    return timestamps

timestamps = extract_timestamps_from_txt(file_path)



def check_timestamp_order(timestamps):
    for i in range(len(timestamps) - 1):
        end_time_1 = timestamps[i][1]
        start_time_2 = timestamps[i + 1][0]

        if end_time_1 > start_time_2:
            print(" ",end_time_1)

    print(" 문제가 되는 line이 없습니다.")


is_ordered = check_timestamp_order(timestamps)






