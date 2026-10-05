import tkinter as tk
import psutil
from datetime import datetime


class SystemMonitor:

    def __init__(self, root):
        self.root = root

        self.root.title("System Resource Monitor")
        self.root.geometry("650x550")
        self.root.resizable(False, False)

        self.cpu_value = tk.StringVar()
        self.ram_value = tk.StringVar()
        self.disk_value = tk.StringVar()
        self.network_value = tk.StringVar()
        self.process_value = tk.StringVar()
        self.time_value = tk.StringVar()

        self.create_ui()
        self.update_system_info()

    def create_ui(self):

        title = tk.Label(
            self.root,
            text="SYSTEM RESOURCE MONITOR",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=20)

        subtitle = tk.Label(
            self.root,
            text="Real-Time Computer Performance Monitoring",
            font=("Arial", 11)
        )
        subtitle.pack()

        frame = tk.Frame(self.root)
        frame.pack(pady=25, padx=30, fill="both")

        self.create_metric(frame, "CPU Usage", self.cpu_value, 0)
        self.create_metric(frame, "RAM Usage", self.ram_value, 1)
        self.create_metric(frame, "Disk Usage", self.disk_value, 2)
        self.create_metric(frame, "Network", self.network_value, 3)
        self.create_metric(frame, "Running Processes", self.process_value, 4)

        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=15)

        tk.Label(
            status_frame,
            text="System Status:",
            font=("Arial", 12, "bold")
        ).pack(side="left")

        self.status_label = tk.Label(
            status_frame,
            text="Checking...",
            font=("Arial", 12, "bold")
        )
        self.status_label.pack(side="left", padx=10)

        tk.Label(
            self.root,
            textvariable=self.time_value,
            font=("Arial", 10)
        ).pack(pady=10)

        refresh_button = tk.Button(
            self.root,
            text="Refresh Now",
            font=("Arial", 11, "bold"),
            command=self.update_system_info
        )
        refresh_button.pack(pady=10)

    def create_metric(self, parent, name, variable, row):

        tk.Label(
            parent,
            text=name,
            font=("Arial", 12, "bold"),
            width=20,
            anchor="w"
        ).grid(row=row, column=0, pady=8, sticky="w")

        tk.Label(
            parent,
            textvariable=variable,
            font=("Arial", 12),
            width=25,
            anchor="w"
        ).grid(row=row, column=1, pady=8, sticky="w")

    def update_system_info(self):

        cpu = psutil.cpu_percent(interval=0.5)

        memory = psutil.virtual_memory()
        ram = memory.percent

        disk = psutil.disk_usage("C:\\").percent

        network = psutil.net_io_counters()

        upload = network.bytes_sent / (1024 * 1024)
        download = network.bytes_recv / (1024 * 1024)

        processes = len(psutil.pids())

        current_time = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        self.cpu_value.set(f"{cpu:.1f}%")
        self.ram_value.set(f"{ram:.1f}%")
        self.disk_value.set(f"{disk:.1f}%")

        self.network_value.set(
            f"↑ {upload:.1f} MB  ↓ {download:.1f} MB"
        )

        self.process_value.set(str(processes))

        self.time_value.set(
            f"Last Updated: {current_time}"
        )

        if cpu > 80 or ram > 80 or disk > 90:
            self.status_label.config(
                text="HIGH RESOURCE USAGE"
            )
        else:
            self.status_label.config(
                text="SYSTEM NORMAL"
            )

        self.root.after(2000, self.update_system_info)


if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitor(root)
    root.mainloop()