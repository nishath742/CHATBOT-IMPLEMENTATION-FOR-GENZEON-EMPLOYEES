# import sqlite3
# import eel
# import pyttsx3
# import speech_recognition as sr
# import datetime
# import wikipedia
# import webbrowser
# import os
# import smtplib
# import cv2
# from sumy.parsers.plaintext import PlaintextParser
# from sumy.nlp.tokenizers import Tokenizer
# from sumy.summarizers.lsa import LsaSummarizer
# from langdetect import detect
# from googletrans import Translator
# from db_utils import create_db, insert_response, get_response

# # Initialize the text-to-speech engine
# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)

# def speak(audio):
#     engine.say(audio)
#     engine.runAndWait()

# def summarizeDocument(document):
#     parser = PlaintextParser.from_string(document, Tokenizer("english"))
#     summarizer = LsaSummarizer()
#     summary = summarizer(parser.document, 2)  # Adjust number of sentences
#     summarized_text = " ".join([str(sentence) for sentence in summary])
#     return summarized_text

# def translate_text(text, dest_lang='en'):
#     translator = Translator()
#     translated = translator.translate(text, dest=dest_lang)
#     return translated.text

# import webbrowser

# def browse_internet(query):
#     query = query.lower()
    
#     if 'search for' in query:
#         search_query = query.replace('search for', '').strip()
#         url = f"https://www.google.com/search?q={search_query}"
#         webbrowser.open(url)
#         speak(f"Searching for {search_query} on Google.")
#         return f"Searching for {search_query} on Google."

#     elif 'open website' in query:
#         website = query.replace('open website', '').strip()
#         if not website.startswith('http'):
#             website = 'http://' + website
#         webbrowser.open(website)
#         speak(f"Opening the website {website}.")
#         return f"Opening the website {website}."

#     return "I can only search on Google or open a specified website."

# # Update process_query to handle browsing commands
# @eel.expose
# def process_query(query):
#     # Detect language
#     lang = detect(query)
#     original_query = query  # Keep the original query for later use

#     print(f"Original Query: {original_query}")
#     print(f"Detected Language: {lang}")

#     if lang == 'tl':  # Filipino
#         # Translate query to English
#         query = translate_text(query, 'en')
#         print(f"Translated Query (English): {query}")

#     # Handle browsing commands
#     if 'search for' in query.lower() or 'open website' in query.lower():
#         return browse_internet(query)

#     # Check if the query involves capturing an image
#     if 'capture image' in query.lower():
#         captureImage()
#         response = "Image captured and saved."
#         speak(response)
#         return response

#     # Check if the query involves a mathematical operation
#     if any(op in query.lower() for op in ['addition of', 'subtraction of', 'multiplication of', 'division of']):
#         result = performMathOperation(query)
#         speak(result)  # Optional: Uncomment if you want Jarvis to speak the result
#         return result

#     # Process query as usual
#     query = query.lower()
#     response = get_response_for_query(query)
#     print(f"Response (English): {response}")

#     if lang == 'tl':  # Filipino
#         # Translate response back to Filipino
#         response = translate_text(response, 'tl')
#         print(f"Translated Response (Filipino): {response}")

#     speak(response)  # Optional: Uncomment if you want Jarvis to speak the response
#     return response



# def captureImage():
#     # Initialize the camera
#     cap = cv2.VideoCapture(0)  # 0 is usually the default camera
    
#     if not cap.isOpened():
#         print("Error: Unable to open camera.")
#         return "Error: Unable to open camera."
    
#     # Capture a single frame
#     ret, frame = cap.read()
    
#     if ret:
#         # Save the captured frame
#         filename = 'captured_image.jpg'
#         cv2.imwrite(filename, frame)
#         print(f"Image captured and saved as {filename}")
#         cap.release()  # Release the camera
#         cv2.destroyAllWindows()  # Close any OpenCV windows
#         return f"Image captured and saved as {filename}"
#     else:
#         print("Error: Unable to capture image.")
#         cap.release()  # Release the camera
#         cv2.destroyAllWindows()  # Close any OpenCV windows
#         return "Error: Unable to capture image."


# def get_response_for_query(query):
#     response = get_response(query)
#     if response:
#         return response

#     # Extract keywords from the query
#     keywords = extract_keywords(query)
#     if keywords:
#         response = search_keywords(keywords)
#         if response:
#             return response

#     # Fallback logic for specific keywords
#     keyword_responses = {
#         'wikipedia': lambda q: wikipedia.summary(q.replace("wikipedia", "").strip(), sentences=2),
#         'play music': 'Playing music for you.',
#         'open google': open_google,
#         # Add more keywords and corresponding responses as needed
#     }

#     for keyword, resp in keyword_responses.items():
#         if keyword in query:
#             if callable(resp):
#                 return resp(query) if keyword == 'wikipedia' else resp()
#             return resp

