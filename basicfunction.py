




def multiply(first: int , second:int):
    return first * second

class Broke(Exception):
    pass

class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            # raise Exception("you're kind of broke")
            raise Broke

        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1


class lies(Exception):
    pass

class Language_Learner():
    

    def __init__(self, initial_languages = {}):
        self.known_languages = initial_languages
        self.last_added_lang = None
        self.last_forgotten_lang = None
    
    def add_language(self,lang, description='just a language'):
        new_lang = {lang: description}
        self.known_languages.update(new_lang)
        self.last_added_lang = new_lang

    def forget_language(self, lang: str):
        lang_desc = self.known_languages.pop(lang,None)
        if not lang_desc:
            raise lies("you thought you knew this language")
        self.last_forgotten_lang = lang

    @classmethod
    def class_method_test(cls, initial_languages={}, lang=None):
        initial_languages.pop(lang, None)
        start = initial_languages
        return cls(initial_languages)
