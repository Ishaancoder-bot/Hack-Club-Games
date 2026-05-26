import random

WORDS = ["python","programming","hackclub","algorithm","variable","function","debugging"]

STAGES = ["""
  +---+
  |   |
      |
      |
=========""","""
  +---+
  |   |
  O   |
      |
=========""","""
  +---+
  |   |
  O   |
  |   |
=========""","""
  +---+
  |   |
  O   |
 /|   |
=========""","""
  +---+
  |   |
  O   |
 /|\\  |
=========""","""
  +---+
  |   |
  O   |
 /|\\  |
 /    |
=========""","""
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
========="""]

def play():
    word = random.choice(WORDS)
    guessed = set()
    wrong = 0

    while wrong < 6:
        print(STAGES[wrong])
        print(" ".join(c if c in guessed else "_" for c in word))
        print(f"Wrong guesses: {', '.join(sorted(guessed - set(word))) or 'none'}")

        if all(c in guessed for c in word):
            print(f"\nYou won! The word was '{word}'!")
            return

        g = input("\nGuess a letter: ").strip().lower()
        if not g or len(g) != 1 or not g.isalpha():
            print("Single letter only!")
            continue
        if g in guessed:
            print("Already guessed!")
            continue
        guessed.add(g)
        if g not in word:
            wrong += 1
            print(f"'{g}' is not in the word.")
        else:
            print("Good guess!")

    print(STAGES[6])
    print(f"\nGame over! The word was '{word}'.")

while True:
    play()
    if input("\nPlay again? (yes/no): ").lower() not in ("yes","y"):
        break