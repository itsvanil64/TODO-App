from flask import Flask, render_template, request, jsonify
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

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
    logging.info("Home page accessed")
    return render_template("index.html")


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    logging.info("Fetching all tasks")
    return jsonify(list(tasks.values()))


@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    title = (data or {}).get("title", "").strip()

    if not title:
        logging.warning("Attempt to add empty task")
        return jsonify({"error": "Title is required"}), 400

    task = make_task(title)
    tasks[task["id"]] = task

    logging.info(f"Task added: {task['title']}")
    return jsonify(task), 201


@app.route("/api/tasks/<task_id>", methods=["PATCH"])
def toggle_task(task_id):
    task = tasks.get(task_id)

    if not task:
        logging.warning(f"Task not found: {task_id}")
        return jsonify({"error": "Task not found"}), 404

    task["completed"] = not task["completed"]
    logging.info(f"Task toggled: {task['title']} -> {task['completed']}")
    return jsonify(task)


@app.route("/api/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = tasks.pop(task_id, None)

    if not task:
        logging.warning(f"Delete failed, task not found: {task_id}")
        return jsonify({"error": "Task not found"}), 404

    logging.info(f"Task deleted: {task['title']}")
    return jsonify({"deleted": task_id})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)