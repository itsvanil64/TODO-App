from flask import Flask, render_template, request, jsonify
import uuid

app = Flask(__name__)

# In-memory task storage
tasks = {}


def make_task(title):
    task_id = str(uuid.uuid4())
    return {
        "id": task_id,
        "title": title.strip(),
        "completed": False,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(list(tasks.values()))


@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    title = (data or {}).get("title", "").strip()
    if not title:
        return jsonify({"error": "Title is required"}), 400
    task = make_task(title)
    tasks[task["id"]] = task
    return jsonify(task), 201


@app.route("/api/tasks/<task_id>", methods=["PATCH"])
def toggle_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    task["completed"] = not task["completed"]
    return jsonify(task)


@app.route("/api/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = tasks.pop(task_id, None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"deleted": task_id})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
