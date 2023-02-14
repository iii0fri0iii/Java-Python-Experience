# Python, Java Experience

## Python. Restaurant Search using NLP
This project implements the functionality of a simple restaurant recommender which will process the user input and search for the most suitable options for the given request, using the database.

### Algorithm
1. Program reads an external file with database of restaurants 
2. It creates correlations between **location**, **price level**, **cuisine** and restaurant name
3. User searches for a restaurant using these key words
4. If information is not complete, program asks user to clarify it
5. Program finds a restaurant in data and returns result
### Test it!
```
1. Run the Python file
2. It will give you examples of probable users search and program's answers to it
3. Then it will run the dialogue system, where you can try it by your own*
```
>Note: the list of keywords you can use in program:
			locations = ["Tuebingen", "Reutlingen", "Stuttgart"]
			cuisines = ["swabian", "turkish", "thai", "chinese", "italian"]
			price_levels = ["cheap", "normal", "expensive"]
--- 
## Java. Java Corpus Analyzing for Flesch Readabillity Index
This project analyzes a text file and returns a [Flesch Readbility Index](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests) of it.

### Algorithm
1. Program reads an external text file 
2. It identifies words, sentences and syllables 
3. It calculates their numbers and uses these parameters for Flesch Index calculation
4. It returns the Flesch Index for the file
### Test it!
```
1. Use "java CorpusDemo Beowulf.txt" or the name of any other txt file in the folder
2. The program will return the Flesch Index of a file
```
>Note: you can clearly see and feel the difference of readability comparing Flesch1.txt and Flesch2. txt. Indeed, the latter is easier to read, which proves the program results.
--- 
