from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique = True)
    name = db.Column(db.String(64))
    email = db.Column(db.String, nullable = True)
    passhash = db.Column(db.String(256), nullable = False)
    followers = db.Column(db.Integer, nullable = True)
    niche = db.Column(db.String(32), nullable = True)
    is_admin = db.Column(db.Boolean, nullable = False, default = False)

    campaigns = db.relationship('Campaigns', backref='influencer', lazy = True)
    ads = db.relationship('Ads', backref='influencer', lazy = True)

class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique = True)
    company_name = db.Column(db.String(64))
    email = db.Column(db.String)
    passhash = db.Column(db.String(256), nullable = False)
    industry = db.Column(db.String(32))
    is_admin = db.Column(db.Boolean, nullable = False, default = False)

    campaigns = db.relationship('Campaigns', backref='sponsor', lazy = True)
    ads = db.relationship('Ads', backref='sponsor', lazy = True)

class Campaigns(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), unique = True)
    flag = db.Column(db.Boolean)
    reason = db.Column(db.String(256))

    influencer_username = db.Column(db.String(32), db.ForeignKey('influencer.username'))
    sponsor_username = db.Column(db.String(32),db.ForeignKey('sponsor.username'), nullable = False)

    ads = db.relationship('Ads', backref='campaigns', lazy = True)
 
class Ads(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(32), unique = True)
    budget = db.Column(db.Integer)    
    niche = db.Column(db.String(32))
    nature = db.Column(db.String(32))
    description = db.Column(db.String(256))

    accepted = db.Column(db.Boolean)
    completed = db.Column(db.Boolean)
    paid = db.Column(db.Boolean)
    request = db.Column(db.Boolean)
    
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable = False)
    influencer_username = db.Column(db.String(32), db.ForeignKey('influencer.username'))
    sponsor_username = db.Column(db.String(32),db.ForeignKey('sponsor.username'))

with app.app_context():
    db.create_all()

    admin = Influencer.query.filter_by(is_admin = True).first()
    if not admin:
        password_hash = generate_password_hash('admin')
        admin = Influencer(username='admin', passhash=password_hash, is_admin = True)
        db.session.add(admin)
        db.session.commit()