#     return "I'm not sure how to help with that."

# def performMathOperation(query):
#     try:
#         if 'addition of' in query:
#             numbers = [int(s) for s in query.split() if s.isdigit()]
#             if len(numbers) == 2:
#                 result = numbers[0] + numbers[1]
#                 return f"The addition of {numbers[0]} and {numbers[1]} is {result}"
#             else:
#                 return "Please provide two numbers for addition."
        
#         elif 'subtraction of' in query:
#             numbers = [int(s) for s in query.split() if s.isdigit()]
#             if len(numbers) == 2:
#                 result = numbers[0] - numbers[1]
#                 return f"The subtraction of {numbers[1]} from {numbers[0]} is {result}"
#             else:
#                 return "Please provide two numbers for subtraction."
        
#         elif 'multiplication of' in query:
#             numbers = [int(s) for s in query.split() if s.isdigit()]
#             if len(numbers) == 2:
#                 result = numbers[0] * numbers[1]
#                 return f"The multiplication of {numbers[0]} and {numbers[1]} is {result}"
#             else:
#                 return "Please provide two numbers for multiplication."

#         elif 'division of' in query:
#             numbers = [int(s) for s in query.split() if s.isdigit()]
#             if len(numbers) == 2:
#                 if numbers[1] != 0:
#                     result = numbers[0] / numbers[1]
#                     return f"The division of {numbers[0]} by {numbers[1]} is {result}"
#                 else:
#                     return "Cannot divide by zero."
#             else:
#                 return "Please provide two numbers for division."
                
#     except Exception as e:
#         return f"An error occurred during the math operation: {e}"




# def extract_keywords(query):
#     keywords = []
#     query = query.lower()
#     conn = sqlite3.connect('jarvis.db')
#     c = conn.cursor()
#     c.execute('SELECT keywords FROM responses')
#     rows = c.fetchall()
#     for row in rows:
#         keyword = row[0]
#         if keyword in query:
#             keywords.append(keyword)
#     conn.close()
#     return keywords

# def search_keywords(keywords):
#     conn = sqlite3.connect('jarvis.db')
#     c = conn.cursor()
#     for keyword in keywords:
#         c.execute('SELECT response FROM responses WHERE keywords = ?', (keyword,))
#         row = c.fetchone()
#         if row:
#             conn.close()
#             return row[0]
#     conn.close()
#     return None

# import os

# def open_google():
#     url = 'https://www.google.com'
#     try:
#         if os.name == 'nt':  # For Windows
#             os.system(f'start {url}')
#         elif os.name == 'posix':  # For macOS and Linux
#             os.system(f'open {url}')
#         else:
#             webbrowser.open(url)
#         print("Attempted to open Google.")
#         return "Opening Google."
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return "Failed to open Google."

# def sendEmail(to, content):
#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.ehlo()
#         server.starttls()
#         server.login('your_email@gmail.com', 'your_password')
#         server.sendmail('your_email@gmail.com', to, content)
#         server.close()
#     except smtplib.SMTPAuthenticationError:
#         speak("Authentication failed. Please check your email and password.")
#     except smtplib.SMTPException as e:
#         speak(f"An error occurred while sending the email: {e}")
#     except Exception as e:
#         speak(f"An unexpected error occurred: {e}")

# def captureImage():
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print("Error: Unable to open camera.")
#         return

#     ret, frame = cap.read()
#     if ret:
#         filename = 'captured_image.jpg'
#         cv2.imwrite(filename, frame)
#         print(f"Image captured and saved as {filename}")
#     else:
#         print("Error: Unable to capture image.")

#     cap.release()
#     cv2.destroyAllWindows()

# def openFolderByName(folder_name):
#     folder_path = search_folder("C:/", folder_name)
#     if folder_path:
#         try:
#             sub_folders = list_folders(folder_path)
#             speak("Folders in the specified folder:")
#             for folder in sub_folders:
#                 speak(folder)
#             speak("Please specify the name of the folder you want to open.")
#             selected_folder = get_folder_name()
#             selected_folder_path = os.path.join(folder_path, selected_folder)
#             if os.path.exists(selected_folder_path):
#                 os.startfile(selected_folder_path)
#                 speak(f"Folder '{selected_folder}' opened successfully.")
#                 files = os.listdir(selected_folder_path)
#                 speak("Files in the folder:")
#                 for file in files:
#                     speak(file)
#                 speak("Please specify the name of the file you want to open.")
#                 selected_file = get_file_name()
#                 selected_file_path = os.path.join(selected_folder_path, selected_file)
#                 if os.path.exists(selected_file_path):
#                     os.startfile(selected_file_path)
#                     speak(f"File '{selected_file}' opened successfully.")
#                 else:
#                     speak(f"File '{selected_file}' not found in the folder.")
#             else:
#                 speak(f"Folder '{selected_folder}' not found in the specified directory.")
#         except Exception as e:
#             speak(f"An error occurred while opening the folder: {e}")
#     else:
#         speak(f"Folder '{folder_name}' not found.")

