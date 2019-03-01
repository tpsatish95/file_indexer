import multiprocessing as mp
import ntpath
import os
import time
from collections import defaultdict

import nltk


def words_index_entry():
    return {"file_wise_counts": defaultdict(int), "total_count": 0}


def index(text_file_path):
    '''
    Reads and parses the contents of the file at text_file_path and produces an index dictionary, like below:

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

    :param text_file_path: path to the file to be parsed and indexed
    :type text_file_path: str

    :return: words_index dict as described above
    :rtype: dict
    '''
    file_name = ntpath.basename(text_file_path)
    words_index = defaultdict(words_index_entry)

    with open(text_file_path, "r", encoding="latin_1") as file_obj:
        file_content = file_obj.read()

        # tokenize the file's contents based on Penn Treebank's TreebankWordTokenizer
        tokens = nltk.word_tokenize(file_content)

        for token in tokens:
            words_index[token]["file_wise_counts"][file_name] += 1
            words_index[token]["total_count"] += 1

    return words_index


def merge_words_indices(words_indices):
    '''
    Merges a list of word indices into a single master_words_index at a file level for each word

    :param words_indices: list of word indices
    :type words_indices: list

    :return: master_words_index dictionary
    :rtype: dict
    '''
    master_words_index = defaultdict(words_index_entry)

    for words_index in words_indices:
        for word in words_index:
            master_words_index[word]["file_wise_counts"].update(words_index[word]["file_wise_counts"])
            master_words_index[word]["total_count"] += words_index[word]["total_count"]

    return master_words_index


def unified_indexer(master_file_path):
    '''
    Indexes all files present in the master_file_path text file, serially (NO divide and conquer)

    :param master_file_path: path to the master file to get the list of files to processed
    :type master_file_path: str

    :return: master_words_index dictionary
    :rtype: dict
    '''
    master_words_index = defaultdict(words_index_entry)

    with open(master_file_path, "r") as file_obj:
        for text_file_path in file_obj.readlines():
            file_name = ntpath.basename(text_file_path.strip())
            with open(text_file_path.strip(), "r", encoding="latin_1") as file_obj:
                file_content = file_obj.read()

                # tokenize the file's contents based on Penn Treebank's TreebankWordTokenizer
                tokens = nltk.word_tokenize(file_content)

                for token in tokens:
                    master_words_index[token]["file_wise_counts"][file_name] += 1
                    master_words_index[token]["total_count"] += 1

    return master_words_index


def serial_indexer(master_file_path):
    '''
    Indexes all files present in the master_file_path text file, serially (divide and conquer)

    :param master_file_path: path to the master file to get the list of files to processed
    :type master_file_path: str

    :return: master_words_index dictionary
    :rtype: dict
    '''
    with open(master_file_path, "r") as file_obj:
        text_file_paths = [text_file_path.strip() for text_file_path in file_obj.readlines()]

    return merge_words_indices([index(text_file_path) for text_file_path in text_file_paths])


def parallel_indexer(master_file_path):
    '''
    Indexes all files present in the master_file_path text file, parallely (divide and conquer)

    :param master_file_path: path to the master file to get the list of files to processed
    :type master_file_path: str

    :return: master_words_index dictionary
    :rtype: dict
    '''
    with open(master_file_path, "r") as file_obj:
        text_file_paths = [text_file_path.strip() for text_file_path in file_obj.readlines()]

    with mp.Pool(mp.cpu_count()-1) as p:
        words_indices = p.map(index, text_file_paths)

    return merge_words_indices(words_indices)


if __name__ == '__main__':
    # start_time = time.time()
    # print(unified_indexer("./input.txt")["the"])
    # print('Unified indexer took {} seconds'.format((time.time() - start_time)))
    #
    # start_time = time.time()
    # print(serial_indexer("./input.txt")["the"])
    # print('Serial indexer took {} seconds'.format((time.time() - start_time)))

    start_time = time.time()
    print(parallel_indexer("./input.txt")["the"])
    print('Parallel indexer took {} seconds'.format((time.time() - start_time)))

    # # generate input file
    # open("input.txt", "w").writelines(["./data/"+i+"\n" for i in os.listdir("./data/")])

    # # test
    # print(index("./data/1")["the"])
    # print(index("./data/10")["the"])
    # print(merge_words_indices([index("./data/1"), index("./data/10")])["the"])
