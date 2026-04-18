from flask import Flask, request, jsonify, render_template
from cs2rcon import CS2RCON
from workshopmaps import setup_workshop_db, WorkshopMap
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
rcon = CS2RCON()
setup_workshop_db(app)

rcon.connect_and_login()

@app.route("/", methods=["GET", "POST"])
def dashboard():
    all_maps = WorkshopMap.query.order_by(WorkshopMap.map_name.asc()).all()
    return render_template("dashboard.html", maps=all_maps)

@app.route("/map_manager", methods=["GET", "POST"])
def map_manager():
    return render_template("map_manager.html")

@app.route("/send_command", methods=["GET"])
def send_command():
    cmd = request.args.get("cmd")  # get ?cmd=some_command

    if rcon.sock is None:
        print("Attempting to reconnect...")
        rcon.connect_and_login()
        return jsonify({"response": "Error: Server unreachable. Attempting reconnect"})

    if not cmd:
        return jsonify({"error": "No command provided"}), 400

    try:
        response = rcon.send_rcon_command(cmd)
        return jsonify({"response": response})
    except Exception as e:
        rcon.sock = None
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

#http://IP-ADDRESS:5000/send_command?cmd=COMMANDHERE