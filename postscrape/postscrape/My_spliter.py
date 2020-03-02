from nltk.stem import WordNetLemmatizer
def My_spliter (a):
    stopwords = "ourselves hers between yourself but almost may would again there about once during out very having with hi ha they own an be some for do its yours such into of most itself other off is s am or who as from him each the themselves until below are we these your his through don nor me were her more himself this down should our their while above both up to ours had she all no when at any before them same and been have in will on does yourselves then that because what over why so can did not now under he you herself has ha just where too only myself which those i after few whom t being if theirs my against a by doing it how further was wa here than also said could – _ ----- "
    stopwords = stopwords.split()
    wnl = WordNetLemmatizer()
    l = []
    for word in a.lower().split():
        word.strip()
        word = word.replace(".","")
        word = word.replace(",","")
        word = word.replace(":","")
        word = word.replace("'","")
        word = word.replace("“","")
        word = word.replace("”","")
        word = word.replace("[","")
        word = word.replace("]","")
        word = word.replace("(","")
        word = word.replace(")","")
        word = word.replace("•","")
        word = word.replace("\"","")
        word = word.replace("!","")
        word = word.replace("?","")
        word = word.replace("â€œ","")
        word = word.replace("â€˜","")
        word = word.replace("*","")
        word = wnl.lemmatize(word)
        if word not in stopwords:
            l.append(word)
    return l