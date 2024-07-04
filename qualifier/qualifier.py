import re
import warnings
from enum import auto, StrEnum

MAX_QUOTE_LENGTH = 50


# The two classes below are available for you to use
# You do not need to implement them
class VariantMode(StrEnum):
    NORMAL = auto()
    UWU = auto()
    PIGLATIN = auto()


class DuplicateError(Exception):
    """Error raised when there is an attempt to add a duplicate entry to a database"""


# Implement the class and function below
class Quote:
    def __init__(self, quote: str, mode: "VariantMode") -> None:
        self.quote = quote
        self.mode = mode

        self.quote = self._create_variant()

    def __str__(self) -> str:
        return self.quote

    def _create_variant(self) -> str:
        """
        Transforms the quote to the appropriate variant indicated by `self.mode` and returns the result
        """
        if self.mode == VariantMode.UWU:
            sillyfied_quote = self.quote
            replacements = {'l': 'w', 'L': 'W', 'r': 'w', 'R': 'W', ' u': ' u-u', ' U': ' U-U'}
            for candidate, replacement in replacements.items():
                sillyfied_quote = sillyfied_quote.replace(candidate, replacement)

            if len(sillyfied_quote) > MAX_QUOTE_LENGTH:
                sillyfied_quote = sillyfied_quote.replace('u-u', 'u')
                sillyfied_quote = sillyfied_quote.replace('U-U', 'U')
                warnings.warn('Quote too long, only partially transformed')

        elif self.mode == VariantMode.PIGLATIN:
            words = []
            for word in self.quote.split(" "):
                consonant_cluster = ''
                for char in word:
                    if char not in 'aeiouAEIOU':
                        consonant_cluster += char
                    else:
                        break
                if consonant_cluster:
                    words.append(f"{word[len(consonant_cluster):]}{consonant_cluster}ay")
                else:
                    words.append(f"{word}way")
            sillyfied_quote = " ".join(words).capitalize()

            if len(sillyfied_quote) > MAX_QUOTE_LENGTH:
                sillyfied_quote = self.quote

        else:
            sillyfied_quote = self.quote

        if len(self.quote) > MAX_QUOTE_LENGTH:
            raise ValueError("Quote is too long")

        if self.mode != VariantMode.NORMAL and self.quote == sillyfied_quote:
            raise ValueError("Quote was not modified")

        return sillyfied_quote


def run_command(command: str) -> None:
    """
    Will be given a command from a user. The command will be parsed and executed appropriately.

    Current supported commands:
        - `quote` - creates and adds a new quote
        - `quote uwu` - uwu-ifys the new quote and then adds it
        - `quote piglatin` - piglatin-ifys the new quote and then adds it
        - `quote list` - print a formatted string that lists the current
           quotes to be displayed in discord flavored markdown
    """
    if match := re.search(r"[\"“‘'](.*)[\"”’']", command):
        command, quote = command[:match.start()].strip(), match.group(1)
    else:
        quote = ''

    match command:
        case 'quote': variant = VariantMode.NORMAL
        case 'quote uwu': variant = VariantMode.UWU
        case 'quote piglatin': variant = VariantMode.PIGLATIN
        case 'quote list': return print(f"- {"\n- ".join(Database.get_quotes())}")
        case _: raise ValueError("Invalid command")

    try:
        Database.add_quote(Quote(quote, variant))
    except DuplicateError:
        print("Quote has already been added previously")


# The code below is available for you to use
# You do not need to implement it, you can assume it will work as specified
class Database:
    quotes: list["Quote"] = []

    @classmethod
    def get_quotes(cls) -> list[str]:
        "Returns current quotes in a list"
        return [str(quote) for quote in cls.quotes]

    @classmethod
    def add_quote(cls, quote: "Quote") -> None:
        "Adds a quote. Will raise a `DuplicateError` if an error occurs."
        if str(quote) in [str(quote) for quote in cls.quotes]:
            raise DuplicateError
        cls.quotes.append(quote)
