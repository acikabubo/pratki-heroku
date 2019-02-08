import json
import requests
import xmltodict
from dateutil.parser import parse
from datetime import datetime, time
from flask import g, request, jsonify, flash, render_template, \
    redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from app import app, db, cache, limiter
from ..forms import PackageForm, UploadForm
from ..models import Package



@app.route('/add_pkgs', methods=['POST'])
@login_required
def add_pkgs():
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

            # When user add new package clean cache
            cache.delete(current_user.username)

            return redirect(url_for('info'))

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
                err_occ = False

                file_content = uploaded_file.read().decode('utf8')
                pkgs = [item.split(' - ') for item in file_content.split('\n')]

                total = 0
                for track_no, shipped_on, pkg_name in pkgs:
                    try:
                        package = Package(
                            track_no=track_no,
                            shipped_on=parse(shipped_on, dayfirst=True),
                            name=pkg_name,
                            user=current_user
                        )
                        db.session.add(package)
                        db.session.flush()

                        total += 1
                    except IntegrityError:
                        db.session.rollback()
                        continue
                    except Exception as ex:
                        err_occ = True
                        db.session.rollback()
                        flash('Error occurred while syncing data.', 'warning')
                        break

                if not err_occ:
                    db.session.commit()

                    if total:
                        flash('Sync %s packages.' % total, 'info')

                        return redirect(url_for('info'))
                    else:
                        flash('There is no packages for sync.', 'info')

            except Exception as ex:
                flash(
                    'Error occurred while reading file or invalid data format.', 'warning')

@app.route('/info', methods=['GET'])
@login_required
@cache.cached(key_prefix=lambda : current_user.username)
@limiter.limit('5/hour', key_func = lambda : current_user.username)
def info():
    # Get packages from logged user
    pkgs = Package.query.filter_by(user=current_user).all()

    packages = []
    waiting, arrived = 0, 0
    for item in pkgs:
        track_no = item.track_no
        pkg_date = item.shipped_on
        pkg_name = item.name
        send_date = datetime.combine(pkg_date, datetime.min.time())
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

        try:
            # Convert xml data to dict
            req_data = xmltodict.parse(r.text)
        except Exception as ex:
            print("Error occurred while parsing xml data: %s" % str(ex))
            continue

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

    # Make final data
    data = {
        'packages': packages,
        'info': {
            'waiting': waiting,
            'arrived': arrived,
            'total': waiting + arrived
        }
    }

    g.page = 'info'
    return render_template('info.html',
        data=data, form=PackageForm(), upload_form=UploadForm(), cached=True)


@app.route('/<track_no>/')
@login_required
@cache.cached()
@limiter.limit('5/hour', key_func = lambda : current_user.username)
def pkg_details(track_no):

    # Initial data
    data = {
        'fnl': [],
        'track_no': track_no,
        'item_name': request.args.get('item_name', 'NO PACKAGE NAME')
    }

    if len(track_no) != 13:
        return render_template('package.html', data=data, cached=True)

    r = requests.get(
        'http://www.posta.com.mk/tnt/api/query?id=%s' % track_no)

    # Convert xml data to dict
    req_data = xmltodict.parse(r.text)

    if not req_data['ArrayOfTrackingData']:
        return render_template('package.html', data=data, cached=True)

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

    return render_template('package.html', data=data, cached=True)


@app.route('/delete_pkgs/<pkgs>/', methods=['DELETE'])
@login_required
def delete_pkgs(pkgs):
    pkgs = json.loads(pkgs)

    try:
        db.session.query(Package).filter(
            Package.user_id == current_user.id,
            Package.track_no.in_(pkgs)
        ).delete(synchronize_session='fetch')

        db.session.commit()

        # When user remove packages clear the cache
        cache.delete(current_user.username)

        flash('Package/s removed successfully.', 'info')
        return "OK"

    except Exception:
        db.session.rollback()
