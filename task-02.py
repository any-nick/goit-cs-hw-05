import string
import requests
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"{response}")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"{e}")
        return None

def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    return word.lower(), 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

def map_reduce(text):

    text = remove_punctuation(text)
    words = text.split()

    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    shuffled_values = shuffle_function(mapped_values)

    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)


def visualize_top_words(word_counts):
    sorted_word_counts = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:10]
    words, counts = zip(*sorted_word_counts)

    plt.figure(figsize=(10, 6))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Слово')
    plt.ylabel('Частота')
    plt.title('10 найвживаніших слів')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)

    if text:
        word_counts = map_reduce(text)

        for word, count in sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:10]:
            print(f"{word}: {count}")

        visualize_top_words(word_counts)
    else:
        print("Текст не було отримано з вказаної URL адреси")
