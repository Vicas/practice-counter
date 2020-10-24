from collections import Counter
import tkinter as tk

class CounterFrame:
    def __init__(self, window, rc):
        # Data counters
        self.counter = 0
        self.max_streak = 0

        # Parent RatioCounter, for updating global labels
        self.rc = rc

        # TK window stuff
        self.frm_box = tk.Frame(master=window)
        # TODO: HOOK THIS TEXT BOX NAME UP TO YOUR LABELS
        self.txt_name = tk.Text(master=frm_box)
        self.button = tk.Button(master=self.frm_box, text=f'Counter')
        self.lbl_total = tk.Label(master=self.frame, text=f'Total: {self.counter}')
        self.lbl_max_streak = tk.Label(master=self.frame, text=f'Max Streak: {self.max_streak}')
        self.txt_name.pack()
        self.lbl_total.pack()
        self.lbl_max_streak.pack()
        self.button.pack()

        # Bind the button to inc/dec functions
        self.button.bind("<Button-1>", self.pressed)
        self.button.bind("<Button-3>", self.pressed)

    # TODO: UPDATE increment and decrement for one counter
    def increment(self):
        self.counter += 1

        # Update the streak, reseting it if this isn't the same as the previous action
        if self.current_streak_idx == counter_idx:
            self.current_streak_value += 1
        else:
            self.current_streak_value = 1
            self.current_streak_idx = counter_idx

        # If this is the max streak we've seen for counter_idx, update it
        if self.max_streak[counter_idx] < self.current_streak_value:
            self.max_streak[counter_idx] = self.current_streak_value

        self.update_labels()

    def decrement(self, counter_idx):
        if self.counters[counter_idx] > 0:
            self.counters[counter_idx]-= 1

        self.update_labels()

    def pressed(self, button):
        if button.num == 1:
            self.increment()
        elif button.num == 3:
            self.decrement()

        rc.self.update_globals()
        self.update_labels()


    def update_labels(self):
        self.lbl_total["text"] = f'Total: {self.counter}'
        self.lbl_max_streak["text"] = f'Max Streak: {self.max_streak}'

    def pack(self):
        self.frame.pack()


class RatioCounter:
    def __init__(self, window, num_options=2):
        self.num_options = num_options
        self.counters = Counter()
        self.max_streak = [0]*num_options
        self.current_streak_value = 0
        self.current_streak_idx = 0
        self.curr_streak_text = tk.StringVar()

        self.update_labels()
    
    def reset(self):
        self.counters.clear()
        self.max_streak = [0]*self.num_options
        self.current_streak_value = 0
        self.current_streak_idx = 0

        self.update_labels()

    def get_success_percentage(success_idxs):
        '''
        Given a set of successful indices, get a percentage of that vs all others
        '''
        return sum([cnt for (idx, cnt) in self.counters.items() if idx in success_idxs]) / sum(self.counters.values())

    def update_labels(self):
        STRK_TXT_TEMPLATE = "Current Streak: Type: {idx}, Streak: {val}"
        self.curr_streak_text.set(STRK_TXT_TEMPLATE.format(idx=self.current_streak_idx, val=self.current_streak_value))


top = tk.Tk()
top.title("Practice counter")

# Inititalize the RatioCounter with defaults
rc = RatioCounter()

lbl_curr_streak = tk.Label(master=top, textvariable=rc.curr_streak_text)
lbl_curr_streak.pack()

# Create CounterDisplays and pack them into the top window
for i in range(rc.num_options):
    cd = CounterDisplay(rc, i, top)
    cd.pack()

btn_reset = tk.Button(master=top, text='Reset Counters', command=rc.reset)
btn_reset.pack()

top.mainloop()
