from flask import render_template, request, redirect, url_for, flash, session
from app import app
from models import db, Influencer, Sponsor, Campaigns, Ads
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# auth_required decorator for influencers and sponsors

def admin_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        influencer = Influencer.query.get(session['influencer_id'])
        if influencer.is_admin:
            return func(*args, **kwargs)
        else:
            flash('Please login to continue')
            return redirect(url_for('admin_login'))
    return inner

def auth_required_1(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if 'influencer_id' in session:
            return func(*args, **kwargs)
        else:
            flash('Please login to continue')
            return redirect(url_for('inf_login'))
    return inner

def auth_required_2(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if 'sponsor_id' in session:
            return func(*args, **kwargs)
        else:
            flash('Please login to continue')
            return redirect(url_for('spon_login'))
    return inner

@app.route('/')
@auth_required_1
def index():   
    influencer = Influencer.query.get(session['influencer_id'])
    return render_template('inf_dash.html', influencer = influencer)
    
# ---> login
# ---> influencer
@app.route('/inf_login')
def inf_login():
    return render_template('inf_login.html')

@app.route('/inf_login', methods=['POST'])
def inf_login_1():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Please fill all the fields')
        return redirect(url_for('inf_login'))
    
    influencer = Influencer.query.filter_by(username=username).first()
    if not influencer:
        flash('Username not found')
        return redirect(url_for('inf_login'))
    
    if not check_password_hash(influencer.passhash, password):
        flash('Incorrect password!')
        return redirect(url_for('inf_login'))
        
    session['influencer_id'] = influencer.id
    flash('Login successful')
    return redirect(url_for('inf_dash'))

# ---> sponsor
@app.route('/spon_login')
def spon_login():
    return render_template('spon_login.html')

@app.route('/spon_login', methods=['POST'])
def spon_login_1():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Please fill all the fields')
        return redirect(url_for('spon_login'))
    sponsor = Sponsor.query.filter_by(username=username).first()
    if not sponsor:
        flash('Username not found')
        return redirect(url_for('spon_login'))
    if not check_password_hash(sponsor.passhash, password):
        flash('Incorrect password!')
        return redirect(url_for('spon_login'))
    session['sponsor_id'] = sponsor.id
    flash('Login successful')
    return redirect(url_for('spon_dash'))
# ---> End of login

# ---> registration
# ---> influencer
@app.route('/inf_reg')
def inf_reg():
    return render_template('inf_reg.html')

@app.route('/inf_reg', methods=['POST'])
def infl_reg():
    name = request.form.get('name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    niche = request.form.get('niche')
    followers = request.form.get('followers')

    if not name or not email or not username or not password or not confirm_password:
        flash('Please fill all the fields')
        return redirect(url_for('inf_reg'))
    if password != confirm_password:
        flash('Passwords do not match')
        return redirect(url_for('inf_reg'))  

    influencer = Influencer.query.filter_by(username = username).first()
    if influencer:
        flash('username already exists')
        return redirect(url_for('inf_reg'))
    password_hash = generate_password_hash(password)


    new_influencer = Influencer(name=name, email=email, username=username, passhash=password_hash, followers=followers, niche=niche)
    db.session.add(new_influencer)
    db.session.commit()
    flash('registration succesful')
    return redirect(url_for('inf_login'))

# ---> sponsor
@app.route('/spon_reg')
def spon_reg():
    return render_template('spon_reg.html')

@app.route('/spon_reg', methods=['POST'])
def spons_reg():
    company_name = request.form.get('company_name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    industry = request.form.get('industry')

    if not company_name or not email or not username or not password or not confirm_password:
        flash('Please fill all the fields')
        return redirect(url_for('spon_reg'))
    
    if password != confirm_password:
        flash('Passwords do not match')
        return redirect(url_for('spon_reg'))
    
    sponsor = Sponsor.query.filter_by(username=username).first()
    if sponsor:
        flash('username already exists')
        return redirect(url_for('spon_reg'))

    password_hash = generate_password_hash(password)

    new_sponsor = Sponsor(company_name=company_name, email=email, username=username, passhash=password_hash, industry=industry)
    db.session.add(new_sponsor)
    db.session.commit()
    flash('Registration succesful')
    return redirect(url_for('spon_login'))

# ---> End of registration

# ---> Dashboard
# ---> Influencer
@app.route('/inf_dash')
@auth_required_1
def inf_dash():
    campaigns = Campaigns.query.all()
    influencer = Influencer.query.get(session['influencer_id'])
    ads = Ads.query.all()

    return render_template('inf_dash.html', influencer=influencer, ads = ads, campaigns = campaigns)

# ---> Sponsor

@app.route('/spon_dash')
@auth_required_2
def spon_dash():
    sponsor = Sponsor.query.get(session['sponsor_id'])
    campaigns = Campaigns.query.filter_by(sponsor_username = sponsor.username)
    ads = Ads.query.filter_by(sponsor_username = sponsor.username)

    return render_template('spon_dash.html', sponsor=sponsor, ads = ads, campaigns = campaigns)

# ---> end of Dashboard

# ---> profile
# ---> Influencer
@app.route('/inf_prof')
@auth_required_1
def inf_prof():
    influencer = Influencer.query.get(session['influencer_id'])
    return render_template('inf_prof.html', influencer=influencer) 


@app.route('/inf_prof', methods=["POST"])
@auth_required_1
def inf_prof1():
    username = request.form.get('username')
    cpassword = request.form.get('cpassword')
    password = request.form.get('password')
    name = request.form.get('name')
    email = request.form.get('email')
    followers = request.form.get('followers')
    niche = request.form.get('niche')


    if not username or not cpassword or not password:
        flash("please enter all the details ")
        return redirect(url_for('inf_prof'))
    
    influencer = Influencer.query.get(session['influencer_id'])

    if not check_password_hash(influencer.passhash, cpassword):
        flash('Incorrect password')
        return redirect(url_for('inf_prof'))
    
    if username != influencer.username:
        new_username = Influencer.query.filter_by(username = username).first()
        if new_username:
            flash('Username already exists')
            return redirect(url_for('inf_login'))
    
    new_passhash = generate_password_hash(password)
    influencer.username = username
    influencer.passhash = new_passhash
    influencer.name = name
    influencer.followers = followers
    influencer.niche = niche
    influencer.email = email
    db.session.commit()
    flash('profile updated succesfully')
    return redirect(url_for('inf_prof'))

# ---> Sponsor

@app.route('/spon_prof')
@auth_required_2
def spon_prof():
    sponsor = Sponsor.query.get(session['sponsor_id'])
    return render_template('spon_prof.html', sponsor=sponsor) 
    
    
@app.route('/spon_prof', methods=["POST"])
@auth_required_2
def spon_prof1():
    username = request.form.get('username')
    cpassword = request.form.get('cpassword')
    password = request.form.get('password')
    company_name = request.form.get('company_name')
    email = request.form.get('email')
    industry = request.form.get('industry') 


    if not username or not cpassword or not password:
        flash("please enter all the details")
        return redirect(url_for('spon_prof'))
    
    sponsor = Sponsor.query.get(session['sponsor_id'])

    if not check_password_hash(sponsor.passhash, cpassword):
        flash('Incorrect password')
        return redirect(url_for('spon_prof'))
    
    if username != sponsor.username:
        new_username = Sponsor.query.filter_by(username = username).first()
        if new_username:
            flash('Username already exists')
            return redirect(url_for('spon_login'))
    
    new_passhash = generate_password_hash(password)
    sponsor.username = username
    sponsor.passhash = new_passhash
    sponsor.company_name = company_name
    sponsor.email = email
    sponsor.industry = industry

    db.session.commit()
    flash('profile updated succesfully')
    return redirect(url_for('spon_prof'))

# ---> End of profiles

# ---> logout
# ---> Influencer

@app.route('/inf_logout')
@auth_required_1
def inf_logout():
    session.pop('influencer_id')    
    flash('You have logged out succesfully')
    return redirect(url_for('inf_login'))
    
# ---> Sponsor

@app.route('/spon_logout')
@auth_required_2
def spon_logout():
    session.pop('sponsor_id')    
    flash('You have logged out succesfully')
    return redirect(url_for('spon_login'))
    
# ---> Admin

@app.route('/admin_logout')
@admin_required
def admin_logout():
    session.pop('influencer_id')    
    flash('You have logged out succesfully')
    return redirect(url_for('admin_login'))
# ---> End of logout

# ---> Find

@app.route('/inf_find')
@auth_required_1
def inf_find():
    campaigns = Campaigns.query.all()
    influencer = Influencer.query.get(session['influencer_id'])
    ads = Ads.query.all()

    if not influencer:
        flash('Please login to continue')
        return redirect(url_for('inf_login'))

    return render_template('inf_find.html', influencer=influencer, ads = ads, campaigns = campaigns)

@app.route('/spon_find')
@auth_required_2
def spon_find():
    sponsor = Sponsor.query.get(session['sponsor_id'])
    campaigns = Campaigns.query.all()
    ads = Ads.query.all()
    influencers = Influencer.query.all()

    if not sponsor:
        flash('Please login to continue')
        return redirect(url_for('spon_login'))
    
    return render_template('spon_find.html', sponsor=sponsor, influencers = influencers, campaigns = campaigns, ads=ads)


@app.route('/<int:id>/inf_list')
@auth_required_2
def inf_list(id):
    sponsor = Sponsor.query.get(session['sponsor_id'])
    ad = Ads.query.get(id)
    influencers = Influencer.query.all()

    if not ad:
        flash('Advetisement does not exist')
        return redirect(url_for('spon_dash'))

    return render_template('inf_list.html', sponsor=sponsor, influencers = influencers, ad = ad)

# ---> End of Find

# ---> Admin

@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin_login', methods=['POST'])
def admin_login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Please fill all the fields')
        return redirect(url_for('admin_login'))
    
    influencer = Influencer.query.filter_by(username=username).first()
    if not influencer:
        flash('Username not found')
        return redirect(url_for('admin_login'))
    
    if not influencer.is_admin:
        flash('User is not admin')

    if not check_password_hash(influencer.passhash, password):
        flash('Incorrect password!')
        return redirect(url_for('admin_login'))
        
    session['influencer_id'] = influencer.id
    flash('Login successful')
    return redirect(url_for('admin_dash'))

@app.route('/admin_dash')
@admin_required
def admin_dash():
    influencer = Influencer.query.get(session['influencer_id'])
    campaigns = Campaigns.query.all()
    influencers = Influencer.query.all()
    sponsor = Sponsor.query.all()
    ads = Ads.query.all()

    if not influencer:
        flash('Please login to continue')
        return redirect(url_for('admin_login'))
    return render_template('admin_dash.html', campaigns = campaigns, sponsor = sponsor, influencer = influencer, influencers = influencers, ads = ads)


@app.route('/admin_prof')
@admin_required
def admin_prof():
    influencer = Influencer.query.get(session['influencer_id'])
    return render_template('admin_prof.html', influencer=influencer) 
        

@app.route('/admin_prof', methods=["POST"])
@auth_required_1
def admin_prof_post():
    username = request.form.get('username')
    cpassword = request.form.get('cpassword')
    password = request.form.get('password')
    name = request.form.get('name')

    if not username or not cpassword or not password:
        flash("please enter all the details ")
        return redirect(url_for('admin_prof'))
    
    influencer = Influencer.query.get(session['influencer_id'])

    if not check_password_hash(influencer.passhash, cpassword):
        flash('Incorrect password')
        return redirect(url_for('admin_prof'))
    
    if username != influencer.username:
        new_username = Influencer.query.filter_by(username = username).first()
        if new_username:
            flash('Username already exists')
            return redirect(url_for('admin_prof'))
    
    new_passhash = generate_password_hash(password)
    influencer.username = username
    influencer.passhash = new_passhash
    influencer.name = name

    db.session.commit()

    flash('profile updated succesfully')
    return redirect(url_for('admin_prof'))

@app.route('/campaigns/<int:id>/admin_view')
@admin_required
def admin_view(id):
    influencer = Influencer.query.get(session['influencer_id'])
    campaign = Campaigns.query.get(id)
    ads = Ads.query.all()
    if not campaign:
        flash('Campaign doesnot exist')
        return redirect(url_for('spon_dash'))
    if not influencer:
        flash('Please login to continue')
        return redirect(url_for('admin_login'))
    return render_template('campaigns/admin_view.html',campaign = campaign,  ads = ads, influencer = influencer)

# ---> Campaigns


@app.route('/campaigns/<int:id>/')
def camp_view(id):
    campaign = Campaigns.query.get(id)
    if not campaign:
        flash('Campaign doesnot exist')
        return redirect(url_for('spon_dash'))    
    return render_template('campaigns/view.html', campaign = campaign)


@app.route('/campaigns/<int:id>/flag')
@admin_required
def camp_flag(id):
    influencer = Influencer.query.get(session['influencer_id'])
    campaign = Campaigns.query.get(id)
    if not campaign:
        flash('Campaign does not exist')
        return redirect(url_for('admin_dash'))    
    return render_template('campaigns/flag.html', campaign = campaign, influencer = influencer)

@app.route('/campaigns/<int:id>/flag', methods = ['POST'])
def camp_flag_post(id):
    reason = request.form.get('reason')
    campaign = Campaigns.query.get(id)
    if not campaign:
        flash('Campaign does not exist')
        return redirect(url_for('admin_dash'))
    
    if not reason:
        flash('Please enter the reason')
        return redirect(url_for('camp_flag'))
    
    campaign.flag = True
    campaign.reason = reason
    db.session.commit()

    flash('Campaign flagged succesfully')
    return redirect(url_for('admin_dash', campaign = campaign))

@app.route('/campaigns/add')
@auth_required_2
def camp_add():
    sponsor = Sponsor.query.get(session['sponsor_id'])
    return render_template('campaigns/add.html', sponsor = sponsor)

@app.route('/campaigns/add', methods=['POST'])
@auth_required_2
def camp_add1():
    name = request.form.get('name')
    sponsor = Sponsor.query.get(session['sponsor_id'])

    if not name:
        flash('Please fill all the fields')
        return redirect(url_for('camp_add'))

    new_campaign = Campaigns(name=name, sponsor_username = sponsor.username)
    db.session.add(new_campaign)
    db.session.commit()
    flash('Campaign added succesfully')
    return redirect(url_for('spon_dash'))

@app.route('/campaigns/<int:id>/edit')
@auth_required_2
def camp_edit(id):
    campaign = Campaigns.query.get(id)
    if not campaign:
        flash('Campaign doesnot exist')
        return redirect(url_for(spon_dash))
    return render_template('campaigns/edit.html', campaign = campaign)

@app.route('/campaigns/<int:id>/edit', methods = ['POST'] )
@auth_required_2
def camp_edit_post(id):
    campaign = Campaigns.query.get(id)
    if not campaign: 
        flash('Campaign doesnot exist')
        return redirect(url_for(spon_dash))
    
    name = request.form.get('name')

    if not name:
        flash('Please fill all the fields')
        return redirect(url_for('camp_add')) 

    campaign.name = name

    db.session.commit()
    flash('Campaign updated succesfully')
    return redirect(url_for('spon_dash')) 

@app.route('/campaigns/<int:id>/delete', methods = ['POST'])
@auth_required_2
def camp_delete_post(id):
    campaign = Campaigns.query.get(id)
    if not campaign:
        flash('Campaign doesnot exist')
        return redirect(url_for('spon_dash'))
    
    db.session.delete(campaign)
    db.session.commit()

    flash('Campaign deleted succesfully')
    return redirect(url_for('spon_dash'))

# ---> End of Campaigns

# ---> AD requests

@app.route('/ads/<int:camp_id>/<int:id>/')
@auth_required_1
def ad_view(camp_id, id):
    influencer = Influencer.query.get(session['influencer_id'])
    campaign = Campaigns.query.get(camp_id)
    ad = Ads.query.get(id)
    if not ad:
        flash('Advertisement does not exist')
        return redirect(url_for('inf_dash'))   
    if not campaign:
        flash('Campaign doesnot exist')
        return redirect(url_for('inf_dash'))
    
    return render_template('ads/view.html', ad = ad, influencer = influencer, campaign = campaign)

@app.route('/ads/<int:camp_id>/<int:id>/view')
@auth_required_2
def ad_spon_view(camp_id, id):
    sponsor = Sponsor.query.get(session['sponsor_id'])
    campaign = Campaigns.query.get(camp_id)
    ad = Ads.query.get(id)
    if not ad:
        flash('Advertisement does not exist')
        return redirect(url_for('spon_dash'))   
    if not campaign:
        flash('Campaign doesnot exist')
        return redirect(url_for('spon_dash'))
    
    return render_template('ads/view.html', ad = ad, sponsor = sponsor, campaign = campaign)

@app.route('/ads/add/<int:campaign_id>') 
@auth_required_2
def ad_add(campaign_id):
    campaigns = Campaigns.query.all()
    sponsor = Sponsor.query.get(session['sponsor_id'])
    campaign = Campaigns.query.get(campaign_id)

    if not campaign:
        flash('Campaign does not exist')
        return redirect(url_for('spon_dash')) 
     
    return render_template('ads/add.html', campaign = campaign, campaigns = campaigns, sponsor = sponsor, campaign_id = campaign_id)

@app.route('/ads/add/<int:campaign_id>', methods=['POST'])
@auth_required_2
def ad_add_post(campaign_id):
    sponsor = Sponsor.query.get(session['sponsor_id'])
    name = request.form.get('name')
    niche = request.form.get('niche')
    budget = request.form.get('budget')
    nature = request.form.get('nature')
    description = request.form.get('description')
    sponsor = Sponsor.query.get(session['sponsor_id'])

    if not name or not niche or not budget or not nature or not description:
        flash('Please fill all the fields')
        return redirect(url_for('ad_add'))

    new_ad = Ads(name=name, niche=niche, budget=budget, nature=nature, sponsor_username = sponsor.username, campaign_id = campaign_id, description = description)
    db.session.add(new_ad)
    db.session.commit()
    flash('Advetisement added succesfully')
    return redirect(url_for('spon_dash'))

@app.route('/ads/<int:camp_id>/<int:id>/edit')
@auth_required_2
def ad_edit(camp_id, id):
    campaign = Campaigns.query.get(camp_id)
    ad = Ads.query.get(id)
    if not ad:
        flash('Advertisement does not exist')
        return redirect(url_for(spon_dash))
    if not campaign:
        flash('Campaign doesnot exist')
        return redirect(url_for('spon_dash'))
    return render_template('ads/edit.html', ad=ad, campaign = campaign)

@app.route('/ads/<int:camp_id>/<int:id>/edit', methods = ['POST'])
@auth_required_2
def ad_edit_post(camp_id, id):
    campaign = Campaigns.query.get(camp_id)
    ad = Ads.query.get(id)
    if not ad: 
        flash('Advertisement does not exist')
        return redirect(url_for(spon_dash))
    if not campaign:
        flash('Campaign doesnot exist')
        return redirect(url_for('spon_dash'))
    
    name = request.form.get('name')
    niche = request.form.get('niche')
    budget = request.form.get('budget')
    nature = request.form.get('nature')
    description = request.form.get('description')

    if not name or not niche or not budget or not nature or not description:
        flash('Please fill all the fields')
        return redirect(url_for('camp_add')) 

    ad.name = name
    ad.niche = niche
    ad.budget = budget
    ad.nature = nature
    ad.description = description


    db.session.commit()
    flash('Advertisement updated succesfully')
    return redirect(url_for('spon_dash')) 

@app.route('/ads/<int:camp_id>/<int:id>/delete')
@auth_required_2
def ad_delete(camp_id, id):
    campaign = Campaigns.query.get(camp_id)
    sponsor = Sponsor.query.get(session['sponsor_id'])
    ad = Ads.query.get(id)
    if not ad:
        flash('Advertisement does not exist')
        return redirect(url_for('spon_dash')) 
    if not campaign:
        flash('Campaign doesnot exist')
        return redirect(url_for('spon_dash'))   
    return render_template('ads/delete.html', ad = ad, sponsor = sponsor, campaign = campaign)

@app.route('/ads/<int:camp_id>/<int:id>/delete', methods = ['POST'])
@auth_required_2
def ad_delete_post(camp_id, id):
    ad = Ads.query.get(id)
    campaign = Campaigns.query.get(camp_id)
    if not ad:
        flash('Advertisement does not exist')
        return redirect(url_for('spon_dash'))
    if not campaign:
        flash('Campaign doesnot exist')
        return redirect(url_for('spon_dash'))
    
    db.session.delete(ad)
    db.session.commit()

    flash('Advertisement deleted succesfully')
    return redirect(url_for('spon_dash'))

@app.route('/ads/<int:camp_id>/<int:id>/accept')
@auth_required_1
def ad_accept(camp_id, id):
    campaign = Campaigns.query.get(camp_id)
    influencer = Influencer.query.get(session['influencer_id'])
    ad = Ads.query.get(id)
    if not ad:
        flash('Advertisement does not exist')
        return redirect(url_for('inf_dash'))  
    if not campaign:
        flash('Campaign doesnot exist')
        return redirect(url_for('inf_dash'))  
    return render_template('ads/accept.html', ad = ad, influencer = influencer, campaign = campaign)

@app.route('/ads/<int:camp_id>/<int:id>/accept', methods = ['POST'])
@auth_required_1
def ad_accept_post(camp_id, id):
    campaign = Campaigns.query.get(camp_id)
    influencer = Influencer.query.get(session['influencer_id'])
    ad = Ads.query.get(id)
    if not ad:
        flash('Advertisement doesnot exist')
        return redirect(url_for('inf_dash'))
    
    ad.influencer_username = influencer.username
    ad.accepted = True
    db.session.commit()

    flash('Advertisement accepted succesfully')
    return redirect(url_for('inf_dash'))

@app.route('/ads/<int:camp_id>/<int:id>/complete')
@auth_required_1
def ad_complete(camp_id, id):
    campaign = Campaigns.query.get(camp_id)
    influencer = Influencer.query.get(session['influencer_id'])
    ad = Ads.query.get(id)
    if not ad:
        flash('Advertisement does not exist')
        return redirect(url_for('inf_dash'))  
    if not campaign:
        flash('Campaign doesnot exist')
        return redirect(url_for('inf_dash'))  
    return render_template('ads/complete.html', ad = ad, influencer = influencer, campaign = campaign)

@app.route('/ads/<int:camp_id>/<int:id>/complete', methods = ['POST'])
@auth_required_1
def ad_complete_post(camp_id, id):
    campaign = Campaigns.query.get(camp_id)
    influencer = Influencer.query.get(session['influencer_id'])
    ad = Ads.query.get(id)
    if not ad:
        flash('Advertisement doesnot exist')
        return redirect(url_for('inf_dash'))
    if not campaign:
        flash('Campaign doesnot exist')
        return redirect(url_for('inf_dash'))
    ad.influencer_username = influencer.username
    ad.completed = True

    db.session.commit()

    flash('Advertisement completed  succesfully!')
    return redirect(url_for('inf_dash', influencer=influencer))


@app.route('/ads/<int:ad_id>/<int:id>/request')
@auth_required_2
def ad_request(ad_id, id):
    influencer = Influencer.query.get(id)
    ad = Ads.query.get(ad_id)

    if not influencer:
        flash('influencer does not exist')
        return redirect(url_for('spon_dash'))   
    return render_template('ads/request.html', influencer = influencer, ad = ad)

@app.route('/ads/<int:ad_id>/<int:id>/request', methods = ['POST'])
@auth_required_2
def ad_request_post(ad_id, id):
    influencer = Influencer.query.get(id)
    ad = Ads.query.get(ad_id)

    if not influencer:
        flash('influencer does not exist')
        return redirect(url_for('spon_dash'))
    if not ad:
        flash('Advertisement doesnot exist')
        return redirect(url_for('spon_dash'))
    
    ad.request = True
    ad.influencer_username = influencer.username
    
    db.session.commit()

    flash('Request sent succesfully')
    return redirect(url_for('spon_dash'))

@app.route('/ads/<int:camp_id>/<int:id>/reject')
@auth_required_1
def ad_reject(camp_id, id):
    campaign = Campaigns.query.get(camp_id)
    influencer = Influencer.query.get(session['influencer_id'])
    ad = Ads.query.get(id)
    if not ad:
        flash('Advertisement does not exist')
        return redirect(url_for('inf_dash'))   
    if not campaign:
        flash('Campaign doesnot exist')
        return redirect(url_for('inf_dash'))
    return render_template('ads/reject.html', ad = ad, influencer = influencer, campaign = campaign)

@app.route('/ads/<int:camp_id>/<int:id>/reject', methods = ['POST'])
@auth_required_1
def ad_reject_post(camp_id, id):
    campaign = Campaigns.query.get(camp_id)
    influencer = Influencer.query.get(session['influencer_id'])
    ad = Ads.query.get(id)
    if not ad:
        flash('Advertisement doesnot exist')
        return redirect(url_for('inf_dash'))
    if not campaign:
        flash('Campaign doesnot exist')
        return redirect(url_for('inf_dash'))
    
    ad.influencer_username = None
    ad.request = False
    db.session.commit()

    flash('Advertisement rejected succesfully')
    return redirect(url_for('inf_dash'))


@app.route('/ads/<int:camp_id>/<int:id>/payment')
@auth_required_2
def ad_payment(camp_id,id):
    campaign = Campaigns.query.get(camp_id)
    ad = Ads.query.get(id)
    if not ad:
        flash('Advertisement does not exist')
        return redirect(url_for('spon_dash'))  
    if not campaign:
        flash('Campaign doesnot exist')
        return redirect(url_for('spon_dash'))
      
    return render_template('ads/payment.html', ad = ad, campaign = campaign)

@app.route('/ads/<int:camp_id>/<int:id>/payment', methods = ['POST'])
@auth_required_2
def ad_payment_post(camp_id, id):
    campaign = Campaigns.query.get(camp_id)
    ad = Ads.query.get(id)
    if not ad:
        flash('Advertisement does not exist')
        return redirect(url_for('spon_dash'))
    if not campaign:
        flash('Campaign doesnot exist')
        return redirect(url_for('spon_dash'))
    
    ad.paid = True
    db.session.commit()

    flash('Payment completed succesfully')
    return redirect(url_for('spon_dash'))
