from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/', methods=['GET', 'POST'])
@login_required
def admin():
    from app import db, Users 
    # Check if the current user is an admin
    if current_user.is_authenticated and current_user.is_admin:
        if request.method == 'POST':
            # Handle form submission to update admin status
            for user in Users.query.all():
                user_id = int(request.form.get(f'user_id_{ user.id }'))
                is_admin = request.form.get(f'is_admin_{user.id}') == '1'

                user = Users.query.get(user_id)
                if user:
                    user.is_admin = is_admin
                    db.session.commit()

        # Get all users and their events
        users = Users.query.all()

        # Pass the users variable to the template
        return render_template('admin.html', users=users)
    else:
        return "Unauthorized Access", 403