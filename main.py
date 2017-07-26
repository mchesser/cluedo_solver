import game


def main():
    game_state = game.GameState(8)
    print("Starting game, the target cards are: ", game_state.target_cards)

    num_rounds = 0
    while game_state.run_round():
        print("It is Player ", game_state.current_player_id, "'s turn", sep="")
        num_rounds += 1

    print("The winner is Player", game_state.current_player_id)
    print("Over after", num_rounds, "rounds")
    return num_rounds



if __name__ == "__main__":
    total_rounds = 0
    for i in range(1000):
        total_rounds += main() / 8.0

    print("average: ", total_rounds / 1000.0)