from flask_restful import Resource, Api
from app import app
from models import db, Influencer, Sponsor, Campaigns, Ads

api = Api(app)

class Influencer_api (Resource):
    def get(self):
         influencers = Influencer.query.all()
         return {'influencers': [ {
              'id' : influencer.id,
              'name' : influencer.name,
              'username' : influencer.username,
              'email' : influencer.email,
              'niche' : influencer.niche,
              'followers' :  influencer.followers

         }for influencer in influencers]}

api.add_resource(Influencer_api, '/api/influencer' )


class Sponsor_api (Resource):
    def get(self):
         sponsors = Sponsor.query.all()
         return {'sponsors': [ {
              'id' : sponsor.id,
              'company name' : sponsor.company_name,
              'username' : sponsor.username,
              'email' : sponsor.email,
              'industry' : sponsor.industry, 
         }for sponsor in sponsors]}

api.add_resource(Sponsor_api, '/api/sponsor' )