# def search_folder(root_folder, target_folder_name):
#     for root, dirs, files in os.walk(root_folder):
#         if target_folder_name.lower() in map(str.lower, dirs):
#             return os.path.join(root, target_folder_name)
#     return None

# def list_folders(root_folder):
#     folders = [f.name for f in os.scandir(root_folder) if f.is_dir()]
#     return folders

# def get_email_content():
#     return "Sample email content."

# def get_folder_name():
#     return "Sample Folder Name"

# def get_file_name():
#     return "Sample File Name"

# # Initialize the database
# create_db()

# # Initialize Eel with the correct folder
# eel.init('D:/projects/projects/plan-b')

# # Start the Eel application on port 8081
# eel.start('index.html', size=(1200, 800), port=8081)




import sqlite3
import eel
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import cv2
import subprocess
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from langdetect import detect
from googletrans import Translator
from db_utils import create_db, insert_response, get_response
import yagmail


# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def summarizeDocument(document):
    parser = PlaintextParser.from_string(document, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 2)  # Adjust number of sentences
    summarized_text = " ".join([str(sentence) for sentence in summary])
    return summarized_text

def send_anonymous_email(to_address, subject, content):
    # Use yagmail to send an email through an anonymous SMTP relay
    yag = yagmail.SMTP('anonymous@example.com')  # Use a relay service that allows anonymous emails
    yag.send(to=to_address, subject=subject, contents=content)
    print(f"Anonymous email sent to {to_address}.")

def translate_text(text, dest_lang='en'):
    translator = Translator()
    translated = translator.translate(text, dest=dest_lang)
    return translated.text

# Update process_query to handle browsing commands
@eel.expose
def process_query(query):
    # Detect language
    lang = detect(query)
    original_query = query  # Keep the original query for later use

    print(f"Original Query: {original_query}")
    print(f"Detected Language: {lang}")

    if lang == 'tl':  # Filipino
        # Translate query to English
        query = translate_text(query, 'en')
        print(f"Translated Query (English): {query}")

    if 'send email' in query.lower():
        try:
            to_address = 'b21cs037@kitsw.ac.in'
            subject = 'Anonymous Email from Jarvis'
            content = 'This is an anonymous email sent from Jarvis.'
            send_anonymous_email(to_address, subject, content)
            response = f"Anonymous email sent to {to_address}."
        except Exception as e:
            response = f"An error occurred while sending the email: {e}"
        speak(response)
        return response

    # Handle browsing commands
    if 'search for' in query.lower() or 'open website' in query.lower():
        return browse_internet(query)
    
    if 'open google' in query.lower() or 'open youtube' in query.lower():
        return execute_external_command(query)

    # Check if the query involves capturing an image
    if 'capture image' in query.lower():
        captureImage()
        response = "Image captured and saved."
        speak(response)
        return response

    # Check if the query involves a mathematical operation
    if any(op in query.lower() for op in ['addition of', 'subtraction of', 'multiplication of', 'division of']):
        result = performMathOperation(query)
        speak(result)  # Optional: Uncomment if you want Jarvis to speak the result
        return result

    # Process query as usual
    query = query.lower()
    response = get_response_for_query(query)
    print(f"Response (English): {response}")

    if lang == 'tl':  # Filipino
        # Translate response back to Filipino
        response = translate_text(response, 'tl')
        print(f"Translated Response (Filipino): {response}")

    if query.lower() == "thank you":
        eel.redirectToBlank()  # Call the JavaScript function
        return "Redirecting to a blank page."

    speak(response)  # Optional: Uncomment if you want Jarvis to speak the response
    return response

@eel.expose
def redirect_to_blank():
    eel.execute_js("window.location.href = 'about:blank';")


def captureImage():
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # 0 is usually the default camera
    
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return "Error: Unable to open camera."
    
    # Capture a single frame
    ret, frame = cap.read()
    
    if ret:
        # Save the captured frame
        filename = 'captured_image.jpg'
        cv2.imwrite(filename, frame)
        print(f"Image captured and saved as {filename}")
        cap.release()  # Release the camera
        cv2.destroyAllWindows()  # Close any OpenCV windows
        return f"Image captured and saved as {filename}"
    else:
        print("Error: Unable to capture image.")
        cap.release()  # Release the camera
        cv2.destroyAllWindows()  # Close any OpenCV windows
        return "Error: Unable to capture image."

