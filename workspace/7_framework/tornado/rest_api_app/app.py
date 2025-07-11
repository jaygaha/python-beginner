import tornado.ioloop
import tornado.web
import json

# Sample in-memory data
items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
    {"id": 3, "name": "Item 3"}
]

class ItemListHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")

    def get(self):
        self.write(json.dumps(items))

    def post(self):
        try:
            data = json.loads(self.request.body)
            new_item = {
                "id": items[-1]["id"] + 1 if items else 1,
                "name": data["name"]
            }
            items.append(new_item)
            self.set_status(201)
            self.write(json.dumps(new_item))
        except Exception as e:
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))

class ItemHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")

    def get(self, item_id):
        item = next((item for item in items if item["id"] == int(item_id)), None)
        if item:
            self.write(json.dumps(item))
        else:
            self.set_status(404)
            self.write(json.dumps({"error": "Item not found"}))

    def put(self, item_id):
        try:
            item = next((item for item in items if item["id"] == int(item_id)), None)
            if not item:
                self.set_status(404)
                self.write(json.dumps({"error": "Item not found"}))
                return

            data = json.loads(self.request.body)
            item["name"] = data["name"]
            self.write(json.dumps(item))
        except Exception as e:
            self.set_status(400)
            self.write(json.dumps({"error": str(e)}))

    def delete(self, item_id):
        global items
        items = [item for item in items if item["id"] != int(item_id)]
        self.set_status(204)

def make_app():
    return tornado.web.Application([
        (r"/items", ItemListHandler),
        (r"/items/([0-9]+)", ItemHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8880)
    print("REST API server running at http://localhost:8880")
    tornado.ioloop.IOLoop.current().start()
