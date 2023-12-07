from collections import Counter
from enum import Enum

JOKER = 'J'
VALUE = '23456789TJQKA'

HIGH_CARD = 0
ONE_PAIR = 1
TWO_PAIR = 2
THREE_OF_A_KIND = 3
FULL_HOUSE = 4
FOUR_OF_A_KIND = 5
FIVE_OF_A_KIND = 6

def get_value(card, use_jokers):
    return -1 if use_jokers and card == JOKER else VALUE.index(card)

def pull_jokers(cards):
    return cards.replace(JOKER, ''), cards.count(JOKER)

def get_hand(cards):
    c = sorted(Counter(cards).values(), reverse=True)
    if len(c) == 0:
        return None
    if c[0] == 5:
        return FIVE_OF_A_KIND
    if c[0] == 4:
        return FOUR_OF_A_KIND
    if c[0] == 3:
        if len(c) > 1 and c[1] == 2:
            return FULL_HOUSE
        return THREE_OF_A_KIND
    if c[0] == 2:
        if len(c) > 1 and c[1] == 2:
            return TWO_PAIR
        return ONE_PAIR
    return HIGH_CARD

def upgrade_hand(hand, jokers):
    if jokers == 0:
        return hand
    if jokers == 1:
        if hand == FOUR_OF_A_KIND:
            return FIVE_OF_A_KIND
        if hand == THREE_OF_A_KIND:
            return FOUR_OF_A_KIND
        if hand == TWO_PAIR:
            return FULL_HOUSE
        if hand == ONE_PAIR:
            return THREE_OF_A_KIND
        return ONE_PAIR
    if jokers == 2:
        if hand == THREE_OF_A_KIND:
            return FIVE_OF_A_KIND
        if hand == ONE_PAIR:
            return FOUR_OF_A_KIND
        return THREE_OF_A_KIND
    if jokers == 3:
        if hand == ONE_PAIR:
            return FIVE_OF_A_KIND
        return FOUR_OF_A_KIND
    return FIVE_OF_A_KIND

def parse(lines):
    for line in lines:
        l, r = line.split()
        yield (l, int(r))

def map_hand(cards, bid, use_jokers):
    jokers = 0
    old_cards = cards
    card_values = tuple(get_value(card, use_jokers) for card in cards)
    if use_jokers:
        cards, jokers = pull_jokers(cards)
    hand = get_hand(cards)
    old_hand = hand
    hand = upgrade_hand(hand, jokers)
    return hand, card_values, bid

def get_hands_total(lines, use_jokers):
    hands = sorted(map_hand(cards, bid, use_jokers) for cards, bid in parse(lines))
    return sum(hand[-1] * i for i, hand in enumerate(hands, start=1))

def solve_p1(lines):
    return get_hands_total(lines, False)

def solve_p2(lines):
    return get_hands_total(lines, True)
