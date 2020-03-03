# Collect_Store_Search
This app crawls for articles from the famous news website Theguardian.com, stores them in a [hosted MongoDB](https://www.mongodb.com/cloud/atlas), then makes it available to search via an API.

## Installation
 - Download (or clone) the repo to your computer and unzip it.
 - You should have [**Python 3**](https://www.python.org/downloads/) installed in your computer.

#### Use the package manager [pip](https://pip.pypa.io/en/stable/) to install these required packages :

 - [PyMongo](https://api.mongodb.com/python/current/)  
```bash
pip install pymongo
```
 - [DNS PYTHON](http://www.dnspython.org/)  
```bash
pip install dnspython
```
 - [Natural Language Toolkit](https://www.nltk.org/)  
```bash
pip install nltk
```
#### To install the required NLTK data, run your Python interpreter and type the commands :
```python
>>> import nltk
>>> nltk.download('wordnet')
```

## Usage
- Run your terminal.
- Navigate (change directory) to the *Collect_Store_Search\postscrape\postscrape* folder.
- Type the command :
```bash
python search_API.py
```
- Type what you want to search for.
- A *"search_results.txt"* file should appears in the *Collect_Store_Search\postscrape\postscrape* folder, it contains your search results.