def get_response_for_query(query):
    response = get_response(query)
    if response:
        return response

    # Extract keywords from the query
    keywords = extract_keywords(query)
    if keywords:
        response = search_keywords(keywords)
        if response:
            return response

    # Fallback logic for specific keywords
    keyword_responses = {
        'wikipedia': lambda q: wikipedia.summary(q.replace("wikipedia", "").strip(), sentences=2),
        'play music': 'Playing music for you.',
        'open google': open_google,
        # Add more keywords and corresponding responses as needed
    }

    for keyword, resp in keyword_responses.items():
        if keyword in query:
            if callable(resp):
                return resp(query) if keyword == 'wikipedia' else resp()
            return resp

    return "I'm not sure how to help with that."

def performMathOperation(query):
    try:
        if 'addition of' in query:
            numbers = [int(s) for s in query.split() if s.isdigit()]
            if len(numbers) == 2:
                result = numbers[0] + numbers[1]
                return f"The addition of {numbers[0]} and {numbers[1]} is {result}"
            else:
                return "Please provide two numbers for addition."
        
        elif 'subtraction of' in query:
            numbers = [int(s) for s in query.split() if s.isdigit()]
            if len(numbers) == 2:
                result = numbers[0] - numbers[1]
                return f"The subtraction of {numbers[1]} from {numbers[0]} is {result}"
            else:
                return "Please provide two numbers for subtraction."
        
        elif 'multiplication of' in query:
            numbers = [int(s) for s in query.split() if s.isdigit()]
            if len(numbers) == 2:
                result = numbers[0] * numbers[1]
                return f"The multiplication of {numbers[0]} and {numbers[1]} is {result}"
            else:
                return "Please provide two numbers for multiplication."

        elif 'division of' in query:
            numbers = [int(s) for s in query.split() if s.isdigit()]
            if len(numbers) == 2:
                if numbers[1] != 0:
                    result = numbers[0] / numbers[1]
                    return f"The division of {numbers[0]} by {numbers[1]} is {result}"
                else:
                    return "Cannot divide by zero."
            else:
                return "Please provide two numbers for division."
                
    except Exception as e:
        return f"An error occurred during the math operation: {e}"

def extract_keywords(query):
    keywords = []
    query = query.lower()
    conn = sqlite3.connect('jarvis.db')
    c = conn.cursor()
    c.execute('SELECT keywords FROM responses')
    rows = c.fetchall()
    for row in rows:
        keyword = row[0]
        if keyword in query:
            keywords.append(keyword)
    conn.close()
    return keywords

def search_keywords(keywords):
    conn = sqlite3.connect('jarvis.db')
    c = conn.cursor()
    for keyword in keywords:
        c.execute('SELECT response FROM responses WHERE keywords LIKE ?', ('%' + keyword + '%',))
        row = c.fetchone()
        if row:
            conn.close()
            return row[0]
    conn.close()
    return None

def browse_internet(query):
    query = query.lower()
    
    if 'search for' in query:
        search_query = query.replace('search for', '').strip()
        url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(url)
        speak(f"Searching for {search_query} on Google.")
        return f"Searching for {search_query} on Google."

    elif 'open website' in query:
        website = query.replace('open website', '').strip()
        if not website.startswith('http'):
            website = 'http://' + website
        webbrowser.open(website)
        speak(f"Opening the website {website}.")
        return f"Opening the website {website}."

    return "I can only search on Google or open a specified website."

def execute_external_command(query):
    if 'open google' in query.lower():
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
        return "Opening Google."
    elif 'open youtube' in query.lower():
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
        return "Opening YouTube."
    return "Command not recognized."

def open_google():
    url = 'https://www.google.com'
    try:
        if os.name == 'nt':  # For Windows
            os.system(f'start {url}')
        elif os.name == 'posix':  # For macOS and Linux
            os.system(f'open {url}')
        else:
            webbrowser.open(url)
        print("Attempted to open Google.")
        return "Opening Google."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Failed to open Google."

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your_email@gmail.com', 'your_password')
        server.sendmail('your_email@gmail.com', to, content)
        server.close()
    except smtplib.SMTPAuthenticationError:
        speak("Authentication failed. Please check your email and password.")
    except smtplib.SMTPException as e:
        speak(f"An error occurred while sending the email: {e}")
    except Exception as e:
        speak(f"An unexpected error occurred: {e}")

def note_this(query):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    note = query.replace("note this", "").strip()
    filename = "notes.txt"
    with open(filename, "a") as f:
        f.write(f"{date}: {note}\n")
    speak("Note taken.")
    return "Note taken."

@eel.expose
def start_jarvis():
    # Implement logic to start Jarvis
    print("Starting Jarvis...")
    speak("Jarvis is now active. How can I assist you?")
    return "Jarvis is now active. How can I assist you?"

# Initialize Eel with the correct folder
eel.init('D:/projects/projects/plan-b')

# Start the Eel application on port 8081
eel.start('index.html', size=(1200, 800), port=8081)
