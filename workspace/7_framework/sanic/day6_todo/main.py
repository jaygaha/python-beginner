from app import app

if __name__ == "__main__":
    app.run(host="localhost", port=8880, debug=True, single_process=True)
