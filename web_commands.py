import webbrowser
import os
import sys
import requests
import re

def open_google():
    url = 'https://www.google.com'
    try:
        if os.name == 'nt':  # For Windows
            os.system(f'start {url}')
        elif os.name == 'posix':  # For macOS and Linux
            os.system(f'open {url}')
        else:
            webbrowser.open(url)
        return "Opening Google."
    except Exception as e:
        return f"Failed to open Google: {e}"

def open_youtube():
    url = 'https://www.youtube.com'
    try:
        if os.name == 'nt':
            os.system(f'start {url}')
        elif os.name == 'posix':
            os.system(f'open {url}')
        else:
            webbrowser.open(url)
        return "Opening YouTube."
    except Exception as e:
        return f"Failed to open YouTube: {e}"


def get_weather(location):
    api_key = 'your_openweathermap_api_key'
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    complete_url = base_url + 'appid=' + api_key + '&q=' + location
    response = requests.get(complete_url)
    weather_data = response.json()

    if weather_data['cod'] != '404':
        main = weather_data['main']
        weather_desc = weather_data['weather'][0]['description']
        temperature = main['temp'] - 273.15  # Convert temperature from Kelvin to Celsius
        return f"The temperature in {location} is {temperature:.2f}°C with {weather_desc}."
    else:
        return "City not found."

def get_latest_news():
    api_key = 'your_newsapi_api_key'
    base_url = 'https://newsapi.org/v2/top-headlines?'
    country = 'us'  # You can change this to any country code
    complete_url = base_url + 'country=' + country + '&apiKey=' + api_key
    response = requests.get(complete_url)
    news_data = response.json()

    if news_data['status'] == 'ok':
        articles = news_data['articles'][:5]  # Get top 5 articles
        news_summary = 'Here are the latest news headlines:\n'
        for i, article in enumerate(articles, 1):
            news_summary += f"{i}. {article['title']}\n"
        return news_summary
    else:
        return "Failed to retrieve news."

def play_on_youtube(query):
    search_query = query.replace('play', '').strip()
    search_query = re.sub(r'\s+', '+', search_query)
    youtube_search_url = f"https://www.youtube.com/results?search_query={search_query}"
    webbrowser.open(youtube_search_url)
    return f"Searching for {search_query} on YouTube."

def search_on_google(query):
    search_query = query.replace('search', '').strip()
    search_query = re.sub(r'\s+', '+', search_query)
    google_search_url = f"https://www.google.com/search?q={search_query}"
    webbrowser.open(google_search_url)
    return f"Searching for {search_query} on Google."

def browse_internet(query):
    query = query.lower()
    if 'search for' in query:
        search_query = query.replace('search for', '').strip()
        url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(url)
        return f"Searching for {search_query} on Google."
    elif 'open website' in query:
        website = query.replace('open website', '').strip()
        if not website.startswith('http'):
            website = 'http://' + website
        webbrowser.open(website)
        return f"Opening the website {website}."
    return "I can only search on Google or open a specified website."

def handle_web_command(command):
    if 'weather' in command.lower():
        location = command.split('in')[-1].strip()
        return get_weather(location)
    elif 'latest news' in command.lower():
        return get_latest_news()
    elif 'play' in command.lower():
        return play_on_youtube(command)
    elif 'search' in command.lower():
        return search_on_google(command)
    else:
        return browse_internet(command)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])
        response = handle_web_command(command)
        print(response)
    else:
        print("No command provided.")
