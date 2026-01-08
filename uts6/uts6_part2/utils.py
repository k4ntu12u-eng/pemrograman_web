import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def konversi_nilai_ke_label(nilai):
    if nilai >= 85: return "A"
    elif nilai >= 80: return "A-"
    elif nilai >= 75: return "B+"
    elif nilai >= 70: return "B"
    elif nilai >= 65: return "B-"
    elif nilai >= 60: return "C+"
    elif nilai >= 55: return "C"
    elif nilai >= 45: return "D"
    else: return "E"

def konversi_label_ke_bobot(label):
    bobot_map = {
        "A": 4, "A-": 3.75, "B+": 3.5, "B": 3, 
        "B-": 2.75, "C+": 2.5, "C": 2, "D": 1, "E": 0
    }
    return bobot_map.get(label.upper(), 0)