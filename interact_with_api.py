import os
import json
import sys

import requests


def get_option():
    print("\nChoose one of these options:")
    print("1. Index new files (Note: will merge with already indexed files)")
    print("2. Display word counts")
    print("3. Search for a word")
    print("4. List all words")
    print("5. Clear words index")
    print("6. Download words index as JSON")
    print("7. Exit")

    return input()


if __name__ == '__main__':
    try:
        base_api = requests.get("http://localhost:8080")
    except Exception:
        print("Please run the flask app with 'python app.py' or run the dockerized version as in readme.md, then run this file.")
        sys.exit(1)

    while True:
        option = get_option()
        while option not in set([str(i) for i in range(1, 8)]):
            print("\nPlease pick one from 1 to 7.")
            option = get_option()

        if option == "1":
            print("\nEnter master file path:")
            file_path = input()
            while not os.path.exists(file_path):
                print("\nPlease enter a valid master file path:")
                file_path = input()

            is_path_absolute = int(os.path.isabs(file_path))
            if is_path_absolute:
                file_path = file_path[1:]

            response = requests.get("http://localhost:8080/file-indexer/api/v1/index/" + file_path + "?is_absolute=" + str(is_path_absolute))
            if response.status_code == 200:
                print(response.json()["message"])
            else:
                print(response)

        elif option == "2":
            response = requests.get("http://localhost:8080/file-indexer/api/v1/word-counts/")
            json_data = response.json()

            print("\n"+json_data["message"])
            print("\nAll words indexed with counts:")
            print(json.dumps(json_data["result"], indent=4, sort_keys=True))

        elif option == "3":
            print("\nEnter word to search:")
            word = input()

            response = requests.get("http://localhost:8080/file-indexer/api/v1/search/" + word)
            json_data = response.json()

            print("\n"+json_data["message"])
            print("\nThe statistics for the word:")
            print(json.dumps(json_data["result"], indent=4, sort_keys=True))

        elif option == "4":
            response = requests.get("http://localhost:8080/file-indexer/api/v1/words/")
            json_data = response.json()

            print("\n"+json_data["message"])
            print("\nAll words indexed:")
            print(json.dumps(json_data["result"], indent=4, sort_keys=True))

        elif option == "5":
            response = requests.get("http://localhost:8080/file-indexer/api/v1/clear-index/")
            print("\n"+response.json()["message"])

        elif option == "6":
            response = requests.get("http://localhost:8080/file-indexer/api/v1/download-index/")
            json_data = response.json()

            print("\n"+json_data["message"])
            if json_data["is_success"]:
                with open("words_index.json", "w") as outfile:
                    json.dump(json_data["result"], outfile, indent=4, sort_keys=True)
                    print("Words index saved as JSON to words_index.json")
        else:
            break
