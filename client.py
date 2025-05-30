import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser


class FaceitFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Faceit Finder (CS2) - by Kacper Pianka")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        self.bg_color = "#000000"
        self.frame_color = "#1E1E1E"
        self.text_color = "#FFFFFF"
        self.accent_color = "#FF6F00"
        self.secondary_color = "#FF8F00"
        self.error_color = "#CF6679"
        self.stats_bg_color = "#2A2A2A"

        self.font_standard = ("Arial", 10)
        self.font_bold = ("Arial", 12, "bold")
        self.font_small = ("Arial", 8)
        self.font_title = ("Arial", 14, "bold")
        self.font_stats = ("Arial", 10, "bold")

        self.root.configure(bg=self.bg_color)
        self.setup_ui()
        self.current_player_id = None
        self.avatar_img = None
        self.steam_profile_url = None
        self.api_url = "http://localhost:5000/api/player"

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(main_frame, text="FACEIT STATS FINDER", font=self.font_title, fg=self.accent_color,
                 bg=self.bg_color).pack(pady=(0, 20))

        input_frame = tk.Frame(main_frame, bg=self.bg_color)
        input_frame.pack(fill="x", pady=(0, 15))

        tk.Label(input_frame, text="Wprowadź Steam URL:", font=self.font_bold, fg=self.text_color,
                 bg=self.bg_color).pack(anchor="w", pady=(0, 5))
        self.entry = ttk.Entry(input_frame, font=self.font_standard, width=40)
        self.entry.pack(fill="x")

        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill="x", pady=(20, 0))

        style = ttk.Style()
        style.theme_use('alt')
        style.configure("TButton", font=self.font_bold, padding=10, background=self.accent_color,
                        foreground="#000000", borderwidth=0)
        style.map("TButton", background=[("active", self.secondary_color)], foreground=[("active", "#000000")])

        self.search_button = ttk.Button(button_frame, text="SZUKAJ GRACZA", command=self.find_faceit, style="TButton")
        self.search_button.pack(ipadx=30, ipady=5)

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, pady=(20, 0))

        # Statystyki gracza
        self.result_frame = tk.Frame(self.notebook, bg=self.frame_color)
        self.notebook.add(self.result_frame, text="Statystyki gracza")

        # Znajomi
        self.friends_frame = tk.Frame(self.notebook, bg=self.frame_color)
        self.notebook.add(self.friends_frame, text="Znajomi na Steam")

        # Footer
        tk.Label(self.root, text=f"\u00a9 {datetime.now().year} Faceit Stats Finder by Kacper Pianka",
                 font=self.font_small, fg="#777777", bg=self.bg_color).pack(side="bottom", pady=(0, 10))

    def open_steam_profile(self, event=None):
        if self.steam_profile_url:
            webbrowser.open(self.steam_profile_url)

    def find_faceit(self):
        steam_url = self.entry.get().strip()
        self.clear_results()

        if not steam_url:
            messagebox.showerror("Błąd", "Wprowadź URL profilu Steam!")
            return

        try:
            response = requests.get(self.api_url, params={"steam_url": steam_url})
            data = response.json()

            if response.status_code != 200:
                messagebox.showerror("Błąd", data.get("error", "Nieznany błąd serwera"))
                return

            self.steam_profile_url = data['steam_profile_url']
            self.display_avatar(data['avatar_url'])
            self.display_selected_stats(
                data['nick'],
                data['elo'],
                data['level'],
                data['stats'],
                data['hours_played'],
                data['hours_2weeks'],
                data['steam_status'],
                data['steam_creation']
            )
            self.display_friends(data['friends'])

        except Exception as e:
            messagebox.showerror("Błąd", f"Problem z połączeniem: {str(e)}")

    def clear_results(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        for widget in self.friends_frame.winfo_children():
            widget.destroy()
        self.avatar_img = None

    def display_selected_stats(self, nick, elo, level, stats, hours_played, hours_2weeks, steam_status, steam_creation):
        # Główny kontener
        main_container = tk.Frame(self.result_frame, bg=self.frame_color)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Lewa kolumna (avatar + podstawowe info)
        left_frame = tk.Frame(main_container, bg=self.frame_color)
        left_frame.pack(side="left", fill="y", padx=5, pady=5)

        # Avatar
        if hasattr(self, 'avatar_img') and self.avatar_img:
            avatar_label = tk.Label(left_frame, image=self.avatar_img, bg=self.frame_color, cursor="hand2")
            avatar_label.pack(pady=(0, 10))
            avatar_label.bind("<Button-1>", self.open_steam_profile)

        # Podstawowe informacje
        info_frame = tk.Frame(left_frame, bg=self.stats_bg_color, padx=10, pady=10)
        info_frame.pack(fill="x")

        tk.Label(info_frame, text=nick.upper(), font=self.font_bold, fg=self.accent_color, bg=self.stats_bg_color).pack(
            anchor="w")
        tk.Label(info_frame, text=f"ELO: {elo}", font=self.font_standard, fg=self.text_color,
                 bg=self.stats_bg_color).pack(anchor="w")
        tk.Label(info_frame, text=f"Poziom: {level}", font=self.font_standard, fg=self.text_color,
                 bg=self.stats_bg_color).pack(anchor="w")

        # Statystyki Steam
        steam_frame = tk.Frame(left_frame, bg=self.stats_bg_color, padx=10, pady=10)
        steam_frame.pack(fill="x", pady=(10, 0))

        tk.Label(steam_frame, text="STEAM INFO", font=self.font_bold, fg=self.accent_color,
                 bg=self.stats_bg_color).pack(anchor="w")
        tk.Label(steam_frame, text=f"Status: {steam_status}", font=self.font_standard, fg=self.text_color,
                 bg=self.stats_bg_color).pack(anchor="w")
        tk.Label(steam_frame, text=f"Utworzono: {steam_creation}", font=self.font_standard, fg=self.text_color,
                 bg=self.stats_bg_color).pack(anchor="w")
        tk.Label(steam_frame, text=f"Godziny w CS2: {hours_played if hours_played else 'brak'}",
                 font=self.font_standard, fg=self.text_color, bg=self.stats_bg_color).pack(anchor="w")
        tk.Label(steam_frame, text=f"Godziny (2 tyg.): {hours_2weeks if hours_2weeks else 'brak'}",
                 font=self.font_standard, fg=self.text_color, bg=self.stats_bg_color).pack(anchor="w")

        # Prawa kolumna (statystyki FACEIT)
        right_frame = tk.Frame(main_container, bg=self.frame_color)
        right_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        stats_frame = tk.Frame(right_frame, bg=self.stats_bg_color, padx=10, pady=10)
        stats_frame.pack(fill="both", expand=True)

        if stats and 'lifetime' in stats:
            lifetime = stats['lifetime']

            tk.Label(stats_frame, text="STATYSTYKI FACEIT", font=self.font_bold, fg=self.accent_color,
                     bg=self.stats_bg_color).pack(anchor="w")

            # Statystyki w formie tabeli
            stats_grid = tk.Frame(stats_frame, bg=self.stats_bg_color)
            stats_grid.pack(fill="x", pady=(5, 0))

            stats_data = [
                ("K/D Ratio", f"{round(float(lifetime.get('Average K/D Ratio', 0)), 2)}"),
                ("Headshots %", f"{round(float(lifetime.get('Average Headshots %', 0)), 1)}%"),
                ("Win Rate %", f"{round(float(lifetime.get('Win Rate %', 0)), 1)}%"),
                ("Mecze", lifetime.get('Matches', 'brak')),
                ("Wygrane", lifetime.get('Wins', 'brak')),
                ("Ostatnie wyniki", ' '.join(str(r) for r in lifetime.get('Recent Results', [])))
            ]

            for i, (stat_name, stat_value) in enumerate(stats_data):
                row_frame = tk.Frame(stats_grid, bg=self.stats_bg_color)
                row_frame.grid(row=i, column=0, sticky="ew", pady=2)

                tk.Label(row_frame, text=stat_name + ":", width=15, anchor="w",
                         font=self.font_standard, fg=self.text_color, bg=self.stats_bg_color).pack(side="left")
                tk.Label(row_frame, text=stat_value, anchor="w",
                         font=self.font_stats, fg=self.accent_color, bg=self.stats_bg_color).pack(side="left")
        else:
            tk.Label(stats_frame, text="BRAK DANYCH STATYSTYCZNYCH",
                     font=self.font_bold, fg=self.error_color, bg=self.stats_bg_color).pack()

    def display_avatar(self, url):
        if not url:
            return

        try:
            response = requests.get(url)
            image_data = response.content
            image = Image.open(BytesIO(image_data)).resize((128, 128))
            self.avatar_img = ImageTk.PhotoImage(image)
        except Exception:
            self.avatar_img = None

    def display_friends(self, friends):
        for widget in self.friends_frame.winfo_children():
            widget.destroy()

        if not friends:
            tk.Label(self.friends_frame, text="Brak znajomych do wyświetlenia",
                     font=self.font_standard, fg=self.text_color, bg=self.frame_color).pack(anchor="nw")
            return

        canvas = tk.Canvas(self.friends_frame, bg=self.frame_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.friends_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.frame_color)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for friend in friends:
            persona_name = friend.get('personaname', 'Nieznany')
            steam_id = friend.get('steamid')
            profile_url = f"https://steamcommunity.com/profiles/{steam_id}"

            label = tk.Label(scrollable_frame, text=persona_name, font=self.font_standard,
                             fg=self.accent_color, bg=self.frame_color, cursor="hand2")
            label.pack(anchor="nw", pady=2)
            label.bind("<Button-1>", lambda e, url=profile_url: webbrowser.open(url))


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceitFinderApp(root)
    root.mainloop()