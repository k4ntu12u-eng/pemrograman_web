from utils import clear_screen, konversi_nilai_ke_label, konversi_label_ke_bobot, format_angka

def jalankan_cli():
    while True:
        clear_screen()
        print("---------- menu ----------")
        print("1. konversi nilai ke label")
        print("2. konversi label ke bobot")
        print("3. hitung total sks yang diambil")
        print("4. hitung total nilai")
        print("5. hitung IPS")
        print("6. exit")
        print("--------------------------")
        
        pilihan = input("Pilihan: ")

        if pilihan == '1':
            n = float(input("Masukkan nilai angka: "))
            print(f"Label: {konversi_nilai_ke_label(n)}")
        
        elif pilihan == '2':
            lbl = input("Masukkan label: ")
            bobot = konversi_label_ke_bobot(lbl)
            print(f"Bobot: {format_angka(bobot)}")

        elif pilihan == '3':
            jumlah = int(input("\nJumlah Data: "))
            list_sks = []
            print("--------- input sks ---------")
            for i in range(jumlah):
                sks = int(input(f"SKS {i+1}: "))
                list_sks.append(sks)
            print(f"\nTotal SKS: {sum(list_sks)}")

        elif pilihan == '4':
            jumlah = int(input("\nJumlah Data: "))
            list_sks = []
            total_poin = 0
            print("--------- input sks ---------")
            for i in range(jumlah):
                sks = int(input(f"SKS {i+1}: "))
                list_sks.append(sks)
            print("\n--------- input Nilai Mahasiswa ---------")
            for i in range(jumlah):
                nilai_angka = float(input(f"Nilai {i+1}: "))
                label = konversi_nilai_ke_label(nilai_angka)
                bobot = konversi_label_ke_bobot(label)
                total_poin += (bobot * list_sks[i])
            
            print(f"\nTotal Nilai: {total_poin:.1f}")

        elif pilihan == '5':
            jumlah = int(input("\nJumlah Data: "))
            list_sks_ips = [] 
            total_sks = 0
            total_poin = 0
            
            print("--------- input sks ---------")
            for i in range(jumlah):
                sks = int(input(f"SKS {i+1}: "))
                list_sks_ips.append(sks)
                total_sks += sks
            
            print("\n--------- input Nilai Mahasiswa ---------")
            for i in range(jumlah):
                nilai_angka = float(input(f"Nilai {i+1}: "))
                bobot = konversi_label_ke_bobot(konversi_nilai_ke_label(nilai_angka))
                total_poin += (bobot * list_sks_ips[i])
            
            ips = total_poin / total_sks if total_sks > 0 else 0
            
            print(f"\nIPS: {format_angka(ips)}")

        elif pilihan == '6':
            break

        input("\nKlik Enter untuk kembali ke menu...")