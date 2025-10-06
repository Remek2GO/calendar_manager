import tkinter as tk
from tkinter import Frame, LEFT, Y, BOTH, TOP, RIGHT, X
import matplotlib.pyplot as plt
import datetime
import os
from ics import Calendar
from matplotlib.colors import to_rgba
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Harmonogram zajęć")
        self.root.geometry("1200x800")

        self.root.iconphoto(False, tk.PhotoImage(file='.resources/icon.png'))
        # ----------------------

        # --- Główne ramki aplikacji ---
        self.control_frame = Frame(root, padx=10, pady=10)
        self.control_frame.pack(side=LEFT, fill=Y)

        self.plot_frame = Frame(root)
        self.plot_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        # --- Wczytywanie danych ---
        self.load_data()

        if not self.schedule:
            tk.Label(self.root, text="Nie znaleziono żadnych wydarzeń w plikach ICS.", font=("Arial", 16)).pack(pady=50)
            return

        # --- Przygotowanie danych do wizualizacji ---
        self.prepare_schedule_for_view()
        
        # --- Tworzenie elementów sterujących ---
        self.create_controls()

        # --- Konfiguracja osadzonego wykresu Matplotlib ---
        self.fig = Figure(figsize=(10, 7), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=TOP, fill=BOTH, expand=True)

        # --- Inicjalne narysowanie wykresu ---
        self.on_checkboxes_change()

    def load_data(self):
        # Ścieżka do folderu z plikami ICS
        # Upewnij się, że ta ścieżka jest poprawna dla Twojego systemu
        folder_path = "/home/remek2go/Downloads/calendars"
        self.schedule = []
        self.ics_files = []

        try:
            self.ics_files = [f for f in os.listdir(folder_path) if f.endswith(".ics")]
        except FileNotFoundError:
            tk.Label(self.root, text=f"Błąd: Folder '{folder_path}' nie został znaleziony.", fg="red").pack()
            return

        for ics_file in self.ics_files:
            with open(os.path.join(folder_path, ics_file), "r", encoding="utf-8") as file:
                calendar = Calendar(file.read())
                for event in calendar.events:
                    self.schedule.append((event.begin, event.end, event.name, ics_file))
        
        self.schedule.sort()

    def prepare_schedule_for_view(self):
        start_date = min(event[0] for event in self.schedule).date()
        end_date = start_date + datetime.timedelta(days=6)
        self.weekly_schedule = [e for e in self.schedule if start_date <= e[0].date() <= end_date]
        self.days = ["Pon", "Wt", "Śr", "Czw", "Pt"]
        self.day_map = {day: i for i, day in enumerate(self.days)}
        self.file_colors = {file: plt.cm.tab10(i % 10) for i, file in enumerate(self.ics_files)}

    def create_controls(self):
        tk.Label(self.control_frame, text="Wybierz kalendarze:", font=("Arial", 12, "bold")).pack(pady=5)
        self.checkboxes = {}
        for file in self.ics_files:
            var = tk.BooleanVar(value=True)
            checkbox = tk.Checkbutton(self.control_frame, text=file, variable=var, anchor='w')
            checkbox.pack(fill=X)
            self.checkboxes[file] = var

        self.show_lectures_var = tk.BooleanVar(value=True)
        show_lectures_checkbox = tk.Checkbutton(self.control_frame, text="Pokaż wykłady (W)", variable=self.show_lectures_var)
        show_lectures_checkbox.pack(pady=(10, 0))

        button = tk.Button(self.control_frame, text="Zaktualizuj wykres", command=self.on_checkboxes_change)
        button.pack(pady=10)

    def on_checkboxes_change(self):
        selected_files = [file for file, var in self.checkboxes.items() if var.get()]
        self.update_plot(selected_files)

    def update_plot(self, selected_files):
        # 1. Wyczyść poprzedni wykres
        self.ax.clear()

        # 2. Przefiltruj dane
        filtered_events = [event for event in self.weekly_schedule if event[3] in selected_files]
        if not self.show_lectures_var.get():
            filtered_events = [event for event in filtered_events if not event[2].startswith("W")]

        if not filtered_events:
            self.ax.text(0.5, 0.5, "Brak wydarzeń do wyświetlenia", ha='center', va='center')
            self.canvas.draw()
            return
            
        # 3. Logika rysowania (przeniesiona z oryginalnego kodu)
        day_events_filtered = {day: [] for day in self.days}
        for event in filtered_events:
            if event[0].weekday() < 5:
                day_events_filtered[self.days[event[0].weekday()]].append(event)
        
        plotted_bars_with_info = []
        used_files = set()

        for day, events in day_events_filtered.items():
            events.sort(key=lambda e: e[0])
            hour_events = {}
            for event in events:
                start_hour = event[0].hour
                if start_hour not in hour_events: hour_events[start_hour] = []
                hour_events[start_hour].append(event)
            
            for hour, hour_events_list in hour_events.items():
                num_events = len(hour_events_list)
                for i, event in enumerate(hour_events_list):
                    start_time = event[0].time()
                    end_time = event[1].time()
                    height = 0.8 / num_events if num_events > 1 else 0.8
                    position = self.day_map[day] - 0.4 + (i * height)
                    base_color = self.file_colors[event[3]]
                    color_with_alpha = to_rgba(base_color, alpha=min(1, 0.5 + 0.5 * num_events / 10))
                    file_label = event[3] if event[3] not in used_files else None
                    duration = (datetime.datetime.combine(datetime.date.today(), end_time) - datetime.datetime.combine(datetime.date.today(), start_time)).seconds / 3600
                    
                    bar_container = self.ax.barh(position, duration, left=start_time.hour + start_time.minute / 60, color=color_with_alpha, label=file_label, height=height, align='edge')
                    plotted_bars_with_info.append((bar_container[0], event[2]))
                    used_files.add(event[3])

        # Ustawienia osi i etykiet
        for i in range(len(self.days) - 1): self.ax.axhline(i + 0.5, color='gray', linestyle='--', linewidth=0.7, alpha=0.7)
        for hour in range(7, 21): self.ax.axvline(hour, color='gray', linestyle='--', linewidth=0.7, alpha=0.7)
        self.ax.set_yticks(range(len(self.days)))
        self.ax.set_yticklabels(self.days)
        self.ax.set_xlim(7, 20)
        self.ax.set_xlabel("Godzina")
        self.ax.set_ylabel("Dzień tygodnia")
        self.ax.set_title("Harmonogram zajęć na tydzień")
        self.ax.legend(title="Pliki ICS", loc="upper right")
        self.fig.tight_layout()

        # 4. Logika etykiety przy najechaniu myszą
        annot = self.ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                                 bbox=dict(boxstyle="round", fc="yellow", ec="black", lw=1),
                                 arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        def on_hover(event):
            is_visible = annot.get_visible()
            if event.inaxes == self.ax:
                for bar, name in plotted_bars_with_info:
                    if bar.contains(event)[0]:
                        annot.set_text(name)
                        annot.xy = (event.xdata, event.ydata)
                        annot.set_visible(True)
                        self.canvas.draw_idle()
                        return
            if is_visible:
                annot.set_visible(False)
                self.canvas.draw_idle()

        self.canvas.mpl_connect("motion_notify_event", on_hover)

        # 5. Odśwież płótno
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()