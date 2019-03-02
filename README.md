# Parallel File Indexer

- Pre-indexed search vs dynamic search in varying files
- Assume, macOS and Linux
- Docker
- Tokenizer (NLTK word_tokenize on the other hand is based on a TreebankWordTokenizer, see the docs here. It basically tokenizes text like in the Penn Treebank.), we can also use punkt, eliminate stop words, twokenize, etc
- Reuters Corpus contains 10,788 news documents totaling 1.3 million words (will help with unit tests as well)
- Parallel indexing (3 times faster than serial and 2-3 times faster than unified) - based on divide and conquer mechanism - scales really well, 15 secs to 5 secs, left them commented to show how it works
- It is case sensitive and supports 'latin_1' encoding only, it can easily be extended to support these features as well.
- dump to json
- copy readme from mgcpy
- I am assuming the files are static and not dynamically written in real time
- will merge old and new index, already present files are replaced with new stats
- talk about bonus question
- assumes the path is relative to app's path
-  instruction to interact_with_api (install urllib)
- point to large and small data
- clear words and download words

- Install python 3.6 https://docs.python-guide.org/starting/installation/ or https://realpython.com/installing-python/
- Install pip: https://pip.pypa.io/en/stable/installing/
- Then, pip3 install -r requirements.txt, python3 -m nltk.downloader punkt or setup.sh
- py.test -s --cov=file_indexer .
- Then run app, python3 app.py
- Then run interact_with_api, python3 interact_with_api.py

- talk bout why you removed docker
- future scope

# License

This project is covered under the **Apache 2.0 License**.
