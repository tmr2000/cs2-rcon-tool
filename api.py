from flask import Flask, request, jsonify, render_template
from cs2rcon import CS2RCON  

app = Flask(__name__)
rcon = CS2RCON()
if not rcon.connect_and_login():
    print("Failed to connect to server")
    exit(1)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_command", methods=["GET"])
def send_command():
    cmd = request.args.get("cmd")  # get ?cmd=some_command
    if not cmd:
        return jsonify({"error": "No command provided"}), 400

    try:
        response = rcon.send_rcon_command(cmd)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

#http://IP-ADDRESS:5000/send_command?cmd=COMMANDHERE