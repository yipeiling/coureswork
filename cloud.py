#from flask import jsonify
from flask import Flask, redirect, url_for, request, render_template
from flask import jsonify
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.errors import DuplicateKeyError
from OpenSSL import SSL
import os
#pip install pyopenssl
#context = SSL.Context(SSL.TLSv1_METHOD)
#context.use_privatekey_file('key.pem')
#context.use_certificate_file('cert.pem')



app = Flask(__name__)

#client = MongoClient('mongodb://localhost:27017/')
client = MongoClient('mongodb://mongo-0.mongo:27017,mongo-1.mongo:27017,mongo-2.mongo/myproject?replicaSet=rs0')

#client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'],27017)
#client = MongoClient('mongodb://mongodb:27017/')
#client =MongoClient('mongodb://mongo-0.mongo,mongo-1.mongo,mongo-2.mongo:27017')
#client =MongoClient('mongodb://mongo-0.mongo:27017')

db = client['stock']
try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
except ConnectionFailure:
    print("Server not available")

collection_stock = db['stock']

@app.route('/', methods=['GET'])
def StockList():
#    collection_stock.insert_one({"item":"stock1","level":"1"})
    i=0
    output=""
    for r in collection_stock.find():
        output=output+str(r)
        i+=1
    client.close()
    if i>0:
        return jsonify(output)
    else:
       return("The database is empty!")


@app.route('/<item>', methods=['GET'])
def StockLook(item):
    output=""
    for r in collection_stock.find({"item":item}):
        output=output+str(r)
    client.close()
    return jsonify(output)

@app.route('/<item>/<level>', methods=['GET','POST'])
def StockAdd(item,level):
    i = 0;
    for r in collection_stock.find({"item": item,"level": level}):
        i+=1
    if i>0:
        client.close()
        return ("The item already exists!")

    collection_stock.insert_one({"item":item,"level":level})
    for r in collection_stock.find({"item": item,"level": level}):
        client.close()
        return jsonify("Insert is successful!    "+str(r))

@app.route('/d/<item>/<level>', methods=['GET','DELETE'])
def StockDelete(item,level):
    i=0
    output=""
    for r in collection_stock.find({"item":item,"level":level}):
        output=output+str(r)
        i+=1
    if i>0:
        collection_stock.delete_many({"item":item,"level":level})
        output = "The item is delete!   "+output
    else:
        output = "The item is not exits!"

    client.close()
    return jsonify(output)

@app.route('/p/<item>/<level>', methods=['GET','PUT'])
def StockSet(item,level):
    i=0
    output=""
    for r in collection_stock.find({"item":item}):
        r["level"] = level
        output=output+str(r)
        i+=1
    if i>0:
        output = "The item is set!   "+output
    else:
        output = "The item is not exists!"
    client.close()
    return jsonify(output)


if __name__ == '__main__':
 #  app.run(host='0.0.0.0',debug = True,ssl_context=('cert.pem', 'key.pem'))
#    app.run(host='0.0.0.0', debug = True,ssl_context=context)
    app.run(host='0.0.0.0', debug = True,ssl_context="adhoc")
#    app.run(host='0.0.0.0', debug = True)
