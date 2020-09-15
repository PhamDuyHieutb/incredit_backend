from flask import Flask, request
from flask_pymongo import PyMongo
import jwt

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/credit"
mongo = PyMongo(app)


def decode_authen(encoded):
    decoded = jwt.decode(encoded, 'secret', algorithms=['HS256'])
    return decoded


@app.route("/search")
def get_user_infor():
    phone = request.args.get('phone')
    custormer_infor = mongo.db.cus_info.find({"phone": int(phone)})
    if custormer_infor:
        custormer_infor = list(custormer_infor)[0]
        return custormer_infor
    else:
        return {"Code": 400, "Error": 'No Information'}


@app.route("/change_pass")
def change_password():
    user_name = request.args.get('user_name')
    new_password = request.args.get('new_password')

    # check user_name in account table
    if mongo.db.account.find({"user_name": user_name}):
        mongo.db.change_pass.insert({"user_name": user_name, "new_password": new_password})
        return {"Code": 200}
    else:
        return {"Code": 400, "Error": "Invalid user_name"}


@app.route("/token", methods=['GET'])
def authen():
    user_name = request.args.get('user_name')
    password = request.args.get('password')

    check_account = mongo.db.account.find({"user_name": user_name})

    # check valid account
    if check_account and password == check_account["password"]:
        encoded = jwt.encode({user_name: password}, 'secret', algorithm='HS256')
        return {"Code": 200, "token": str(encoded)}
    else:
        return {"Code": 400, "Error": "No Permission! Wrong password!"}


if __name__ == '__main__':
    app.run()
