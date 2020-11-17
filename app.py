from flask import Flask, make_response, jsonify, request
import json

app = Flask(__name__)


@app.route('/todo/<id>', methods=["GET"])
@app.route('/todo/', methods=["POST"])
def todo(id=None):
    with open("todos.json") as f:
        todos = json.load(f)
    if request.method == "GET":
        if len(todos) <= int(id):
            id = len(todos)-1
        print(id)
        data = todos[int(id)]
        res = make_response(jsonify(data))
        res.mimetype = 'application/json'
        return res
    elif request.method == "POST":
        payload = request.get_json()
        todos.append({"title": payload.get("title", None), "userId": payload.get("userId", None), "completed": payload.get("completed", None)})
        data = {"title": payload.get("title", None), "userId": payload.get("userId", None),
                "completed": payload.get("completed", None)}
        return jsonify(data), 200
    with open("todos.json", "w") as f:
        json.dump(todos, f, indent=4)



if __name__ == '__main__':
    app.run()
