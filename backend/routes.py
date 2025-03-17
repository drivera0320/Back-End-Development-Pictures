from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401
from http import HTTPStatus  

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    pic = next((item for item in data if item["id"] == id), None)
    if not pic:
        return {"message": "Picture not found"}, 404
    return jsonify(pic), 200


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.json

    if not picture:
        return {"message": "Invalid input parameter"}, 422
    
    try:
        id_lst = [item['id'] for item in data]
        
        if picture.get('id') in id_lst:
            return {"Message": f"picture with id {picture['id']} already present"}, 302
        else:
            data.append(picture)

    except NameError:
        return {"message": "data not defined"}, 500

    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.get_json()

    if not picture:
        return {"message": "Invalid input parameter"}, 422

    pict_id = picture['id']

    id_lst = [item['id'] for item in data]

    if pict_id in id_lst:
        for item in data:
            if item["id"] == pict_id:
                item.update(picture)
                return jsonify(picture), 200
    else:
        return {"message": "picture not found"}, 404
    

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for item in data:
        if item["id"] == id:
            data.remove(item)
            return make_response('', HTTPStatus.NO_CONTENT)

    return jsonify({"message": "picture not found"}), 404
