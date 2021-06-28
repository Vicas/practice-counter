from collections import Counter, deque
import tkinter as tk

import keyboard

class CounterFrame:
    def __init__(self, name, rc):
        self.window = rc.window
        self.name = tk.StringVar()
        self.name.set(name)
        self.name.trace_add('write', self.rename_counter)
        self.old_name = self.name.get()
        self.success = tk.BooleanVar()

        # Init Variable entries
        self.success.set(False)

        # Data counters
        self.counter = 0
        self.max_streak = 0

        # Parent RatioCounter, for updating global labels
        self.rc = rc

        # TK window stuff
        self.frm_box = tk.Frame(self.window, borderwidth=5)
        self.ent_name = tk.Entry(
                self.frm_box,
                width=10,
                textvariable=self.name)
        self.cb_success = tk.Checkbutton(
                self.frm_box,
                text='Success',
                variable=self.success,
                onvalue=True,
                offvalue=False,
                command=self.update_success)
        self.btn_increment = tk.Button(self.frm_box, textvariable=self.name)
        self.lbl_total = tk.Label(self.frm_box, text=f'Total: {self.counter}')
        self.lbl_max_streak = tk.Label(self.frm_box, text=f'Max Streak: {self.max_streak}')

        # Bind the button to inc/dec functions
        self.btn_increment.bind("<Button-1>", self.pressed)
        self.btn_increment.bind("<Button-3>", self.pressed)

        self.update_success()

    def increment(self):
        self.counter += 1

        # Tell the RatioCounter about this update
        self.rc.increment_counter(self.name.get())

        # If this is the max streak we've seen for counter, update it
        if self.max_streak < self.rc.current_streak_value:
            self.max_streak = self.rc.current_streak_value


    def decrement(self):
        if self.counter > 0:
            self.counter -= 1
            self.rc.decrement_counter(self.name.get())

    def pressed(self, button):
        if button.num == 1:
            self.increment()
        elif button.num == 3:
            self.decrement()

        self.update_labels()

    def rename_counter(self, var, idx, mode):
        # Tell the RatioCounter our new name, and then set it as our old name for
        # when we change names again
        self.rc.rename_counter(self.old_name, self.name.get())
        self.old_name = self.name.get()

    def reset(self):
        self.counter = 0
        self.max_streak = 0
        self.update_labels()

    # TKinter updates/packing
    def update_success(self):
        self.btn_increment['bg'] = '#03c2fc' if self.success.get() else '#ff525a'

    def update_labels(self):
        self.lbl_total["text"] = f'Total: {self.counter}'
        self.lbl_max_streak["text"] = f'Max Streak: {self.max_streak}'

    def pack(self):
        self.ent_name.grid(row=0, column=0)
        self.cb_success.grid(row=0, column=1)
        self.lbl_total.grid(row=1, column=0)
        self.lbl_max_streak.grid(row=1, column=1)
        self.btn_increment.grid(row=2, column=0, columnspan=2)

class RatioFrame:
    '''
    Frame class of success ratios based on the last <x> inputs
    '''
    def __init__(self, window, lookback_counts):
        self.window = window
        self.lookback_counts = lookback_counts
        self.lookback_counts.sort()
        self.frm_box = tk.Frame(self.window, borderwidth=5)

        self.lbl_ratios = tk.Label(self.frm_box, text="Success Ratios")
        self.ratio_list = []
        for count in lookback_counts:
            self.ratio_list.append(tk.Label(self.frm_box, text=f"Last {count}: 0%"))

    def update_ratios(self, input_history, success_dict):
        '''
        Given an update history and a list of success/failures, generate a success ratio for each
        count in the lookback_counts
        '''
        count_idx = 0
        lookback_idx = 0
        percent = 0
        success_counter = Counter()
        for name in input_history:
            # Update our success/failure counts
            success_counter[success_dict[name]] += 1
            percent = (success_counter[True] / sum(success_counter.values())) * 100

            count_idx += 1

            # If we've hit a count breakpoint, compute the success/failure ratio
            # based ont he current counters
            if count_idx == self.lookback_counts[lookback_idx]:
                self.ratio_list[lookback_idx]['text'] = \
                    f'Last {self.lookback_counts[lookback_idx]}: {percent:.3g}%'
                lookback_idx += 1

                # If we've covered all our ratios, stop scanning the list
                if lookback_idx >= len(self.lookback_counts):
                    break

        # If we don't have enough actions for all lookback_counts, update the rest of them
        # with what we have now
        while lookback_idx < len(self.lookback_counts):
            self.ratio_list[lookback_idx]['text'] = \
                f'Last {self.lookback_counts[lookback_idx]}: {percent:.3g}%'
            lookback_idx += 1

    def pack(self):
        self.lbl_ratios.pack()
        for label in self.ratio_list:
            label.pack()

