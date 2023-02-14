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
1. Run the Python file
2. It will give you examples of probable users search and program's answers to it
	```
	Case 1. User searchs for results properly.
	User inputs: 'I am looking for turkish restaurants with normal prices in Tuebingen with.'
	Slots (complete information): (['Tuebingen'], ['turkish'], ['normal'])
	Answer: There is one restaurant which you could find interesting: Aspendos
	---------- + ----------
	Case 2. User gives incomplete info.
	User inputs: 'I am looking for cheap thai and swabian restaurants.'
	Slots (incomplete information): ([], ['thai', 'swabian'], ['cheap'])
	Program asks: Which area are you interested in?
	User inputs additional information: 'around Stuttgart'
	Slots (complete information): (['Stuttgart'], ['thai', 'swabian'], ['cheap'])
	Answer: There are several restaurants which you could find interesting: Goldener Adler, Thai Thaani
	Note, that program also considers the case when several restaurants are suitable
	```
3. Then it will run the dialogue system, where you can try it by your own*
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
1. Use "java CorpusDemo Beowulf.txt" or the name of any other txt file in the folder
2. The program will return the Flesch Index of a file
>Note: you can clearly see and feel the difference of readability comparing Flesch1.txt and Flesch2. txt. Indeed, the latter is easier to read, which proves the program results.
--- 
