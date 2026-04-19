import os
from flask_sqlalchemy import SQLAlchemy

# Initialize the db object
db = SQLAlchemy()

class WorkshopMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    map_name = db.Column(db.String(100), unique=True, nullable=False)
    map_alias = db.Column(db.String(100), unique=True, nullable=False)
    image_url = db.Column(db.String(255))
    is_officialmap = db.Column(db.Boolean, default=False)
    is_competitive = db.Column(db.Boolean, default=False)
    is_wingman = db.Column(db.Boolean, default=False)
    is_casual = db.Column(db.Boolean, default=False)
    is_deathmatch = db.Column(db.Boolean, default=False)
    is_armsrace = db.Column(db.Boolean, default=False)

def setup_workshop_db(app):
    basedir = os.path.abspath(os.path.dirname(__file__))
    data_path = os.path.join(basedir, 'data')
    if not os.path.exists(data_path):
        os.makedirs(data_path)
        print(f"Created directory: {data_path}")
    db_path = os.path.join(data_path, 'workshop_maps.db')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        if not os.path.exists(db_path):
            db.create_all()
            print(f"Success: Database created at {db_path}")
        else:
            print("Database already exists.")
        seed_official_maps()

def seed_official_maps():
    """Run this to fill the DB with the basic CS2 maps."""
    valve_maps = [
        {
            "map_name": "Baggage",
            "map_alias": "ar_baggage",
            "is_officialmap": True,
            "is_armsrace": True,
            "image_url": "/static/img/map_images/official/ar_baggage.png"
        },       
        {
            "map_name": "Pool Day",
            "map_alias": "ar_pool_day",
            "is_officialmap": True,
            "is_armsrace": True,
            "image_url": "/static/img/map_images/official/ar_pool_day.png"
        },
        {
            "map_name": "Shoots (Day)",
            "map_alias": "ar_shoots",
            "is_officialmap": True,
            "is_armsrace": True,
            "image_url": "/static/img/map_images/official/ar_shoots.png"
        },
        {
            "map_name": "Shoots (Night)",
            "map_alias": "ar_shoots_night",
            "is_officialmap": True,
            "is_armsrace": True,
            "image_url": "/static/img/map_images/official/ar_shoots_night.png"
        },
        {
            "map_name": "Alpine",
            "map_alias": "cs_alpine",
            "is_officialmap": True,
            "is_competitive": True,
            "is_casual": True,
            "is_deathmatch": True,
            "image_url": "/static/img/map_images/official/cs_alpine.png"
        },
        {
            "map_name": "Italy",
            "map_alias": "cs_italy",
            "is_officialmap": True,
            "is_competitive": True,
            "is_casual": True,
            "is_deathmatch": True,
            "image_url": "/static/img/map_images/official/cs_italy.png"
        },
        {
            "map_name": "Office",
            "map_alias": "cs_office",
            "is_officialmap": True,
            "is_competitive": True,
            "is_casual": True,
            "is_deathmatch": True,
            "image_url": "/static/img/map_images/official/cs_office.png"
        },
        {
            "map_name": "Italy",
            "map_alias": "cs_italy",
            "is_officialmap": True,
            "is_competitive": True,
            "is_casual": True,
            "is_deathmatch": True,
            "image_url": "/static/img/map_images/official/cs_italy.png"
        },
        {
            "map_name": "Ancient",
            "map_alias": "de_ancient",
            "is_officialmap": True,
            "is_competitive": True,
            "is_casual": True,
            "is_deathmatch": True,
            "image_url": "/static/img/map_images/official/de_ancient.png"
        },
        {
            "map_name": "Anubis",
            "map_alias": "de_anubis",
            "is_officialmap": True,
            "is_competitive": True,
            "is_casual": True,
            "is_deathmatch": True,
            "image_url": "/static/img/map_images/official/de_anubis.png"
        },
        {
            "map_name": "Dust II",
            "map_alias": "de_dust2",
            "is_officialmap": True,
            "is_competitive": True,
            "is_casual": True,
            "is_deathmatch": True,
            "image_url": "/static/img/map_images/official/de_dust2.png"
        },
        {
            "map_name": "Inferno",
            "map_alias": "de_inferno",
            "is_officialmap": True,
            "is_competitive": True,
            "is_casual": True,
            "is_deathmatch": True,
            "is_wingman": True,
            "image_url": "/static/img/map_images/official/de_inferno.png"
        },
        {
            "map_name": "Dust II",
            "map_alias": "de_dust2",
            "is_officialmap": True,
            "is_competitive": True,
            "is_casual": True,
            "is_deathmatch": True,
            "image_url": "/static/img/map_images/official/de_dust2.png"
        },
        {
            "map_name": "Mirage",
            "map_alias": "de_mirage",
            "is_officialmap": True,
            "is_competitive": True,
            "is_casual": True,
            "is_deathmatch": True,
            "image_url": "/static/img/map_images/official/de_mirage.png"
        },
        {
            "map_name": "Nuke",
            "map_alias": "de_nuke",
            "is_officialmap": True,
            "is_competitive": True,
            "is_casual": True,
            "is_deathmatch": True,
            "is_wingman": True,
            "image_url": "/static/img/map_images/official/de_nuke.png"
        },
        {
            "map_name": "Overpass",
            "map_alias": "de_overpass",
            "is_officialmap": True,
            "is_competitive": True,
            "is_casual": True,
            "is_deathmatch": True,
            "is_wingman": True,
            "image_url": "/static/img/map_images/official/de_overpass.png"
        },
        {
            "map_name": "Poseidon",
            "map_alias": "de_poseidon",
            "is_officialmap": True,
            "is_wingman": True,
            "image_url": "/static/img/map_images/official/de_poseidon.png"
        },
        {
            "map_name": "Sanctum",
            "map_alias": "de_sanctum",
            "is_officialmap": True,
            "is_wingman": True,
            "image_url": "/static/img/map_images/official/de_sanctum.png"
        },
        {
            "map_name": "Stronghold",
            "map_alias": "de_stronghold",
            "is_officialmap": True,
            "is_competitive": True,
            "is_casual": True,
            "is_deathmatch": True,
            "image_url": "/static/img/map_images/official/de_stronghold.png"
        },
        {
            "map_name": "Train",
            "map_alias": "de_train",
            "is_officialmap": True,
            "is_competitive": True,
            "is_casual": True,
            "is_deathmatch": True,
            "image_url": "/static/img/map_images/official/de_train.png"
        },
        {
            "map_name": "Vertigo",
            "map_alias": "de_vertigo",
            "is_officialmap": True,
            "is_competitive": True,
            "is_casual": True,
            "is_deathmatch": True,
            "is_wingman": True,
            "image_url": "/static/img/map_images/official/de_vertigo.png"
        },
        {
            "map_name": "Warden",
            "map_alias": "de_warden",
            "is_officialmap": True,
            "is_competitive": True,
            "is_casual": True,
            "is_deathmatch": True,
            "image_url": "/static/img/map_images/official/de_warden.png"
        },
    ]

    for data in valve_maps:
        exists = WorkshopMap.query.filter_by(map_alias=data['map_alias']).first()
        if not exists:
            new_map = WorkshopMap(**data)
            db.session.add(new_map)
    
    db.session.commit()
    print("Official maps seeded!")