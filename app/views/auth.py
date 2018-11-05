from flask import flash, redirect, url_for
from flask_login import current_user, login_user
from app import app, db
from ..oauth import OAuthSignIn
from ..models import User, ExternalLogin


@app.route('/authorize/<provider>/<int:link>')
def oauth_authorize(provider, link):
    if not link and not current_user.is_anonymous:
        return redirect(url_for('info'))
    oauth = OAuthSignIn.get_provider(provider)
    oauth.link = link
    return oauth.authorize()


@app.route('/callback/<provider>/<int:link>')
def oauth_callback(provider, link):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))

    # Get exteral login data filtered by social id
    ext_login = ExternalLogin.query.filter_by(
        social_id=social_id).first()

    try:
        user = ext_login.user
    except AttributeError:
        user = current_user
    
    # If external login does not exist create new one
    if not ext_login:    
        if not current_user.is_authenticated:
            # Get user by username
            user = User.query.filter_by(username=username).first()

            # If user does not exist create new one
            if not user:
                user = User(username=username, email=email)
                db.session.add(user)
                # Get id before insert
                db.session.flush()
        
        ext_login = ExternalLogin(
            provider=provider,
            social_id=social_id,
            nickname=username,
            email=email,
            user=user
        )
        db.session.add(ext_login)
        db.session.commit()

        user = ext_login.user

    # Login user and redirect to info page
    login_user(user, True)
    return redirect(url_for('info'))

    # # FIXME: This code should refactor
    # try:
    #     login_user(ext_login.user, True)
    #     return redirect(url_for('info'))
    # except AttributeError:
    #     flash('You need to create regular account')
    #     return redirect(url_for('index'))
