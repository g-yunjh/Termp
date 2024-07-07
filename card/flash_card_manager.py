import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import random

class FlashCard:
    def __init__(self, word, meaning):
        self.word = word
        self.meaning = meaning
        self.difficulty = 0
        self.rounds_seen = defaultdict(int)

class FlashCardManager:
    def __init__(self, filename):
        self.flash_cards = []
        self.load_flashcards(filename)
        self.current_round = 0
        self.all_easy = True
    
    def load_flashcards(self, filename):
        df = pd.read_csv(filename)
        for row in df.itertuples(index=False):
            self.flash_cards.append(FlashCard(row[0], row[1]))
        random.shuffle(self.flash_cards)
    
    def show_current_word(self):
        if not self.flash_cards:
            return None
        return self.flash_cards[0].word
    
    def show_answer(self):
        if not self.flash_cards:
            return None
        return self.flash_cards[0].meaning
    
    def move_word(self, difficulty):
        if not self.flash_cards:
            return
        current_card = self.flash_cards[0]
        current_card.difficulty = difficulty
        current_card.rounds_seen[difficulty] += 1
        self.flash_cards.pop(0)
        if difficulty == 0:
            return
        elif difficulty == 1:
            self.flash_cards.insert(20, current_card)
            self.all_easy = False
        elif difficulty == 3:
            self.flash_cards.insert(30, current_card)
            self.all_easy = False
        else:
            self.flash_cards.insert(10, current_card)
            self.all_easy = False
    
    def next_round(self):
        self.current_round += 1
        self.flash_cards.sort(key=lambda x: (x.rounds_seen[2], x.rounds_seen[1]))
        if self.all_easy:
            self.flash_cards.sort(key=lambda x: x.rounds_seen[0])
        self.all_easy = True

    def save_repetition_counts(self):
        data = []
        for card in self.flash_cards:
            data.append({'word': card.word, 'easy': card.rounds_seen[0], 'medium': card.rounds_seen[1], 'hard': card.rounds_seen[2]})
        if data:  # Check if data is not empty
            df = pd.DataFrame(data)
            df.to_csv('card/static/card/repetition_counts.csv', index=False)
        else:
            print("No data to save.")

    def plot_repetition_counts(self):
        try:
            df = pd.read_csv('card/static/card/repetition_counts.csv')
            if df.empty:
                print("CSV file is empty.")
                return
            df.set_index('word').plot(kind='bar', stacked=True)
            plt.title('Repetition Counts per Word')
            plt.xlabel('Words')
            plt.ylabel('Counts')
            plt.savefig('card/static/card/repetition_counts.png')
        except pd.errors.EmptyDataError:
            print("No columns to parse from file.")

    def get_remaining_cards_count(self):
        return len(self.flash_cards)