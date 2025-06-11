import tkinter as tk
from tkinter import ttk

class Pet:
    """Reprezentuje zwierzaka z poziomami głodu, znudzenia i monetami."""
    def __init__(self):
        """Inicjalizuje obiekt zwierzaka z domyślnymi wartościami."""
        self.hunger = 50
        self.boredom = 50
        self.coins = 0
    def every_second(self):
        """Zwiększa głód i znudzenie o 2 jednostki, maksymalnie do 100."""
        self.hunger = min(100, self.hunger + 2)
        self.boredom = min(100, self.boredom + 2)
    def feed(self, amount, cost):
        """
        Karmi zwierzaka, zmniejszając jego głód.

        Args:
            amount (int): Liczba punktów głodu do odjęcia.
            cost (int): Koszt w monetach.
        """
        if self.coins >= cost:
            self.coins -= cost
            self.hunger = max(0, self.hunger - amount)
    def play(self, fun_value, hunger_value):
        """
        Bawi się ze zwierzakiem, zmniejszając znudzenie i zwiększając głód.

        Args:
            fun_value (int): Liczba punktów znudzenia do odjęcia.
            hunger_value (int): Liczba punktów głodu do dodania.
        """
        self.boredom = max(0, self.boredom - fun_value)
        self.hunger = min(100, self.hunger + hunger_value)


def start_screen():
    """Tworzy ekran startowy z wyborem zwierzaka i polem na imię."""
    for w in root.winfo_children():
        w.destroy()

    tk.Label(root, text="Choose your pet", font=("Arial", 24), bg="pale turquoise").pack(pady=20)

    global name_entry
    tk.Label(root, text="Enter your pet's name:", font=("Arial", 14), bg="pale turquoise").pack()
    name_entry = tk.Entry(root, font=("Arial", 14))
    name_entry.pack(pady=5)

    frame = tk.Frame(root, bg="pale turquoise")
    frame.pack(pady=10)

    pets = ["Cat", "Dog", "Rabbit", "Monkey"]
    for species in pets:
        button = tk.Button(frame, text=species, width=12, height=2,
                           command=lambda s=species: start_game(s))
        button.pack(side="left", padx=5)

def start_game(species):
    """
    Rozpoczyna grę, tworzy nowego zwierzaka i przechodzi do ekranu gry.

    Parameters:
        species (str): Gatunek wybranego zwierzaka.
    """
    global pet
    pet = Pet()
    entered_name = name_entry.get().strip()
    pet.name = entered_name if entered_name else "Bob"
    pet.species = species
    game_screen()
    every_second()

