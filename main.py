"""Simple application that will select 'n' random Kanye West quotes,
rate them and then select the most extreme
quote(or quotes if there is more then one) with 'extremes score'"""
from concurrent.futures import ThreadPoolExecutor, wait
import random
import requests


class Quotes:
    """Class which contains all necessary methods to provide solution for user"""

    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        self.url = 'https://raw.githubusercontent.com/ajzbc/kanye.rest/master/quotes.json'
        self.url2 = "https://sentim-api.herokuapp.com/api/v1/"
        self.positive, self.negative, self.neutral = 0, 0, 0
        self.most_extreme, self.number_of_most_extreme = 0, 0
        self.most_extreme_quote = ""
        self.selected_quotes = None

    def get_quotes(self):
        """Return all quotes """
        return requests.get(self.url).json()

    def collect_quotes(self):
        """Get number given by user and select quotes """
        print("Enter the number of random Quotes you want to get: ", end="")
        quotes = self.get_quotes()

        while True:
            number_of_quotes = int(input())
            if isinstance(number_of_quotes, int) and 5 <= number_of_quotes <= 20:
                selected_quotes = random.sample(range(0, len(quotes)), number_of_quotes)
                break

            print("Please select integer number between 5 and 20")
            print("Enter the number of random Quotes you want to get: ", end="")

        print("Quotes selected for you: ", end="\n\n\t")
        self.selected_quotes = [quotes[int(i)] for i in selected_quotes]
        print(*self.selected_quotes, sep="\n\t")

    def get_score(self, quote_text):
        """Calculate number of positive, negative and neutral quotes.
        Searching for most extreme quote with 'extremes score' (where 0 <= 'extremes score' <= 1)"""
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        quote_json = requests.post(self.url2, json={"text": quote_text}, headers=headers).json()

        if quote_json["result"]["polarity"] > 0:
            self.positive += 1
        elif quote_json["result"]["polarity"] < 0:
            self.negative += 1
        else:
            self.neutral += 1
        if self.most_extreme < abs(quote_json["result"]["polarity"]):
            self.most_extreme = abs(quote_json["result"]["polarity"])
            self.most_extreme_quote = quote_json["sentences"][0]["sentence"]
            self.number_of_most_extreme = 1
        elif self.most_extreme == abs(quote_json["result"]["polarity"]) and self.most_extreme != 0:
            self.most_extreme_quote += "\n\t" + quote_json["sentences"][0]["sentence"]
            self.number_of_most_extreme += 1
        return quote_json

    def count_score(self):
        """Runs get_score in multithreading """
        with ThreadPoolExecutor() as executor:
            res = [executor.submit(self.get_score, q) for q in self.selected_quotes]
            wait(res)

    def print_results(self):
        """Print results to console"""
        print(f"\nnumber of positive: {self.positive}"
              f"\nnumber of negative {self.negative}"
              f"\nnumber of neutral: {self.neutral}")
        if self.number_of_most_extreme == 1:
            print(f"\nThe most extreme quote is: "
                  f"\n\t{self.most_extreme_quote}"
                  f"\nwith extreme score: {self.most_extreme}")
        elif self.number_of_most_extreme == len(self.selected_quotes) \
                or self.number_of_most_extreme == 0:
            print("\nThere was no most extreme quote")
        else:
            print(f"\nThere were {self.number_of_most_extreme} quotes with highest extreme score: "
                  f"\n\t{self.most_extreme_quote}\nwith extreme score: {self.most_extreme}")


if __name__ == '__main__':
    quote = Quotes()
    quote.collect_quotes()
    quote.count_score()
    quote.print_results()
