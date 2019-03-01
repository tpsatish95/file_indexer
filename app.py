'''
Flask APP that parses the incoming booking requests and
Uses the select_partner module to get the optimal list of partners
That can service the list of input theatre locations.
'''

import json
import logging
import uuid
from time import time

from flask import Flask, abort, jsonify, request

from file_indexer.indexing_routines import (merge_words_indices,
                                            parallel_indexer)

APP = Flask(__name__, static_url_path='')
APP.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
APP.url_map.strict_slashes = False

MASTER_WORDS_INDEX = None


@APP.route('/')
def root():
    return jsonify("The File Indexer API is up and running!")


@APP.route('/file-indexer/api/v1/index/<path:path_to_master_file>')
def index_files(path_to_master_file):
    global MASTER_WORDS_INDEX

    if request.args.get('is_absolute', "0") == "1":
        path_to_master_file = "/" + path_to_master_file

    requestUUID = uuid.uuid4()
    logging.info("Processing request id:", str(requestUUID))
    logging.info("Request from ip: " + str(request.remote_addr) + ", url: " + str(request.url))

    try:
        logging.info("Indexing the files in " + str(path_to_master_file) + "...")

        start = time()
        if MASTER_WORDS_INDEX:
            MASTER_WORDS_INDEX = merge_words_indices([MASTER_WORDS_INDEX, parallel_indexer(path_to_master_file)])
        else:
            MASTER_WORDS_INDEX = parallel_indexer(path_to_master_file)
        stop = time()

        logging.info("File indexing completed in " + str(stop - start) + "seconds.")

    except Exception as e:
        logging.error("The indexing algorithm failed. " + json.dumps({"error": str(e)}))
        abort(500, {"is_success": False, "message": "Internal server error. See server logs for more details."})

    return jsonify({"is_success": True, "message": "File indexing completed in " + str(stop - start) + "seconds."})


@APP.route('/file-indexer/api/v1/search/<word>')
def search_files(word):
    global MASTER_WORDS_INDEX

    requestUUID = uuid.uuid4()
    logging.info("Processing request id:", str(requestUUID))
    logging.info("Request from ip: " + str(request.remote_addr) + ", url: " + str(request.url))

    if MASTER_WORDS_INDEX:
        if word in MASTER_WORDS_INDEX:
            return jsonify({"is_success": True, "message": "Successfully retrived!", "result": MASTER_WORDS_INDEX[word]})
        else:
            return jsonify({"is_success": True, "message": "Word not found in any file!", "result": None})
    else:
        return jsonify({"is_success": False, "message": "No files indexed yet. Call /file-indexer/api/v1/index/ first.", "result": None})


@APP.route('/file-indexer/api/v1/words')
def list_words_in_index():
    global MASTER_WORDS_INDEX

    requestUUID = uuid.uuid4()
    logging.info("Processing request id:", str(requestUUID))
    logging.info("Request from ip: " + str(request.remote_addr) + ", url: " + str(request.url))

    if MASTER_WORDS_INDEX:
        return jsonify({"is_success": True, "message": "Successfully retrived!", "result": list(MASTER_WORDS_INDEX.keys())})
    else:
        return jsonify({"is_success": False, "message": "No files indexed yet. Call /file-indexer/api/v1/index/ first.", "result": None})


if __name__ == '__main__':
    APP.run(
        host='0.0.0.0',
        debug=True,
        port=8080
    )
