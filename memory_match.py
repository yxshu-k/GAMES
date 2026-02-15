import tkinter as tk
import random
import time

class MemoryMatchGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Match Game")

        self.symbols = ['🍎','🍌','🍇','🍒','🍍','🥝','🍉','🍑']
        self.cards = self.symbols * 2
        random.shuffle(self.cards)

        self.buttons = []
        self.first_card = None
        self.second_card = None
        self.matches = 0

        # Timer
        self.start_time = time.time()
        self.timer_running = True

        self.timer_label = tk.Label(root, text="Time: 0 sec", font=("Arial", 12))
        self.timer_label.grid(row=0, column=0, columnspan=4)

        self.create_board()
        self.update_timer()

    def create_board(self):
        index = 0
        for r in range(4):
            row = []
            for c in range(4):
                btn = tk.Button(self.root, text="?", width=6, height=3,
                                command=lambda i=index: self.reveal_card(i),
                                font=("Arial", 14))
                btn.grid(row=r+1, column=c, padx=5, pady=5)
                row.append(btn)
                index += 1
            self.buttons.append(row)

    def reveal_card(self, index):
        r = index // 4
        c = index % 4
        button = self.buttons[r][c]

        if button["text"] != "?":
            return

        button.config(text=self.cards[index], state="disabled")

        if self.first_card is None:
            self.first_card = (index, button)
        else:
            self.second_card = (index, button)
            self.root.after(700, self.check_match)

    def check_match(self):
        i1, btn1 = self.first_card
        i2, btn2 = self.second_card

        if self.cards[i1] == self.cards[i2]:
            self.matches += 1
            if self.matches == 8:
                self.timer_running = False
                self.show_win()
        else:
            btn1.config(text="?", state="normal")
            btn2.config(text="?", state="normal")

        self.first_card = None
        self.second_card = None

    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed} sec")
            self.root.after(1000, self.update_timer)

    def show_win(self):
        elapsed = int(time.time() - self.start_time)
        win_label = tk.Label(self.root,
                             text=f"You Won! Time Taken: {elapsed} sec 🎉",
                             font=("Arial", 14), fg="green")
        win_label.grid(row=6, column=0, columnspan=4)

# Run Game
if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryMatchGame(root)
    root.mainloop()
