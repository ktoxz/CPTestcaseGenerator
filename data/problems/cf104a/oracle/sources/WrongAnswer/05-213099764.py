def value_of_card(card):
    if(card in {'J', 'Q', 'K'}):
        return 10
    elif(card == 'A'):
        return 1
    return int(card)
def higher_card(card_one, card_two):
    if(value_of_card(card_one) > value_of_card(card_two)):
        return card_one
    elif(value_of_card(card_one) < value_of_card(card_two)):
        return card_two
    return card_one, card_two
def value_of_ace(card_one, card_two):
    value_of_hand = value_of_card(card_one) + value_of_card(card_two)
    if((value_of_hand <= 10) and 'A' not in {card_one, card_two}):
        return 11
    return 1
def is_blackjack(card_one, card_two):
    value_of_hand = value_of_card(card_one) + value_of_card(card_two)
    if((value_of_hand == 11) and ('A' in {card_one, card_two})):
        return True
    return False
def can_split_pairs(card_one, card_two):
    if(value_of_card(card_one) == value_of_card(card_two)):
        return True
    return False
def can_double_down(card_one, card_two):
    value_of_hand = value_of_card(card_one) + value_of_card(card_two)
    if( 9 <= value_of_hand <= 11):
        return True
    return False