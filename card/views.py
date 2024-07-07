from django.shortcuts import render, redirect
from .flash_card_manager import FlashCardManager

flash_card_manager = None

def select_deck(request):
    global flash_card_manager
    if request.method == 'POST':
        selected_language = request.POST.get('selected_language')
        if selected_language == 'Eng':
            flash_card_manager = FlashCardManager('card/static/card/Eng.csv')
        elif selected_language == 'CC':
            flash_card_manager = FlashCardManager('card/static/card/CC.csv')
        return redirect('main')
    return render(request, 'select_deck.html')

def main(request):
    return render(request, 'main.html')

def show_current_word(request):
    global flash_card_manager
    if flash_card_manager is None:
        return redirect('select_deck')
    current_word = flash_card_manager.show_current_word()
    if current_word is None:
        return redirect('end_of_study')
    remaining_cards_count = flash_card_manager.get_remaining_cards_count()
    return render(request, 'wordcards.html', {'current_word': current_word, 'remaining_cards_count': remaining_cards_count})

def show_answer(request):
    global flash_card_manager
    if flash_card_manager is None:
        return redirect('select_deck')
    answer = flash_card_manager.show_answer()
    if answer is None:
        return redirect('end_of_study')
    remaining_cards_count = flash_card_manager.get_remaining_cards_count()
    return render(request, 'show_answer.html', {'answer': answer, 'remaining_cards_count': remaining_cards_count})

def move_word(request):
    global flash_card_manager
    if flash_card_manager is None:
        return redirect('select_deck')
    if request.method == 'POST':
        difficulty = int(request.POST.get('difficulty'))
        flash_card_manager.move_word(difficulty)
    return redirect('show_current_word')

def next_round(request):
    global flash_card_manager
    if flash_card_manager is None:
        return redirect('select_deck')
    flash_card_manager.next_round()
    return redirect('main')

def end_of_study(request):
    global flash_card_manager
    if flash_card_manager is None:
        return redirect('select_deck')
    flash_card_manager.save_repetition_counts()
    flash_card_manager.plot_repetition_counts()
    return render(request, 'end_of_study.html')

def summary(request):
    return render(request, 'summary.html')