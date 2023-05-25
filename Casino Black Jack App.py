# Description:
# You are responsible for writing a program that allows a user to play casino Black Jack.
# The user will put a set amount of money onto the table and make a minimum $20 bet each hand.
# Each hand, the user will be dealt two cards and be given the option to hit or stay.
# If the user hits 21 or goes over the round will end.
# The dealer will continue to hit until their hand has a minimum value of 17 as per casino guidelines.
# The user will be able to play as long as their total money is greater than or equal to the minimum bet of the table.

import random
import time

class Card:
    """Simulate a single card with rank, value, and suit."""
    def __init__(self, rank, value, suit):
        self.rank = rank
        self.value = value
        self.suit = suit

    def display_card(self):
        print("{} of {}" .format(self.rank, self.suit))

class Deck:
    """Simulate a deck of 52 individual playing cards."""
    def __init__(self):
        self.cards = []

    def build_deck(self):
        # Create a dictionary called ranks.
        # Each key should be the rank of a card: 2-10, J, Q, K, A
        # Each value should be the corresponding value of the card.
        suits = ['Ace', 'King', 'Queen', 'Jack']
        rank = {
                '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, #Numeric cards are their integer value.
                'J': 10, 'K': 10, 'Q': 10, # J,Q,K are 10.
                'A': 11 # A is 11
                }

        # Build the deck, creating 52 individual cards and append them to the cards list.
        for suit in suits:
            for key, value in rank.items():
                card = Card(key, value, suit)
                self.cards.append(card)

    def shuffle_deck(self):
        """Shuffle a deck of cards"""
        # Use random.shuffle() to shuffle deck
        random.shuffle(self.cards)

    def deal_card(self):
        """Remove a card from the deck to be dealt."""
        # Deal the last card in the shuffled deck
        card = self.cards.pop()
        return card

class Participant:
    """A base class for the participants (Player and Dealer) in Black Jack."""
    def __init__(self):
        self.hand = []
        self.hand_value = 0
        self.playing_hand = True

    def draw_hand(self, deck):
        """Deal the players starting hand"""
        # Player must start with 2 cards in hand
        for i in range(2):
            card = deck.deal_card()
            self.hand.append(card)

    def display_hand(self):
        print("\nPlayer's Hand:")
        for card in self.hand:
            card.display_card()

    def hit(self, deck):
        card = deck.deal_card()
        self.hand.append(card)

    def get_hand_value(self):
        self.hand_value = 0
        ace_in_hand = False

        for card in self.hand:
            self.hand_value += card.value
            if card.rank == 'A':
                ace_in_hand = True

        # The user went over 21, but they have an ace so treat ace as a 1.
        if ace_in_hand and self.hand_value > 21:
            self.hand_value -= 10 #Ace is treated as 1 instead of 11 so subtract 10 from hand_value.

class Player(Participant):
    """A class for the user to play Black Jack."""
    def update_hand(self, deck):
        """Update the players hand by allowing them to hit."""
        # The player has the option to hit
        if self.hand_value < 21:
            hit = input("Would you like to hit (y/n): ").lower()
            if hit == 'y':
                self.hit(deck)
            # Player is happy with hand value, done playing hand
            else:
                self.playing_hand = False
        # Player is over 21, cannot hit again
        else:
            self.playing_hand = False

    def get_hand_value(self):
        super().get_hand_value()
        print("Total Value:", self.hand_value)

class Dealer(Participant):
    """A class simulating the black jack dealer. They must hit up to 17 and they must reveal their first card."""
    def display_hand(self):
        input("\nPress enter to reveal the dealer cards. ")
        for card in self.hand:
            card.display_card()
            time.sleep(2)

    def hit(self, deck):
        """The dealer must hit until they have reached 17, then they stop."""
        self.get_hand_value()

        # As long as the hand_value is less than 17, dealer must hit.
        while self.hand_value < 17:
            card = deck.deal_card()
            self.hand.append(card)
            self.get_hand_value()

        print("\nDealer is set with a total of ", str(len(self.hand)) + " cards.")

class Game:
    """A class to hold bets and payouts"""
    def __init__(self, money):
        self.money = int(money)
        self.bet = 20
        self.winner = ''

    def set_bet(self):
        betting = True
        while betting:
            # Get a users bet
            bet = int(input("What would you like to bet (minimum bet of 20): "))  # Bet is too small, set to min value
            if bet < 20:
                bet = 20
            # Bet is too high, make them bet again
            if bet > self.money:
                print("Sorry, you can't afford that bet.")
            # Bet is acceptable, set bet and stop betting.
            else:
                self.bet = bet
                betting = False

    def scoring(self, p_value, d_value):
        """Score a round of black jack."""  # Someone got black jack 21!
        if p_value == 21:
            print("You got BLACK JACK!!! You win!")
            self.winner = 'p'
        elif d_value == 21:
            print("The dealer got black jack...You loose!")
            self.winner = 'd'

        # Someone went over 21.
        elif p_value > 21:
            print("You went over 21...You loose!")
            self.winner = 'd'
        elif d_value > 21:
            print("Dealer went over 21! You win!")
            self.winner = 'p'

        # Other cases.
        else:
            if p_value > d_value:
                print("Dealer gets " + str(d_value) + ". You Win!")
                self.winner = 'p'
            elif d_value > p_value:
                print("Dealer gets " + str(d_value) + ". You loose.")
                self.winner = 'd'
            else:
                print("Dealer gets " + str(d_value) + ". It's a push...")
                self.winner = 'tie'

    def payout(self):
        """Update the money attribute based on who won a hand."""
        # You won, you earn money
        if self.winner == 'p':
            self.money += self.bet  # You lost, you loose money
        elif self.winner == 'd':
            self.money -= self.bet

    def display_money(self):
        print("\nCurrent Money: $" + str(self.money))

    def display_money_and_bet(self):
        print("\nCurrent Money: $" + str(self.money) + "\t\tCurrent Bet: $" + str(self.bet))

if __name__ == '__main__':
    print("Welcome to the Blackjack App.")
    print("The minimum bet at this table is $20.\n")

    # Create a game object to keep track of bets, total cash, round winners, and payouts
    money = int(input("How much money are you willing to play with today: "))
    game = Game(money)

    # The main game loop
    playing = True
    while playing:
        # Build a deck, populate it with cards, and shuffle.
        game_deck = Deck()
        game_deck.build_deck()
        game_deck.shuffle_deck()

        # Create a player and dealer
        player = Player()
        dealer = Dealer()

        # Show how much money
        game.display_money()
        game.set_bet()

        # Draw the player and
        player.draw_hand(game_deck)
        dealer.draw_hand(game_deck)

        # Simulate a single round of
        game.display_money_and_bet()
        print("The dealer is showing a " + dealer.hand[0].rank + " of " + dealer.hand[0].suit + ".")

        # While the player is playing, show hand, calc values, allow player to hit or stay
        while player.playing_hand:
            player.display_hand()
            player.get_hand_value()
            player.update_hand(game_deck)

        # Simulate a single round of black jack for the dealer
        dealer.hit(game_deck)
        dealer.display_hand()

        # Determine the winner and the payout
        game.scoring(player.hand_value, dealer.hand_value)
        game.payout()

        # The user ran out of money, kick them out
        if game.money < 20:
            playing = False
            print("Sorry, you ran out of money. Please try again.")

