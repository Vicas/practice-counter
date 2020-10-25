from collections import Counter
import tkinter as tk

class CounterFrame:
    def __init__(self, idx, window, rc):
        # index within the RatioCounter
        self.idx = idx
        self.name = tk.StringVar()

        # Data counters
        self.counter = 0
        self.max_streak = 0

        # Parent RatioCounter, for updating global labels
        self.rc = rc

        # TK window stuff
        self.frm_box = tk.Frame(master=window, borderwidth=5)
        self.ent_name = tk.Entry(
                master=self.frm_box,
                textvariable=self.name)
        self.btn_increment = tk.Button(master=self.frm_box, textvariable=self.name)
        self.lbl_total = tk.Label(master=self.frm_box, text=f'Total: {self.counter}')
        self.lbl_max_streak = tk.Label(master=self.frm_box, text=f'Max Streak: {self.max_streak}')

        # Bind the button to inc/dec functions
        self.btn_increment.bind("<Button-1>", self.pressed)
        self.btn_increment.bind("<Button-3>", self.pressed)

    def increment(self):
        self.counter += 1

        # Tell the RatioCounter to update its current streak
        rc.update_current_streak(self.name.get())

        # If this is the max streak we've seen for counter, update it
        if self.max_streak < self.rc.current_streak_value:
            self.max_streak = self.rc.current_streak_value

    def decrement(self):
        if self.counter > 0:
            self.counter -= 1

    def pressed(self, button):
        if button.num == 1:
            self.increment()
        elif button.num == 3:
            self.decrement()

        self.update_labels()

    def update_labels(self):
        self.lbl_total["text"] = f'Total: {self.counter}'
        self.lbl_max_streak["text"] = f'Max Streak: {self.max_streak}'

    def pack(self):
        self.ent_name.pack()
        self.lbl_total.pack()
        self.lbl_max_streak.pack()
        self.btn_increment.pack()
        self.frm_box.pack()


class RatioCounter:
    def __init__(self, window, num_options=2):
        self.window = window
        self.num_options = num_options
        self.counter_frames = []

        # Reset button
        self.btn_reset = tk.Button(master=window, text='Reset Counters', command=self.reset)

        # Current streak vars
        self.current_streak_value = 0
        self.current_streak_name = "None"
        self.curr_streak_text = tk.StringVar()

        # Current streak display vars
        self.lbl_curr_streak = tk.Label(master=window, textvariable=self.curr_streak_text)

        # TODO: Keep a list of the last x events and use that to derive streaks/dependent ratios
        self.update_labels()

        for idx in range(num_options):
            self.counter_frames.append(CounterFrame(idx, self.window, self))
    
    def reset(self):
        self.counters.clear()
        self.max_streak = [0]*self.num_options
        self.current_streak_value = 0
        self.current_streak_idx = 0

        self.update_labels()

    def update_current_streak(self, name):
        '''
        If this event is the same as the current streak, increment it. If not, start
        a new streak
        '''
        if self.current_streak_name == name:
            self.current_streak_value += 1
        else:
            self.current_streak_value = 1
            self.current_streak_name = name

        self.update_labels()

    def get_success_percentage(success_idxs):
        '''
        Given a set of successful indices, get a percentage of that vs all others
        '''
        return sum([cnt for (idx, cnt) in self.counters.items() if idx in success_idxs]) / sum(self.counters.values())

    def update_labels(self):
        STRK_TXT_TEMPLATE = "Current Streak: Type: {name}, Streak: {val}"
        self.curr_streak_text.set(
                STRK_TXT_TEMPLATE.format(name=self.current_streak_name, val=self.current_streak_value))

    def pack(self):
        self.lbl_curr_streak.pack()
        for cf in self.counter_frames:
            cf.pack()
        self.btn_reset.pack()

top = tk.Tk()
top.title("Practice counter")

# Inititalize the RatioCounter with defaults
rc = RatioCounter(top)
rc.pack()

top.mainloop()
