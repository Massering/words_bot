import random


def get_random_word(min_length, used_words) -> str:
    while 1:
        word = random.choice(BaseWord.all_words)
        if len(word) > min_length and word not in used_words:
            return word


def get_possible_words(base_word: str, word_list: list) -> set:
    words = set()
    for word in word_list:
        if all(word.count(j) <= base_word.count(j) for j in word) and word != base_word:
            words.add(word)
    return words


class BaseWord:
    all_words = open('all.txt', encoding='UTF-8').read().split()
    set_of_all_words = set(all_words)

    hard_words = open('hard.txt', encoding='UTF-8').read().split()
    set_of_hard_words = set(hard_words)

    normal_words = open('normal.txt', encoding='UTF-8').read().split()
    set_of_normal_words = set(normal_words)

    easy_words = open('easy.txt', encoding='UTF-8').read().split()
    set_of_easy_words = set(easy_words)

    def __init__(self, level: int, used_words: set):
        self.level = level
        while 1:
            self.word = get_random_word(6, used_words)
            self.possible_words = get_possible_words(self.word,
                                                     [self.easy_words, self.normal_words, self.hard_words][level])
            if self.possible_words:
                break

    def __repr__(self):
        return f'Слово "{self.word}" {self.level + 1} уровня ' \
               f'с {len(self.possible_words)} возможными словами'

    def __str__(self):
        return self.word
