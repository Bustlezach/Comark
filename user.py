from flask import (
    Blueprint, render_template, redirect, url_for
)

user = Blueprint(
    "user", __name__, static_folder="static", template_folder="templates"
    )


@user.route('/')
def user_page():
    return render_template('user.html')


@user.route('/addPost', methods=['POST'])
def add_post():
    return redirect(url_for('user_page'))


@user.route('/update', methods=['POST'])
def update():
    return redirect(url_for('user_page'))


@user.route('/signUp')
def sign_up():
    return "<p>Sign up here!</p>"


# @user.route('/user_page')
# def user_page():
#     return render_template('homepage.html')