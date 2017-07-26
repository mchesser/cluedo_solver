import random
import cards


class Player(object):
    """
    Keeps track of the information known by a player
    """

    def __init__(self, id, all_cards, num_players):
        self.id = id

        # The cards that this player was given at the start of the game
        self.starting_cards = set()

        # The knowledge that the player has about each of their opponents
        self.opponents = dict()
        for i in filter(lambda player_id: player_id != id, range(num_players)):
            self.opponents[i] = Opponent()

        # The set of cards that are still unknown
        self.valid_cards = all_cards.copy()


    def add_card(self, card):
        self.starting_cards.add(card)
        self.valid_cards.discard(card)

        # We also know that each opponent cannot have this card
        for opponent in self.opponents.values():
            opponent.does_not_have.add(card)


    def respond_to_suggestion(self, cards: set):
        valid_responses = cards & self.starting_cards

        if len(valid_responses) == 0:
            return None

        return random.sample(valid_responses, 1)


    def make_suggestion(self):
        self.update_valid_cards()

        places = cards.PLACES & self.valid_cards
        weapons = cards.WEAPONS & self.valid_cards
        people = cards.PEOPLE & self.valid_cards

        return set(random.sample(places, 1) + random.sample(weapons, 1) + random.sample(people, 1))

    def update_valid_cards(self):
        for opponent in self.opponents.values():
            known_cards = opponent.cards()

            # We know that these cards can't be the target cards
            self.valid_cards -= known_cards

            # And no other opponent can have this card
            for other_opponent in self.opponents.values():
                if other_opponent is not opponent:
                    other_opponent.does_not_have |= known_cards


class Opponent(object):
    """
    Keeps track of the knowledge about what a player knows about an individual opponent
    """

    def __init__(self):
        # Keeps track of all the cards that this opponent has indicated that they may have.
        self.could_have = []

        # Keeps track of all the cards that we know this opponent does not have
        self.does_not_have = set()


    def responded_yes(self, cards: set):
        self.could_have.append(cards - self.does_not_have)


    def responded_no(self, cards: set):
        self.does_not_have = self.does_not_have | cards

        # Update all our previous guesses with our newly obtained knowledge
        self.could_have = [card_set - self.does_not_have for card_set in self.could_have]


    def cards(self):
        return set([next(iter(card)) for card in filter(lambda c: len(c) == 1, self.could_have)])
