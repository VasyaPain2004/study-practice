log_levels = ["INFO", "WARNING", "ERROR"]
counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}

with open("first-task/log.txt", "r") as file:
    lines = file.readlines()

for level in log_levels:
    for line in lines:
        if f"] {level}:" in line:
            counts[level] += 1

print("Статистика (неоптимизированная):")
for level, count in counts.items():
    print(f"{level}: {count}")