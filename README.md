# file_indexer

- Pre-indexed search vs dynamic search in varying files
- Assume, macOS and Linux
- Docker
- Tokenizer (NLTK word_tokenize on the other hand is based on a TreebankWordTokenizer, see the docs here. It basically tokenizes text like in the Penn Treebank.), we can also use punkt, eliminate stop words, twokenize, etc
- Reuters Corpus contains 10,788 news documents totaling 1.3 million words (will help with unit tests as well)
- Parallel indexing (3 times faster than serial and 2-3 times faster than unified) - based on divide and conquer mechanism - scales really well, 15 secs to 5 secs, left them commented to show how it works
- It is case sensitive and supports 'latin_1' encoding only, it can easily be extended to support these features as well.
- dump to json
- py.test -s --cov=file_indexer .
- copy readme from mgcpy
- I am assuming the files are static and not dynamically written in real time
- will merge old and new index
- talk about bonus question
- assumes the path is relative to app's path

# License

This project is covered under the **Apache 2.0 License**.
