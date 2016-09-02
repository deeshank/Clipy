from flask import request, redirect, jsonify
from base64 import b64decode
from services import *
import logging
from app import app

logger = logging.getLogger('clipy')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)

logger.addHandler(ch)


@app.route('/')
def start():
    name = None
    while True:
        name = generate_uname()
        if not find_uid(name):
            break
        logger.debug('[' + name + '] used already')
    logger.info('Created new UID [' + name + ']')
    return redirect('/' + name)


@app.route('/<uid>')
def create_session(uid):
    logger.info('New session opened for [' + uid + ']')
    return app.send_static_file("wall.html")


#
# @app.route('/test/<data>')
# def test(data):
#     print data
#     list = [
#         {'param': 'foo', 'val': 2},
#         {'param': 'bar', 'val': 10}
#     ]
#     # return jsonify(results=list)
#     return data


@app.route('/get/<uid>')
def getPost(uid):
    logger.info('Request for get [' + uid + ']')
    record = find_uid(uid)
    if record:
        print record
        return jsonify(data=record['data'], status='OK')
    else:
        return jsonify(status='ERR')


@app.route('/paste', methods=['POST'])
def updatePost():
    data = cleanup(request.json)
    logger.debug('Received JSON => ' + str(data))
    data['uid'] = data['uid'].strip().split('/')[-1]
    uid = data['uid']
    logger.info('Update request for [' + data['uid'] + ']')

    if find_uid(uid):
        logger.info('[' + uid + '] already found')
        update_uid(uid, data['data'])
        logger.info("Update data for [" + uid + "]")
    else:
        insert_uid(data)
        logger.info("[" + uid + "] not found in DB")
        logger.info("Inserted data for [" + uid + "]")

    # data = request.get("data")
    # data = b64decode(data)
    # with open('abc.png') as f:
    #     f.write(data)
    return jsonify(status='OK')


def find_uid(uid):
    return app.config["IDS"].find_one({'uid': uid})


def update_uid(uid, data):
    return app.config["IDS"].update_one({'uid': uid}, {'$set': {'data': data}, "$currentDate": {"lastModified": True}})


def insert_uid(data):
    return app.config["IDS"].insert_one(data)


if __name__ == '__main__':
    app.run()
