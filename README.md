# Kanye West Quotes

A simple console program to grab few random quotes from webpage "https://kanye.rest/" and then show them to user. 
Next, collected quotes run through SENTIM-API: "https://sentim-api.herokuapp.com/" in order to get polarity aspect. 
After this user gets total number of positive, negative and neutral quotes,
as well as the most extreme quote with extreme score(|polarity aspect|).
If there is more than one quote with the exact same extreme score, all of them will be given to user. 

### Requirements:

* Python 3

### Dependencies:

* Requests

### Instructions:

* Install python 3
* Install requests
  - python -m pip install requests
* Clone git repository
  - git clone https://github.com/krob2610/random-quote.git
* Run main.py
  - python main.py
* Insert number of quotes you want to get 
