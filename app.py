import random
import json
from flask import Flask
from flask import session
from tensorflow import keras


app = Flask(__name__)
app.secret_key = 'e332c75bc8de5a684596e55242f9beb5c1cff28d8dc771618a90e82af17a2610'

@app.route("/get-response/<prompt>")
def get_response(prompt):
    if "current_book_index" not in session:
        session["current_book_index"] = 0
    return send_prompt(prompt)

# Load your model
model = keras.models.load_model('model.h5')

# Load intents data
data_file = open('intents.json').read()
intents = json.loads(data_file)

def get_books_by_tag(tag):
    # Get all books for a specific tag from intents data
    tag_books = []
    for intent in intents['intents']:
        if intent['tag'].lower() == tag.lower():
            tag_books.extend(intent['responses'])
           
    return tag_books

def get_highest_rated_book(tag):
    # Get all books for a specific tag from intents data
    tag_books = []
    for intent in intents['intents']:
        if intent['tag'].lower() == tag.lower():
            tag_books.extend(intent['responses'])  # Assuming 'responses' contain dictionaries
           
    # Ensure tag_books is a list of dictionaries
    if isinstance(tag_books, list):
        # Filter out items without a 'Rate' key
        rated_books = [book for book in tag_books if 'Rate' in book]
        
        if rated_books:
            # Sort the books by the 'Rate' key in descending order
            sorted_books = sorted(rated_books, key=lambda x: x['Rate'], reverse=True)
            return sorted_books[0]  # Return the highest rated book
        else:
            return None  # No books with a 'Rate' key found
    else:
        return None  # Invalid data structure for tag_books


def get_next_book(tag, current_index):
    # Get the next book for a specific tag based on the current index
    tag_books = get_books_by_tag(tag)
    return tag_books[current_index] if current_index < len(tag_books) else None


def send_prompt(user_input):
    # Define tag_input here to ensure it's always defined
    tag_input = user_input.lower()

    response = None

    if tag_input in ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']:
        response = random.choice(intents['intents'][0]['responses'])  # 'greeting' 
    elif tag_input in ['goodbye', 'bye', 'see you later', 'adios', 'take care']:
        response = random.choice(intents['intents'][1]['responses'])  # 'goodbye' intent
    elif tag_input in ['thanks', 'thank you', 'thanks a lot', 'appreciate it', 'thank you so much']:
        response = random.choice(intents['intents'][2]['responses'])  # 'thanks' intent
    elif tag_input in ['can you recommend a book', 'i\'m looking for a book', 'recommend me something to read']:
        response = random.choice(intents['intents'][3]['responses'])  # 'book_search' intent
    elif tag_input in ['can you tell me about author j.k. rowling', 'who is author j.k. rowling', 'recommend books by j.k. rowling']:
        response = random.choice(intents['intents'][4]['responses'])  # 'author_info' intent for J.K. Rowling
    elif tag_input in ['can you tell me about author stephen king', 'who is author stephen king', 'recommend books by stephen king']:
        response = random.choice(intents['intents'][5]['responses'])  # 'author_info' intent for Stephen King
    elif tag_input in ['can you tell me about author agatha christie', 'who is authoragatha christie ', 'recommend books by agatha christie']:
        response = random.choice(intents['intents'][6]['responses'])  # 'author_info' intent for Agatha Christie
    elif 'dan brown' in tag_input:
        response = random.choice(intents['intents'][7]['responses'])
    elif 'importance of books' in tag_input:
        response = random.choice(intents['intents'][8]['responses'])
    elif 'reading habit' in tag_input:
        response = random.choice(intents['intents'][9]['responses'])
    elif 'reading spots' in tag_input:
        response = random.choice(intents['intents'][10]['responses'])
    elif 'book for beginners' in tag_input:
        response = random.choice(intents['intents'][11]['responses'])
    elif 'personal library' in tag_input:
        response = random.choice(intents['intents'][12]['responses'])
    elif 'reading speed' in tag_input:
        response = random.choice(intents['intents'][13]['responses'])
    elif 'brief of the book' in tag_input:
        response = random.choice(intents['intents'][14]['responses'])
    elif 'write a book' in tag_input:
        response = random.choice(intents['intents'][15]['responses'])
   
    elif 'feel boring' in tag_input:
        response = random.choice(intents['intents'][16]['responses'])
    elif 'gone girl' in tag_input:
        response = random.choice(intents['intents'][17]['responses'])
        
    elif 'to kill a mockingbird' in tag_input:
        response = random.choice(intents['intents'][18]['responses'])
        
    elif '1984' in tag_input:
        response = random.choice(intents['intents'][19]['responses'])
                
    elif 'the hobbit' in tag_input:
        response = random.choice(intents['intents'][20]['responses'])
    elif 'the great gatsby' in tag_input:
        response = random.choice(intents['intents'][21]['responses'])    
    elif 'loves reading' in tag_input:
        response = random.choice(intents['intents'][22]['responses'])

    else:
        # Check if the user input contains any pattern in the intents file
        for intent in intents['intents']:
            for pattern in intent['patterns']:
                if pattern.lower() in tag_input:  # Match if any pattern is contained within the user input
                    response = get_highest_rated_book(intent['tag'])
                    session["current_book_index"] += 1
                    if response:
                        next_book = get_next_book(intent['tag'], session["current_book_index"])
                        if next_book:
                            response = next_book
                        else:
                            response = {'message': "No more books found for this category."}

                        return response
                    break
            if response:
                    break

        # If no matching pattern is found, display the default response
        if not response:
            response = "I'm sorry, I didn't understand that."    
    return {'message': response}