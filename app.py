from flask import Flask, request, jsonify, render_template, send_from_directory
from cs2rcon import CS2RCON
from workshopmaps import setup_workshop_db, WorkshopMap, db
import logging
import requests
import os
from dotenv import load_dotenv

load_dotenv()
STEAM_WEB_API_KEY = os.getenv("STEAM_WEB_API_KEY")
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
WORKSHOP_MAP_IMAGES_FOLDER = 'data/workshop_images'

app = Flask(__name__)
rcon = CS2RCON()
setup_workshop_db(app)
rcon.connect_and_login()

if not os.path.exists(WORKSHOP_MAP_IMAGES_FOLDER):
    os.makedirs(WORKSHOP_MAP_IMAGES_FOLDER)

@app.route("/", methods=["GET", "POST"])
def dashboard():
    all_maps = WorkshopMap.query.order_by(WorkshopMap.map_name.asc()).all()
    return render_template("dashboard.html", maps=all_maps)

@app.route("/map_manager", methods=["GET", "POST"])
def map_manager():
    return render_template("map_manager.html")

@app.route('/workshop_images/<filename>')
def serve_workshop_image(filename):
    return send_from_directory(WORKSHOP_MAP_IMAGES_FOLDER, filename)

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

@app.route("/add_workshop_map", methods=["POST"])
def add_workshop():
    data = request.json
    ws_id = data.get("workshop_id")
    steam_url = f"https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/?key={STEAM_WEB_API_KEY}"
    
    existing_map = WorkshopMap.query.filter_by(map_alias=ws_id).first()
    if existing_map:
        return jsonify({
            "success": False, 
            "error": f"The map '{existing_map.map_name}' is already in your database!"
        }), 400


    # Valve expects the data in a specific format
    post_data = {
        'itemcount': 1,
        'publishedfileids[0]': ws_id
    }

    try:
        response = requests.post(steam_url, data=post_data)
        response.raise_for_status() # Check for internet/API errors
        details = response.json().get('response', {}).get('publishedfiledetails', [{}])[0]
        raw_tags = details.get('tags', [])
        tags = [t.get('tag').lower() for t in raw_tags]

        if 'cs2' not in tags:
            return jsonify({
                "success": False, 
                "error": "Invalid Workshop ID. Please ensure this is a CS2 Workshop Map."
            }), 400

        #real_name = details.get('title', f"Workshop ({ws_id})")
        steam_title = details.get('title', 'Unknown Map')
        real_name = f"{steam_title}"
        preview_url = details.get('preview_url', "")


        filename = f"{ws_id}.jpg"
        local_path = os.path.join(WORKSHOP_MAP_IMAGES_FOLDER, filename)
        db_path = "img/map_images/official/default.png"

        if preview_url:
            try:
                img_data = requests.get(preview_url).content
                with open(local_path, 'wb') as handler:
                    handler.write(img_data)
                db_path = f"/workshop_images/{filename}"
            except Exception as e:
                print(f"Failed to download image: {e}")

        try:
            new_map = WorkshopMap(
                map_name=real_name,
                map_alias=ws_id,
                is_officialmap=False,
                image_url=db_path,
                is_wingman     = 'wingman' in tags,
                is_deathmatch  = 'deathmatch' in tags,
                is_armsrace    = 'armsrace' in tags or 'arms race' in tags,
                is_competitive = 'competitive' in tags or 'classic' in tags,
                is_casual      = 'casual' in tags or 'classic' in tags
            )
            db.session.add(new_map)
            db.session.commit()
            return jsonify({"success": True, "map_name": real_name})
        
        except Exception as e:
            db.session.rollback() # Important! Clears the "failed" transaction
            print(f"Database Error: {e}")
            return jsonify({
                "success": False, 
                "error": "Failed to save to database. It might be a duplicate."
            }), 500
        
    except Exception as e:
        print(f"Steam API Error: {e}")
        return jsonify({"error": "Could not fetch map info from Steam"}), 500

@app.route("/get_workshop_maps")
def get_workshop_maps():
    maps = WorkshopMap.query.filter_by(is_officialmap=False).order_by(WorkshopMap.map_name.asc()).all()
    # Convert the database objects into a list of dictionaries
    return jsonify([{
        "id": m.map_alias,
        "name": m.map_name,
        "image": m.image_url
    } for m in maps])

@app.route("/delete_workshop_map/<map_id>", methods=['DELETE'])
def delete_workshop_map(map_id):
    try:
        # Find the map in the database
        map_to_delete = WorkshopMap.query.filter_by(map_alias=map_id).first()
        
        if map_to_delete:
            if map_to_delete.image_url:
                filename = map_to_delete.image_url.split('/')[-1]
                file_path = os.path.join(app.root_path, 'data', 'workshop_images', filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Deleted image file: {file_path}")
            db.session.delete(map_to_delete)
            db.session.commit()
            return jsonify({"success": True, "message": "Map removed"})
        
        return jsonify({"success": False, "error": "Map not found"}), 404
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/update_map_name/<map_id>", methods=['POST'])
def update_map_name(map_id):
    try:
        # 1. Get the new name from the JSON body sent by JS
        data = request.json
        new_name = data.get('new_name')
        
        if not new_name:
            return jsonify({"success": False, "error": "No name provided"}), 400

        # 2. Find the map using the workshop ID (map_alias)
        map_record = WorkshopMap.query.filter_by(map_alias=map_id).first()
        
        if map_record:
            # 3. Update the field and save
            map_record.map_name = new_name
            db.session.commit()
            return jsonify({"success": True})
        
        return jsonify({"success": False, "error": "Map not found"}), 404

    except Exception as e:
        db.session.rollback()
        print(f"Update Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

#http://IP-ADDRESS:5000/send_command?cmd=COMMANDHERE