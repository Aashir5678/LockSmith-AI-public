import random, string
import requests

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
WORDS = response.content.splitlines()

def get_random_word():
    rand_index = random.randint(0, len(WORDS) - 1)
    
    return (str(WORDS[rand_index]).replace("b'", "")).replace("'", "")

def get_random_num():
    return random.randint(0,9)

def get_random_char():
    return random.choice(string.punctuation)

def process_file(file_path):
    records = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = line.strip().split(':')

            if len(data) == 4:
                link, uri, username, password = data
                username = f"{get_random_word().capitalize()}{get_random_word().capitalize()}{get_random_num()}{get_random_num()}"
                password = f"{get_random_num()}{get_random_num()}{get_random_word()}{get_random_char()}{get_random_num()}"
                if (link == "https") or (link == "http"):
                    records.append({'uri': f"{link}:{uri}", 'username': username, 'password': password})


    return records

if __name__ == "__main__":
    file_path = "sample.txt"
    try:
        records = process_file(file_path)
        if records:
            for record in records:
                print(f"URI: {record['uri']}, Username: {record['username']}, Password: {record['password']}")
        else:
            print("No valid records found in the file.")
    except UnicodeDecodeError as e:
        print(f"Error reading the file: {e}")
