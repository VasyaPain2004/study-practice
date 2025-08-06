log_levels = ["INFO", "WARNING", "ERROR"]
counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}

with open("first-task/log.txt", "r") as file:
    for line in file:  
        if "] INFO:" in line:
            counts["INFO"] += 1
        elif "] WARNING:" in line:
            counts["WARNING"] += 1
        elif "] ERROR:" in line:
            counts["ERROR"] += 1

print("Статистика (оптимизированная):")
for level, count in counts.items():
    print(f"{level}: {count}")