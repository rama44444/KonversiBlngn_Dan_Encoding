import tkinter as tk
from tkinter import ttk, messagebox

# ======================================================================
#  TAB 1: SIMULATOR LOGIKA DIGITAL (KODE LAMA ANDA, DIRAPIKAN JADI TAB)
# ======================================================================
class CounterTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1e1e1e")

        self.count = 0
        self.is_running = True
        self.count_dir = 1
        self.speed_delay = 800

        self.font_digit = ("Consolas", 32, "bold")
        self.font_bin   = ("Consolas", 20, "bold")
        self.font_label = ("Segoe UI", 11, "bold")
        self.font_math  = ("Consolas", 10)

        top_container = tk.Frame(self, bg="#1e1e1e")
        top_container.pack(pady=10, fill="x")

        frame_dec = tk.Frame(top_container, bg="#1e1e1e")
        frame_dec.pack(side=tk.TOP, pady=5)
        tk.Label(frame_dec, text="DECIMAL (10)", fg="#aaa", bg="#1e1e1e", font=self.font_label).pack()
        self.entry_dec = tk.Entry(frame_dec, font=self.font_digit, justify='center', width=5,
                                   bg="black", fg="#FF3333", insertbackground="white")
        self.entry_dec.pack()
        self.entry_dec.bind("<Return>", self.manual_input)
        tk.Label(frame_dec, text="(Ketik 0-255 lalu Enter)", fg="gray", bg="#1e1e1e", font=("Arial", 8)).pack()

        frame_hex = tk.Frame(top_container, bg="#1e1e1e")
        frame_hex.pack(side=tk.TOP, pady=10)
        tk.Label(frame_hex, text="HEXADECIMAL (16)", fg="#aaa", bg="#1e1e1e", font=self.font_label).pack()
        self.lbl_hex = tk.Label(frame_hex, text="00", font=self.font_digit, fg="#33FF33", bg="black", width=4, relief="sunken")
        self.lbl_hex.pack()

        frame_bin = tk.Frame(top_container, bg="#1e1e1e")
        frame_bin.pack(side=tk.TOP, pady=10)
        tk.Label(frame_bin, text="BINARY (2) - Klik bit untuk ubah!", fg="#aaa", bg="#1e1e1e", font=self.font_label).pack()

        bits_container = tk.Frame(frame_bin, bg="#1e1e1e")
        bits_container.pack(pady=5)

        self.bit_buttons = []
        for i in range(7, -1, -1):
            f_col = tk.Frame(bits_container, bg="#1e1e1e")
            f_col.pack(side=tk.LEFT, padx=3)
            btn = tk.Button(f_col, text="0", font=self.font_bin, width=2, bg="#333", fg="cyan",
                             command=lambda idx=i: self.toggle_bit(idx))
            btn.pack()
            self.bit_buttons.append(btn)
            tk.Label(f_col, text=str(2 ** i), fg="gray", bg="#1e1e1e", font=("Arial", 8)).pack()

        ctrl_frame = tk.Frame(self, bg="#2a2a2a", bd=1, relief="groove")
        ctrl_frame.pack(fill="x", padx=20, pady=5)

        btn_row = tk.Frame(ctrl_frame, bg="#2a2a2a")
        btn_row.pack(pady=5)

        self.btn_pause = tk.Button(btn_row, text="Pause", command=self.toggle_pause, width=10, bg="#ddd")
        self.btn_pause.pack(side=tk.LEFT, padx=5)
        tk.Button(btn_row, text="Step (+1)", command=self.manual_step, width=10, bg="#88ccff").pack(side=tk.LEFT, padx=5)
        self.btn_dir = tk.Button(btn_row, text="Mode: UP \u25b2", command=self.toggle_direction, width=12, bg="#ffffcc")
        self.btn_dir.pack(side=tk.LEFT, padx=5)
        tk.Button(btn_row, text="Reset", command=self.reset_count, width=8, bg="#ffaaaa").pack(side=tk.LEFT, padx=5)

        slider_row = tk.Frame(ctrl_frame, bg="#2a2a2a")
        slider_row.pack(pady=5, fill="x", padx=20)
        tk.Label(slider_row, text="Kecepatan:", fg="white", bg="#2a2a2a").pack(side=tk.LEFT)
        self.speed_slider = tk.Scale(slider_row, from_=50, to=2000, orient=tk.HORIZONTAL, bg="#2a2a2a",
                                      fg="white", highlightthickness=0, command=self.update_speed)
        self.speed_slider.set(800)
        self.speed_slider.pack(side=tk.LEFT, fill="x", expand=True, padx=10)

        formula_frame = tk.Frame(self, bg="#1e1e1e")
        formula_frame.pack(fill="both", expand=True, padx=10, pady=5)

        left_pane = tk.LabelFrame(formula_frame, text=" [LOGIKA 1] Desimal ke Heksadesimal (\u00f7 16) ",
                                   fg="#55FF55", bg="#1e1e1e", font=self.font_label)
        left_pane.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        self.txt_hex_logic = tk.Text(left_pane, height=8, bg="#000", fg="#ddd", font=self.font_math, bd=0, padx=10, pady=10)
        self.txt_hex_logic.pack(fill="both", expand=True)

        right_pane = tk.LabelFrame(formula_frame, text=" [LOGIKA 2] Desimal ke Biner (Bobot Bit) ",
                                    fg="cyan", bg="#1e1e1e", font=self.font_label)
        right_pane.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        self.txt_bin_logic = tk.Text(right_pane, height=8, bg="#000", fg="#ddd", font=self.font_math, bd=0, padx=10, pady=10)
        self.txt_bin_logic.pack(fill="both", expand=True)

        self.refresh_display()
        self.run_timer()

    def toggle_bit(self, bit_index):
        self.is_running = False
        self.btn_pause.config(text="Resume")
        mask = 1 << bit_index
        self.count = self.count ^ mask
        self.refresh_display()

    def manual_input(self, event):
        try:
            val = int(self.entry_dec.get())
            if 0 <= val <= 255:
                self.count = val
                self.is_running = False
                self.btn_pause.config(text="Resume")
                self.refresh_display()
            else:
                messagebox.showerror("Error", "Range 0-255")
        except ValueError:
            pass

    def update_speed(self, val):
        self.speed_delay = int(val)

    def toggle_direction(self):
        self.count_dir *= -1
        self.btn_dir.config(text="Mode: UP \u25b2" if self.count_dir == 1 else "Mode: DOWN \u25bc")

    def toggle_pause(self):
        self.is_running = not self.is_running
        self.btn_pause.config(text="Pause" if self.is_running else "Resume")

    def manual_step(self):
        self.is_running = False
        self.btn_pause.config(text="Resume")
        self.increment_logic()

    def reset_count(self):
        self.count = 0
        self.refresh_display()

    def increment_logic(self):
        self.count = (self.count + self.count_dir) % 256
        self.refresh_display()

    def run_timer(self):
        if self.is_running:
            self.increment_logic()
        self.after(self.speed_delay, self.run_timer)

    def refresh_display(self):
        self.entry_dec.delete(0, tk.END)
        self.entry_dec.insert(0, str(self.count))
        self.lbl_hex.config(text=f"{self.count:02X}")

        for i, btn in enumerate(self.bit_buttons):
            bit_idx = 7 - i
            is_on = (self.count >> bit_idx) & 1
            btn.config(text="1" if is_on else "0",
                       bg="#004400" if is_on else "#333",
                       fg="#00FF00" if is_on else "#555")

        self.update_logic_text()

    def update_logic_text(self):
        val = self.count
        digit_high = val // 16
        digit_low = val % 16

        def get_hex_char_desc(n):
            if n < 10:
                return f"{n}"
            char = chr(ord('A') + n - 10)
            return f"{n} ('{char}')"

        desc_high = get_hex_char_desc(digit_high)
        desc_low = get_hex_char_desc(digit_low)

        hex_text = (
            f"Angka Desimal : {val}\n"
            f"Rumus         : Bagi dengan 16\n"
            f"----------------------------------------\n"
            f"[1] DIGIT PERTAMA (Kiri):\n"
            f"    {val} \u00f7 16 = {digit_high} (Sisa {digit_low})\n"
            f"    -> Ambil hasil bagi: {desc_high}\n\n"
            f"[2] DIGIT KEDUA (Kanan):\n"
            f"    -> Ambil sisa bagi : {desc_low}\n"
            f"----------------------------------------\n"
            f"HASIL AKHIR: {digit_high:X}{digit_low:X}"
        )
        self.txt_hex_logic.delete(1.0, tk.END)
        self.txt_hex_logic.insert(1.0, hex_text)

        bin_parts = []
        calculation_str = ""
        total_check = 0
        for i in range(7, -1, -1):
            weight = 2 ** i
            is_active = (val >> i) & 1
            if is_active:
                bin_parts.append("1")
                calculation_str += f"({weight}) + "
                total_check += weight
            else:
                bin_parts.append("0")

        if calculation_str.endswith(" + "):
            calculation_str = calculation_str[:-3]
        if val == 0:
            calculation_str = "0"

        bin_str_display = " ".join(bin_parts)
        bin_text = (
            f"Angka Desimal : {val}\n"
            f"Visual Bit    : {bin_str_display}\n"
            f"----------------------------------------\n"
            f"Rumus: Menjumlahkan bobot bit yang bernilai '1'\n\n"
            f"Perhitungan:\n"
            f"   {calculation_str}\n"
            f"   = {total_check}\n\n"
            f"Bobot Bit Referensi:\n"
            f"128  64  32  16   8   4   2   1"
        )
        self.txt_bin_logic.delete(1.0, tk.END)
        self.txt_bin_logic.insert(1.0, bin_text)


