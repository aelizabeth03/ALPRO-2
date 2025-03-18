class RencanaLiburan:
    def __init__(self, anggaran):
        self.anggaran = anggaran
        self.destinasi = [
            ("Candi Prambanan", 50000),
            ("Lava Tour Merapi - Sunrise Long Trip & Medium Trip", 1100000),
            ("Pantai Parangtritis", 10000),
            ("Goa Pindul", 40000),
            ("Malioboro", 0)  
        ]
        self.hotel = ("Hotel Jogja Nyaman", 1200000)  
        self.resto = [
            ("Gudeg Yu Djum", 60000 * 2),
            ("Kesuma Restaurant", 100000 * 2)
        ]
        self.transportasi = ("Transportasi Mobil + Bensin", 1600000)
        self.parkir = ("Tarif Parkir", 10000)
        self.tol = ("Tol Surabaya - Yogyakarta", 370000)
    
    def hitung_total(self):
        total_wisata = sum(harga for _, harga in self.destinasi)
        total_makan = sum(harga for _, harga in self.resto)
        total = total_wisata + total_makan + self.hotel[1] + self.transportasi[1] + self.parkir[1] + self.tol[1]
        return total
    
    def tampilkan_rencana(self):
        print("Rencana Liburan ke Jogja")
        print("========================")
        print("Destinasi Wisata:")
        for nama, harga in self.destinasi:
            print(f"- {nama}: Rp {harga:,}")
        print("\nHotel:")
        print(f"- {self.hotel[0]}: Rp {self.hotel[1]:,}")
        print("\nResto:")
        for nama, harga in self.resto:
            print(f"- {nama}: Rp {harga:,}")
        print("\nTransportasi:")
        print(f"- {self.transportasi[0]}: Rp {self.transportasi[1]:,}")
        print("\nParkir:")
        print(f"- {self.parkir[0]}: Rp {self.parkir[1]:,}")
        print("\nTol:")
        print(f"- {self.tol[0]}: Rp {self.tol[1]:,}")
        print("\nTotal Estimasi Biaya:")
        total = self.hitung_total()
        print(f"Rp {total:,}")
        if total <= self.anggaran:
            print("Anggaran mencukupi!")
        else:
            print("Anggaran kurang, perlu menyesuaikan rencana.")

liburan = RencanaLiburan(4800000)
liburan.tampilkan_rencana()