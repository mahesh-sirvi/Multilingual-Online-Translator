import requests
from bs4 import BeautifulSoup
import sys
args = sys.argv

dict_languages = {'1': 'arabic', '2': 'german', '3': 'english', '4': 'spanish', '5': 'french', '6': 'hebrew',
                  '7': 'japanese', '8': 'dutch', '9': 'polish', '10': 'portuguese', '11': 'romanian',
                  '12': 'russian', '13': 'turkish'}
list_languages = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese', 'dutch', 'polish',
                  'portuguese', 'romanian', 'russian', 'turkish']
req = requests.Session()
temp = req.get('https://google.com')
if temp.status_code != 200:
    print('Something wrong with your internet connection')
    sys.exit()
language = args[1]

translate_to = args[2]
if language not in list_languages:
    print("Sorry, the program doesn't support {}".format(language))
    sys.exit()
elif translate_to not in list_languages and translate_to != 'all':
    print("Sorry, the program doesn't support {}".format(translate_to))
    sys.exit()

word = args[3]
list_languages.remove(language)
count = 0
if translate_to == 'all':
    while count != 12:
        url = 'https://context.reverso.net/translation/{}-{}/{}'.format(language, list_languages[count], word)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
        r = req.get(url, headers=headers)
        if r.status_code >= 300:
            print('Sorry, unable to find {}'.format(word))
            sys.exit()
        soup = BeautifulSoup(r.content, 'html.parser')
        s = soup.select('.translation')
        word_list = []
        for a in s:
            word_list.append(a.get_text().strip())
        word_list.pop(0)
        sentences = soup.select('#examples-content .text')
        sentences_list = []
        for s in sentences:
            sentences_list.append(s.get_text().strip())
        translated_word = word_list[0] + '\n'
        new_line = '\n'
        line1 = '{} Translations: \n'.format(list_languages[count]).title()

        with open('{}.txt'.format(word), 'a', encoding='utf-8') as my_file:
            my_file.writelines(line1)
            my_file.write(translated_word)
            my_file.write(new_line)

        line2 = '{} Examples:'.format(list_languages[count]).title()
        res = list(zip(sentences_list, sentences_list[1:] + sentences_list[:1]))
        my_dict = {k: v for (k, v) in res}
        count += 1
        for k, v in my_dict.items():

            with open('{}.txt'.format(word), 'a', encoding='utf-8') as my_file:
                my_file.write(line2 + '\n')
                my_file.write(k + ':' + '\n')
                my_file.write(v + '\n')
                my_file.write('\n' * 2)

            break

    with open('{}.txt'.format(word), 'r', encoding='utf-8') as read:
        print(read.read())
else:
    url = 'https://context.reverso.net/translation/{}-{}/{}'.format(language, translate_to, word)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.select('.translation')
    word_list = []
    for a in s:
        word_list.append(a.get_text().strip())
    word_list.pop(0)
    sentences = soup.select('#examples-content .text')
    sentences_list = []
    for s in sentences:
        sentences_list.append(s.get_text().strip())

    line1 = '{} Translations:'.format(translate_to).title()
    with open('{}.txt'.format(word), 'a', encoding='utf-8') as my_file:
        my_file.writelines(line1 + '\n')
    new_list_words = word_list[:5]
    for new in new_list_words:
        with open('{}.txt'.format(word), 'a', encoding='utf-8') as my_file:
            my_file.write(new)
            my_file.write('\n')

    line2 = '{} Examples:'.format(translate_to).title()
    with open('{}.txt'.format(word), 'a', encoding='utf-8') as my_file:
        my_file.writelines('\n' + line2 + '\n')
    res = list(zip(sentences_list, sentences_list[1:] + sentences_list[:1]))
    my_dict = {k: v for (k, v) in res}
    count = 0
    for k, v in my_dict.items():
        with open('{}.txt'.format(word), 'a', encoding='utf-8') as my_file:
            my_file.write(k + ':' + '\n')
            my_file.write(v + '\n')
            my_file.write('\n')
        count += 1
        if count == 5:
            break
    with open('{}.txt'.format(word), 'r', encoding='utf-8') as my_file:
        print(my_file.read())