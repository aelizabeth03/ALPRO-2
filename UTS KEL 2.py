import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ElectricityOptimizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Optimasi Penggunaan Listrik Rumah")
        self.root.geometry("900x700")
        
        # Data untuk rumah
        self.house_data = {
            "luas_rumah": 0,
            "golongan_listrik": 0,
            "rtm": False,
            "anggaran": 0,
            "max_kwh": 0,
            "tarif_per_kwh": 0,
            "max_watt": 0
        }
        
        # Mengatur style agar teks tab lebih besar
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Arial", 14, "bold"))  
        style.configure("TLabel", font=("Arial", 14))  
        style.configure("TButton", font=("Arial", 14, "bold"))  
        style.configure("TCombobox", font=("Arial", 14))  
        
        # Data untuk ruangan
        self.rooms = []
        
        # Data untuk alat elektronik
        self.devices = []
        self.setup_ac_database()

        # Membuat notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Informasi Rumah
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Informasi Rumah")
        self.setup_tab1()
        
        # Tab 2: Ruangan dan Alat Elektronik
        self.tab2 = ttk.Frame(self.notebook)
        self.tab2.bind("<Enter>", lambda e: self.canvas2.bind_all("<MouseWheel>", self._on_mousewheel2))
        self.tab2.bind("<Leave>", lambda e: self.canvas2.unbind_all("<MouseWheel>"))
        self.notebook.add(self.tab2, text="Ruangan & Alat Elektronik")
        self.setup_tab2()
        
        # Tab 3: Hasil Rekomendasi
        self.tab3 = ttk.Frame(self.notebook)
        self.tab3.bind("<Enter>", lambda e: self.canvas3.bind_all("<MouseWheel>", self._on_mousewheel3))
        self.tab3.bind("<Leave>", lambda e: self.canvas3.unbind_all("<MouseWheel>"))
        self.notebook.add(self.tab3, text="Hasil Rekomendasi")
        self.setup_tab3()

        # Binding event saat tab berubah
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
    
        # Tambahkan ini di bagian setup_tab1 atau di dekat deklarasi golongan_entry
        self.golongan_entry.bind("<FocusOut>", self.check_custom_golongan)

    def check_custom_golongan(self, event=None):
        """Periksa nilai kustom golongan listrik dan update RTM status"""
        try:
            custom_value = self.golongan_entry.get().strip()
            if custom_value:
                golongan = int(custom_value)
                # Jika golongan 900 VA
                if golongan == 900:
                    self.rtm_checkbox.config(state="normal")
                # Jika golongan 450 VA
                elif golongan == 450:
                    self.rtm_var.set(False)
                    self.rtm_checkbox.config(state="disabled")
                # Untuk golongan lainnya
                else:
                    self.rtm_var.set(True)
                    self.rtm_checkbox.config(state="disabled")
        except ValueError:
            # Jika bukan angka yang valid, biarkan saja
            pass

    def _on_mousewheel2(self, event):
        self.canvas2.yview_scroll(int(-1*(event.delta/120)), "units")

    # Untuk Tab 3
    def _on_mousewheel3(self, event):
        self.canvas3.yview_scroll(int(-1*(event.delta/120)), "units")

    def setup_ac_database(self):
        """Setup database of common AC models and their specifications"""
        self.ac_database = {
            "0.5": {
                "watt_range": (320, 400),
                "coverage": "< 8 m²",
                "models": [
                    {"brand": "LG", "model": "T05EV4", "watt": 320},
                    {"brand": "Panasonic", "model": "XN5TKJ", "watt": 350},
                    {"brand": "Daikin", "model": "FTV15AXV14", "watt": 380}
                ]
            },
            "1": {
                "watt_range": (700, 900),
                "coverage": "8-15 m²",
                "models": [
                    {"brand": "LG", "model": "T10EV4", "watt": 750},
                    {"brand": "Panasonic", "model": "CS/CU-XN9TKJ", "watt": 800},
                    {"brand": "Daikin", "model": "FTV15AXV14", "watt": 840}
                ]
            },
            "1.5": {
                "watt_range": (1000, 1200),
                "coverage": "15-25 m²",
                "models": [
                    {"brand": "LG", "model": "T13EV4", "watt": 1120},
                    {"brand": "Panasonic", "model": "CS/CU-XN12TKJ", "watt": 1090},
                    {"brand": "Daikin", "model": "FTV20AXV14", "watt": 1150}
                ]
            },
            "2": {
                "watt_range": (1400, 1700),
                "coverage": "25-35 m²",
                "models": [
                    {"brand": "LG", "model": "T19EV4", "watt": 1500},
                    {"brand": "Panasonic", "model": "CS/CU-XN18TKJ", "watt": 1620},
                    {"brand": "Daikin", "model": "FTV25AXV14", "watt": 1650}
                ]
            }
        }

    # Fungsi untuk mengupdate entry saat memilih opsi dari dropdown
    def update_golongan_entry(self, event=None):
        selected_golongan = self.golongan_var.get()
        self.golongan_entry.delete(0, tk.END)
        self.golongan_entry.insert(0, selected_golongan)

    def setup_tab1(self):
        # Frame untuk informasi rumah
        house_frame = ttk.LabelFrame(self.tab1, text="Informasi Rumah")
        house_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Luas Rumah
        ttk.Label(house_frame, text="Luas Rumah (m²):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.luas_rumah_entry = ttk.Entry(house_frame, font=("Arial", 14))
        self.luas_rumah_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Anggaran Maksimal
        ttk.Label(house_frame, text="Anggaran Maksimal (Rp):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.anggaran_entry = ttk.Entry(house_frame, font=("Arial", 14))
        self.anggaran_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Golongan Listrik - Kombinasi text dan dropdown
        ttk.Label(house_frame, text="Golongan Listrik (VA):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        # Frame untuk menampung text box dan dropdown
        golongan_frame = ttk.Frame(house_frame)
        golongan_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Text entry untuk golongan listrik
        self.golongan_entry = ttk.Entry(golongan_frame, font=("Arial", 14), width=10)
        self.golongan_entry.pack(side="left", padx=(0, 5))
        
        # Variable untuk menyimpan golongan listrik
        self.golongan_var = tk.StringVar()
        
        # Dropdown untuk opsi golongan listrik
        golongan_options = ["450", "900", "1300", "2200", "3500", "4400", "5500"]
        self.golongan_combobox = ttk.Combobox(
            golongan_frame, 
            textvariable=self.golongan_var, 
            values=golongan_options, 
            state="readonly",
            width=10
        )
        self.golongan_combobox.pack(side="left")
        
        # Binding untuk mengupdate entry ketika dropdown dipilih
        self.golongan_combobox.bind("<<ComboboxSelected>>", self.update_golongan_entry)
        
        # Binding untuk mengupdate RTM status
        self.golongan_combobox.bind("<<ComboboxSelected>>", self.update_rtm_status, add="+")
        
        # RTM Status (Rumah Tangga Mampu)
        ttk.Label(house_frame, text="Rumah Tangga Mampu (RTM):").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.rtm_var = tk.BooleanVar()
        self.rtm_checkbox = ttk.Checkbutton(house_frame, variable=self.rtm_var)
        self.rtm_checkbox.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        # Tombol Simpan
        save_button = ttk.Button(house_frame, text="Simpan & Lanjutkan", command=self.save_house_data)
        save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)
        
        # Informasi Tarif
        info_frame = ttk.LabelFrame(self.tab1, text="Informasi Tarif Listrik (Triwulan I 2025)")
        info_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tarif_info = (
            "- Pelanggan rumah tangga daya 450 VA bersubsidi: Rp 415 per kWh\n"
            "- Pelanggan rumah tangga daya 900 VA bersubsidi: Rp 605 per kWh\n"
            "- Pelanggan rumah tangga daya 900 VA RTM: Rp 1.352 per kWh\n"
            "- Pelanggan rumah tangga daya 1.300-2.200 VA: Rp 1.444,70 per kWh\n"
            "- Pelanggan rumah tangga daya 3.500 ke atas: Rp 1.699,53 per kWh"
        )
        
        info_label = ttk.Label(info_frame, text=tarif_info, justify="left")
        info_label.pack(padx=10, pady=10, anchor="w")
        
    
    def setup_tab2(self):
        # Buat canvas dan scrollbar
        self.canvas2 = tk.Canvas(self.tab2)
        scrollbar2 = ttk.Scrollbar(self.tab2, orient="vertical", command=self.canvas2.yview)
        self.scrollable_frame2 = ttk.Frame(self.canvas2)
        
        # Konfigurasi canvas
        self.scrollable_frame2.bind(
            "<Configure>",
            lambda e: self.canvas2.configure(scrollregion=self.canvas2.bbox("all"))
        )
        self.canvas2.create_window((0, 0), window=self.scrollable_frame2, anchor="nw")
        self.canvas2.configure(yscrollcommand=scrollbar2.set)
        
        # Pack canvas dan scrollbar
        self.canvas2.pack(side="left", fill="both", expand=True)
        scrollbar2.pack(side="right", fill="y")
        
        # 1. Frame untuk Ruangan (tetap di posisi pertama)
        room_frame = ttk.LabelFrame(self.scrollable_frame2, text="Informasi Ruangan")
        room_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # [isi frame ruangan tetap sama]
        # Luas Total Ruangan
        self.luas_total_var = tk.StringVar(value="Luas Total Ruangan: 0 m² (Max: 0 m²)")
        luas_total_label = ttk.Label(room_frame, textvariable=self.luas_total_var)
        luas_total_label.grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky="w")
        
        # Input untuk Ruangan Baru
        ttk.Label(room_frame, text="Nama Ruangan:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.room_name_entry = ttk.Entry(room_frame, font=("Arial", 14))
        self.room_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        ttk.Label(room_frame, text="Luas Ruangan (m²):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.room_size_entry = ttk.Entry(room_frame, font=("Arial", 14))
        self.room_size_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        # Tombol Ruangan
        button_frame_room = ttk.Frame(room_frame)
        button_frame_room.grid(row=3, column=0, columnspan=4, padx=10, pady=10)
        
        add_room_button = ttk.Button(button_frame_room, text="Tambah Ruangan", command=self.add_room)
        add_room_button.grid(row=0, column=0, padx=5)
        
        update_room_button = ttk.Button(button_frame_room, text="Update Ruangan", command=self.update_room)
        update_room_button.grid(row=0, column=1, padx=5)
        
        del_room_button = ttk.Button(button_frame_room, text="Hapus Ruangan", command=self.delete_room)
        del_room_button.grid(row=0, column=2, padx=5)
        
        # Daftar Ruangan
        ttk.Label(room_frame, text="Daftar Ruangan:").grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky="w")
        
        self.room_listbox = tk.Listbox(room_frame, font=("Arial", 14), width=50, height=5)
        self.room_listbox.grid(row=5, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")
        self.room_scrollbar = ttk.Scrollbar(room_frame, orient="vertical", command=self.room_listbox.yview)
        self.room_scrollbar.grid(row=5, column=4, pady=5, sticky="ns")
        self.room_listbox.config(yscrollcommand=self.room_scrollbar.set)
        self.room_listbox.bind('<<ListboxSelect>>', self.room_selected)
        
        # 2. Frame untuk Alat Elektronik (tetap di posisi kedua)
        device_frame = ttk.LabelFrame(self.scrollable_frame2, text="Informasi Alat Elektronik")
        device_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # [isi frame alat elektronik tetap sama]
        # Power consumtion
        self.power_usage_var = tk.StringVar(value="Total Penggunaan Daya: 0 Watt (Max: 0 Watt)")
        power_usage_label = ttk.Label(device_frame, font=("Arial", 14), textvariable=self.power_usage_var)
        power_usage_label.grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky="w")
        
        # Input untuk Alat Elektronik Baru
        ttk.Label(device_frame, text="Nama Alat:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.device_name_entry = ttk.Entry(device_frame, font=("Arial", 14))
        self.device_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        ttk.Label(device_frame, text="Ruangan:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.device_room_var = tk.StringVar()
        self.device_room_combobox = ttk.Combobox(device_frame, font=("Arial", 14), textvariable=self.device_room_var, state="readonly")
        self.device_room_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        ttk.Label(device_frame, text="Daya (Watt):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.device_power_entry = ttk.Entry(device_frame, font=("Arial", 14))
        self.device_power_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        
        ttk.Label(device_frame, text="Waktu Min (jam/hari):").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.device_min_time_entry = ttk.Entry(device_frame, font=("Arial", 14))
        self.device_min_time_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        
        ttk.Label(device_frame, text="Hari Pemakaian/Minggu:").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.device_days_entry = ttk.Entry(device_frame, font=("Arial", 14))
        self.device_days_entry.grid(row=1, column=3, padx=10, pady=5, sticky="w")
        
        ttk.Label(device_frame, text="Prioritas (1-5):").grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.device_priority_var = tk.StringVar()
        priority_options = ["1 (Sangat Penting)", "2 (Penting)", "3 (Normal)", "4 (Kurang Penting)", "5 (Tidak Penting)"]
        self.device_priority_combobox = ttk.Combobox(device_frame, font=("Arial", 14), textvariable=self.device_priority_var, values=priority_options, state="readonly")
        self.device_priority_combobox.grid(row=2, column=3, padx=10, pady=5, sticky="w")
        self.device_priority_combobox.current(2)  # Default ke Normal
        
        # Tombol Alat Elektronik
        button_frame_device = ttk.Frame(device_frame)
        button_frame_device.grid(row=5, column=0, columnspan=4, padx=10, pady=10)
        
        add_device_button = ttk.Button(button_frame_device, text="Tambah Alat", command=self.add_device)
        add_device_button.grid(row=0, column=0, padx=5)
        
        update_device_button = ttk.Button(button_frame_device, text="Update Alat", command=self.update_device)
        update_device_button.grid(row=0, column=1, padx=5)
        
        del_device_button = ttk.Button(button_frame_device, text="Hapus Alat", command=self.delete_device)
        del_device_button.grid(row=0, column=2, padx=5)
        
        # Tombol Reset Form
        reset_device_form_button = ttk.Button(button_frame_device, text="Reset Form", command=self.reset_device_form)
        reset_device_form_button.grid(row=0, column=3, padx=5)
        
        # 3. Pindahkan Tambah Cepat Alat ke posisi ketiga (setelah device_frame)
        quick_add_frame = ttk.LabelFrame(self.scrollable_frame2, text="Tambah Cepat Alat Elektronik Umum")
        quick_add_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Buat grid untuk tombol alat elektronik umum
        common_devices = [
            {"name": "Lampu LED", "power": 7, "min_time": 6, "days": 7, "priority": 2},
            {"name": "Kulkas", "power": 100, "min_time": 24, "days": 7, "priority": 1},
            {"name": "TV LED", "power": 60, "min_time": 4, "days": 7, "priority": 3},
            {"name": "Mesin Cuci", "power": 375, "min_time": 1, "days": 3, "priority": 3},
            {"name": "Rice Cooker", "power": 350, "min_time": 1, "days": 7, "priority": 2},
            {"name": "Kipas Angin", "power": 45, "min_time": 8, "days": 7, "priority": 3},
            {"name": "Charger HP", "power": 10, "min_time": 2, "days": 7, "priority": 2},
            {"name": "Laptop", "power": 65, "min_time": 4, "days": 7, "priority": 2}
        ]

        # Buat grid 4x2 untuk tombol alat elektronik umum
        row, col = 0, 0
        for device in common_devices:
            device_btn = ttk.Button(
                quick_add_frame, 
                text=f"{device['name']} ({device['power']}W)", 
                command=lambda d=device: self.quick_add_device(d)
            )
            device_btn.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
            col += 1
            if col > 3:  # 4 tombol per baris
                col = 0
                row += 1

        # Tambahkan label instruksi
        ttk.Label(
            quick_add_frame, 
            text="Pilih ruangan terlebih dahulu sebelum menambahkan alat cepat",
            font=("Helvetica", 9, "italic")
        ).grid(row=row+1, column=0, columnspan=4, pady=(10,5))
        
        # 4. Pindahkan Frame Rekomendasi AC ke posisi keempat
        ac_rec_frame = ttk.LabelFrame(self.scrollable_frame2, text="Rekomendasi AC")
        ac_rec_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(ac_rec_frame, text="Pilih Ruangan:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.ac_room_var = tk.StringVar()
        self.ac_room_combobox = ttk.Combobox(ac_rec_frame, font=("Arial", 14), textvariable=self.ac_room_var, state="readonly")
        self.ac_room_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.ac_room_combobox.bind("<<ComboboxSelected>>", self.show_ac_recommendation)

        self.ac_recommendation_label = ttk.Label(ac_rec_frame, text="Pilih ruangan untuk melihat rekomendasi AC")
        self.ac_recommendation_label.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="w")

        add_ac_button = ttk.Button(ac_rec_frame, text="Tambahkan AC yang Direkomendasikan", command=self.add_recommended_ac)
        add_ac_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        
        # 5. Pindahkan Daftar Alat Elektronik ke posisi kelima (terakhir)
        # Daftar Alat Elektronik
        ttk.Label(device_frame, text="Daftar Alat Elektronik:").grid(row=6, column=0, columnspan=4, padx=10, pady=5, sticky="w")
        
        self.device_listbox = tk.Listbox(device_frame, font=("Arial", 14), width=80, height=5)
        self.device_listbox.grid(row=7, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")
        self.device_scrollbar = ttk.Scrollbar(device_frame, orient="vertical", command=self.device_listbox.yview)
        self.device_scrollbar.grid(row=7, column=4, pady=5, sticky="ns")
        self.device_listbox.config(yscrollcommand=self.device_scrollbar.set)
        self.device_listbox.bind('<<ListboxSelect>>', self.device_selected)
        
        # Tombol Lanjutkan ke Optimasi (tetap di bagian akhir)
        optimize_button = ttk.Button(self.tab2, text="Lanjutkan ke Optimasi", command=self.calculate_optimization)
        optimize_button.pack(pady=20)
    
    def setup_tab3(self):
        # Buat canvas dan scrollbar
        self.canvas3 = tk.Canvas(self.tab3)
        scrollbar3 = ttk.Scrollbar(self.tab3, orient="vertical", command=self.canvas3.yview)
        self.scrollable_frame3 = ttk.Frame(self.canvas3)
        
        # Konfigurasi canvas
        self.scrollable_frame3.bind(
            "<Configure>",
            lambda e: self.canvas3.configure(scrollregion=self.canvas3.bbox("all"))
        )
        self.canvas3.create_window((0, 0), window=self.scrollable_frame3, anchor="nw")
        self.canvas3.configure(yscrollcommand=scrollbar3.set)
        
        # Pack canvas dan scrollbar
        self.canvas3.pack(side="left", fill="both", expand=True)
        scrollbar3.pack(side="right", fill="y")
        
        # Frame untuk hasil optimasi - ubah parent dari self.tab3 menjadi self.scrollable_frame3
        result_frame = ttk.LabelFrame(self.scrollable_frame3, text="Hasil Optimasi Penggunaan Listrik")
        result_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame untuk hasil optimasi
        result_frame = ttk.LabelFrame(self.scrollable_frame3, text="Hasil Optimasi Penggunaan Listrik")
        result_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Informasi Ringkasan
        self.summary_frame = ttk.LabelFrame(result_frame, text="Ringkasan")
        self.summary_frame.pack(fill="x", padx=10, pady=10)
        
        self.kwh_label = ttk.Label(self.summary_frame, text="Estimasi Penggunaan: 0 kWh")
        self.kwh_label.pack(anchor="w", padx=10, pady=2)
        
        self.cost_label = ttk.Label(self.summary_frame, text="Estimasi Biaya: Rp 0")
        self.cost_label.pack(anchor="w", padx=10, pady=2)
        
        self.budget_label = ttk.Label(self.summary_frame, text="Anggaran: Rp 0")
        self.budget_label.pack(anchor="w", padx=10, pady=2)
        
        self.status_label = ttk.Label(self.summary_frame, text="Status: -")
        self.status_label.pack(anchor="w", padx=10, pady=2)
        
        # Jadwal Penggunaan
        self.schedule_frame = ttk.LabelFrame(result_frame, text="Jadwal Penggunaan Alat")
        self.schedule_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.schedule_text = tk.Text(self.schedule_frame, width=80, height=15, wrap="word", font=("Arial", 14))
        self.schedule_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Rekomendasi
        self.recommendation_frame = ttk.LabelFrame(result_frame, text="Rekomendasi Penghematan")
        self.recommendation_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.recommendation_text = tk.Text(self.recommendation_frame, width=80, height=8, wrap="word", font=("Arial", 14))
        self.recommendation_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame untuk grafik
        self.graph_frame = ttk.LabelFrame(result_frame, text="Grafik Penggunaan Daya")
        self.graph_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Placeholder untuk grafik
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def quick_add_device(self, device_template):
        """Menambahkan alat elektronik umum dengan cepat"""
        # Ambil ruangan yang dipilih
        room = self.device_room_var.get()
        if not room:
            messagebox.showerror("Error", "Pilih ruangan terlebih dahulu sebelum menambahkan alat")
            return
        
        device_name = device_template["name"]
        
        # Tambahkan nomor jika nama sudah ada
        count = 1
        original_name = device_name
        while any(d["name"] == device_name for d in self.devices):
            device_name = f"{original_name} {count}"
            count += 1
        
        # Tambahkan alat dengan data dari template
        new_device = {
            "name": device_name,
            "room": room,
            "power": device_template["power"],
            "min_time": device_template["min_time"],
            "days": device_template["days"],
            "priority": device_template["priority"]
        }
        
        self.devices.append(new_device)
        
        # Update listbox alat
        self.update_device_listbox()
        
        # Update total penggunaan daya
        current_power = sum(device["power"] for device in self.devices)
        self.power_usage_var.set(f"Total Penggunaan Daya: {current_power} Watt (Max: {self.house_data['max_watt']} Watt)")
        
        # Tampilkan pesan
        messagebox.showinfo("Sukses", f"{device_name} berhasil ditambahkan ke ruangan {room}")

    # Fungsi untuk mengupdate status RTM berdasarkan golongan listrik
    def update_rtm_status(self, event=None):
        golongan = self.golongan_var.get()
        
        # Jika golongan dari dropdown
        if golongan == "900":
            self.rtm_checkbox.config(state="normal")
        elif golongan == "450":
            self.rtm_var.set(False)
            self.rtm_checkbox.config(state="disabled")
        else:
            self.rtm_var.set(True)
            self.rtm_checkbox.config(state="disabled")
    
    def save_house_data(self):
        try:
            luas_rumah = float(self.luas_rumah_entry.get())
            anggaran = float(self.anggaran_entry.get())
            
            # Ambil nilai golongan dari text entry jika diisi, jika tidak, ambil dari dropdown
            golongan_text = self.golongan_entry.get().strip()
            if golongan_text:
                golongan = int(golongan_text)
            else:
                golongan = int(self.golongan_var.get())
                
            rtm = self.rtm_var.get()
            
            # Validasi input
            if luas_rumah <= 0 or anggaran <= 0:
                messagebox.showerror("Error", "Luas rumah dan anggaran harus lebih dari 0")
                return
                
            if golongan <= 0:
                messagebox.showerror("Error", "Golongan listrik harus lebih dari 0")
                return
            
            # Simpan data rumah
            self.house_data["luas_rumah"] = luas_rumah
            self.house_data["golongan_listrik"] = golongan
            self.house_data["rtm"] = rtm
            self.house_data["anggaran"] = anggaran
            
            # Hitung tarif per kWh
            if golongan == 450:
                tarif = 415
            elif golongan == 900:
                tarif = 1352 if rtm else 605
            elif golongan in (1300, 2200):
                tarif = 1444.70
            else:  # 3500 ke atas
                tarif = 1699.53
            
            self.house_data["tarif_per_kwh"] = tarif
            
            # Hitung max kWh
            max_kwh = anggaran / tarif
            self.house_data["max_kwh"] = max_kwh
            
            # Hitung max watt
            pf = 0.85  # Power Factor
            max_watt = golongan * pf
            self.house_data["max_watt"] = max_watt
            
            messagebox.showinfo("Sukses", "Data rumah berhasil disimpan")
            
            # Update total luas ruangan
            self.luas_total_var.set(f"Luas Total Ruangan: 0 m² (Max: {luas_rumah} m²)")
            
            # Update power usage
            self.power_usage_var.set(f"Total Penggunaan Daya: 0 Watt (Max: {max_watt} Watt)")
            
            # Pindah ke tab berikutnya
            self.notebook.select(1)
            
        except ValueError:
            messagebox.showerror("Error", "Mohon masukkan angka yang valid")
    
    def add_room(self):
        try:
            name = self.room_name_entry.get().strip()
            size = float(self.room_size_entry.get())
            
            # Validasi input
            if not name:
                messagebox.showerror("Error", "Nama ruangan tidak boleh kosong")
                return
            
            if size <= 0:
                messagebox.showerror("Error", "Luas ruangan harus lebih dari 0")
                return
            
            # Cek apakah nama ruangan sudah ada
            if any(room["name"] == name for room in self.rooms):
                messagebox.showerror("Error", "Nama ruangan sudah ada")
                return
            
            # Hitung total luas ruangan sejauh ini
            current_total = sum(room["size"] for room in self.rooms)
            
            # Cek apakah melebihi luas rumah
            if current_total + size > self.house_data["luas_rumah"]:
                messagebox.showerror("Error", "Total luas ruangan melebihi luas rumah")
                return
            
            # Tambahkan ruangan baru
            self.rooms.append({
                "name": name,
                "size": size,
                "devices": []
            })
            
            # Update listbox ruangan
            self.update_room_listbox()
            
            # Update combobox ruangan untuk alat
            room_names = [room["name"] for room in self.rooms]
            self.device_room_combobox["values"] = room_names
            
            # Update total luas ruangan
            current_total += size
            self.luas_total_var.set(f"Luas Total Ruangan: {current_total} m² (Max: {self.house_data['luas_rumah']} m²)")
            
            # Reset form
            self.room_name_entry.delete(0, tk.END)
            self.room_size_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Mohon masukkan angka yang valid untuk luas ruangan")
    
    def delete_room(self):
        selection = self.room_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Pilih ruangan yang akan dihapus")
            return
        
        index = selection[0]
        room_name = self.rooms[index]["name"]
        
        # Cek apakah ada alat yang terkait dengan ruangan ini
        for device in self.devices:
            if device["room"] == room_name:
                messagebox.showerror("Error", f"Tidak dapat menghapus ruangan yang memiliki alat. Hapus alat di ruangan {room_name} terlebih dahulu.")
                return
        
        # Hapus ruangan
        del self.rooms[index]
        
        # Update listbox ruangan
        self.update_room_listbox()
        
        # Update combobox ruangan untuk alat
        room_names = [room["name"] for room in self.rooms]
        self.device_room_combobox["values"] = room_names
        
        # Update total luas ruangan
        current_total = sum(room["size"] for room in self.rooms)
        self.luas_total_var.set(f"Luas Total Ruangan: {current_total} m² (Max: {self.house_data['luas_rumah']} m²)")
    
    def room_selected(self, event):
        selection = self.room_listbox.curselection()
        if selection:
            index = selection[0]
            room = self.rooms[index]
            self.room_name_entry.delete(0, tk.END)
            self.room_name_entry.insert(0, room["name"])
            self.room_size_entry.delete(0, tk.END)
            self.room_size_entry.insert(0, str(room["size"]))
    
    def update_room_listbox(self):
        self.room_listbox.delete(0, tk.END)
        for room in self.rooms:
            self.room_listbox.insert(tk.END, f"{room['name']} - {room['size']} m²")

        # Update AC room combobox
        room_names = [room["name"] for room in self.rooms]
        self.ac_room_combobox["values"] = room_names
        self.device_room_combobox["values"] = room_names

    def update_room(self):
        """Fungsi untuk mengupdate informasi ruangan yang sudah ada"""
        try:
            selection = self.room_listbox.curselection()
            if not selection:
                messagebox.showerror("Error", "Pilih ruangan yang ingin diupdate")
                return
                
            index = selection[0]
            old_room = self.rooms[index]
            
            name = self.room_name_entry.get().strip()
            size = float(self.room_size_entry.get())
            
            # Validasi input
            if not name:
                messagebox.showerror("Error", "Nama ruangan tidak boleh kosong")
                return
            
            if size <= 0:
                messagebox.showerror("Error", "Luas ruangan harus lebih dari 0")
                return
            
            # Cek apakah ada ruangan lain dengan nama yang sama (kecuali ruangan yang sedang diupdate)
            if name != old_room["name"] and any(room["name"] == name for room in self.rooms):
                messagebox.showerror("Error", "Nama ruangan sudah ada")
                return
            
            # Hitung total luas ruangan sejauh ini (tanpa ruangan yang sedang diupdate)
            current_total = sum(room["size"] for room in self.rooms if room != old_room)
            
            # Cek apakah melebihi luas rumah
            if current_total + size > self.house_data["luas_rumah"]:
                messagebox.showerror("Error", "Total luas ruangan melebihi luas rumah")
                return
            
            # Cek apakah ada alat elektronik yang terkait dengan ruangan ini
            for device in self.devices:
                if device["room"] == old_room["name"]:
                    # Update nama ruangan pada alat jika nama ruangan berubah
                    if name != old_room["name"]:
                        device["room"] = name
            
            # Update informasi ruangan
            self.rooms[index] = {
                "name": name,
                "size": size,
                "devices": old_room.get("devices", [])
            }
            
            # Update listbox ruangan
            self.update_room_listbox()
            
            # Update combobox ruangan untuk alat
            room_names = [room["name"] for room in self.rooms]
            self.device_room_combobox["values"] = room_names
            
            # Update total luas ruangan
            updated_total = sum(room["size"] for room in self.rooms)
            self.luas_total_var.set(f"Luas Total Ruangan: {updated_total} m² (Max: {self.house_data['luas_rumah']} m²)")
            
            # Update listbox alat (karena nama ruangan mungkin berubah)
            self.update_device_listbox()
            
            # Reset form
            self.room_name_entry.delete(0, tk.END)
            self.room_size_entry.delete(0, tk.END)
            
            messagebox.showinfo("Sukses", f"Ruangan {name} berhasil diupdate")
            
        except ValueError:
            messagebox.showerror("Error", "Mohon masukkan angka yang valid untuk luas ruangan")

    def add_device(self):
        try:
            name = self.device_name_entry.get().strip()
            room = self.device_room_var.get()
            power = float(self.device_power_entry.get())
            min_time = float(self.device_min_time_entry.get())
            days = float(self.device_days_entry.get())
            priority_str = self.device_priority_var.get()
            
            # Ekstrak nilai prioritas (1-5)
            priority = int(priority_str[0])
            
            # Validasi input
            if not name:
                messagebox.showerror("Error", "Nama alat tidak boleh kosong")
                return
                
            if not room:
                messagebox.showerror("Error", "Pilih ruangan terlebih dahulu")
                return
                
            if power <= 0 or min_time <= 0 or days <= 0:
                messagebox.showerror("Error", "Daya, waktu minimal, dan hari penggunaan harus lebih dari 0")
                return
                
            if min_time > 24:
                messagebox.showerror("Error", "Waktu minimal tidak boleh lebih dari 24 jam")
                return
                
            if days > 7:
                messagebox.showerror("Error", "Hari penggunaan tidak boleh lebih dari 7 hari")
                return
                
            # Cek apakah nama alat sudah ada
            if any(device["name"] == name for device in self.devices):
                messagebox.showerror("Error", "Nama alat sudah ada")
                return
            
            # PERBAIKAN: Cek apakah daya alat melebihi kapasitas maksimal
            if power > self.house_data["max_watt"]:
                messagebox.showerror("Error", f"Daya alat ({power} Watt) melebihi kapasitas maksimal rumah ({self.house_data['max_watt']} Watt)")
                return
                
            # Hitung total daya yang sudah digunakan
            current_power = sum(device["power"] for device in self.devices)
            
            # Cek apakah melebihi daya maksimal rumah
            if current_power + power > self.house_data["max_watt"]:
                messagebox.showwarning("Peringatan", "Total daya alat melebihi kapasitas listrik rumah. Ini dapat menyebabkan pemadaman listrik jika semua alat digunakan secara bersamaan.")
            
            # Tambahkan alat baru
            self.devices.append({
                "name": name,
                "room": room,
                "power": power,
                "min_time": min_time,
                "days": days,
                "priority": priority
            })
            
            # Update listbox alat
            self.update_device_listbox()
            
            # Update total penggunaan daya
            current_power += power
            self.power_usage_var.set(f"Total Penggunaan Daya: {current_power} Watt (Max: {self.house_data['max_watt']} Watt)")
            
            # Reset form
            self.device_name_entry.delete(0, tk.END)
            self.device_power_entry.delete(0, tk.END)
            self.device_min_time_entry.delete(0, tk.END)
            self.device_days_entry.delete(0, tk.END)
            self.device_priority_combobox.current(2)  # Reset ke Normal
            
        except ValueError:
            messagebox.showerror("Error", "Mohon masukkan angka yang valid")
    
    def delete_device(self):
        selection = self.device_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Pilih alat yang akan dihapus")
            return
        
        index = selection[0]
        
        # Hitung power yang akan dihapus
        power_to_remove = self.devices[index]["power"]
        
        # Hapus alat
        del self.devices[index]
        
        # Update listbox alat
        self.update_device_listbox()
        
        # Update total penggunaan daya
        current_power = sum(device["power"] for device in self.devices)
        self.power_usage_var.set(f"Total Penggunaan Daya: {current_power} Watt (Max: {self.house_data['max_watt']} Watt)")
    
    def device_selected(self, event):
        selection = self.device_listbox.curselection()
        if selection:
            index = selection[0]
            device = self.devices[index]
            
            self.device_name_entry.delete(0, tk.END)
            self.device_name_entry.insert(0, device["name"])
            
            self.device_room_var.set(device["room"])
            
            self.device_power_entry.delete(0, tk.END)
            self.device_power_entry.insert(0, str(device["power"]))
            
            self.device_min_time_entry.delete(0, tk.END)
            self.device_min_time_entry.insert(0, str(device["min_time"]))
            
            self.device_days_entry.delete(0, tk.END)
            self.device_days_entry.insert(0, str(device["days"]))
            
            # Set prioritas
            priority_index = device["priority"] - 1
            self.device_priority_combobox.current(priority_index)
    
    def update_device_listbox(self):
        self.device_listbox.delete(0, tk.END)
        for device in self.devices:
            priority_text = ["Sangat Penting", "Penting", "Normal", "Kurang Penting", "Tidak Penting"][device["priority"]-1]
            self.device_listbox.insert(tk.END, f"{device['name']} - {device['room']} - {device['power']} Watt - {device['min_time']} jam/hari - {device['days']} hari/minggu - Prioritas: {priority_text}")
    
    def update_device(self):
        """Fungsi untuk mengupdate informasi alat elektronik yang sudah ada"""
        try:
            selection = self.device_listbox.curselection()
            if not selection:
                messagebox.showerror("Error", "Pilih alat elektronik yang ingin diupdate")
                return
                
            index = selection[0]
            old_device = self.devices[index]
                
            name = self.device_name_entry.get().strip()
            room = self.device_room_var.get()
            power = float(self.device_power_entry.get())
            min_time = float(self.device_min_time_entry.get())
            days = float(self.device_days_entry.get())
            priority_str = self.device_priority_var.get()
            
            # Ekstrak nilai prioritas (1-5)
            priority = int(priority_str[0])
            
            # Validasi input
            if not name:
                messagebox.showerror("Error", "Nama alat tidak boleh kosong")
                return
                
            if not room:
                messagebox.showerror("Error", "Pilih ruangan terlebih dahulu")
                return
                
            if power <= 0 or min_time <= 0 or days <= 0:
                messagebox.showerror("Error", "Daya, waktu minimal, dan hari penggunaan harus lebih dari 0")
                return
                
            if min_time > 24:
                messagebox.showerror("Error", "Waktu minimal tidak boleh lebih dari 24 jam")
                return
                
            if days > 7:
                messagebox.showerror("Error", "Hari penggunaan tidak boleh lebih dari 7 hari")
                return
            
            # Cek apakah ada alat lain dengan nama yang sama (kecuali alat yang sedang diupdate)
            if name != old_device["name"] and any(device["name"] == name for device in self.devices):
                messagebox.showerror("Error", "Nama alat sudah ada")
                return
            
            # Hitung total daya yang sudah digunakan (tanpa alat yang sedang diupdate)
            current_power = sum(device["power"] for device in self.devices if device != old_device)
            
            # Cek apakah daya alat melebihi kapasitas maksimal
            if power > self.house_data["max_watt"]:
                messagebox.showerror("Error", f"Daya alat ({power} Watt) melebihi kapasitas maksimal rumah ({self.house_data['max_watt']} Watt)")
                return
            
            # Cek apakah melebihi daya maksimal rumah
            if current_power + power > self.house_data["max_watt"]:
                messagebox.showwarning("Peringatan", "Total daya alat melebihi kapasitas listrik rumah. Ini dapat menyebabkan pemadaman listrik jika semua alat digunakan secara bersamaan.")
            
            # Update informasi alat
            self.devices[index] = {
                "name": name,
                "room": room,
                "power": power,
                "min_time": min_time,
                "days": days,
                "priority": priority
            }
            
            # Update listbox alat
            self.update_device_listbox()
            
            # Update total penggunaan daya
            updated_power = sum(device["power"] for device in self.devices)
            self.power_usage_var.set(f"Total Penggunaan Daya: {updated_power} Watt (Max: {self.house_data['max_watt']} Watt)")
            
            # Reset form
            self.device_name_entry.delete(0, tk.END)
            self.device_power_entry.delete(0, tk.END)
            self.device_min_time_entry.delete(0, tk.END)
            self.device_days_entry.delete(0, tk.END)
            self.device_priority_combobox.current(2)  # Reset ke Normal
            
            messagebox.showinfo("Sukses", f"Alat {name} berhasil diupdate")
            
        except ValueError:
            messagebox.showerror("Error", "Mohon masukkan angka yang valid")

    def reset_device_form(self):
        """Fungsi untuk mereset form alat elektronik"""
        self.device_name_entry.delete(0, tk.END)
        self.device_power_entry.delete(0, tk.END)
        self.device_min_time_entry.delete(0, tk.END)
        self.device_days_entry.delete(0, tk.END)
        self.device_priority_combobox.current(2)  # Reset ke Normal
        
        # Deselect any selected item in the device listbox
        self.device_listbox.selection_clear(0, tk.END)
        
        # Set focus to name entry
        self.device_name_entry.focus()

    def on_tab_change(self, event):
        selected_tab = self.notebook.index(self.notebook.select())
        if selected_tab == 2:  # Tab Hasil Rekomendasi
            self.calculate_optimization()
    
    def calculate_optimization(self):
        # Validasi data
        if not self.rooms:
            messagebox.showerror("Error", "Tambahkan ruangan terlebih dahulu")
            return
                
        if not self.devices:
            messagebox.showerror("Error", "Tambahkan alat elektronik terlebih dahulu")
            return
        
        # Optimasi penggunaan alat
        schedule, kwh_usage, cost, status, savings_recommendations = self.optimize_devices()
        
        # Update informasi di tab 3
        self.update_results(schedule, kwh_usage, cost, status, savings_recommendations)
        
        # Pindah ke tab hasil
        self.notebook.select(2)
    
    def show_ac_recommendation(self, event=None):
        """Menampilkan rekomendasi AC berdasarkan ruangan yang dipilih"""
        room_name = self.ac_room_var.get()
        if not room_name:
            return
        
        # Cari ruangan yang dipilih
        selected_room = None
        for room in self.rooms:
            if room["name"] == room_name:
                selected_room = room
                break
        
        if not selected_room:
            return
        
        size = selected_room["size"]
        
        # Tentukan PK AC berdasarkan luas ruangan
        if size < 8:
            pk = "0.5"
            watt = 320
        elif size < 15:
            pk = "1"
            watt = 750
        elif size < 25:
            pk = "1.5"
            watt = 1120
        elif size < 35:
            pk = "2"
            watt = 1500
        else:
            pk = f"{size / 15:.1f}"
            watt = int(size / 15 * 750)
        
        # Get specific model recommendations if available
        model_text = ""
        if pk in self.ac_database:
            ac_info = self.ac_database[pk]
            model_text = "\nModel yang direkomendasikan:\n"
            for model in ac_info["models"]:
                model_text += f"- {model['brand']} {model['model']} ({model['watt']} Watt)\n"
        
        self.ac_recommendation_label.config(
            text=f"Rekomendasi: AC {pk} PK ({watt} Watt) untuk ruangan {room_name} ({size} m²){model_text}"
        )
        
        # Simpan rekomendasi untuk digunakan di add_recommended_ac
        self.current_ac_recommendation = {
            "room": room_name,
            "pk": pk,
            "watt": watt,
            "models": self.ac_database.get(pk, {}).get("models", [])
        }

    def show_ac_model_selection(self):
        """Tampilkan dialog untuk memilih model AC spesifik"""
        if not hasattr(self, 'current_ac_recommendation') or not self.current_ac_recommendation.get("models"):
            return None
        
        models = self.current_ac_recommendation["models"]
        
        # Create a popup dialog
        ac_dialog = tk.Toplevel(self.root)
        ac_dialog.title("Pilih Model AC")
        ac_dialog.geometry("400x300")
        ac_dialog.grab_set()  # Make dialog modal
        
        ttk.Label(ac_dialog, text="Pilih model AC yang diinginkan:").pack(pady=10)
        
        # Model selection
        model_var = tk.StringVar()
        model_frame = ttk.Frame(ac_dialog)
        model_frame.pack(fill="both", expand=True, padx=10)
        
        for i, model in enumerate(models):
            model_text = f"{model['brand']} {model['model']} ({model['watt']} Watt)"
            ttk.Radiobutton(model_frame, text=model_text, variable=model_var, value=i).pack(anchor="w", pady=5)
         
        # Default selection
        if models:
            model_var.set("0")
        
        # Buttons
        button_frame = ttk.Frame(ac_dialog)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        selected_model = [None]  # Using list to be able to modify it in the inner function
        
        def on_select():
            if model_var.get():
                selected_model[0] = models[int(model_var.get())]
                ac_dialog.destroy()
        
        def on_cancel():
            ac_dialog.destroy()
        
        ttk.Button(button_frame, text="Pilih", command=on_select).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Batal", command=on_cancel).pack(side="right", padx=5)
        
        # Wait for the dialog to close
        self.root.wait_window(ac_dialog)
        return selected_model[0]

    def add_recommended_ac(self):
        """Menambahkan AC yang direkomendasikan ke daftar alat"""
        if not hasattr(self, 'current_ac_recommendation'):
            messagebox.showerror("Error", "Pilih ruangan terlebih dahulu untuk mendapatkan rekomendasi AC")
            return
        
        rec = self.current_ac_recommendation
        room_name = rec["room"]
        pk = rec["pk"]
        
        # Allow user to select a specific model if available
        selected_model = None
        if rec.get("models"):
            selected_model = self.show_ac_model_selection()
        
        if selected_model:
            watt = selected_model["watt"]
            ac_name = f"AC {pk} PK {selected_model['brand']} {selected_model['model']}"
        else:
            watt = rec["watt"]
            ac_name = f"AC {pk} PK ({room_name})"
        
        # Verifikasi bahwa watt AC tidak melebihi kapasitas maksimal
        if watt > self.house_data["max_watt"]:
            messagebox.showerror("Error", 
                                f"Daya AC yang direkomendasikan ({watt} Watt) melebihi kapasitas maksimal rumah ({self.house_data['max_watt']} Watt). "
                                f"Pilih AC dengan kapasitas yang lebih kecil atau tingkatkan kapasitas listrik rumah.")
            return
        
        # Cek apakah nama sudah ada
        if any(device["name"] == ac_name for device in self.devices):
            count = 1
            while any(device["name"] == f"{ac_name} ({count})" for device in self.devices):
                count += 1
            ac_name = f"{ac_name} ({count})"
        
        # Pre-fill device form
        self.device_name_entry.delete(0, tk.END)
        self.device_name_entry.insert(0, ac_name)
        
        self.device_room_var.set(room_name)
        
        self.device_power_entry.delete(0, tk.END)
        self.device_power_entry.insert(0, str(watt))
        
        self.device_min_time_entry.delete(0, tk.END)
        self.device_min_time_entry.insert(0, "6")  # Default 6 jam/hari
        
        self.device_days_entry.delete(0, tk.END)
        self.device_days_entry.insert(0, "7")  # Default 7 hari/minggu
        
        self.device_priority_var.set("2 (Penting)")  # AC biasanya penting
        
        # Tambahkan pesan untuk konfirmasi
        if messagebox.askyesno("Konfirmasi", f"Apakah Anda ingin menambahkan {ac_name} dengan spesifikasi:\n"
                                            f"- Daya: {watt} Watt\n"
                                            f"- Waktu: 6 jam/hari\n"
                                            f"- Hari: 7 hari/minggu\n"
                                            f"- Prioritas: Penting\n\n"
                                            f"Anda dapat mengubah nilai defaultnya sebelum menambahkan."):
            self.add_device()  # Gunakan fungsi add_device yang sudah ada
    
    def optimize_devices(self):
        # Konversi ke penggunaan mingguan
        max_weekly_kwh = self.house_data["max_kwh"] * 7 / 30  # Asumsi 30 hari per bulan
        max_watt = self.house_data["max_watt"]
        tarif = self.house_data["tarif_per_kwh"]
        
        # Perhitungan max_kwh yang ideal: max_watt (kW) × 24 jam × 30 hari
        calculated_max_kwh = (max_watt / 1000) * 24 * 30

        # Jika max_kwh di database terlalu tinggi dibandingkan dengan kapasitas watt,
        # gunakan nilai yang lebih realistis
        if self.house_data["max_kwh"] > calculated_max_kwh : 
            max_monthly_kwh = calculated_max_kwh
            max_weekly_kwh = max_monthly_kwh * 7 / 30
        else:
            max_monthly_kwh = self.house_data["max_kwh"]

        # Tambahkan pajak 12% untuk daya >= 3500
        if self.house_data["golongan_listrik"] >= 3500:
            tarif *= 1.12
        
        # Urutkan alat berdasarkan prioritas (prioritas rendah = angka kecil = lebih penting)
        devices_sorted = sorted(self.devices, key=lambda x: x["priority"])
        
        # Alokasikan waktu untuk alat berdasarkan prioritas
        schedule = {}
        total_kwh = 0
        hourly_usage = [0] * 24  # Penggunaan daya per jam
        
        # Menggunakan algoritma greedy + constraint satisfaction
        for device in devices_sorted:
            name = device["name"]
            power_watt = device["power"]
            min_hours = device["min_time"]
            days_per_week = device["days"]
            
            # Verifikasi bahwa perangkat tidak melebihi kapasitas maksimal
            if power_watt > max_watt:
                continue  # Skip perangkat yang melebihi kapasitas

            # Konversi watt ke kWh per minggu
            kwh_per_hour = power_watt / 1000
            
            # Total kWh yang dibutuhkan alat ini per minggu
            total_kwh_needed = kwh_per_hour * min_hours * days_per_week
            
            # Cek apakah penambahan alat ini akan melebihi batas kWh maksimal
            if total_kwh + total_kwh_needed > max_weekly_kwh:
                # Jika prioritas tinggi (1-2), tetap tambahkan tapi catat melebihi batas
                if device["priority"] <= 2:
                    total_kwh += total_kwh_needed
                else:
                    # Untuk prioritas rendah, kurangi jam penggunaan jika memungkinkan
                    adjusted_hours = 0
                    adjusted_kwh = 0
                    
                    # Cari berapa jam maksimal yang bisa digunakan tanpa melebihi batas
                    for hour in range(int(min_hours), 0, -1):
                        adjusted_kwh = kwh_per_hour * hour * days_per_week
                        if total_kwh + adjusted_kwh <= max_weekly_kwh:
                            adjusted_hours = hour
                            break
                    
                    # Jika bisa kurangi jam penggunaan
                    if adjusted_hours > 0:
                        min_hours = adjusted_hours
                        total_kwh_needed = adjusted_kwh
                        total_kwh += total_kwh_needed
                    else:
                        # Jika tidak bisa kurangi jam, kurangi hari
                        for day in range(int(days_per_week), 0, -1):
                            adjusted_kwh = kwh_per_hour * min_hours * day
                            if total_kwh + adjusted_kwh <= max_weekly_kwh:
                                days_per_week = day
                                total_kwh_needed = adjusted_kwh
                                total_kwh += total_kwh_needed
                                break
                        else:
                            # Jika tidak bisa kurangi hari, skip alat ini
                            continue
            else:
                # Jika tidak melebihi batas, tambahkan seperti biasa
                total_kwh += total_kwh_needed
            
            # Tentukan jadwal penggunaan optimal
            best_hours = self.find_best_hours(hourly_usage, power_watt, min_hours, max_watt)
            
            schedule[name] = {
                "hours": best_hours,
                "days_per_week": days_per_week,
                "power": power_watt,
                "kwh_per_week": total_kwh_needed
            }
            
            # Update penggunaan daya per jam
            for hour in best_hours:
                hourly_usage[hour] += power_watt
        
        # Hitung biaya
        weekly_cost = total_kwh * tarif
        monthly_cost = weekly_cost * 30 / 7
        
        # Tentukan status berdasarkan anggaran dan batas kWh
        monthly_kwh = total_kwh * 30 / 7
        
        if monthly_cost <= self.house_data["anggaran"] and monthly_kwh <= max_monthly_kwh:
            status = "Di bawah anggaran & batas kWh"
        elif monthly_cost > self.house_data["anggaran"] and monthly_kwh <= max_monthly_kwh:
            status = "Melebihi anggaran"
        elif monthly_cost <= self.house_data["anggaran"] and monthly_kwh > max_monthly_kwh:
            status = "Melebihi batas kWh"
        else:
            status = "Melebihi anggaran & batas kWh"
        
        # Rekomendasi penghematan
        savings_recommendations = []
        
        # Cek terhadap anggaran
        if monthly_cost > self.house_data["anggaran"]:
            excess_cost = monthly_cost - self.house_data["anggaran"]
            excess_kwh = excess_cost / tarif
            
            savings_recommendations.append(f"Penggunaan listrik melebihi anggaran sebesar Rp {excess_cost:,.2f} (setara {excess_kwh:.2f} kWh)")
        
        # Cek terhadap batas kWh
        if monthly_kwh > max_monthly_kwh:
            excess_kwh = monthly_kwh - max_monthly_kwh
            excess_cost = excess_kwh * tarif
            
            savings_recommendations.append(f"Penggunaan listrik melebihi batas kWh sebesar {excess_kwh:.2f} kWh (setara Rp {excess_cost:,.2f})")
        
        # Rekomendasi penghematan jika melebihi anggaran atau batas kWh
        if status != "Di bawah anggaran & batas kWh":
            # Identifikasi alat yang bisa dikurangi penggunaannya
            for device in reversed(devices_sorted):  # Mulai dari prioritas terendah
                name = device["name"]
                power_watt = device["power"]
                min_hours = device["min_time"]
                days_per_week = device["days"]
                kwh_per_hour = power_watt / 1000
                
                # Jika prioritas rendah (4-5) dan penggunaan > 1 jam, sarankan pengurangan
                if device["priority"] >= 4 and min_hours > 1:
                    savings = kwh_per_hour * days_per_week  # Penghematan jika mengurangi 1 jam
                    cost_savings = savings * tarif * 30 / 7
                    
                    savings_recommendations.append(f"Kurangi penggunaan {name} sebanyak 1 jam/hari untuk menghemat {savings * 30 / 7:.2f} kWh (Rp {cost_savings:,.2f})/bulan")
                
                # Jika alat non-esensial (prioritas 3-5), sarankan pengurangan hari
                if device["priority"] >= 3 and days_per_week > 1:
                    savings = kwh_per_hour * min_hours  # Penghematan jika mengurangi 1 hari
                    cost_savings = savings * tarif * 30 / 7
                    
                    savings_recommendations.append(f"Kurangi penggunaan {name} sebanyak 1 hari/minggu untuk menghemat {savings * 30 / 7:.2f} kWh (Rp {cost_savings:,.2f})/bulan")
        
        # Check if any hour exceeds maximum capacity
        exceeds_capacity = any(usage > max_watt for usage in hourly_usage)
        
        # Update status to include capacity overload
        if exceeds_capacity:
            if status == "Di bawah anggaran & batas kWh":
                status = "Melebihi kapasitas daya"
            else:
                status += " & melebihi kapasitas daya"
        
        # Add capacity overload recommendations
        if exceeds_capacity:
            overloaded_hours = [f"{h}:00" for h, usage in enumerate(hourly_usage) if usage > max_watt]
            overload_amount = max(hourly_usage) - max_watt
            
            savings_recommendations.append(f"Penggunaan daya melebihi kapasitas maksimal ({max_watt} Watt) pada jam {', '.join(overloaded_hours)} sebesar {overload_amount:.2f} Watt")
            
            # Find devices running during overloaded hours and suggest alternatives
            devices_to_reschedule = []
            for device_name, details in schedule.items():
                if any(hour in overloaded_hours for hour in [f"{h}:00" for h in details["hours"]]):
                    # Prioritize lower priority devices
                    device_priority = next((d["priority"] for d in self.devices if d["name"] == device_name), 3)
                    devices_to_reschedule.append((device_name, details["power"], device_priority))
            
            # Sort by priority (higher number = lower priority) and then by power consumption
            devices_to_reschedule.sort(key=lambda x: (-x[2], -x[1]))
            
            # Suggest rescheduling or reducing usage of non-essential devices
            if devices_to_reschedule:
                device_name, power, _ = devices_to_reschedule[0]
                non_overloaded_hours = [f"{h}:00" for h in range(24) if f"{h}:00" not in overloaded_hours]
                if non_overloaded_hours:
                    alternative_time = ", ".join(non_overloaded_hours[:3])  # Suggest first 3 non-overloaded hours
                    savings_recommendations.append(f"Pindahkan penggunaan {device_name} ({power} Watt) ke jam {alternative_time}")
        
        # Tampilkan max_monthly_kwh yang sebenarnya dan yang dikoreksi (untuk debug)
        if self.house_data["max_kwh"] > calculated_max_kwh:
            savings_recommendations.append(f"Catatan: Batas kWh bulanan disesuaikan dari {self.house_data['max_kwh']:.2f} kWh menjadi {max_monthly_kwh:.2f} kWh berdasarkan kapasitas daya {max_watt} Watt")

        return schedule, monthly_kwh, monthly_cost, status, savings_recommendations
    
    def find_best_hours(self, hourly_usage, power_watt, min_hours, max_watt):
        """Mencari jam optimal untuk menggunakan alat menggunakan algoritma greedy."""
        hours_needed = int(min_hours)
        best_hours = []
        
        # Buat daftar (penggunaan saat ini, jam) untuk diurutkan
        hours_with_usage = [(hourly_usage[hour], hour) for hour in range(24)]
        
        # Urutkan berdasarkan penggunaan terendah
        hours_with_usage.sort()
        
        # Prioritize hours that won't exceed capacity
        safe_hours = []
        for usage, hour in hours_with_usage:
            if usage + power_watt <= max_watt:
                safe_hours.append(hour)
                if len(safe_hours) >= hours_needed:
                    return sorted(safe_hours)
        
        # If we couldn't find enough non-exceeding hours, fill with lowest usage hours
        # but mark them for the optimization function to handle
        remaining_hours = hours_needed - len(safe_hours)
        best_hours = safe_hours.copy()
        
        for usage, hour in hours_with_usage:
            if hour not in best_hours:
                best_hours.append(hour)
                remaining_hours -= 1
                if remaining_hours == 0:
                    break
        
        return sorted(best_hours)
    
    def update_results(self, schedule, kwh_usage, cost, status, savings_recommendations):
        # Hitung max_kwh berdasarkan max_watt
        calculated_max_kwh = (self.house_data["max_watt"] / 1000) * 24 * 30
        max_monthly_kwh = min(self.house_data["max_kwh"], calculated_max_kwh)
        
        # Update label ringkasan
        self.kwh_label.config(text=f"Estimasi Penggunaan: {kwh_usage:.2f} kWh/bulan (Max: {max_monthly_kwh:.2f} kWh/bulan)")
        self.cost_label.config(text=f"Estimasi Biaya: Rp {cost:,.2f}/bulan")
        self.budget_label.config(text=f"Anggaran: Rp {self.house_data['anggaran']:,.2f}/bulan")
        
        if "Di bawah anggaran" in status:
            self.status_label.config(text=f"Status: {status}", foreground="green")
        else:
            self.status_label.config(text=f"Status: {status}", foreground="red")
                    
        # Update jadwal penggunaan
        self.schedule_text.delete(1.0, tk.END)
        
        self.schedule_text.insert(tk.END, "=== JADWAL PENGGUNAAN ALAT ===\n\n")
        
        if not schedule:
            self.schedule_text.insert(tk.END, "Tidak ada alat untuk dijadwalkan.")
        else:
            for name, details in schedule.items():
                hours = details["hours"]
                hours_str = ", ".join([f"{h}:00-{h+1}:00" for h in hours])
                power = details["power"]
                days = details["days_per_week"]
                kwh = details["kwh_per_week"] * 30 / 7  # Konversi ke bulanan
                
                self.schedule_text.insert(tk.END, f"{name}:\n")
                self.schedule_text.insert(tk.END, f"  - Penggunaan: {len(hours)} jam/hari, {days} hari/minggu\n")
                self.schedule_text.insert(tk.END, f"  - Waktu optimal: {hours_str}\n")
                self.schedule_text.insert(tk.END, f"  - Daya: {power} Watt\n")
                self.schedule_text.insert(tk.END, f"  - Estimasi konsumsi: {kwh:.2f} kWh/bulan\n")
                self.schedule_text.insert(tk.END, f"  - Estimasi biaya: Rp {kwh * self.house_data['tarif_per_kwh']:,.2f}/bulan\n\n")
        
        # Update rekomendasi penghematan
        self.recommendation_text.delete(1.0, tk.END)
        
        if not savings_recommendations:
            self.recommendation_text.insert(tk.END, "Penggunaan listrik sudah optimal dan sesuai anggaran. Tidak ada rekomendasi penghematan khusus.")
        else:
            for rec in savings_recommendations:
                self.recommendation_text.insert(tk.END, f"- {rec}\n")
        
        # Update grafik
        self.update_graph(schedule)
    
    def update_graph(self, schedule):
        self.ax.clear()
        
        # Buat data penggunaan daya per jam
        hourly_usage = [0] * 24
        
        for device_name, details in schedule.items():
            for hour in details["hours"]:
                hourly_usage[hour] += details["power"]
        
        # Buat grafik batang
        hours = list(range(24))
        self.ax.bar(hours, hourly_usage, color='royalblue')
        
        # Tambahkan garis untuk max watt
        max_watt = self.house_data["max_watt"]
        self.ax.axhline(y=max_watt, color='r', linestyle='-', label=f'Kapasitas Max ({max_watt} Watt)')
        
        # Tambahkan label
        self.ax.set_xlabel('Jam')
        self.ax.set_ylabel('Penggunaan Daya (Watt)')
        self.ax.set_title('Penggunaan Daya Listrik per Jam')
        self.ax.set_xticks(hours)
        self.ax.set_xticklabels([f"{h}:00" for h in hours], rotation=45)
        self.ax.legend()
        
        # Refresh grafik
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = ElectricityOptimizer(root)
    root.mainloop()