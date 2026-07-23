import json

# Load the file (update path if necessary)
file_path = 'data/territories.json'

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Define the list of IDs you want to remove
ids_to_remove = ["rumelia_early", "rumelia_mid", "rumelia_late"]

# Filter out entries where the 'id' is in our removal list
filtered_data = [entry for entry in data if entry.get('id') not in ids_to_remove]

# Write back to the file with clean formatting
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(filtered_data, file, indent=2, ensure_ascii=False)

print(f"Removed {len(data) - len(filtered_data)} entries. File updated successfully.")
