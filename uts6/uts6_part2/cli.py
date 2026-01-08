import sys
from utils import clear_screen, konversi_nilai_ke_label, konversi_label_ke_bobot

data_mahasiswa = {
    "nama": "",
    "nim": "",
    "list_sks": [],
    "list_nilai": [],
    "list_matkul": []
}

def jalankan_cli():
    while True:
        clear_screen()
        print("---------- Menu Utama ----------")
        print("1. Biodata")
        print("2. SKS")
        print("3. Input Nilai")
        print("4. Lihat Nilai")
        print("5. Lihat IP")
        print("6. Keluar")
        print("--------------------------------")
        
        pilihan = input("Pilihan: ")

        if pilihan == '1':
            print("\n=== Input Biodata ===")
            data_mahasiswa["nama"] = input("Masukkan Nama: ")
            data_mahasiswa["nim"] = input("Masukkan NIM : ")
            print("\nBiodata berhasil disimpan!")

        elif pilihan == '2':
            print("\n=== Input SKS ===")
            jumlah = int(input("Jumlah Mata Kuliah: "))
            data_mahasiswa["list_sks"] = []
            for i in range(jumlah):
                sks = int(input(f"SKS Mata Kuliah {i+1}: "))
                data_mahasiswa["list_sks"].append(sks)
            print("\nData SKS berhasil disimpan!")

        elif pilihan == '3':
            print("\n=== Input Nilai ===")
            if not data_mahasiswa["list_sks"]:
                print("Error: Isi data SKS (Menu 2) terlebih dahulu!")
            else:
                data_mahasiswa["list_nilai"] = []
                data_mahasiswa["list_matkul"] = []
                for i in range(len(data_mahasiswa["list_sks"])):
                    matkul = input(f"Nama Mata Kuliah {i+1}: ")
                    nilai = float(input(f"Nilai Angka untuk {matkul}: "))
                    data_mahasiswa["list_matkul"].append(matkul)
                    data_mahasiswa["list_nilai"].append(nilai)
                print("\nNilai berhasil diinput!")

        elif pilihan == '4':
            print("\n=== Daftar Nilai ===")
            if not data_mahasiswa["list_matkul"]:
                print("Data kosong!")
            else:
                print(f"Nama: {data_mahasiswa['nama']} ({data_mahasiswa['nim']})")
                print("-" * 30)
                for i in range(len(data_mahasiswa["list_matkul"])):
                    label = konversi_nilai_ke_label(data_mahasiswa["list_nilai"][i])
                    print(f"{data_mahasiswa['list_matkul'][i]}: {data_mahasiswa['list_nilai'][i]:g} ({label})")

        elif pilihan == '5':
            print("\n=== Hasil IP ===")
            total_sks = sum(data_mahasiswa["list_sks"])
            total_poin = 0
            if total_sks == 0:
                print("Biodata belum di input !")
            else:
                for i in range(len(data_mahasiswa["list_sks"])):
                    label = konversi_nilai_ke_label(data_mahasiswa["list_nilai"][i])
                    bobot = konversi_label_ke_bobot(label)
                    total_poin += (bobot * data_mahasiswa["list_sks"][i])
                
                ip = total_poin / total_sks
                print(f"Total SKS: {total_sks}")
                print(f"IP Anda  : {ip:.2f}")

        elif pilihan == '6':
            print("Keluar program...")
            sys.exit()

        input("\nKlik Enter untuk kembali ke menu...")