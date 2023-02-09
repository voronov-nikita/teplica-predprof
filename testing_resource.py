from translate import Translator

translator = Translator(from_lang="ru", to_lang="en")


txt = input()
print(translator.translate(txt))
