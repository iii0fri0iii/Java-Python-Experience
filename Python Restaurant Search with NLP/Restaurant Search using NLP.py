locations = ["Tuebingen", "Reutlingen", "Stuttgart"]
cuisines = ["swabian", "turkish", "thai", "chinese", "italian"]
price_levels = ["cheap", "normal", "expensive"]

import csv
def advanced_fill_slots(sentence_str, slots=None):
    """
    Read the string with a sentence and subtract information which is connected to a restaurant request.
    There are three types of useful information: location, cuisine, price level.
    The function returns a tuple of three lists. Each list represents one of the slots.

    :param sentence_str: string with a user input to extract information from
    :type sentence_str: str
    :param slots: (optional) a tuple of three lists of strings to append information to:
                  ([locations], [cuisines], [price levels])
    :type slots: tuple[list[str], list[str], list[str]]
    :return: a tuple of three lists of strings with the information extracted from sentence_str:
             ([locations], [cuisines], [price levels])
    :rtype: tuple[list[str], list[str], list[str]]
    """
    if slots==None:
        slots=[],[],[]
    for token in tokenize(sentence_str):
        if is_location(token):
            slots[0].append(token)
        if is_cuisine(token):
            slots[1].append(token)
        if is_price_level(token):
            slots[2].append(token)
    return slots


def is_not_complete(slots):
    """
    Check if one of the slots in the tuple is empty.
    Each slot is represented by a list of strings.

    :param slots: a tuple with three lists of strings: ([locations], [cuisines], [price levels])
    :type slots: tuple[list[str], list[str], list[str]]
    :return: True if one of the slots is empty
    :rtype: bool
    """
    for slot in slots:
        if len(slot)==0:
            return True
    return False


def generate_question(slots):
    """
    Generate an additional question based on empty slots.

    :param slots: a tuple with three lists of strings: ([locations], [cuisines], [price levels])
    :type slots: tuple[list[str], list[str], list[str]]
    :return: a string with a question asking for clarification on empty information slots
    :rtype: str
    """
    if len(slots[0])==0:
        return "Which area are you interested in?"
    if len(slots[1])==0:
        return "Which cuisine do you prefer?"
    if len(slots[2])==0:
        return "What price level do you prefer?"

def read_database_file(database_file_name):
    """
    Read the file which contains the information about the restaurants and 
    return a data structure.

    The file have 4 columns which are separated by a tab:
    - first column contains the information about the location of the restaurant;
    - second column contains the information about the restaurant's cuisine;
    - third column contains the information about the price level in the restaurant
    - fourth column contains the name of the restaurant

    The data structure is list of tuples. Each tuple has four elements of type string:
    - location of the restaurant;
    - restaurant's cuisine;
    - price level of the restaurant;
    - name of the restaurant.

    :param database_file_name: name of the file which contains the data about restaurants
    :type database_file_name: str
    :return: a data structure which contains information about restaurants
    :rtype: list[tuple[str, str, str, str]]
    """
    data_restaurants=[]
    with open(database_file_name,"r", encoding="UTF-8",) as file:
        lines=csv.reader(file, delimiter="\t")
        for line in lines:
            data_restaurants.append((line[0],line[1],line[2],line[3]))
            
    return data_restaurants
            


def search_in_database(slots, database):
    """
    Search in the database for the restaurants which suit the requirements of the slots.

    :param slots: a tuple with three lists of strings: ([locations], [cuisines], [price levels])
    :type slots: tuple[list[str], list[str], list[str]]
    :param database: a data structure which contains information about restaurants
    :type database: list[tuple[str, str, str, str]]
    :return: suitable restaurants from the database
    :rtype: list[tuple[str, str, str, str]]
    """
    result=[]
    for data in database:
        is_suitable=False
        for i in range(3):
            if data[i] in slots[i]:
                is_suitable=True
            else:
                is_suitable=False
                break
        if is_suitable:
            result.append(data)
    return result
            


