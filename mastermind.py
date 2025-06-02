from logic import *
import random

colors = ["red", "blue", "green", "yellow"]
symbols = []
for i in range(4):
    for color in colors:
        symbols.append(Symbol(f"{color}{i}"))

knowledge = And()

# Each color has a position.
for color in colors:
    knowledge.add(Or(
        Symbol(f"{color}0"),
        Symbol(f"{color}1"),
        Symbol(f"{color}2"),
        Symbol(f"{color}3")
    ))

# Only one position per color.
for color in colors:
    for i in range(4):
        for j in range(4):
            if i != j:
                knowledge.add(Implication(
                    Symbol(f"{color}{i}"), Not(Symbol(f"{color}{j}"))
                ))

# Only one color per position.
for i in range(4):
    for c1 in colors:
        for c2 in colors:
            if c1 != c2:
                knowledge.add(Implication(
                    Symbol(f"{c1}{i}"), Not(Symbol(f"{c2}{i}"))
                ))

knowledge.add(Or(
    And(Symbol("red0"), Symbol("blue1"), Not(Symbol("green2")), Not(Symbol("yellow3"))),
    And(Symbol("red0"), Symbol("green2"), Not(Symbol("blue1")), Not(Symbol("yellow3"))),
    And(Symbol("red0"), Symbol("yellow3"), Not(Symbol("blue1")), Not(Symbol("green2"))),
    And(Symbol("blue1"), Symbol("green2"), Not(Symbol("red0")), Not(Symbol("yellow3"))),
    And(Symbol("blue1"), Symbol("yellow3"), Not(Symbol("red0")), Not(Symbol("green2"))),
    And(Symbol("green2"), Symbol("yellow3"), Not(Symbol("red0")), Not(Symbol("blue1")))
))

knowledge.add(And(
    Not(Symbol("blue0")),
    Not(Symbol("red1")),
    Not(Symbol("green2")),
    Not(Symbol("yellow3"))
))
# Randomly choose a secret code (you can allow duplicates if you want)
secret_code = random.sample(colors, 4)  # No repeats. Use random.choices for repeats

print("Welcome to Mastermind with colors!")
print("Available colors: red, blue, green, yellow")
print("Guess the correct order of 4 colors. Separate them with spaces.")
print("Example: red blue green yellow\n")

while True:
    guess = input("Enter your guess: ").lower().strip().split()

    # Input validation
    if len(guess) != 4 or any(color not in colors for color in guess):
        print("❌ Invalid input. Enter exactly 4 valid colors separated by spaces.\n")
        continue

    # Check for exact matches (right color, right position)
    exact_matches = sum(secret_code[i] == guess[i] for i in range(4))

    # Check for partial matches (right color, wrong position)
    partial_matches = 0
    for color in set(guess):
        partial_matches += min(secret_code.count(color), guess.count(color))
    partial_matches -= exact_matches

    print(f"✅ Exact matches (correct color and position): {exact_matches}")
    print(f"🔄 Partial matches (correct color, wrong position): {partial_matches}\n")

    if exact_matches == 4:
        print("🎉 Congratulations! You've cracked the code!")
        break

for symbol in symbols:
    if model_check(knowledge, symbol):
        print(symbol)