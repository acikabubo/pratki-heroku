import os
import dropbox
import requests
import xmltodict
from dateutil.parser import parse
from datetime import datetime, time
from app import app, db
from flask import request, jsonify, render_template, redirect, flash, url_for
from .forms import PackageForm, UploadForm
from .models import Package
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, TEXT
from flask_login import login_user, logout_user, current_user, login_required
from .oauth import OAuthSignIn
from .models import User

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('info'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('info'))


# TODO: This route should be /info
@app.route('/info', methods=('GET', 'POST'))
@login_required
def info():
    try:
        dbx = dropbox.Dropbox(os.environ['DRPB_ACCESS_TOKEN'])
        # Try to read file from dropbox
        md, res = dbx.files_download(os.environ['FILE_PATH'])
    except KeyError:
        return '<h1 align="center">Missing dropbox access token or missing file path</h1>'
    except Exception:
        return '<h1 align="center">Error occurred while getting file from dropbox</h1>'

    # Decode bytes to string
    data = res.content.decode("utf-8")

    if not data:
        return '<h1 align="center">There is no packages</h1>'

    pkgs = [item.split(' - ') for item in data.split('\n')]

    packages = []
    waiting, arrived = 0, 0
    for track_no, pkg_date, pkg_name in pkgs:
        send_date = parse(pkg_date, dayfirst=True)
        shipped_ago = (datetime.now() - send_date).days

        if len(track_no) != 13:
            waiting += 1
            packages.append({
                'track_no': track_no,
                'shipped_ago': shipped_ago,
                'info_date': "",
                'notice': "",
                'pkg_name': pkg_name
            })
            continue

        r = requests.get(
            'http://www.posta.com.mk/tnt/api/query?id=%s' % track_no)

        # Convert xml data to dict
        req_data = xmltodict.parse(r.text)

        # Get required data
        array_of_tracking_data = req_data['ArrayOfTrackingData']

        # Check if there is no package data
        # and add in table without Info/Data & Notice
        if not array_of_tracking_data:
            waiting += 1
            packages.append({
                'track_no': track_no,
                'shipped_ago': shipped_ago,
                'info_date': "",
                'notice': "",
                'pkg_name': pkg_name
            })
            continue

        # Get tracking data per package
        tracking_data = array_of_tracking_data['TrackingData']

        # Get latest tracking data pre package
        try:
            # Tracking data it's a list when there is multiple items
            # Get only the latest item/status
            package = list(tracking_data[-1].items())
        except KeyError:
            # Tracking data it's not a list when there is only one item
            package = list(tracking_data.items())

        # Get datetime format, if there is midnight get only date
        dt_format = '%d.%m.%Y'
        pkg_date = parse(package[3][1])
        if pkg_date.time() != time(0, 0):
            dt_format = '%d.%m.%Y %H:%M:%S'

        # Get data from post office
        pkg_date = parse(package[3][1]).strftime(dt_format)
        pkg_notice = package[4][1]

        arrived += 1
        packages.append({
            'track_no': track_no,
            'shipped_ago': shipped_ago,
            'info_date': pkg_date,
            'notice': pkg_notice,
            'pkg_name': pkg_name
        })

    # Sort by shipped ago
    packages = sorted(packages, key=lambda k: k['shipped_ago'])

    # Return raw json data
    if request.is_json:
        return jsonify(packages)

    # Make final data
    data = {
        'packages': packages,
        'info': {
            'waiting': waiting,
            'arrived': arrived,
            'total': waiting + arrived
        }
    }

    form = PackageForm()
    upload_form = UploadForm()
    if form.validate_on_submit():
        try:
            package = Package(
                track_no=form.track_no.data,
                shipped_on=form.shipped_on.data,
                name=form.name.data,
                user=current_user)

            db.session.add(package)
            db.session.commit()

            flash('Package created successfully.', 'info')
        except IntegrityError:
            db.session.rollback()
            flash(
                'There is package with tracking number: %s.' % form.track_no.data,
                'warning')

    if 'file' in request.files:
        uploaded_file = request.files['file']

        if uploaded_file:
            try:
                file_content = uploaded_file.read().decode('utf8')
                pkgs = [item.split(' - ') for item in file_content.split('\n')]

                total = 0
                for track_no, shipped_on, pkg_name in pkgs:
                    try:
                        package = Package(
                            track_no=track_no,
                            shipped_on=shipped_on,
                            name=pkg_name
                        )
                        db.session.add(package)
                        db.session.flush()

                        total += 1
                    except IntegrityError:
                        db.session.rollback()
                        continue
                    except Exception as ex:
                        print(ex)
                        # flash('Error occurred while syncing data.', 'warning')
                db.session.commit()

                if total:
                    flash('Sync %s packages.' % total, 'info')
                else:
                    flash('There is no packages for sync.', 'info')

            except Exception as ex:
                print(str(ex))
                flash(
                    'Error occurred while reading file or invalid data format.', 'warning')

            # filename = secure_filename(uploaded_file.filename)
            # uploaded_file.save(os.path.join(
            #     app.config['UPLOAD_FOLDER'], filename))

    return render_template('info.html',
        data=data, form=form, upload_form=upload_form)


@app.route('/<track_no>/')
@login_required
def pkg_details(track_no):

    # Initial data
    data = {
        'fnl': [],
        'track_no': track_no,
        'item_name': request.args.get('item_name', 'NO PACKAGE NAME')
    }

    if len(track_no) != 13:
        return render_template('package.html', data=data)

    r = requests.get(
        'http://www.posta.com.mk/tnt/api/query?id=%s' % track_no)

    # Convert xml data to dict
    req_data = xmltodict.parse(r.text)

    if not req_data['ArrayOfTrackingData']:
        return render_template('package.html', data=data)

    # Get required data
    tracking_data = req_data['ArrayOfTrackingData']['TrackingData']

    if type(tracking_data) != list:
        tracking_data = [tracking_data]

    dt_format = '%d.%m.%Y'
    for item in tracking_data:
        row = list(item.items())

        pkg_date = parse(row[3][1])
        if pkg_date.time() != time(0, 0):
            dt_format = '%d.%m.%Y %H:%M:%S'

        data['fnl'].append({
            'from': row[1][1],
            'to': row[2][1],
            'date': parse(row[3][1]).strftime(dt_format),
            'notice': row[4][1]
        })

    # Return raw json data
    if request.is_json:
        return jsonify(data)

    return render_template('package.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
