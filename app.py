#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from distutils.command.config import config
from itertools import count
import json
from pyexpat import model
from unittest import result
from flask_moment import Moment
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
import datetime
from forms import *
from models import *
from config import *
from filters import *

#----------------------------------------------------------------------------#
# Configuration
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config ['PYTHONUNBUFFERED'] = ""
app.config ['DEBUG'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#----------------------------------------------------------------------------#
# Venues.
#----------------------------------------------------------------------------#

@app.route('/venues')
def venues(venue_id):
  num_upcoming_shows = db.session.query(Shows, Venue).select_from(Shows)\
  .join(Venue).filter(Shows.venue_id==venue_id).filter(Shows.start_time>datetime.now()).all()
  venues = []
  result = Venue.query.all()
  flash(result)

  for row in result:
    venue={
      'city' : {row.city},
      'state' : {row.state},
      "id" : {row.id},
      "name" : {row.name},
      "num_upcoming_shows" : {row.num_upcoming_shows}
    }
    venues.append(venue)
  
  return render_template('pages/venues.html', venue=venue, num_upcoming_shows=num_upcoming_shows);

#-- SEARCH
@app.route('/venues/search', methods=['GET', 'POST'])
def search_venues():
 venues = request.args.get("venues")
 all_venues = Venue.query.filter(Venue.name.ilike("%"+ venues + "%")).all()

 return render_template('pages/search_venues.html', venues=venues, all_venues=all_venues)

#-- SHOW VENUES
@app.route('/venues/<int:venue_id>')
def show_venues(venue_id):
  upcoming_shows = db.session.query(Shows, Venue).select_from(Shows)\
    .join(Venue).filter(Shows.venue_id==venue_id).filter(Shows.start_time>datetime.now()).all()
  past_shows = db.session.query(Shows, Venue).select_from(Shows)\
    .join(Venue).filter(Shows.venue_id==venue_id).filter(Shows.start_time<datetime.now()).all()
  past_shows_count = count(past_shows)
  upcoming_shows_count = count(upcoming_shows)
  show_venues = []
  result = Venue.query.get(venue_id)
  flash(result)

  for row in result:
    show_venue={
      'city' : {row.city},
      'state' : {row.state},
      "id" : {row.id},
      "name" : {row.name},
      "genres": {row.genres},
      "address": {row.address},
      "phone": {row.phone},
      "website": {row.website},
      "facebook_link": {row.facebook_link},
      "seeking_talent": {row.seeking_talent},
      "seeking_description": {row.seeking_description},
      "image_link": {row.image_link},
      "past_shows": [{
        "artist_id": {row.show.artist_id},
        "artist_name":{row.show.artist_name},
        "artist_image_link":{row.show.artist_image_link},
        "start_time":{row.show.start_time}
      }],
      "upcoming_shows":{row.upcoming_shows},
      "past_shows_count":{row.past_shows_count},
      "upcoming_shows_count":{row.upcoming_shows_count}
    }
    show_venues.append(show_venue)

  return render_template('pages/show_venue.html', show_venue=show_venue, upcoming_shows=upcoming_shows, 
  upcoming_shows_count=upcoming_shows_count, past_shows=past_shows, past_shows_count=past_shows_count)

#-- CREATE VENUE

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  try:
    form = VenueForm(request.form)
    venue = Venue(
      name = form.name.data,
      city = form.city.data,
      state = form.state.data,
      address = form.address.data,
      phone = form.phone.data,
      genres = form.genres.data,
      facebook_link = form.facebook_link.data,
      image_link = form.image_link.data,
      website_link = form.website_link.data,
      seeking_talent = form.seeking_talent.data,
      seeking_description = form.seeking_description.data,
    )
    db.session.add(venue)
    db.session.commit()

    flash('Venue: {0} created successfully'.format(venue.name))
  
  except Exception as err:
    flash('An error occurred creating the Venue: {0}. Error: {1}'.format(venue.name, err))
    db.session.rollback()

  finally:
    db.session.close()
  
  if not error:
    return render_template('pages/home.html', venue=Venue.query.all())


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  venue_id = venue_id
  delete_venue = Venue.query.filter_by(venue_id = venue_id).delete()
  db.session.commit()
  return render_template('pages/home.html', delete_venue=delete_venue)



#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = []
  result = Artist.query.all()
  flash(result)

  for row in result:
    artist={
      "id" : {row.id},
      "name" : {row.name}
    }
    artists.append(artist)
  
  return render_template('pages/artist.html', artists=artist)

#-- SEARCH 

@app.route('/artists/search', methods=['POST'])
def search_artists():
  artist = request.args.get("artist")
  all_artist = Venue.query.filter(Venue.name.ilike("%"+ artist + "%")).all()

  return render_template('pages/search_artist.html', artist=artist, all_artist=all_artist)

#-- SHOW ARTIST

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  upcoming_shows = db.session.query(Shows, Artist).select_from(Shows)\
    .join(Artist).filter(Shows.artist_id==artist_id).filter(Shows.start_time>datetime.now()).all()
  past_shows = db.session.query(Shows, Artist).select_from(Shows)\
    .join(Artist).filter(Shows.artist_id==artist_id).filter(Shows.start_time<datetime.now()).all()
  past_shows_count = count(past_shows)
  upcoming_shows_count = count(upcoming_shows)
  show_artists = []
  result = Artist.query.get(artist_id)
  flash(result)

  for row in result:
    show_artist={
      'city' : {row.city},
      'state' : {row.state},
      "id" : {row.id},
      "name" : {row.name},
      "genres": {row.genres},
      "address": {row.address},
      "phone": {row.phone},
      "website": {row.website},
      "facebook_link": {row.facebook_link},
      "seeking_venue": {row.seeking_venue},
      "seeking_description": {row.seeking_description},
      "image_link": {row.image_link},
      "past_shows": [{
        "artist_id": {row.show.artist_id},
        "artist_name":{row.show.artist_name},
        "artist_image_link":{row.show.artist_image_link},
        "start_time":{row.show.start_time}
      }],
      "upcoming_shows":{row.upcoming_shows},
      "past_shows_count":{row.past_shows_count},
      "upcoming_shows_count":{row.upcoming_shows_count}
    }
    show_artists.append(show_artist)

  return render_template('pages/show_artist.html', show_artist=show_artist, upcoming_shows=upcoming_shows, 
  upcoming_shows_count=upcoming_shows_count, past_shows=past_shows, past_shows_count=past_shows_count)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id = None):
  form = ArtistForm()
  form_action = url_for('artist.edit_artist')
  artist= Artist.query.get(artist_id)

  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  db.session.add(artist)
  db.session.commit()
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist, form_action=form_action, title="Artist Update")

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm()
  form_action = url_for('artist.edit_artist')
  artist= Artist.get(artist_id)

  if request.method == 'GET':
    form.name = artist.name
    form.city = artist.city
    form.facebook_link = artist.facebook_link
    form.phone = artist.phone
    form.seeking_description = artist.seeking_description
   
    form.state = artist.state
    form.website_link = artist.website_link
    form.genres = artist.genres
    form.image_link = artist.image_link 
  
  if form.validate_on_submit():
    form.name = artist.name
    form.city = artist.city
    form.facebook_link = artist.facebook_link
    form.phone = artist.phone
    form.seeking_description = artist.seeking_description
    form.state = artist.state
    form.website_link = artist.website_link
    form.genres = artist.genres
    form.image_link = artist.image_link 
    

    if form.id == artist_id:
        query = ArtistForm(
          form.name,
          form.city,
          form.facebook_link,
          form.phone,
          form.seeking_description,
          form.state,
          form.website_link,
          form.genres,
          form.image_link, 
        )
        print (query)
        db.session.add(query)
        db.session.commit()
        flash ('Arist Updated')
        print ("added")
        return (url_for('artist.edit_artist'))

  return redirect(url_for('show_artist', artist= artist, artist_id=artist_id, form_action=form_action, title="Artist Update"))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  form_action = url_for('venue.edit_venue')
  venue = Venue.query.get(venue_id)
  
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }

  db.session.add(venue)
  db.session.commit()
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, form_action=form_action, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm()
  form_action = url_for('venue.edit_venue')
  venue = Venue.query.get(venue_id)

  if request.method == 'GET':
    form.name = venue.name
    form.address = venue.address
    form.city = venue.city
    form.facebook_link = venue.facebook_link
    form.phone = venue.phone
    form.seeking_description = venue.seeking_description
    form.seeking_talent = venue.seeking_talent
    form.state = venue.state
    form.website_link = venue.website_link
    form.genres = venue.genres
    form.image_link = venue.image_link 
  
  if form.validate_on_submit():
    form.name = venue.name
    form.address = venue.address
    form.city = venue.city
    form.facebook_link = venue.facebook_link
    form.phone = venue.phone
    form.seeking_description = venue.seeking_description
    form.seeking_talent = venue.seeking_talent
    form.state = venue.state
    form.website_link = venue.website_link
    form.genres = venue.genres
    form.image_link = venue.image_link 
    

    if form.id == venue_id:
        query = VenueForm(
          form.name,
          form.address,
          form.city,
          form.facebook_link,
          form.phone,
          form.seeking_description,
          form.seeking_talent,
          form.state,
          form.website_link,
          form.genres,
          form.image_link, 
        )
        print (query)
        db.session.add(query)
        db.session.commit()
        flash ('Venue Updated')
        print ("added")
        return (url_for('venue.edit_venue'))

  return redirect(url_for('show_venue', venue=venue, venue_id=venue_id, form_action=form_action, title="Venue Update"))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  error = False
  try:
    form = ArtistForm(request.form)
    artist = Artist(
      name = form.name.data,
      city = form.city.data,
      state = form.state.data,
      address = form.address.data,
      phone = form.phone.data,
      genres = form.genres.data,
      facebook_link = form.facebook_link.data,
      image_link = form.image_link.data,
      website_link = form.website_link.data,
      seeking_venue = form.seeking_venue.data,
      seeking_description = form.seeking_description.data,
    )
    db.session.add(artist)
    db.session.commit()

    flash('Artist: {0} created successfully'.format(artist.name))
  
  except Exception as err:
    flash('An error occurred creating the Artist: {0}. Error: {1}'.format(artist.name, err))
    db.session.rollback()

  finally:
    db.session.close()
  
  if not error:
    return render_template('pages/home.html', artist=Artist.query.all())
  
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  shows = []
  result = Shows.query.all()
  flash(result)

  for row in result:
    show={
      'venue_id' : {row.id},
      'venue_name': {row.venue.name},
      'artist_id' : {row.artist_id},
      'artist_name' : {row.artist.name},
      "artist_image_link" : {row.artist.image_link},
      "start_time" : {row.start_time}
    }
    shows.append(show)

  return render_template('pages/shows.html', shows=shows)

# CREATE SHOW

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  try:
    form = ShowForm(request.form)
    show = Shows(
      show_artist = form.artist_name.data,
      show_venue = form.venue_name.data,
      artist_image_link = form.artist_image_link.data,
      start_time = form.start_time.data
    )
    db.session.add(show)
    db.session.commit()

    flash('Show: {0} was successfully listed'.format(show.name))
  
  except Exception as err:
    flash('An error occurred creating the Show: {0}. Error: {1}'.format(show.name, err))
    db.session.rollback()

  finally:
    db.session.close()
  
  if not error:
    return render_template('pages/home.html', show=Shows.query.all())


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(host="0.0.0.0")

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
