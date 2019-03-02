# Parallel File Indexer

- [Overview](#overview)
- [Algorithm](#algorithm)
- [System Requirements](#system-requirements)
- [Setup and Testing Guide](#setup-and-testing-guide)
- [How To](#how-to)
- [Functionalities and Endpoints](#functionalities-and-endpoints)
- [Future Scope](#future-scope)
- [License](#license)

# Overview
`file_indexer` is a Python package containing tools to index 1000's of files in parallel and keep track of the word statistics, especially their occurrences within a file and across files. It has been designed as a lightweight Flask API, which can be accessed via a normal web browser or a tool like [Postman](https://www.getpostman.com/), but to avoid all this hassle, this package also has a script called `interact_with_api.py`, which wraps and automates all the API calls and provides an interactive CLI tool for this.

# Algorithm
- This algorithm is inspired from a map/reduce or divide-and-conquer based approach. (Note: this algorithm assumes that the contents of the files it is indexing are static and are not updated dynamically, more on this in the [Future Scope](#future-scope). So, it follows a pre-indexed search based approach.)
- **Indexing algorithm:** (at a single text file level)
  - Read all the file's contents
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

- **Merging algorithm:** (merges across file `words_index`s)
  - Merges a list of word indices into a single `master_words_index`.
  - If the file is already present in the index, then the old file statistics are replaced with the new statistics
    - This assumes that the `words_indices` are chronologically ordered, with the latest `words_index` at the end of the list.

- **Parallel indexing algorithm:** (Across all text files, with the input master text file)
  - Maps each text file in the master text file, to the **indexing algorithm** described above, in parallel, to multiple logical threads, using the `multiprocessing` library.
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
`file_indexer` mainly depends on the following Python packages. It runs on Python 3.6.

```
nltk
Flask
requests
pytest
pytest-cov
```

# Setup and Testing Guide:

Assuming that the system just has the base OS installed, follow the below instructions to setup and run the Flask API Server (`app.py`) and interface script `interact_with_api.py`

## Setup
- Install Python 3.6 from either the [Hitchhiker's Guide to Python](https://docs.python-guide.org/starting/installation/) or [Real Python](https://realpython.com/installing-python/). It has guides for macOS, Linux, and Windows as well.
- Install pip:
  - Follow instructions [here](https://pip.pypa.io/en/stable/installing/)
  - OR Just download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) and run `python3 get-pip.py`.
- Install Python dependencies:
  - Run the following commands (from package root):

        pip3 install -r requirements.txt
        python3 -m nltk.downloader punkt
  - OR just run `source setup.sh` on macOS or Linux.

## Unit tests and Coverage
In order to run the unit tests and report coverage, from the package root, run the following command:

    py.test -s --cov=file_indexer .

# How To
### Run the Flask API Server
From a new terminal window, go the package root and run the following command:

    python3 app.py

This will be where we can see the live API server logs.

### Interact with the Flask API
The endpoints are pretty straight forward to use, (refer to [Functionalities and Endpoints](#functionalities-and-endpoints)), however `interact_with_api.py` is a script that wraps all the API calls for you. To use it, run:

    python3 interact_with_api.py

### Test Data
When prompted for test data (master file path), use either of the following:
- `input.txt`
  - This is the Reuters corpus and has 10,788 news documents with 1.3 million words.
- `file_indexer/unit_tests/data/index.txt`
  - This is some dummy data that I created to tractably verify if the algorithm works.

# Functionalities and Endpoints
The following functionalities are supported by the app:
- Index new files (`/file-indexer/api/v1/index/<path:path_to_master_file>`)
  - This accepts a master file path, that has the absolute paths of all the files to be indexed and creates an in-memory index which can be queried later.
  - Note: will merge with already indexed files using the **merging algorithm**, if we do not clear the index before indexing new files.
- Display word counts (`/file-indexer/api/v1/word-counts`)
  - This just lists all the words in the index sorted alphabetically along with their frequency counts.
- Search for a word (`/file-indexer/api/v1/search/<word>`)
  - Once the index is created, this helps to search for a specific `word` in the index and display all the files it occurs in, along with the file-wise and across files frequencies.
- List all words (`/file-indexer/api/v1/words`)
  - This just lists all the words in the index.
- Clear words index  (`/file-indexer/api/v1/clear-index`)
  - This is used to clear the in-memory index of all words to start fresh.
- Download words index as JSON (`/file-indexer/api/v1/download-index`)
  - This is used to download the master index from in-memory and dump it into a JSON file for later use.

# Future Scope
- Support and track dynamic files by engineering a solution based off of the [Knuth–Morris–Pratt algorithm](https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm).
- Dockerize the app. Intially the app was Dockerized, but then I removed it when I realized that, it had to deal with absolute paths from the host machine, which makes it a hassle.
- Now the algorithm is case sensitive and supports only `latin_1` encoded files. Can support more variants.
- Use already present docstrings to generate Sphinx documentation on RTD.
- Use **Twokenize** to chop words, etc.

# License

This project is covered under the **Apache 2.0 License**.
