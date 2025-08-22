import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
          'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
                
    def __str__(self):
        return "The deck contains: \n" + "\n".join(str(card) for card in self.deck)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
            
class Chips:

    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet
        
def take_bet(chips):
    while True:
        try:
            bet = int(input("How many chips would you like to bet? "))
            if bet > chips.total:
                print("You do not have enough chips!")
            else:
                chips.bet = bet
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
    
def hit_or_stand(deck,hand):
    global playing
    
    while True:
        try:
            answer = input("Would you like to hit or stand? (h/s) ")
            if answer.lower() == 'h':
                hit(deck, hand)
                break
            elif answer.lower() == 's':
                playing = False
                break
            else:
                print("Invalid input. Please enter 'h' or 's'.")
        except ValueError:
            print("Invalid input. Please enter 'h' or 's'.")

def show_some(player,dealer):
    print('_'*20)
    print("Dealer's Hand: ?")
    print("[?] ", dealer.cards[1], sep="\n")
    print('_'*20)
    print("Player's Hand: ", player.value)
    print(*player.cards, sep="\n")
    print('_'*20)

def show_all(player,dealer):
    print('_'*20)
    print("Dealer's Hand: ", dealer.value)
    print(*dealer.cards, sep="\n")
    print('_'*20)
    print("Player's Hand: ", player.value)
    print(*player.cards, sep="\n")
    print('_'*20)

def player_busts(chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(chips):
    print("Dealer busts!")
    chips.win_bet()

def dealer_wins(chips):
    print("Dealer wins!")
    chips.lose_bet()

def push():
    print("Tie, it's a push!")

def main():
    global playing
    
    while True:
        playing = True
        print("Welcome to Blackjack!")
        print('Get as close to 21 without going over!')
        print('Dealer hits until reaching 17.')
        
        deck = Deck()
        deck.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()
        for _ in range(2):
            player_hand.add_card(deck.deal())
            dealer_hand.add_card(deck.deal())

        player_chips = Chips()
        take_bet(player_chips)
        show_some(player_hand, dealer_hand)
        
        while playing:
            hit_or_stand(deck, player_hand)
            show_some(player_hand, dealer_hand)
            
            if player_hand.value > 21:
                player_busts(player_chips)
                break

        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)
            show_all(player_hand, dealer_hand)

            if dealer_hand.value > 21:
                dealer_busts(player_chips)
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_chips)
            elif dealer_hand.value < player_hand.value:
                player_wins(player_chips)
            else:
                push()

        print(f"Your total chips are: {player_chips.total}")

        new_game = input("Would you like to play again? (y/n): ")
        if new_game.lower() != 'y':
            print("Thanks for playing!")
            playing = False
            break

main()