# ======================================================================
#  TAB 2: SIMULATOR ENCODING DIGITAL + PARITY (FITUR BARU)
# ======================================================================
class EncodingTab(tk.Frame):
    """
    Alur seperti pada slide 'Pengkodean Data':
      1. Karakter -> kode Unicode/ASCII (7-bit) -> Hex -> Biner
      2. Hitung parity bit (Even / Odd)
      3. Bentuk frame serial: [Start(0)] [Data 7-bit] [Parity] [Stop(1)]
      4. Gambarkan frame sebagai gelombang sesuai skema line-coding:
         NRZ-L, NRZI, Bipolar-AMI, Pseudoternary
    """

    BIT_W = 40      # lebar tiap bit (px)
    AMP = 55        # amplitudo (px) mewakili 15V
    TOP_MARGIN = 60
    LABEL_GAP = 22

    def __init__(self, parent):
        super().__init__(parent, bg="#1e1e1e")
        self.font_label = ("Segoe UI", 11, "bold")
        self.font_mono = ("Consolas", 10)

        # ---------- Panel kontrol input ----------
        ctrl = tk.Frame(self, bg="#2a2a2a", bd=1, relief="groove")
        ctrl.pack(fill="x", padx=10, pady=8)

        tk.Label(ctrl, text="Teks / Data:", fg="white", bg="#2a2a2a", font=self.font_label).grid(
            row=0, column=0, padx=6, pady=8, sticky="w")
        self.entry_text = tk.Entry(ctrl, font=("Consolas", 14), width=18, bg="black", fg="#FFDD33",
                                    insertbackground="white")
        self.entry_text.insert(0, "SY")
        self.entry_text.grid(row=0, column=1, padx=6, pady=8, sticky="w")

        tk.Label(ctrl, text="Line Code:", fg="white", bg="#2a2a2a", font=self.font_label).grid(
            row=0, column=2, padx=6, pady=8, sticky="w")
        self.cmb_scheme = ttk.Combobox(ctrl, state="readonly", width=14,
                                        values=["NRZ-L", "NRZI", "Bipolar-AMI", "Pseudoternary"])
        self.cmb_scheme.current(0)
        self.cmb_scheme.grid(row=0, column=3, padx=6, pady=8)

        tk.Label(ctrl, text="Parity:", fg="white", bg="#2a2a2a", font=self.font_label).grid(
            row=0, column=4, padx=6, pady=8, sticky="w")
        self.cmb_parity = ttk.Combobox(ctrl, state="readonly", width=8,
                                        values=["Even", "Odd", "Tanpa"])
        self.cmb_parity.current(0)
        self.cmb_parity.grid(row=0, column=5, padx=6, pady=8)

        tk.Button(ctrl, text="Generate \u25b6", command=self.generate, bg="#88ccff",
                  font=self.font_label).grid(row=0, column=6, padx=10, pady=8)

        if self.BIT_ORDER == "LSB":
            note_text = "\u2139 Mode: bit DATA dibaca/dikirim dari BELAKANG (LSB / bit terkecil duluan)"
            note_fg = "#FFCC66"
        else:
            note_text = "\u2139 Mode: bit DATA dibaca/dikirim dari DEPAN (MSB / bit terbesar duluan) - standar"
            note_fg = "#88ccff"
        tk.Label(ctrl, text=note_text, fg=note_fg, bg="#2a2a2a",
                 font=("Segoe UI", 9, "italic")).grid(row=1, column=0, columnspan=7, padx=6, pady=(0, 8), sticky="w")

        # ---------- Tabel hasil (mirip gambar 2 pada lampiran) ----------
        table_title = " Tabel Konversi Karakter "
        wave_title = " Bentuk Gelombang (Line Coding) "
        if self.BIT_ORDER == "LSB":
            table_title = " Tabel Konversi Karakter (Kirim Data: LSB dulu) "
            wave_title = " Bentuk Gelombang (Line Coding) - Data dibaca dari BELAKANG (LSB First) "

        table_frame = tk.LabelFrame(self, text=table_title, fg="#55FF55", bg="#1e1e1e",
                                     font=self.font_label)
        table_frame.pack(fill="x", padx=10, pady=5)
        self.txt_table = tk.Text(table_frame, height=6, bg="#000", fg="#ddd", font=self.font_mono, bd=0,
                                  padx=10, pady=8)
        self.txt_table.pack(fill="both", expand=True)

        # ---------- Canvas gelombang (scrollable) ----------
        wave_frame = tk.LabelFrame(self, text=wave_title, fg="cyan", bg="#1e1e1e",
                                    font=self.font_label)
        wave_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(wave_frame, bg="white", height=260)
        hbar = tk.Scrollbar(wave_frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=hbar.set)
        self.canvas.pack(side="top", fill="both", expand=True)
        hbar.pack(side="bottom", fill="x")

        self.generate()

    # Urutan pembacaan/pengiriman bit data. "MSB" = dari depan (bit besar dulu,
    # perilaku asli). "LSB" = dari belakang (bit kecil dulu). Di-override oleh
    # subclass EncodingTabLSB.
    BIT_ORDER = "MSB"

    # ---------------- Logika parity & framing ----------------
    def build_frames(self, text, parity_mode):
        frames = []
        for ch in text:
            code = ord(ch) & 0x7F  # 7-bit ASCII, sama seperti contoh di slide
            bin7 = format(code, "07b")  # representasi biner standar (MSB->LSB), dipakai di tabel
            ones = bin7.count("1")

            if parity_mode == "Even":
                parity = ones % 2               # tambah 1 jika ganjil, agar total genap
            elif parity_mode == "Odd":
                parity = 1 - (ones % 2)          # tambah 1 jika genap, agar total ganjil
            else:
                parity = None

            # Urutan bit data yang BENAR-BENAR dibaca/dikirim & digambar di gelombang.
            # Tabel tetap menampilkan bin7 apa adanya (MSB->LSB) sebagai referensi,
            # tapi untuk tab "baca dari belakang", bit data dibalik (LSB duluan).
            if self.BIT_ORDER == "LSB":
                data_sequence = bin7[::-1]
            else:
                data_sequence = bin7

            bits = [0]  # start bit selalu 0
            bits.extend(int(b) for b in data_sequence)
            if parity is not None:
                bits.append(parity)
            bits.append(1)  # stop/end bit selalu 1

            frames.append({
                "char": ch, "code": code, "bin7": bin7,
                "ones": ones, "parity": parity, "bits": bits,
            })
        return frames

    def fill_table(self, frames, parity_mode):
        header = f"{'Char':<6}{'Unicode':<10}{'Hex':<8}{'Biner(7bit)':<14}{'Jml 1':<8}{'Parity':<8}"
        lines = [header, "-" * len(header)]
        for fr in frames:
            parity_disp = str(fr["parity"]) if fr["parity"] is not None else "-"
            lines.append(
                f"{fr['char']:<6}{fr['code']:04X}      {fr['code']:02X}      "
                f"{fr['bin7']:<14}{fr['ones']:<8}{parity_disp:<8}"
            )
        self.txt_table.delete(1.0, tk.END)
        self.txt_table.insert(1.0, "\n".join(lines))

    # ---------------- Encoding ke level tegangan ----------------
    def encode_levels(self, all_bits, scheme):
        """all_bits: list gabungan bit dari semua frame (berurutan).
        Mengembalikan list level (-1, 0, +1) sepanjang all_bits, dengan
        state (NRZI / AMI / Pseudoternary) menyambung antar karakter."""
        levels = []
        last_nrzi = -1
        last_polarity = -1
        for b in all_bits:
            if scheme == "NRZ-L":
                level = 1 if b == 1 else -1
            elif scheme == "NRZI":
                if b == 1:
                    last_nrzi *= -1
                level = last_nrzi
            elif scheme == "Bipolar-AMI":
                if b == 1:
                    last_polarity *= -1
                    level = last_polarity
                else:
                    level = 0
            else:  # Pseudoternary
                if b == 0:
                    last_polarity *= -1
                    level = last_polarity
                else:
                    level = 0
            levels.append(level)
        return levels

    # ---------------- Menggambar ----------------
    def draw_waveform(self, frames, scheme):
        c = self.canvas
        c.delete("all")

        all_bits = []
        for fr in frames:
            all_bits.extend(fr["bits"])
        levels = self.encode_levels(all_bits, scheme)

        mid_y = self.TOP_MARGIN + self.AMP
        x = 40

        # Sumbu referensi tegangan
        c.create_line(10, mid_y - self.AMP, 10, mid_y + self.AMP, fill="#999")
        c.create_text(25, mid_y - self.AMP, text="15V", anchor="w", fill="#666", font=self.font_mono)
        c.create_line(10, mid_y, 20, mid_y, fill="#999")
        c.create_text(25, mid_y, text="0V", anchor="w", fill="#666", font=self.font_mono)
        c.create_text(25, mid_y + self.AMP, text="-15V", anchor="w", fill="#666", font=self.font_mono)
        c.create_line(35, mid_y, 35 + len(all_bits) * self.BIT_W + 10, mid_y, fill="#ccc", dash=(2, 2))

        bit_i = 0
        prev_y = None
        for fr in frames:
            seg_start_x = x
            n_data = len(fr["bin7"])
            has_parity = fr["parity"] is not None
            # posisi tiap kelompok, untuk label bawah
            group_bounds = {"start": (x, x + self.BIT_W)}

            for local_idx, b in enumerate(fr["bits"]):
                level = levels[bit_i]
                y = mid_y - level * self.AMP

                if prev_y is not None:
                    c.create_line(x, prev_y, x, y, fill="#0033AA", width=2)
                c.create_line(x, y, x + self.BIT_W, y, fill="#0033AA", width=2)
                c.create_text(x + self.BIT_W / 2, mid_y + self.AMP + 15, text=str(b), font=self.font_mono)

                prev_y = y
                x += self.BIT_W
                bit_i += 1

                if local_idx == n_data:  # akhir data (setelah start=idx0 + 7 bit data)
                    group_bounds["data"] = (seg_start_x + self.BIT_W, x)
                if has_parity and local_idx == n_data + 1:
                    group_bounds["parity"] = (x - self.BIT_W, x)
            group_bounds["stop"] = (x - self.BIT_W, x)

            # Label kelompok bit (start / data / parity / stop)
            def label(range_, text_):
                x0, x1 = range_
                cx = (x0 + x1) / 2
                c.create_line(x0 + 2, mid_y + self.AMP + 28, x1 - 2, mid_y + self.AMP + 28, fill="#333")
                c.create_text(cx, mid_y + self.AMP + 42, text=text_, font=self.font_mono, fill="#222")

            label(group_bounds["start"], "start")
            label(group_bounds["data"], f"Data \"{fr['char']}\"")
            if has_parity:
                label(group_bounds["parity"], "Parity")
            label(group_bounds["stop"], "End")

            x += 15  # jarak antar karakter

        c.config(scrollregion=(0, 0, x + 20, mid_y + self.AMP + 60))

    def generate(self):
        text = self.entry_text.get()
        if not text:
            messagebox.showwarning("Kosong", "Masukkan teks/karakter terlebih dahulu.")
            return
        scheme = self.cmb_scheme.get()
        parity_mode = self.cmb_parity.get()
        parity_mode = None if parity_mode == "Tanpa" else parity_mode

        frames = self.build_frames(text, parity_mode)
        self.fill_table(frames, parity_mode)
        self.draw_waveform(frames, scheme)


