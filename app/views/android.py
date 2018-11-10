import os
import dropbox
import requests
import xmltodict
from dateutil.parser import parse
from datetime import datetime, time
from flask import request, jsonify, render_template
from app import app, cache


@app.route('/android')
@cache.cached()
def android():
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

    packages = []
    if not data:
        return jsonify(packages)

    pkgs = [item.split(' - ') for item in data.split('\n')]

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

    # # Return raw json data (for android app)
    # if request.user_agent.platform == 'android' and request.is_json:
    if request.is_json:
        return jsonify(packages)


@app.route('/android/<track_no>/')
@cache.cached()
def android_detail(track_no):
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
