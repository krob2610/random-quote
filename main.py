import requests
import random
from concurrent.futures import ThreadPoolExecutor, wait

class Quotes:
    def __init__(self):
        self.url = 'https://raw.githubusercontent.com/ajzbc/kanye.rest/master/quotes.json'
        self.positive, self.negative, self.neutral, self.most_extrime, self.number_of_most_extrime  = 0,0,0,0,0
        self.most_extrime_quote = ""
    def get_quots(self):
        return requests.get(self.url).json()

    def collect_quotes(self):
        print("Enter the number of random Quotes you want to get: ", end="")
        quots = self.get_quots()

        while True:
            number_of_quots = int(input())
            if isinstance(number_of_quots, int) and 5<=number_of_quots<=20:
                selected_quotes = random.sample(range(0,len(quots)),number_of_quots)
                break;
            else:
                print("Please select integer number between 5 and 20\nEnter the number of random Quotes you want to get: ", end="")

        print("Quotes selected for you: ", end="\n\n\t")
        self.selected_quots = [quots[int(i)] for i in selected_quotes]
        print(*self.selected_quots, sep="\n\t")

    def get_scoore(self, quote_text):
        quote_json = requests.post("https://sentim-api.herokuapp.com/api/v1/", json={"text": quote_text}, headers = {"Accept": "application/json", "Content-Type": "application/json"}).json()

        if quote_json["result"]["polarity"] > 0:
            self.positive+=1
        elif quote_json["result"]["polarity"] < 0:
            self.negative+=1
        else:
            self.neutral+=1
        if self.most_extrime < abs(quote_json["result"]["polarity"]):
            self.most_extrime = abs(quote_json["result"]["polarity"])
            self.most_extrime_quote = quote_json["sentences"][0]["sentence"]
            self.number_of_most_extrime = 1
        elif self.most_extrime == abs(quote_json["result"]["polarity"]) and self.most_extrime!=0:
            self.most_extrime_quote += "\n\t" + quote_json["sentences"][0]["sentence"]
            self.number_of_most_extrime +=1
        return quote_json
    def count_Scoore(self):
        with ThreadPoolExecutor() as executor:
            res = [executor.submit(self.get_scoore,quote) for quote in self.selected_quots]
            wait(res)
        #print(res[8].result())
    def Print_results(self):
        #time.sleep(2)
        print(f"\nnumber of positive: {self.positive}\nnumber of negative {self.negative}\nnumber of neutral: {self.neutral}")
        if self.number_of_most_extrime == 1:
            print(f"\nThe most extrime quote is: \n\t{self.most_extrime_quote}\n\nwith extreme scoore: {self.most_extrime}")
        elif self.number_of_most_extrime == len(self.selected_quots) or self.number_of_most_extrime == 0:
            print("\nThere was no most extrime quote")
        else:
            print(f"\nThere was {self.number_of_most_extrime} quotes with highest extrime scoore: \n\t{self.most_extrime_quote}\nwith extreme scoore: {self.most_extrime}")
def get_scoore(quote_text):
    return requests.post("https://sentim-api.herokuapp.com/api/v1/", json={"text": quote_text}, headers = {"Accept": "application/json", "Content-Type": "application/json"}).json()

def get_quots():
    return requests.get('https://raw.githubusercontent.com/ajzbc/kanye.rest/master/quotes.json').json()
    #requests.get('https://api.kanye.rest/').json()["quote"]
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    quote = Quotes()
    quote.collect_quotes()
    quote.count_Scoore()
    quote.Print_results()
    # print("Enter the number of random Quotes you want to get: ", end="")
    # quots = get_quots()
    #
    # while True:
    #     number_of_quots = int(input())
    #     if isinstance(number_of_quots, int) and 5<=number_of_quots<=20:
    #         selected_quotes = random.sample(range(0,len(quots)),number_of_quots)
    #         break;
    #     else:
    #         print("Please select integer number between 5 and 20\nEnter the number of random Quotes you want to get: ", end="")
    #
    # print("Quotes selected for you: ", end="\n\t")
    # selected_Quots = [quots[int(i)] for i in selected_quotes]
    # print(*selected_Quots, sep="\n\t")

    #selected_quotes =
    """sending post request"""

    # positive, negative, neutral, most_extrime, number_of_most_extrime  = 0,0,0,0,0
    # most_extrime_quote = ""
    #
    # for i in range(0, number_of_quots):
    #     post = requests.post("https://sentim-api.herokuapp.com/api/v1/", json={"text": selected_Quots[i]}, headers = {"Accept": "application/json", "Content-Type": "application/json"})
    #     if post.json()["result"]["polarity"] > 0:
    #         positive+=1
    #     elif post.json()["result"]["polarity"] < 0:
    #         negative+=1
    #     else:
    #         neutral+=1
    #
    #     if most_extrime < abs(post.json()["result"]["polarity"]):
    #         most_extrime = abs(post.json()["result"]["polarity"])
    #         most_extrime_quote = selected_Quots[i]
    #         number_of_most_extrime = 1
    #     elif most_extrime == abs(post.json()["result"]["polarity"]) and most_extrime!=0:
    #         most_extrime_quote += "\n" + selected_Quots[i]
    #         number_of_most_extrime +=1
    #     print(post.json()["result"]["polarity"])
    #
    # print(f"number of positive: {positive}\nnumber of negative {negative}\nnumber of neutral: {neutral}")
    #
    # if number_of_most_extrime == 1:
    #     print(f"The most extrime quote is: \n{most_extrime_quote}\n with extreme scoore: {most_extrime}")
    # elif number_of_most_extrime == number_of_quots or number_of_most_extrime == 0:
    #         print("There was no most extrime quote")
    # else:
    #     print(f"There was {number_of_most_extrime} quotes with highest extrime scoore: \n{most_extrime_quote}\nwith extreme scoore: {most_extrime}")
    #
    """przyspieszamy multithreading"""
    #list_of_scoores = []
    # with ThreadPoolExecutor() as executor:
    #     res = [executor.submit(get_scoore,quote) for quote in selected_Quots]
    #     wait(res)
    # print(res[8].result())


