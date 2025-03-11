import time

def hitung_total_belanja(harga_barang):
    return sum(harga_barang.values())

jumlah_barang = int(input("Masukkan jumlah barang: "))
harga_barang = {i+1: int(input(f"Masukkan harga barang #{i+1}: ")) for i in range(jumlah_barang)}

start_time = time.perf_counter()
total = hitung_total_belanja(harga_barang)
end_time = time.perf_counter()

# Menampilkan total belanja dan waktu eksekusi O(n)
print("\nDaftar harga barang:")
for nomor, harga in harga_barang.items():
    print(f"Barang #{nomor}: {harga}")

print("\nTotal belanja:", total)
print(f"Waktu eksekusi: {end_time - start_time:.10f} detik")
