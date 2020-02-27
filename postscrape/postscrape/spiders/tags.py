import collections
import nltk
from nltk.stem import WordNetLemmatizer

# Read input file
#file = open('science-news-100p.json', encoding="utf8")
#a= file.read()
def tags(a):
    # Stopwords
    stopwords = set(line.strip() for line in open('stopwords.txt'))
    #stopwords = stopwords.union(set(['mr','mrs','one','two','the','of','to']))

    wnl = WordNetLemmatizer()

    # Instantiate a dictionary, and for every word in the file, 
    # Add to the dictionary if it doesn't exist. If it does, increase the count.
    wordcount = {}
    myIdx = []
    # To eliminate duplicates, remember to split by punctuation, and use case demiliters.
    for word in str(a).lower().split():
        word.strip()
        word = word.replace(".","")
        word = word.replace(",","")
        word = word.replace(":","")
        word = word.replace("'","")
        #word = word.replace("–","")
        word = word.replace("\"","")
        word = word.replace("!","")
        word = word.replace("â€œ","")
        word = word.replace("â€˜","")
        word = word.replace("*","")
        word = wnl.lemmatize(word)
        if word not in stopwords:
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1
                
    # Print most common word
    #n_print = int(input("How many most common words to print: "))
    n_print  = int(10)
    #print("\nThe {} most common words are as follows\n".format(n_print))
    word_counter = collections.Counter(wordcount)
    for word, count in word_counter.most_common(n_print):
        myIdx.append([word,count])
    return (myIdx)
        #print(word, ": ", count)
        #yield word,count
    
#Close the file
#file.close()