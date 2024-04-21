from flask import render_template, Blueprint
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/myuser', methods=['GET'])
@login_required
def myuser():
    return render_template('myuser.html', username=current_user.username)

