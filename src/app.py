"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def getAllMembers():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200

#CREATE A MEMBER
@app.route('/member', methods=['POST'])
def addNewMember():
    data = request.get_json()
    # this is how you can use the Family datastructure by calling its methods
    newMembers = jackson_family.add_member(data)  
    members = jackson_family.get_all_members()
    response = {
        "family": members
    }
    return jsonify(response), 200

# GET ONE CHARACTER
@app.route('/member/<int:id>', methods=['GET'])

def get_one_member(id):  

    if request.method == 'GET':
        oneMember= jackson_family.get_member(id)
        return jsonify(oneMember),200


# UPDATE ONE CHARACTER
@app.route('/members/<int:id>', methods=['PUT'])

def update_one_member(id):  

    body = request.get_json() 
    
    if request.method == 'PUT':
      
        oneMember = jackson_family.update_member(id,body)
        members = jackson_family.get_all_members()
        response = {
                "family": members
            }
      
        return jsonify(response), 200


# DELETE ONE CHARACTER
@app.route('/member/<int:id>', methods=['DELETE'])

def delete_one_member(id):  

    if request.method == 'DELETE':
        members_after_delete = jackson_family.delete_member(id)
       
        response = {
             "family": members_after_delete
         }
        return jsonify({"done": True}), 200
    
    return jsonify('bad request'), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
