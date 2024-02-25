import matplotlib.pyplot as plt
from collections import Counter
import re
import nltk
import inflect
from nltk.tokenize import word_tokenize

nltk.download('gutenberg', quiet=True)
nltk.download('punkt', quiet=True)

# Наименования книг
books = []
# Содержимое книг
raw_texts = []
for fileid in nltk.corpus.gutenberg.fileids():
    books.append(fileid)
    raw_texts.append(nltk.corpus.gutenberg.raw(fileid))

inf = inflect.engine()

def replace_numbers(match):
    num_text = match.group()
    # Проверка наличия суффикса порядкового числа
    if re.search(r'(st|nd|rd|th|d|ST|ND|RD|TH|D)$', num_text):
        # Удаление суффикса и преобразование в порядковое число
        number = re.sub(r'(st|nd|rd|th|d|ST|ND|RD|TH|D)$', '', num_text)
        return inf.ordinal(inf.number_to_words(number))
    else:
        # Преобразование абсолютного числа в слова
        return inf.number_to_words(num_text)

texts = []  # Новый список для хранения преобразованных текстов

for text in raw_texts:
    processed_text = re.sub(r'\b\d+(?:,\d+)?(?:st|nd|rd|th|d|ST|ND|RD|TH|D)?\b', replace_numbers, text)
    texts.append(processed_text.lower())

books_tokens = [word_tokenize(text) for text in texts]

books_vocabularies = [set(tokens) for tokens in books_tokens]

books_tokens_ext = sum(books_tokens, [])
books_vocabulary = set(books_tokens_ext)


frequency = Counter(books_tokens_ext)
freq_tokens = frequency.most_common(30)


tokens, frequencies = zip(*freq_tokens)

# Plotting the graph
plt.figure(figsize=(10, 8))
plt.bar(tokens, frequencies)
plt.xlabel('Token')
plt.ylabel('Frequency')
plt.title('Top 10 Most Common Tokens in Gutenberg Corpus')
plt.xticks(rotation=45)
plt.show()






