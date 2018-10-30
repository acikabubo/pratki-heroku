from flask import flash, redirect, url_for
from flask_login import current_user, login_user
from app import app, db
from ..oauth import OAuthSignIn
from ..models import ExternalLogin


@app.route('/authorize/<provider>/<int:link>')
def oauth_authorize(provider, link):
    if not link and not current_user.is_anonymous:
        return redirect(url_for('info'))
    oauth = OAuthSignIn.get_provider(provider)
    oauth.link = link
    return oauth.authorize()


@app.route('/callback/<provider>/<int:link>')
def oauth_callback(provider, link):
    if not link and not current_user.is_anonymous:
        return redirect(url_for('index'))

    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))

    ext_login = ExternalLogin.query.filter_by(social_id=social_id).first()
    if not ext_login and current_user.is_authenticated:
        ext_login = ExternalLogin(
            provider=provider,
            social_id=social_id,
            nickname=username,
            email=email,
            user=current_user
        )
        db.session.add(ext_login)
        db.session.commit()

        return redirect(url_for('profile'))

    # FIXME: This code should refactor
    try:
        login_user(ext_login.user, True)
        return redirect(url_for('info'))
    except AttributeError:
        flash('You need to create regular account')
        return redirect(url_for('index'))
