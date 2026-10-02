from database import load_memory


memory = load_memory()

print("Количество элементов:", len(memory["knowledge"]))

for item in memory["knowledge"]:
    print(item)
