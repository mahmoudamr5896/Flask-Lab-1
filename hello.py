from flask import Flask, redirect, render_template, request

app = Flask(__name__, template_folder='template')

# models
users = [{"id": 1, 'name': 'mahmoud', 'age': 27, 'location': 'bani suef'},
         {"id": 2, 'name': 'mina', 'age': 30, 'location': 'cairo'}]



#
def get_id():
    if users:
        latest_user = users[-1]['id']
        return latest_user
    return 1


@app.route("/")
def hello_world():
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
        users.append({'id': get_id() + 1, 'name': name, 'age': age, 'location': location})
    return render_template('users.html', users=users)



@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = None
    for u in users:
        if u['id'] == id:
            user = u
            break

    if user is None:
        return 'User not found', 404
    
    if request.method == 'POST':
        user['name'] = request.form.get('name')
        user['location'] = request.form.get('location')
        user['age'] = request.form.get('age')
        return redirect('/users')
    
    return render_template('edit_user.html', user=user)


@app.route('/delete_user/<int:id>')
def delete_user(id):
    if id is not None and len(users) != 0:
        for i in range(len(users)):
            if users[i]['id'] == id:
                del users[i]
                print("Found and Delete")
                break
    return redirect('/users')


@app.route('/users_list')
def user_list():
    return render_template('users.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)







# @app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
# def edit_user(id):
#     user = next((u for u in users if u['id'] == id), None)
#     if user is None:
#         return 'User not found', 404
    
#     if request.method == 'POST':
#         user['name'] = request.form.get('name')
#         user['location'] = request.form.get('location')
#         user['age'] = request.form.get('age')
#         return redirect('/users')
    
#     return render_template('edit_user.html', user=user)
