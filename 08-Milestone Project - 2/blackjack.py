import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
          'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    '''
    Represents a single playing card with suit and rank
    '''
    def __init__(self, suit, rank):
        if suit not in suits or rank not in ranks:
            raise ValueError(f"Invalid card: {rank} of {suit}")
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
class Deck:
    '''
    Represents a deck of 52 playing cards with shuffle and deal functionality
    '''
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
                
    def __str__(self):
        return "The deck contains: \n" + "\n".join(str(card) for card in self.deck)

    def shuffle(self):
        '''
        Shuffles the deck randomly
        '''
        random.shuffle(self.deck)

    def deal(self):
        '''
        Deals one card from the top of the deck
        '''
        if not self.deck:
            raise IndexError("Cannot deal from an empty deck")
        return self.deck.pop()

class Hand:
    '''
    Represents a player's or dealer's hand of cards
    '''
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    def add_card(self, card):
        '''
        Adds a card to the hand and updates the value
        '''
        if not isinstance(card, Card):
            raise TypeError("Can only add Card objects to hand")
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        '''
        Adjusts hand value when aces are present and value exceeds 21
        '''
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
            
class Chips:
    '''
    Tracks player's chip count and betting
    '''
    def __init__(self, total=100):
        if total < 0:
            raise ValueError("Chip total cannot be negative")
        self.total = total
        self.bet = 0

    def win_bet(self):
        '''
        Adds bet amount to total chips when player wins
        '''
        self.total += self.bet

    def lose_bet(self):
        '''
        Subtracts bet amount from total chips when player loses
        '''
        self.total -= self.bet
        
def take_bet(chips):
    '''
    Prompts player to place a bet and validates the amount
    '''
    while True:
        try:
            bet_input = input("How many chips would you like to bet? ").strip()
            if not bet_input:
                print("Please enter a valid number.")
                continue
                
            bet = int(bet_input)
            if bet <= 0:
                print("Bet must be a positive number.")
            elif bet > chips.total:
                print(f"You do not have enough chips! You have {chips.total} chips.")
            else:
                chips.bet = bet
                break
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\nExiting game...")
            exit()

def hit(deck, hand):
    '''
    Deals one card to the hand and adjusts for aces
    '''
    try:
        hand.add_card(deck.deal())
        hand.adjust_for_ace()
    except IndexError:
        print("Warning: Deck is empty! Creating new deck...")
        deck.__init__()
        deck.shuffle()
        hand.add_card(deck.deal())
        hand.adjust_for_ace()
    
def hit_or_stand(deck, hand):
    '''
    Prompts player to hit or stand and handles the action
    '''
    global playing
    
    while True:
        try:
            answer = input("Would you like to hit or stand? (h/s) ").strip().lower()
            if not answer:
                print("Please enter 'h' for hit or 's' for stand.")
                continue
            elif answer in ['h', 'hit']:
                hit(deck, hand)
                break
            elif answer in ['s', 'stand']:
                print("Player stands. Dealer's turn.")
                playing = False
                break
            else:
                print("Invalid input. Please enter 'h' for hit or 's' for stand.")
        except KeyboardInterrupt:
            print("\nExiting game...")
            exit()
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")

def show_some(player, dealer):
    '''
    Shows dealer's first card hidden and all player cards
    '''
    print('_' * 20)
    print("Dealer's Hand: ?")
    if len(dealer.cards) >= 2:
        print("[Hidden Card]")
        print(dealer.cards[1])
    print('_' * 20)
    print(f"Player's Hand: {player.value}")
    for card in player.cards:
        print(card)
    print('_' * 20)

def show_all(player, dealer):
    '''
    Shows all cards for both player and dealer
    '''
    print('_' * 20)
    print(f"Dealer's Hand: {dealer.value}")
    for card in dealer.cards:
        print(card)
    print('_' * 20)
    print(f"Player's Hand: {player.value}")
    for card in player.cards:
        print(card)
    print('_' * 20)

def player_busts(chips):
    '''
    Handles when player goes over 21
    '''
    print("Player busts!")
    chips.lose_bet()

def player_wins(chips):
    '''
    Handles when player wins the round
    '''
    print("Player wins!")
    chips.win_bet()

def dealer_busts(chips):
    '''
    Handles when dealer goes over 21
    '''
    print("Dealer busts!")
    chips.win_bet()

def dealer_wins(chips):
    '''
    Handles when dealer wins the round
    '''
    print("Dealer wins!")
    chips.lose_bet()

def push():
    '''
    Handles when player and dealer tie
    '''
    print("Tie, it's a push!")

def setup_game():
    '''
    Sets up a new game with deck and hands
    '''
    print("\n" + "="*40)
    print("Welcome to Blackjack!")
    print('Get as close to 21 without going over!')
    print('Dealer hits until reaching 17.')
    print("="*40)

    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()

    for _ in range(2):
        player_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())
    
    return deck, player_hand, dealer_hand

def setup_chips_and_bet(player_chips=None):
    '''
    Initializes player chips (if first game) and takes initial bet
    '''
    if player_chips is None:
        player_chips = Chips()
    
    print(f"\nYou have {player_chips.total} chips.")
    take_bet(player_chips)
    return player_chips

def play_player_turn(deck, player_hand, dealer_hand):
    '''
    Handles the player's turn
    '''
    global playing
    
    while playing and player_hand.value <= 21:
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            return False
    return True

def play_dealer_turn(deck, player_hand, dealer_hand):
    '''
    Handles the dealer's turn
    '''
    print("\nDealer reveals hidden card...")
    show_all(player_hand, dealer_hand)
    
    while dealer_hand.value < 17:
        print("Dealer hits...")
        hit(deck, dealer_hand)
        show_all(player_hand, dealer_hand)

def determine_winner(player_hand, dealer_hand, player_chips):
    '''
    Determines and announces the winner of the round
    '''
    if dealer_hand.value > 21:
        dealer_busts(player_chips)
    elif dealer_hand.value > player_hand.value:
        dealer_wins(player_chips)
    elif dealer_hand.value < player_hand.value:
        player_wins(player_chips)
    else:
        push()

def ask_play_again():
    '''
    Asks player if they want to play another round
    '''
    while True:
        try:
            new_game = input("\nWould you like to play again? (y/n): ").strip().lower()
            if new_game in ['y', 'yes']:
                return True
            elif new_game in ['n', 'no']:
                print("Thanks for playing!")
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")
        except KeyboardInterrupt:
            print("\nThanks for playing!")
            return False

def play_single_round(player_chips=None):
    '''
    Plays a single round of blackjack
    '''
    global playing
    playing = True
    
    deck, player_hand, dealer_hand = setup_game()
    player_chips = setup_chips_and_bet(player_chips)

    show_some(player_hand, dealer_hand)
    player_not_busted = play_player_turn(deck, player_hand, dealer_hand)
    
    if not player_not_busted:
        player_busts(player_chips)
    else:
        play_dealer_turn(deck, player_hand, dealer_hand)
        determine_winner(player_hand, dealer_hand, player_chips)
    print(f"\nYour total chips are: {player_chips.total}")
    
    if player_chips.total <= 0:
        print("You're out of chips! Game over!")
        return None
    
    return player_chips

def main():
    '''
    Main game loop that runs the blackjack game
    '''
    try:
        player_chips = None
        
        while True:
            player_chips = play_single_round(player_chips)
            
            if player_chips is None:
                break
            
            if not ask_play_again():
                break
                
    except KeyboardInterrupt:
        print("\n\nThanks for playing!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Game will now exit.")

if __name__ == "__main__":
    main()