import json
import os

class Card:
    def __init__(self, question, answer, box=1):
        self.question = question.strip()
        self.answer = answer.strip()
        self.box = box

    def to_dict(self):
        return {
            "question": self.question,
            "answer": self.answer,
            "box": self.box
        }


class Deck:
    def __init__(self, filename="flashcards.json"):
        self.cards = []
        self.filename = filename
        self.load_from_file()

    def add_card(self, question, answer):
        new_card = Card(question, answer)
        self.cards.append(new_card)
        self.save_to_file()
        print(f"\n✅ Successfully added: '{question}' to your deck!")

    def save_to_file(self):
        dict_list = [card.to_dict() for card in self.cards]
        with open(self.filename, "w") as f:
            json.dump(dict_list, f, indent=4)

    def load_from_file(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    dict_list = json.load(f)
                self.cards = [Card(d["question"], d["answer"], d["box"]) for d in dict_list]
            except Exception as e:
                print(f"\n⚠️ Warning: Error loading data file ({e}). Starting fresh.")
                self.cards = []
        else:
            self.cards = []


def run_study_session(deck):
    """Filters cards by specific box layers to run target Leitner intervals."""
    if not deck.cards:
        print("\n❌ Your deck is completely empty! Add some cards first.")
        return

    print("\n📦 --- SELECT STUDY TARGET ---")
    box_input = input("Which Box level would you like to practice today? (Leave blank to study ALL cards): ").strip()

    # Step 1: Determine if we are filtering or reviewing the entire array
    if box_input == "":
        filtered_cards = deck.cards
        session_title = "ALL ACTIVE CARDS"
    else:
        try:
            target_box = int(box_input)
            # List Comprehension: Filter the array to match our target box rank
            filtered_cards = [card for card in deck.cards if card.box == target_box]
            session_title = f"BOX {target_box} INDICES"
        except ValueError:
            print("❌ Invalid input! Please enter a valid numerical box rank.")
            return

    if not filtered_cards:
        print(f"\n🏖️ Clean slate! No flashcards currently match that selection filter.")
        return

    print("\n" + "📚" * 15)
    print(f"      STUDY MODE: {session_title}      ")
    print("📚" * 15)
    
    correct_count = 0
    total_cards = len(filtered_cards)

    # Step 2: Loop exclusively through the matching subset
    for index, card in enumerate(filtered_cards, 1):
        print(f"\n📋 Card {index}/{total_cards} | [Current Mastery: Box {card.box}]")
        print(f"❓ QUESTION: {card.question}")
        
        input("👉 Press [Enter] to reveal the answer...")
        print(f"💡 ANSWER  : {card.answer}")
        
        while True:
            response = input("Did you get it right? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                card.box += 1  # Promote card state up to the next tier
                correct_count += 1
                print(f"🎉 Great job! Card promoted to Box {card.box}.")
                break
            elif response in ['n', 'no']:
                card.box = 1  # Reset state back to base box tier
                print("⚠️ No worries! Card sent back to Box 1 for core practice.")
                break
            else:
                print("❌ Invalid input. Please enter 'y' or 'n'.")

    # Step 3: Write changes to disk cache
    deck.save_to_file()
    
    score_percentage = round((correct_count / total_cards) * 100, 1)
    print("\n" + "="*35)
    print("      SESSION COMPLETED!      ")
    print("="*35)
    print(f"🎯 Total Correct Answers: {correct_count}/{total_cards}")
    print(f"📊 Session Accuracy Rate : {score_percentage}%")
    print("="*35)


def main():
    my_deck = Deck()
    
    if not my_deck.cards:
        print("\n📝 Welcome! Loading basic starter cards into your new deck...")
        my_deck.add_card("What is the keyword to define a function in Python?", "def")
        my_deck.add_card("What data structure uses square brackets [] in Python?", "list")

    while True:
        print("\n" + "="*35)
        print("   FLASHCARD TERMINAL STUDIO   ")
        print("="*35)
        print("1. View Total Cards in Deck")
        print("2. Add a Custom Flashcard")
        print("3. Start Interactive Study Session")
        print("4. Exit Program")
        print("-"*35)
        
        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            print(f"\n📊 Your deck currently contains {len(my_deck.cards)} active flashcards.")
            for index, card in enumerate(my_deck.cards, 1):
                print(f"  {index}. Q: '{card.question[:35]}...' | [Box {card.box}]")
            
        elif choice == "2":
            print("\n--- CREATE A NEW FLASHCARD ---")
            q = input("Enter the Question: ")
            a = input("Enter the Answer: ")
            if q.strip() and a.strip():
                my_deck.add_card(q, a)
            else:
                print("❌ Error: Fields cannot be blank!")
                
        elif choice == "3":
            run_study_session(my_deck)
                
        elif choice == "4":
            print("\n👋 Thank you for studying with Flashcard Studio! Happy coding!")
            break
            
        else:
            print("❌ Invalid input! Please type a number between 1 and 4.")


if __name__ == "__main__":
    main()