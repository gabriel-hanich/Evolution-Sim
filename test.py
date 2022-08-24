import time

turnIcons = ["|", "/", "-", "\\"]
for turnNumber in range(100):
    print(f"\r{turnIcons[turnNumber % len(turnIcons)]} Loading {round((turnNumber + 1) / 100, 3) * 100}%", end="") # Print loading info
    time.sleep(0.1)