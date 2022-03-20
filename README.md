# WordleBot
Simple search algorithm to solve the 5-letter wordle puzzle

## Scoring
- Scoring heuristic for generating the initial list of candidates is based on letter frequency
- Simulations are run on each potential "solution" word to determine which word will likely narrow down the possible word list the most
- Tie breakers are based on general word word usage using the Datamuse API

## Parameters
- "-s": specifies the proportional size of the initial candidate selection list (default = 10)
- "-f": specifies a seed word to select as the first guess
  - This is done to reduce runtime or account for a more optimally found seed word
  - The current algorithm will find "raise" as its optimal first word. Thus, "-f raise" will decrease search latency for the first guess
- "-t": specifies a solution word to test the wordle bot's performance automatically. Score will be given automatically and no other user input is needed

## Performance
- The Wordle Bot has a 100% success rate on all possible valid Wordle words (as of 03/20/2022)
- With default parameters, the average performance across all words is 3.48 guesses
- With seed word "crane", the average performance is 3.47 guesses