def generate_answer(suitable_results):
    """
    Generate an output sentence based on the number of suitable results.

    - If there are no suitable results, the functions returns:
    "Unfortunately, there are no suitable options. Do you want to try anything else?"
    - If there is only one suitable result, the function returns:
    "There is one restaurant which you could find interesting: [NAME_OF_THE_RESTAURANT]"
    - If there are several suitable results, the function returns:
    "There are several restaurants which you could find interesting: [NAMES_OF_THE_RESTAURANTS]"

    :param suitable_results: suitable restaurants from the database
    :type suitable_results: list[tuple[str, str, str, str]]
    :return: a string with an answer message
    :rtype: str
    """
    if len(suitable_results)==0:
        return "Unfortunately, there are no suitable options. Do you want to try anything else?"
    if len(suitable_results)==1:
        return "There is one restaurant which you could find interesting: "+suitable_results[0][3]
    names=""
    for result in suitable_results:
        names+=result[3]+", "
    names=names[:-2]
    return "There are several restaurants which you could find interesting: "+names


def is_location(token):
    """
    Check whether the token represents the location.

    :param token: the word to be checked
    :type token: str
    :return: True if token represents the location
    :rtype: bool
    """
    return token in locations


def is_cuisine(token):
    """
    Check whether the token represents one of the types of the cuisine.

    :param token: the word to be checked
    :type token: str
    :return: True if token represents the type of the cuisine
    :rtype: bool
    """
    return token in cuisines


def is_price_level(token):
    """
    Check whether the token represents one of the price levels.

    :param token: the word to be checked
    :type token: str
    :return: True if token represents the price level
    :rtype: bool
    """
    return token in price_levels


def tokenize(sentence):
    """
    Helper function which is used to tokenize 
    the sentence into tokens (words, punctuation).

    :param sentence: sentence to be split.
    :type sentence: str
    :return: list of tokens
    :rtype: list[str]
    """
    punct = ".,!?;"
    tokens = []

    for word in sentence.split():
        if word[-1] in punct:
            tokens += [word[:-1], word[-1]]
        else:
            tokens.append(word)

    return tokens

def dialog_system(database_fn):
    """
    Run a simple dialogue system with user input.

    :param database_fn: The file name of the database from which to retrieve information.
    """
    db = read_database_file(database_fn)                            # initialize the database
    while True:                                                     # start an endless loop
        request = input("\nHow can I help you?\n")                  # ask for a new request
        slots = advanced_fill_slots(request)                        # gather the information from the request
        while is_not_complete(slots):                               # as long as there is information missing:
            information = input(generate_question(slots) + "\n")    # - ask for clarification on the missing parts, and
            slots = advanced_fill_slots(information, slots)         # - fill the missing slots with the new information
        results = search_in_database(slots, db)                     # search for suitable results in the database
        answer = generate_answer(results)                           # generate an answer
        print(answer)                                               # print the answer


if __name__ == '__main__':
    
    database_fn = "database.tsv"
    example_sentence = "I am looking for cheap thai and swabian restaurants."
    additional_info = "around Stuttgart"
    incomplete_slots = ([], ['thai', 'swabian'], ['cheap'])
    complete_slots = (['Stuttgart'], ['thai', 'swabian'], ['cheap'])
    
    # checking the work of advanced_fill_slots
    print("Checking advanced_fill_slots...")
    print("Input sentence: '" + example_sentence + "'")
    example_slots = advanced_fill_slots(example_sentence)
    print("Slots (incomplete information): " + str(example_slots))
    print("Additional information: '" + str(additional_info) + "'")
    complete_example_slots = advanced_fill_slots(additional_info, example_slots)
    print("Slots (complete information): " + str(complete_example_slots))
    print("---------- + ----------")
    
    # checking the work of is_not_complete
    print("Checking is_not_complete...")
    print("incomplete slots: " + str(is_not_complete(incomplete_slots)))
    print("complete slots: " + str(is_not_complete(complete_slots)))
    print("---------- + ----------")
    
    # checking the work of generate_question. 
    print("Checking generate_question...")
    print("Given input: ([], ['thai', 'swabian'], ['cheap']), the function returns:")
    print(generate_question(([], ['thai', 'swabian'], ['cheap'])))
    print("---------- + ----------")
    
    # reading the database. 
    print("Reading the database...")
    db = read_database_file(database_fn)
    print("---------- + ----------")

    # searching for suitable results.
    print("Searching for suitable results...")
    possible_results = search_in_database(complete_example_slots, db)
    print(possible_results)
    print("---------- + ----------")
    
    # generating a well-formed output
    print("Generating a well-formed output for the dialogue system...")
    well_formed_output = generate_answer(possible_results)
    print("'" + well_formed_output + "'")

    print("---------- + ----------")

    # run the dialog system
    dialog_system(database_fn)
 