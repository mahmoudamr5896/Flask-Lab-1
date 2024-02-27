from bson import ObjectId
from flask import Flask, redirect, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__, template_folder='template')
app.config["MONGO_URI"]="mongodb://127.0.0.1:27017/flask"
mongo=PyMongo(app)
# users=list(mongo.db.Users.find({}))


# def get_id():
#     if users:
#         latest_user = users[-1]['id']
#         return latest_user
#     return 1

@app.route("/")
def hello_world():
    data = list(mongo.db.Users.find({}))
    print(data)
    return render_template('index.html')

@app.route('/createuser')
def createuser():
    return render_template('createuser.html')

@app.route('/users', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        location = request.form.get('location')
        if name and age and location: 
            mongo.db.Users.insert_one({'name': name, 'age': age, 'location': location})
    data = list(mongo.db.Users.find({}))  
    return render_template('users.html', users=data) 

@app.route('/users_list')
def user_list():
    data = list(mongo.db.Users.find({}))
    return render_template('users.html', users=data)

# @app.route('/edit_user/<string:_id>', methods=['GET', 'POST'])
# def edit_user(_id):
#     user = mongo.db.Users.find_one({'_id': _id})
#     if request.method == 'POST':
#         user['name'] = request.form.get('name')
#         user['location'] = request.form.get('location')
#         user['age'] = request.form.get('age')
#         mongo.db.Users.update_one({'_id': _id}, {'$set': user})
#     return render_template('edit_user.html', user=user)
@app.route('/edit_user/<string:_id>', methods=['GET', 'POST'])
def edit_user(_id):
    user = mongo.db.Users.find_one({'_id':ObjectId(_id) })
    if request.method == 'POST':
        user['name'] = request.form.get('name')
        user['location'] = request.form.get('location')
        user['age'] = request.form.get('age')
        mongo.db.Users.update_one({'_id': ObjectId(_id)}, {'$set': user})
        return redirect('/users_list')
    return render_template('edit_user.html', user=user)



@app.route('/delete_user/<string:_id>')
def delete_user(_id):
    mongo.db.Users.delete_one({'_id': ObjectId(_id)})
    return redirect('/users')

if __name__ == '__main__':
    app.run(debug=True)

