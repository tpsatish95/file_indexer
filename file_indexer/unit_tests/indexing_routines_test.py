import json
import time

import pytest

from file_indexer.indexing_routines import (index, merge_words_indices,
                                            parallel_indexer)


def test_index():
    expected_words_index = {'hello': {'file_wise_counts': {'test_file_1.txt': 2}, 'total_count': 2},
                            'world': {'file_wise_counts': {'test_file_1.txt': 1}, 'total_count': 1},
                            '!': {'file_wise_counts': {'test_file_1.txt': 1}, 'total_count': 1},
                            'the': {'file_wise_counts': {'test_file_1.txt': 3}, 'total_count': 3},
                            'a': {'file_wise_counts': {'test_file_1.txt': 1}, 'total_count': 1},
                            'this': {'file_wise_counts': {'test_file_1.txt': 2}, 'total_count': 2},
                            'an': {'file_wise_counts': {'test_file_1.txt': 1}, 'total_count': 1},
                            ',': {'file_wise_counts': {'test_file_1.txt': 1}, 'total_count': 1},
                            'pikachu': {'file_wise_counts': {'test_file_1.txt': 1}, 'total_count': 1},
                            "'s": {'file_wise_counts': {'test_file_1.txt': 1}, 'total_count': 1}}

    # dump to a json, so that we can easily compare the two nested python dicts,
    # normal == won't work on such dicts
    expected_words_index_json = json.dumps(expected_words_index, sort_keys=True)
    actual_words_index_json = json.dumps(index("./file_indexer/unit_tests/data/test_file_1.txt"), sort_keys=True)

    assert actual_words_index_json == expected_words_index_json, "index() function - failed!"

    print("\nindex() function - passed!")


def test_merge_words_indices():
    file1_the_count = index("./data/1")["the"]["total_count"]
    file2_the_count = index("./data/10")["the"]["total_count"]

    total_the_count = merge_words_indices([index("./data/1"), index("./data/10")])["the"]["total_count"]

    assert file1_the_count+file2_the_count == total_the_count, "merge_words_indices() function - failed!"

    print("merge_words_indices() function - passed!")


def test_parallel_indexer():
    expected_master_words_index = {'hello': {'file_wise_counts': {'test_file_1.txt': 2, 'test_file_2.txt': 2}, 'total_count': 4},
                                   'world': {'file_wise_counts': {'test_file_1.txt': 1}, 'total_count': 1},
                                   '!': {'file_wise_counts': {'test_file_1.txt': 1, 'test_file_2.txt': 1}, 'total_count': 2},
                                   'the': {'file_wise_counts': {'test_file_1.txt': 3, 'test_file_2.txt': 3}, 'total_count': 6},
                                   'a': {'file_wise_counts': {'test_file_1.txt': 1, 'test_file_2.txt': 1}, 'total_count': 2},
                                   'this': {'file_wise_counts': {'test_file_1.txt': 2, 'test_file_2.txt': 2}, 'total_count': 4},
                                   'an': {'file_wise_counts': {'test_file_1.txt': 1, 'test_file_2.txt': 1}, 'total_count': 2},
                                   ',': {'file_wise_counts': {'test_file_1.txt': 1, 'test_file_2.txt': 1}, 'total_count': 2},
                                   'pikachu': {'file_wise_counts': {'test_file_1.txt': 1, 'test_file_2.txt': 1}, 'total_count': 2},
                                   "'s": {'file_wise_counts': {'test_file_1.txt': 1, 'test_file_2.txt': 1}, 'total_count': 2},
                                   'universe': {'file_wise_counts': {'test_file_2.txt': 1}, 'total_count': 1}}

    actual_master_words_index = parallel_indexer("./file_indexer/unit_tests/data/index.txt")

    # dump to a json, so that we can easily compare the two nested python dicts,
    # normal == won't work on such dicts
    expected_master_words_index_json = json.dumps(expected_master_words_index, sort_keys=True)
    actual_master_words_index_json = json.dumps(actual_master_words_index, sort_keys=True)

    assert expected_master_words_index_json == actual_master_words_index_json, "parallel_indexer() function - failed!"

    print("parallel_indexer() function - passed!")


def test_parallel_indexer_time_taken():
    start_time = time.time()
    parallel_indexer("./input.txt")
    time_taken = time.time() - start_time

    assert time_taken < 16, "parallel_indexer() is doing worse than unified serial indexer"

    print("\nThe parallel file indexer took {} seconds to index the Reuters corpus (10,788 docs)".format(time_taken))
