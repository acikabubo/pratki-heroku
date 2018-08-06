import dropbox
import requests
import xmltodict
from dateutil.parser import parse
from datetime import datetime, time
from flask import Flask, jsonify, request
from flask_table import Table, Col


# Initialize flask app
app = Flask(__name__)


class PratkiTable(Table):
    no_items = 'There is no packages'
    html_attrs = {'align': 'center'}
    border = True

    track_no = Col('Tracking #',
        td_html_attrs={
            'align': 'center', 'width': '150', 'height': '30'
        }, th_html_attrs={
            'height': "50"
        }
    )
    shipped_ago = Col('Shipped ago (days)',
        td_html_attrs={
            'align': 'right', 'width': '150'
        }
    )
    info_date = Col('Info/Date',
        td_html_attrs={
            'align': 'center', 'width': '150'
        }
    )
    notice = Col('Notice',
        td_html_attrs={
            'align': 'left', 'width': '150'
        }
    )
    pkg_name = Col('Item name', td_html_attrs={
        'align': 'left', 'width': '400'
    })


@app.route('/')
def main():
    dbx = dropbox.Dropbox(
        "k3RJ3XBM0RsAAAAAAAADijeXigTJllDcGbCd_u54PNwO0WjtNLEXXaMddvijWBdS")

    try:
        # Try to read file from dropbox
        md, res = dbx.files_download('/pratki.txt')
    except Exception:
        return '<h1 align="center">Unknown file</h1>'

    # Decode bytes to string
    data = res.content.decode("utf-8")

    if not data:
        return '<h1 align="center">There is no packages</h1>'

    pkgs = [item.split(' - ') for item in data.split('\n')]

    fnl_data = []

    for track_no, pkg_date, pkg_name in pkgs:
        send_date = parse(pkg_date, dayfirst=True)
        shipped_ago = (datetime.now() - send_date).days

        if len(track_no) != 13:
            fnl_data.append({
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
            fnl_data.append({
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

        fnl_data.append({
            'track_no': track_no,
            'shipped_ago': shipped_ago,
            'info_date': pkg_date,
            'notice': pkg_notice,
            'pkg_name': pkg_name
        })

    # Sort by shipped ago
    fnl_data = sorted(fnl_data, key=lambda k: k['shipped_ago'])

    # Return raw json data
    if request.is_json:
        return jsonify(fnl_data)

    # Populate and send html table
    table = PratkiTable(fnl_data)
    return table.__html__()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
