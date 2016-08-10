def check_routing_percent (file_string):
    file_lines = file_string.split('\n')
    for line in file_lines:
        if line.upper().startswith("FINAL"):
            while not line[0].isdigit():
                line = line[1:]
            while not line[-1].isdigit():
                line = line[:-1]
            percent = float(line)
            
            if (len(line) >= 3) and (line[:4] == "100"):
                return 100.0
            else:
                return percent