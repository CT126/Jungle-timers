import tkinter as tk
import time
import threading

timers = {}

def countdown(t, label, reset_event):
    while t > 0 and not reset_event.is_set():
        mins, secs = divmod(t, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        label.config(text=time_format)
        time.sleep(1)
        t -= 1
    if not reset_event.is_set():
        label.config(text="Respawn!")
    else:
        label.config(text="00:00")

def start_timer(duration, label, reset_event):
    if label not in timers or not timers[label]['running']:
        reset_event.clear()
        t = threading.Thread(target=countdown, args=(duration, label, reset_event))
        timers[label] = {'thread': t, 'reset_event': reset_event, 'running': True}
        t.start()

def reset_timer(label):
    if label in timers and timers[label]['running']:
        timers[label]['reset_event'].set()
        timers[label]['thread'].join()
        timers[label]['running'] = False
    label.config(text="00:00")


root = tk.Tk()
root.title("Jungle Timer")

def create_timer_row(camp_name, respawn_time):
    row_frame = tk.Frame(root)
    row_frame.pack(pady=5)

    camp_label = tk.Label(row_frame, text=f"{camp_name} Timer", font=("Helvetica", 14))
    camp_label.pack(side=tk.LEFT, padx=10)

    camp_timer = tk.Label(row_frame, text="00:00", font=("Helvetica", 18))
    camp_timer.pack(side=tk.LEFT, padx=10)

    reset_event = threading.Event()
    timers[camp_timer] = {'reset_event': reset_event, 'running': False}

    start_button = tk.Button(row_frame, text=f"Start {camp_name} Timer", 
                            command=lambda: start_timer(respawn_time, camp_timer, reset_event))
    start_button.pack(side=tk.LEFT, padx=10)

    reset_button = tk.Button(row_frame, text=f"Reset {camp_name} Timer",
                             command=lambda: reset_timer(camp_timer))
    reset_button.pack(side=tk.LEFT, padx=10)

jungle_camps = {
    "Gromp": 2 * 60,
    "Blue Buff": 5 * 60,
    "Red Buff": 5 * 60,
    "Raptors": 2 * 60,
    "Wolves": 2 * 60,
    "Krugs": 2 * 60,
    "Dragon": 5 * 60,
    "Baron": 6 * 60
}

for camp, respawn_time in jungle_camps.items():
    create_timer_row(camp, respawn_time)

root.mainloop()
