import time

def input_karyawan():
    jumlah = int(input("Masukkan jumlah karyawan: "))
    return [input("Masukkan nama karyawan: ") for _ in range(jumlah)]

# Algoritma O(n) 
def absen_linear(karyawan_list, nama):
    for karyawan in karyawan_list:
        if karyawan.lower() == nama.lower():
            return True
    return False

# Algoritma O(n log n) 
def binary_search(karyawan_list, nama):
    kiri, kanan = 0, len(karyawan_list) - 1
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        if karyawan_list[tengah].lower() == nama.lower():
            return True
        elif karyawan_list[tengah].lower() < nama.lower():
            kiri = tengah + 1
        else:
            kanan = tengah - 1
    return False

def absen_binary(karyawan_list, nama):
    karyawan_list.sort()  
    return binary_search(karyawan_list, nama)  

karyawan_list = input_karyawan()
nama_absen = input("\nMasukkan nama karyawan yang ingin absen: ")

# Absen O(n)
start = time.perf_counter()
hasil_linear = absen_linear(karyawan_list, nama_absen)
end = time.perf_counter()
print("Hasil O(n) :", "Absen berhasil!" if hasil_linear else "Nama tidak ditemukan!")
print(f"Waktu eksekusi O(n): {end - start:.10f} detik")

# Absen O(n log n)
start = time.perf_counter()
hasil_binary = absen_binary(karyawan_list, nama_absen)
end = time.perf_counter()
print("Hasil O(n log n):", "Absen berhasil!" if hasil_binary else "Nama tidak ditemukan!")
print(f"Waktu eksekusi O(n log n): {end - start:.10f} detik")
