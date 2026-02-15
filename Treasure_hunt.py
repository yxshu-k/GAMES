import tkinter as tk
import random

class TreasureHuntGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Treasure Hunt Game")

        self.rows = 5
        self.cols = 5
        self.attempts = 8

        self.treasure_pos = (random.randint(0,4), random.randint(0,4))

        self.buttons = {}

        self.info_label = tk.Label(root, text=f"Find the Treasure! Attempts left: {self.attempts}")
        self.info_label.grid(row=0, column=0, columnspan=5)

        self.create_grid()

    def create_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.root, text="?", width=6, height=3,
                                command=lambda r=r, c=c: self.check_cell(r,c))
                btn.grid(row=r+1, column=c)
                self.buttons[(r,c)] = btn

    def check_cell(self, r, c):
        if self.attempts <= 0:
            return

        if (r,c) == self.treasure_pos:
            self.buttons[(r,c)].config(text="💰", bg="gold")
            self.info_label.config(text="Congratulations! You found the treasure!")
            self.disable_all()
        else:
            self.buttons[(r,c)].config(text="X", bg="red")
            self.attempts -= 1
            self.info_label.config(text=f"Wrong! Attempts left: {self.attempts}")

            if self.attempts == 0:
                self.info_label.config(text="Game Over! Treasure was hidden.")
                tr, tc = self.treasure_pos
                self.buttons[(tr,tc)].config(text="💰", bg="gold")
                self.disable_all()

    def disable_all(self):
        for btn in self.buttons.values():
            btn.config(state="disabled")

# Run Game
if __name__ == "__main__":
    root = tk.Tk()
    game = TreasureHuntGame(root)
    root.mainloop()
