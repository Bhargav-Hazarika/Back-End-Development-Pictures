from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

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
    # print(len(data))
    if data:
        return jsonify(data), 200
    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    url = None
    for item in data:
        if item['id'] == id:
            url = item
            break
    if url:
        return jsonify(item), 200
    else:
        # Return a 404 error if the ID is not found
        # abort(404, description="Picture not found")
        return {'message': "Picture not found"}, 404
    return {"message": "Internal server error"}, 500


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    # Extract picture data from the request body
    picture = request.get_json()

    check = True
    for item in data:
        if item['id'] == picture['id']:
            check = False  # Picture already exists
    # Append the new picture to the data list
    if check:
        data.append(picture)

    # Call the create_picture function
    if check:
        return jsonify(picture), 201
    else:
        # Return HTTP 302 if the picture already exists
        return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # Extract picture data from the request body
    new_picture_data = request.get_json()


    # Call the update_picture function
    updated_picture = None
    for item in data:
        if item['id'] == id:
            item.update(new_picture_data)
            updated_picture = item
            # break
    # updated_picture = update_picture(id, new_picture_data)
    print(updated_picture)

    if updated_picture:
        return jsonify(updated_picture), 200
    else:
        # Return HTTP 404 if the picture is not found
        return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    del_pic = False
    for index, item in enumerate(data):
        if item['id'] == id:
            del data[index]  # Delete the picture from the list
            del_pic = True
            break

    if del_pic:
        return '', 204  # HTTP 204 No Content
    else:
        # Return HTTP 404 if the picture is not found
        return jsonify({"message": "picture not found"}), 404
