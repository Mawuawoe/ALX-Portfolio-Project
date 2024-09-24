#!/usr/bin/python3
# Python script to generate the text file with Pan creation commands
pan_data = [
    ("R1", 1000, "Reservoir"),
    ("R2", 1000, "Reservoir"),
    ("R3", 1000, "Reservoir"),
    ("R4", 1000, "Reservoir"),
    ("R5", 1000, "Reservoir"),
    ("PCRA", 500, "PCR"),
    ("PCRB", 500, "PCR")
]

# Adding pan1 to pan32
for i in range(1, 33):
    pan_data.append((f"Pan{i}", 750, "Pan"))

# Generate the commands and write to a file
with open("create_pans.txt", "w") as file:
    for pan_id, size, pan_type in pan_data:
        command = f'create Pan location="Agbakpe" pan_id="{pan_id}" size={size} pan_type="{pan_type}"\n'
        file.write(command)

print("Text file 'create_pans.txt' generated.")
