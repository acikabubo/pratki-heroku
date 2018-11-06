from flask import g, redirect, url_for, render_template, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from ..forms import RegistrationForm, LoginForm, ChangePasswordForm
from ..models import User, ExternalLogin


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('info'))

    form = LoginForm(prefix='l')

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid credentials', 'warning')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('info'))

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/unlink/<provider>')
@login_required
def unlink(provider):
    ext_login = ExternalLogin.query.filter_by(
        provider=provider, user=current_user).first()

    db.session.delete(ext_login)
    db.session.commit()

    flash('Unlink %s' % provider.title(), 'info')

    return redirect(url_for('profile'))


@app.route('/profile')
@login_required
def profile():
    ext_auths = app.config['OAUTH_CREDENTIALS'].keys()

    used_ext_auths = {item: False for item in ext_auths}

    data = {'linked': []}

    for item in current_user.ext_logins:
        ext_auth, _ = item.social_id.split('$')

        if ext_auth in ext_auths:
            data['linked'].append(ext_auth)

        used_ext_auths[ext_auth] = True

    data['unlinked'] = list(set(ext_auths) - set(data['linked']))

    g.page = 'profile'
    return render_template('profile.html',
        data=data, cp_form=ChangePasswordForm())


@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        user = current_user
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Your password was changed successfully. Please login again.')

        return redirect(url_for('logout'))

    return redirect(url_for('profile'))
