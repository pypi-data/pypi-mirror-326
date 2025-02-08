def helloWorld(text):
    """Wypisuje podany tekst."""
    print(text)

def helloWorld_up(text):
    """Zamienia tekst na wielkie litery."""
    return text.upper()

def helloWorld_down(text):
    """Zamienia tekst na małe litery."""
    return text.lower()

def helloWorld_countDig(text):
    """Zlicza liczbę znaków w tekście."""
    return len(text)

def helloWorld_reverse(text):
    """Odwraca kolejność liter w tekście."""
    return text[::-1]

def helloWorld_palindrome(text):
    """Sprawdza, czy tekst jest palindromem."""
    return text.lower() == text.lower()[::-1]

def helloWorld_countWrds(text):
    """Zlicza liczbę słów w tekście."""
    return len(text.split())

def helloWorld_spaces(text, replacement="_"):
    """Zamienia spacje w tekście na podany znak (domyślnie: '_')."""
    return text.replace(" ", replacement)

def helloWorld_vow(text):
    """Usuwa samogłoski z tekstu."""
    vowels = "aeiouAEIOUąęó"
    return "".join([char for char in text if char not in vowels])

def helloWorld_fAndL(text):
    """Zwraca pierwszy i ostatni znak tekstu."""
    if len(text) > 1:
        return text[0] + text[-1]
    return text

def helloWorld_title(text):
    """Zamienia tekst na format tytułowy (pierwsza litera każdego słowa wielka)."""
    return text.title()

def helloWorld_swapCase(text):
    """Zamienia wielkość liter: małe na wielkie, wielkie na małe."""
    return text.swapcase()

def helloWorld_punct(text):
    """Usuwa znaki interpunkcyjne z tekstu."""
    import string
    return text.translate(str.maketrans('', '', string.punctuation))

def helloWorld_longest(text):
    """Znajduje najdłuższe słowo w tekście."""
    words = text.split()
    if words:
        return max(words, key=len)
    return ""

def helloWorld_SCletter(text, letter):
    """Zlicza wystąpienia konkretnej litery w tekście."""
    return text.count(letter)
