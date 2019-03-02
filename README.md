# Parallel File Indexer

- [Overview](#overview)
- [Algorithm](#algorithm)
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
- [Future Scope](#future-scope)
- [License](#license)

# Overview
`file_indexer` is a Python package containing tools to index 1000's of files in parallel and keep track of the word statistics, especially their occurrences within a file and across files. It has been designed as a lightweight Flask API, which can be accessed via a normal web browser or a tool like [Postman](https://www.getpostman.com/), but to avoid all this hassle, this package also has a script called `interact_with_api.py`, which wraps and automates all the API calls and provides an interactive CLI tool for this.

# Algorithm
- This algorithm is inspired from a map/reduce or divide-and-conquer based approach. (Note: this algorithm assumes that the contents of the files it is indexing are static and are not updated dynamically, more on this in the [Future Scope](#future-scope). So, it follows a pre-indexed search based approach.)
- **Indexing algorithm:** (at a single text file level)
  - Read all the files contents
  - Tokenize the obtained text to obtain individual words, using *Penn Treebank Tokenizer* from NLTK, which is implemented as the *word_tokenize()* method. (Note: We can also use domain specific Tokenizers like [Twokenize](http://www.cs.cmu.edu/~ark/TweetNLP/) from CMU, but for now I have left it to be generic).
  - Iterate through each word and build a `words_index`, that looks like below:

        words_index = {
              "word1": {
                  "file_wise_counts": {
                      "file_name_1": <int, count1>,
                      "file_name_2": <int, count2>,
                      "file_name_3": <int, count3>,
                      ...
                  },
                  "total_count": <int, total>
              },
              ...
        }

- **Merging algorithm:** (merges across file `words_indices`)
  - Merges a list of word indices into a single `master_words_index`.
  - If the file is already present in the index, then the old file statistics are replaced with the new statistics
    - This assumes that the `words_indices` are chronologically ordered, with the latest `words_index` at the end of the list.

- **Parallel indexing algorithm:** (Across all text files, with the input master text file)
  - Maps each text file in the master text file, to the **indexing algorithm** described above in parallel to multiple logical threads, using the `multiprocessing` library.
  - Merge the `words_index` from the different threads to form the `master_words_index` using the **merging algorithm** described above.
  - **Note:** Apart from `parallel_indexer()`, the `indexing_routines` module also has, `unified_indexer()` and `serial_indexer()`, which can be used when the input data is less than 100s of files, because the parallel processing overhead takes over for less data. For this case, I have assumed the data will be in 1000s and defaulted to `parallel_indexer()`.

- **Data:**
  - In order to match the scale the algorithm was designed for, I used the [Reuters Corpus](https://www.nltk.org/book/ch02.html), from the NLTK library. It has 10,788 news documents in total, with 1.3 million words.
  - The benchmark results:
    - `serial_indexer()`: 15 secs
    - `unified_indexer()`: 12 secs
    - `parallel_indexer()`: 5 secs (2-3 times faster)
  - This algorithm was designed to scaleup really well, with more data coming in and with more processor cores available.

# System Requirements
## Hardware requirements
`file_indexer` package requires only a standard computer with enough cpu cores and RAM to support the in-memory operations. More the cpu cores, much faster the algorithm will be.

## Software requirements
### OS Requirements
This package has been tested on the following systems:
- macOS: Mojave (10.14.1)
- Linux: Ubuntu 16.04

It is untested but should work on Windows too.

### Python Dependencies
`file_indexer` mainly depends on the following Python packages.

```
nltk
Flask
requests
pytest
pytest-cov
```

# Installation Guide:

- Install python 3.6 https://docs.python-guide.org/starting/installation/ or https://realpython.com/installing-python/
- Install pip: https://pip.pypa.io/en/stable/installing/
- Then, pip3 install -r requirements.txt, python3 -m nltk.downloader punkt or setup.sh


- py.test -s --cov=file_indexer .
- unit tests

How to use the code:
- Then run app, python3 app.py
- Then run interact_with_api, python3 interact_with_api.py

- API and CLI that interacts with the API
- list all endpoints and uses
- dump to json
- clear words and download words
- talk about bonus question
- instruction to interact_with_api
- point to large and small data

# Future Scope
- future scope
- dynamic search in varying files (I am assuming the files are static and not dynamically written in real time)
- Docker (talk bout why you removed docker)
- It is case sensitive and supports 'latin_1' encoding only, it can easily be extended to support these features as well.

# License

This project is covered under the **Apache 2.0 License**.
