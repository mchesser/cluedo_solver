import random
import cards

from player import Player


class GameState(object):

    def __init__(self, num_players):
        all_cards = cards.WEAPONS | cards.PEOPLE | cards.PLACES

        # Randomly select a set of cards to be the target for the game
        self.target_cards = set(random.sample(cards.WEAPONS, 1) + random.sample(cards.PEOPLE, 1) +
            random.sample(cards.PLACES, 1))

        # Initialise players
        self.players = []
        for i in range(num_players):
            self.players.append(Player(i, all_cards, num_players))

        self.current_player_id = 0

        # Shuffle and deal out the remaining cards to the players
        remaining_cards = list(all_cards - self.target_cards)
        random.shuffle(remaining_cards)
        for i, card in enumerate(remaining_cards):
            self.players[i % num_players].add_card(card)


    def run_round(self):
        # The current player makes a suggestion
        current_player = self.players[self.current_player_id]
        suggestion = current_player.make_suggestion()
        print("Suggestion: ", suggestion)

        if suggestion == self.target_cards:
            # The current player correctly guessed the current cards, so the game is over
            return False


        num_players = len(self.players)

        # Check with each player (in order) whether they have a response to the current suggestion
        for i in range(num_players - 1):
            player_id = (i + self.current_player_id + 1) % num_players

            response = self.players[player_id].respond_to_suggestion(suggestion)
            if response == None:
                self.player_responded_no(player_id, suggestion)
            else:
                self.player_responded_yes(player_id, suggestion)

                # The current player also gets to see the exact card the player responded with
                current_player.opponents[player_id].responded_yes(set(response))
                break

        self.current_player_id += 1
        if self.current_player_id >= num_players:
            self.current_player_id = 0

        # The game continues
        return True


    def player_responded_no(self, player_id, suggestion):
        for player in filter(lambda p: p.id is not player_id, self.players):
            player.opponents[player_id].responded_no(suggestion)


    def player_responded_yes(self, player_id, suggestion):
        for player in filter(lambda p: p.id is not player_id, self.players):
            player.opponents[player_id].responded_yes(suggestion)
