import csv
import logging
import os

from flask import Blueprint, render_template, abort, url_for, redirect, current_app
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app.db import db
from app.db.models import Song
from app.songs.forms import csv_upload
from werkzeug.utils import secure_filename, redirect

songs = Blueprint('songs', __name__,
                        template_folder='templates')

@songs.route('/songs', methods=['GET'], defaults={"page": 1})
@songs.route('/songs/<int:page>', methods=['GET'])
def songs_browse(page):
    page = page
    per_page = 1000
    pagination = Song.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    try:
        return render_template('browse_songs.html',data=data,pagination=pagination)
    except TemplateNotFound:
        abort(404)

@songs.route('/songs/upload', methods=['POST', 'GET'])
@login_required
def songs_upload():
    log = logging.getLogger("upload_songs")
    form = csv_upload()
    if form.validate_on_submit():
        # log = logging.getLogger("myApp")

        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        #user = current_user
        list_of_songs = []
        with open(filepath) as file:
            log.info("[%s] opened and parsing filepath:[%s]",
                     current_user, filepath)
            csv_file = csv.DictReader(file)
            csv_header = Song.csv_headers()
            for row in csv_file:
                title = row[csv_header[0]]
                artist = row[csv_header[1]]
                year = row[csv_header[2]]
                genre = row[csv_header[3]]
                list_of_songs.append(Song(title, artist, year, genre))
                # list_of_songs.append(Song(row['Name'],row['Artist'],row['Genre']))

        current_user.songs = list_of_songs
        db.session.commit()

        return redirect(url_for('songs.songs_browse'))
    else:
        log.info("form failed validation")

    try:
        return render_template('upload.html', form=form)
    except TemplateNotFound:
        abort(404)

