import random

SUITS = ["♠","♥","♦","♣"]
RANKS = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]

def make_deck():
    deck = [(r,s) for s in SUITS for r in RANKS]
    random.shuffle(deck)
    return deck

def card_value(card):
    r = card[0]
    if r in ("J","Q","K"): return 10
    if r == "A": return 11
    return int(r)

def hand_value(hand):
    total = sum(card_value(c) for c in hand)
    aces = sum(1 for c in hand if c[0]=="A")
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def show_hand(name, hand, hide_second=False):
    if hide_second:
        cards = f"{hand[0][0]}{hand[0][1]}  ??"
        print(f"  {name}: {cards}  (showing {card_value(hand[0])}+?)")
    else:
        cards = "  ".join(f"{c[0]}{c[1]}" for c in hand)
        print(f"  {name}: {cards}  = {hand_value(hand)}")

def play():
    chips = 100
    print("="*45)
    print("  BLACKJACK — Starting chips: 100")
    print("="*45)

    while chips > 0:
        print(f"\n  Your chips: {chips}")
        try:
            bet = int(input(f"  Place your bet (1-{chips}): "))
            if not 1 <= bet <= chips: raise ValueError
        except ValueError:
            print("  Invalid bet!"); continue

        deck = make_deck()
        player = [deck.pop(), deck.pop()]
        dealer = [deck.pop(), deck.pop()]

        print("\n--- DEAL ---")
        show_hand("Dealer", dealer, hide_second=True)
        show_hand("You   ", player)

        # Check player blackjack
        if hand_value(player) == 21:
            print("\n  BLACKJACK! You win 1.5x!")
            chips += int(bet * 1.5)
            if input("  Continue? (yes/no): ").lower() not in ("yes","y"): break
            continue

        # Player turn
        bust = False
        while True:
            print(f"\n  Your total: {hand_value(player)}")
            moves = ["[h]it","[s]tand"]
            if len(player)==2 and chips>=bet:
                moves.append("[d]ouble down")
            action = input(f"  {', '.join(moves)}: ").strip().lower()

            if action == 'h':
                player.append(deck.pop())
                show_hand("You", player)
                if hand_value(player) > 21:
                    print("  BUST! Over 21.")
                    bust = True; break
            elif action == 's':
                break
            elif action == 'd' and len(player)==2 and chips>=bet:
                bet *= 2
                player.append(deck.pop())
                show_hand("You (doubled)", player)
                if hand_value(player) > 21:
                    print("  BUST!")
                    bust = True
                break

        # Dealer turn
        if not bust:
            print("\n--- DEALER TURN ---")
            show_hand("Dealer", dealer)
            while hand_value(dealer) < 17:
                dealer.append(deck.pop())
                show_hand("Dealer", dealer)

        # Result
        pv, dv = hand_value(player), hand_value(dealer)
        print("\n--- RESULT ---")
        show_hand("Dealer", dealer)
        show_hand("You   ", player)

        if bust or (not bust and dv <= 21 and dv >= pv and dv != pv):
            if bust or dv > pv:
                print(f"  Dealer wins! -{bet} chips")
                chips -= bet
            else:
                print("  Push! Tie game.")
        elif dv > 21 or pv > dv:
            print(f"  YOU WIN! +{bet} chips")
            chips += bet

        if chips <= 0:
            print("\n  Out of chips! Game over.")
            break

        if input("\n  Play another hand? (yes/no): ").lower() not in ("yes","y"):
            break

    print(f"\n  Final chips: {chips}. Thanks for playing!")

play()