def game_screen():
    """Tworzy główny ekran gry z paskami stanu, opcjami karmienia i zabawy."""
    for widget in root.winfo_children():
        widget.destroy()

    status_frame = tk.Frame(root, bg="pale turquoise")
    status_frame.pack(pady=5)

    tk.Label(status_frame, text="Hunger", bg="pale turquoise").grid(row=0, column=0)
    global hunger_bar
    hunger_bar = ttk.Progressbar(status_frame, length=200, maximum=100)
    hunger_bar.grid(row=0, column=1, padx=10)

    tk.Label(status_frame, text="Boredom", bg="pale turquoise").grid(row=1, column=0)
    global boredom_bar
    boredom_bar = ttk.Progressbar(status_frame, length=200, maximum=100)
    boredom_bar.grid(row=1, column=1, padx=10)

    pet_label = tk.Label(root, text=f"{pet.name} the {pet.species}", font=("Arial", 32), bg="pale turquoise")
    pet_label.pack(pady=20)

    actions_frame = tk.Frame(root, bg="pale turquoise")
    actions_frame.pack(pady=10)

    food_frame = tk.LabelFrame(actions_frame, text="Food", bg="pale turquoise")
    food_frame.pack(side="left", expand=True, padx=15)

    food_options = [
        ["Candy", 5, 5],
        ["Sushi", 10, 10],
        ["Pizza", 25, 25],
        ["Burger", 50, 50]
    ]

    i = 0
    for food_option in food_options:
        text = food_option[0]
        amount = food_option[1]
        cost = food_option[2]

        button = tk.Button(
            food_frame,
            text=f"{text}\n-{cost} coins, -{amount} hunger",
            command=lambda amt=amount, cst=cost: feed(amt, cst),
            width=22, height=3
        )

        grid_position(button, i)

        i += 1

    play_frame = tk.LabelFrame(actions_frame, text="Play", bg="pale turquoise")
    play_frame.pack(side="right", expand=True, padx=15)

    play_options = [
        ["Chess", 5, 4],
        ["Tag", 10, 8],
        ["Football", 25, 20],
        ["Swimming", 50, 40]
    ]

    i = 0
    for play_option in play_options:
        text = play_option[0]
        boredom_reduction = play_option[1]
        hunger_increase = play_option[2]

        button = tk.Button(
            play_frame,
            text=f"{text}\n-{boredom_reduction} boredom, +{hunger_increase} hunger",
            command=lambda br=boredom_reduction, hi=hunger_increase: play(br, hi),
            width=22, height=3
        )

        grid_position(button, i)

        i += 1

    global coin_label
    coin_label = tk.Label(root, text=f"Coins: {pet.coins}", font=("Arial", 14), bg="pale turquoise")
    coin_label.pack(pady=5)
    click_btn = tk.Button(root, text="Click me!", command=earn_coin)
    click_btn.pack()

def update_screen():
    """Aktualizuje paski postępu i liczbę monet na ekranie."""
    hunger_bar['value'] = pet.hunger
    boredom_bar['value'] = pet.boredom
    coin_label.configure(text=f"Coins: {pet.coins}")

def every_second():
    """Wywoływana co sekundę, zwiększa głód i znudzenie oraz sprawdza stan gry."""
    pet.every_second()
    update_screen()
    if pet.hunger >= 100 or pet.boredom >= 100:
        game_over()
    else:
        root.after(1000, every_second)

def grid_position(button, i):
    """
    Umieszcza przycisk w odpowiednim miejscu w siatce.

    Args:
        button (tk.Button): Przycisk do umieszczenia.
        i (int): Indeks przycisku.
    """
    if i == 0:
        button.grid(row=0, column=0, padx=5, pady=5)
    elif i == 1:
        button.grid(row=0, column=1, padx=5, pady=5)
    elif i == 2:
        button.grid(row=1, column=0, padx=5, pady=5)
    elif i == 3:
        button.grid(row=1, column=1, padx=5, pady=5)

def feed(amount, cost):
    """
    Obsługuje karmienie zwierzaka i aktualizuje ekran.

    Args:
        amount (int): Ilość punktów głodu do odjęcia.
        cost (int): Koszt jedzenia w monetach.
    """
    pet.feed(amount, cost)
    update_screen()

def play(fun_value, hunger_cost):
    """
    Obsługuje zabawę ze zwierzakiem i aktualizuje ekran.

    Args:
        fun_value (int): Ilość punktów znudzenia do odjęcia.
        hunger_cost (int): Ilość punktów głodu do dodania.
    """
    pet.play(fun_value, hunger_cost)
    update_screen()

def earn_coin():
    """Zwiększa liczbę monet o 1 i aktualizuje ekran."""
    pet.coins += 1
    update_screen()

def game_over():
    """Pokazuje ekran końca gry, gdy zwierzak osiągnie 100 głodu lub znudzenia."""
    for w in root.winfo_children():
        w.destroy()

    tk.Label(root, text="Your pet escaped :(", font=("Arial", 24), bg="pale turquoise").pack(pady=20)
    tk.Button(root, text="Play Again", command=start_screen).pack()

def main():
    """Uruchamia interfejs gry."""
    global root
    root = tk.Tk()
    root.title("Pet Simulator")
    root.geometry("800x450")
    root.configure(bg="pale turquoise")
    start_screen()
    root.mainloop()

if __name__ == "__main__":
    main()