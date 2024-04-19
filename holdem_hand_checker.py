import random
from collections import Counter
from itertools import combinations

# Define a deck of cards
suits = ["c", "d", "h", "s"]
values = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
deck = [value + suit for suit in suits for value in values]


# Function to deal two random hole cards for each player
def deal_hole_cards():
    player1_cards = random.sample(deck, 2)
    for card in player1_cards:
        deck.remove(card)

    player2_cards = random.sample(deck, 2)
    for card in player2_cards:
        deck.remove(card)

    return player1_cards, player2_cards


# Function to deal the flop, turn, and river
def deal_community_cards():
    flop = random.sample(deck, 3)
    for card in flop:
        deck.remove(card)

    turn = random.choice(deck)
    deck.remove(turn)

    river = random.choice(deck)
    deck.remove(river)

    board = flop + [turn, river]

    return flop, turn, river, board


def form_pokerhand(cards):
    all_cards = []  # example ["5h", "Tc", "2d", "Ts", "4h", "5s", "5d"] = fives full of tens
    for card in cards:
        all_cards.append(card)

    rank_list = [card[:-1] for card in all_cards]
    suit_list = [card[-1] for card in all_cards]

    rank_counts = Counter(rank_list)
    suit_counts = Counter(suit_list)

    # Check for straight flush
    highest_straight_flush = None
    for suit, count in suit_counts.items():
        if count >= 5:
            # Extract ranks of cards with the same suit
            suited_ranks = [card[:-1] for card in all_cards if card[-1] == suit]

            # Generate all combinations of 5 cards from the flush
            flush_combinations = combinations(suited_ranks, 5)

            # Check if any of the combinations form a straight
            for flush_combination in flush_combinations:
                possible_straights = [
                    ["A", "2", "3", "4", "5"],
                    ["2", "3", "4", "5", "6"],
                    ["3", "4", "5", "6", "7"],
                    ["4", "5", "6", "7", "8"],
                    ["5", "6", "7", "8", "9"],
                    ["6", "7", "8", "9", "T"],
                    ["7", "8", "9", "T", "J"],
                    ["8", "9", "T", "J", "Q"],
                    ["9", "T", "J", "Q", "K"],
                    ["T", "J", "Q", "K", "A"]
                ]

                # Convert suited ranks to a set for efficient comparison
                flush_combination_set = set(flush_combination)

                for straight in possible_straights:
                    if set(straight) == flush_combination_set:
                        # Update the highest straight flush if necessary
                        if highest_straight_flush is None or straight[4] > highest_straight_flush[4]:
                            highest_straight_flush = straight

        # If a straight flush is found, return the result
    if highest_straight_flush is not None:
        if highest_straight_flush[4] == "A":
            return "Royal flush"
        return f"Straight flush, {highest_straight_flush[4]} high"

    # Check for quads
    for rank, count in rank_counts.items():
        if count == 4:
            return f"Four of a kind, {rank}s"

    # Check for full house
    trips = 0
    pair = False
    for rank, count in rank_counts.items():
        if count == 3:
            trips += 1
        elif count == 2:
            pair = True

    if trips == 2:
        return "Full house"
    elif trips == 1 and pair:
        return "Full house"

    # Check for flush
    highest_flush = None
    for suit, count in suit_counts.items():
        if count >= 5:
            # Extract ranks of cards with the same suit
            suited_ranks = [card[:-1] for card in all_cards if card[-1] == suit]

            # Sort the ranks in descending order to find the highest card
            suited_ranks.sort(key=lambda x: "23456789TJQKA".index(x), reverse=True)

            # Get the highest card
            highest_card = suited_ranks[0]

            # Update the highest flush if necessary
            if highest_flush is None or highest_card > highest_flush:
                highest_flush = highest_card

        # If a flush is found, return the result
    if highest_flush is not None:
        return f"Flush, {highest_flush} high"

    # Check for straight
    possible_straights = [
        ["A", "2", "3", "4", "5"],
        ["2", "3", "4", "5", "6"],
        ["3", "4", "5", "6", "7"],
        ["4", "5", "6", "7", "8"],
        ["5", "6", "7", "8", "9"],
        ["6", "7", "8", "9", "T"],
        ["7", "8", "9", "T", "J"],
        ["8", "9", "T", "J", "Q"],
        ["9", "T", "J", "Q", "K"],
        ["T", "J", "Q", "K", "A"]
    ]

    # Convert input cards to a set for efficient comparison
    input_set = set(rank_list)

    for straight in possible_straights:
        # Generate all combinations of 5 cards from the input hand
        hand_combinations = combinations(input_set, 5)

        # Check if any of the combinations match the current straight
        for combination in hand_combinations:
            if set(straight) == set(combination):
                return f"Straight, {straight[4]} high"

    # Check for three of a kind
    for rank, count in rank_counts.items():
        if count == 3:
            return f"Three of a kind, {rank}s"

    # Check for two pair
    pairs = []
    for rank, count in rank_counts.items():
        if count == 2:
            pairs.append(rank)

    # Sort pairs in descending order
    pairs.sort(key=lambda x: "23456789TJQKA".index(x), reverse=True)

    # Take the top two pairs if available
    if len(pairs) >= 2:
        return f"Two pair, {pairs[0]}s and {pairs[1]}s"

    # Check for one pair
    one_pair_count = 0
    pair_value = ""
    for rank, count in rank_counts.items():
        if count == 2:
            one_pair_count += 1
            pair_value = rank

    if one_pair_count == 1:
        return f"One pair, {pair_value}s"

    # Else return high card
    card_list = []
    for rank, count in rank_counts.items():
        if count == 1:
            card_list.append(rank)

    # Sort cards
    card_list.sort(key=lambda x: "23456789TJQKA".index(x), reverse=True)

    return f"High card, {card_list[0]}"


# Main function
if __name__ == "__main__":
    p1, p2 = deal_hole_cards()
    f, t, r, b = deal_community_cards()

    p1_hand = p1 + b
    p2_hand = p2 + b

    print("Player 1's Hand:", ", ".join(p1))
    print("Player 2's Hand:", ", ".join(p2))
    print("Community Cards: " + ", ".join(f + [t, r]))

    print(f"Player 1's hand is: {form_pokerhand(p1_hand)}")
    print(f"Player 2's hand is: {form_pokerhand(p2_hand)}")