# ======================================================================
#  TAB 3: SIMULATOR ENCODING DIGITAL + PARITY (BACA DARI BELAKANG / LSB)
# ======================================================================
class EncodingTabLSB(EncodingTab):
    """
    Sama persis dengan EncodingTab (Tab 2), hanya saja urutan bit DATA yang
    dibaca/dikirim dan digambar pada gelombang dibalik: dimulai dari bit
    paling belakang / LSB (bit terkecil) terlebih dahulu, bukan dari MSB
    (bit terbesar) seperti pada Tab 2.

    Frame yang dikirim tetap: [Start(0)] [7 bit Data] [Parity] [Stop(1)],
    hanya urutan 7 bit datanya yang dibalik.
    """
    BIT_ORDER = "LSB"


# ======================================================================
#  APLIKASI UTAMA
# ======================================================================
class MainApp:
    def __init__(self, root):
        self.root = root
        root.title("Simulator Logika Digital, Konversi Bilangan & Encoding Data")
        root.geometry("1050x850")
        root.configure(bg="#1e1e1e")

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="#1e1e1e", borderwidth=0)
        style.configure("TNotebook.Tab", background="#2a2a2a", foreground="white", padding=(15, 8))
        style.map("TNotebook.Tab", background=[("selected", "#3a3a3a")])

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        tab1 = CounterTab(notebook)
        tab2 = EncodingTab(notebook)
        tab3 = EncodingTabLSB(notebook)
        notebook.add(tab1, text="  Counter Desimal / Biner / Hex  ")
        notebook.add(tab2, text="  Encoding Digital + Parity (Depan/MSB)  ")
        notebook.add(tab3, text="  Encoding Digital + Parity (Belakang/LSB)  ")


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
