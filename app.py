from flask import Flask, jsonify, request

app = Flask(__name__)


class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


events = []


@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    new_id = max((e.id for e in events), default=0) + 1
    event = Event(new_id, data["title"])
    events.append(event)
    return jsonify(event.to_dict()), 201


@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = next((e for e in events if e.id == event_id), None)
    if event is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    event.title = data["title"]
    return jsonify(event.to_dict()), 200


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = next((e for e in events if e.id == event_id), None)
    if event is None:
        return jsonify({"error": "Not found"}), 404
    events.remove(event)
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
