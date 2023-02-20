import re
import random


class Ngram:
    """
    A class for n-gram models based on a text file.

    :attr filename: The name of the file  that the model is based on
    :type filename: str
    :attr n: The number of tokens in the tuples
    :type n: int
    :attr raw_counts: The raw counts of the n-gram tuples
    :type raw_counts: dict
    :attr prob: The probabilities of the n-gram tuples
    :type prob: dict
    :attr cond_prob: The probability distributions over the respective next tokens for each n-1-gram
    :type cond_prob: dict
    """

    def __init__(self, filename="", n=0):
        """
        Initialize an Ngram object.
        :param filename: The name of the file to base the model on.
        :param n: The number of tokens in the n-gram tuples.
        """
        Ngram.filename=filename
        Ngram.n=n
        Ngram.raw_counts=dict()
        Ngram.prob=dict()
        Ngram.cond_prob=dict()
        

    def extract_raw_counts(self):
        """Compute the raw counts for each n-gram occurring in the text."""
        with open(Ngram.filename,"r",encoding="UTF-8") as file:
            lines=file.readlines()
            for line in lines:
                line = re.sub(r"\n", "", line)
                tokens=tokenize_smart(line)
                tokens=["BOS"]*(Ngram.n-1)+tokens+["EOS"]*(Ngram.n-1)
                for i in range(len(tokens)-(Ngram.n-1)):
                    token=[]
                    for k in range(i, i+Ngram.n):
                        token.append(tokens[k])
                    token=tuple(token)
                    if token in Ngram.raw_counts:
                        Ngram.raw_counts[token]+=1
                    else:
                        Ngram.raw_counts[token]=1
                    
                    
                
            

    def extract_probabilities(self):
        """Compute the probability of an n-gram occurring in the text."""
        sum_of_frequencies=sum(Ngram.raw_counts.values())
        for i in Ngram.raw_counts:
            Ngram.prob[i]=Ngram.raw_counts[i]/sum_of_frequencies
            
        

    def extract_conditional_probabilities(self):
        """Compute the probability distribution over the next tokens given an n-1-gram."""
        for i in Ngram.prob:
            mgram=i[:Ngram.n-1]
            ugram=i[Ngram.n-1]
            if mgram not in Ngram.cond_prob:
                Ngram.cond_prob[mgram]={}
            Ngram.cond_prob[mgram][ugram]=Ngram.prob[i]
        for i in Ngram.cond_prob:
            sum_of_frequencies=sum(Ngram.cond_prob[i].values())
            for k in Ngram.cond_prob[i]:
                Ngram.cond_prob[i][k]=Ngram.cond_prob[i][k]/sum_of_frequencies
            
            
            

    def generate_random_token(self, mgram):
        """Generate a random next token based on an n-1 gram,
        taking into account the probability distribution over the possible next tokens for that n-1-gram.

        :param mgram: The n-1 gram to generate the next token for.
        :type mgram: A tuple (of length n-1) of strings.
        :return A random next token for the n-1-gram.
        :rtype string
        """
        candidates_with_probs=Ngram.cond_prob[mgram].items()
        candidates=[]
        probs=[]
        """
        I have used items, because the order in sets is not important.
        Thus, I suppose, the lists generated from values() and keys()
        are random and don't have correlation.
        """
        for i in candidates_with_probs:
            candidates.append(i[0])
            probs.append(i[1])
        return random.choices(candidates,probs)[0]

    def generate_random_sentence(self):
        """Generate a random sentence.

        :return A random sentence.
        :rtype list(str)
        """
        sentence=[]
        mgram=[]
        for i in range(Ngram.n-1):
            mgram.append("BOS")
        mgram=tuple(mgram)
        ugram=""
        while ugram!="EOS":
            ugram=Ngram.generate_random_token(self, mgram)
            mgram=tuple(list(mgram[1:Ngram.n-1])+[ugram])
            sentence.append(ugram)
            
        return sentence[:-1]


def tokenize_smart(sentence):
    """
    Tokenize the sentence into tokens (words, punctuation).

    :param sentence: the sentence to be tokenized
    :type sentence: str
    :return: list of tokens in the sentence
    :rtype: list(str)
    """
    tokens = []

    for word in re.sub(r" +", " ", sentence).split():
        word = re.sub(r"[\"„”“»«`\(\)]", "", word)
        if word != "":
            if word[-1] in ".,!?;:":
                if len(word) == 1:
                    tokens += [word]
                else:
                    tokens += [word[:-1], word[-1]]
            else:
                tokens.append(word)

    return tokens


def list2str(sentence):
    """
    Convert a sentence given as a list of strings to the sentence as a string separated by whitespace.
    :param sentence: The string list to be joined
    :type sentence: list[str]
    :return: sentence as a string, separated by whitespace
    :rtype: str
    """
    sentence = " ".join(sentence)
    sentence = re.sub(r" ([\.,!\?;:])", r"\1", sentence)
    return sentence


if __name__ == '__main__':
    
    # Creating model
    print("Frist, program creates a model for N-gram with three dictionaries, which will be filled in further.")
    print("Let's create one for 2-grams:")
    ngram_model = Ngram("de-sentences-tatoeba.txt", 2)
    print(ngram_model.n, ngram_model.filename)
    print("Dictionary for how many N-grams there:", ngram_model.raw_counts)
    print("Dictionary for probailities of these N-grams:", ngram_model.prob)
    print("Dictionary for probability of word apperaing, if there are N-1 words given:",ngram_model.cond_prob)

    # Counting number of raws
    print("-------------+-------------")
    print("Now let's count every appearence for N-grams and fill in the first dictionary")
    print("It might take a while . . .")
    ngram_model.extract_raw_counts()
    print("Done!")
    print("Let's see how many appearances of \"kaltes Land\" is in dictionary:")
    print(ngram_model.raw_counts[("kaltes", "Land")])
    print("Appearances of \"schönes Land\" in dictionary:")
    print(ngram_model.raw_counts[("schönes", "Land")])
    
    # Calculating probabilities of N-grams
    print("-------------+-------------")
    print("Now let's calculate probabilities for N-grams and fill in the second dictionary")
    print(". . .")
    ngram_model.extract_probabilities()
    print("Done!")
    print("Probability of \"kaltes Land\" in dictionary:")
    print(ngram_model.prob[("kaltes", "Land")])
    print("Probability of \"schönes Land\" in dictionary:")
    print(ngram_model.prob[("schönes", "Land")])
    
    # Calculating conditional probabilities
    print("-------------+-------------")
    print("Now let's calculate conditional probabilities for N-grams and fill in the third dictionary")  
    print(". . .")
    ngram_model.extract_conditional_probabilities()
    print("Done!")
    print("For example, these tokens appear after \"beobachteten\" with this probabilies: ")
    print(ngram_model.cond_prob[("beobachteten",)])
    print("The probability of appearing \"Land\" after \"schönes\"")
    print(ngram_model.cond_prob[("schönes",)][("Land")])
     
    # Generating random token
    print("-------------+-------------")
    print("Let's generate some random tokens! These ones are generated, considering conditional probability of appearing after word \"den\"")
    print(ngram_model.generate_random_token(("den",)))
    print(ngram_model.generate_random_token(("den",)))
    print(ngram_model.generate_random_token(("den",)))
    
    # Generating random sentence
    print("-------------+-------------")
    print("We can even generate a random sentences:")
    print(list2str(ngram_model.generate_random_sentence()))
    print(list2str(ngram_model.generate_random_sentence()))
    