class RatioCounter:
    def __init__(self, window, name_list):
        self.window = window
        self.counter_frames = [CounterFrame(name, self) for name in name_list]
        self.counter_names = {name: idx for idx, name in enumerate(name_list)}
        self.counter_hotkeys = {str(idx): name for idx, name in enumerate(name_list)}
        self.ratio_frame = RatioFrame(window, [10, 50, 100])

        # History of all inputs, used for building streaks and calculating ratios
        # Limiting to 1000 for now, probably add some zeroes to that later
        self.input_history = deque(maxlen=1000)

        # Reset button
        self.btn_reset = tk.Button(master=window, text='Reset Counters', command=self.reset)

        # Current streak vars
        self.current_streak_value = 0
        self.current_streak_name = "None"
        self.curr_streak_text = tk.StringVar()

        # Current streak display vars
        self.lbl_curr_streak = tk.Label(master=window, textvariable=self.curr_streak_text, borderwidth=2)

        self.update_labels()

    def reset(self):
        # TODO: dedupe this reset code from the constructor code
        for cf in self.counter_frames:
            cf.reset()
        self.current_streak_value = 0
        self.current_streak_name = "None"
        self.input_history = deque(maxlen=1000)

        self.ratio_frame.update_ratios(self.input_history, self.get_counter_success_dict())

        self.update_labels()

    def increment_counter(self, name):
        '''
        Record an event in our input_history and update any dependent ratios/max streak/etc
        '''
        self.input_history.appendleft(self.counter_names[name])
        self.ratio_frame.update_ratios(self.input_history, self.get_counter_success_dict())
        self.update_current_streak(name)

    def decrement_counter(self, name):
        '''
        Remove the most recent instance of a given event and update counters
        '''
        try:
            self.input_history.remove(self.counter_names[name])
        except:
            # ignore not found errors
            print(f'value not found! {self.counter_names[name]}')

        # update the ratios but don't bother with the current streak, i don't wanna deal with side cases, lol
        self.ratio_frame.update_ratios(self.input_history, self.get_counter_success_dict())


    def rename_counter(self, old_name, new_name):
        '''
        Rename a given counter, updating everything in its update history
        '''
        # Rename the counter in counter_names
        self.counter_names[new_name] = self.counter_names.pop(old_name)

        if old_name == self.current_streak_name:
            self.current_streak_name = new_name

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

    def hotkey_released(self, keyboard_event):
        '''
        Compare the input to our list of counter_hotkeys, and if there's a match, increment that counter
        '''
        # TODO TOMORROW: instead of increment, call pressed by spoofing a button event (i guess??)
        print(f'Key pressed! {keyboard_event}')
        if keyboard_event.name in self.counter_hotkeys:
            self.counter_frames[self.counter_names[self.counter_hotkeys[keyboard_event.name]]].increment()

    def get_counter_success_dict(self):
        '''
        Return a dict where keys are counter names and values are true/fale depending on if this
        counter is a success or not
        '''
        return {idx: cf.success.get() for idx, cf in enumerate(self.counter_frames)}

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
        self.lbl_curr_streak.grid(row=0, column=0, columnspan=2)
        cf_row_idx = 1
        for cf in self.counter_frames:
            cf.pack()
            cf.frm_box.grid(row=cf_row_idx, column=0)
            cf_row_idx += 1
        self.ratio_frame.pack()
        self.ratio_frame.frm_box.grid(row=int(cf_row_idx/2), column=1, rowspan=2)
        self.btn_reset.grid(row=cf_row_idx, column=0, columnspan=2)

top = tk.Tk()
top.title("Practice counter")

# Inititalize the RatioCounter with defaults
rc = RatioCounter(top, ["Success!", "Failure!"])

# Init the counter labels
rc.counter_frames[0].success.set(True)
rc.counter_frames[0].update_success()

rc.pack()

keyboard.on_release(rc.hotkey_released)

top.mainloop()
