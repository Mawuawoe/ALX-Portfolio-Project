#!/usr/bin/env python3
"""
Web Application using Flask for Managing Salinity Data
Author:
    Your Name (Desmond Dzakago)
"""


from flask import Flask, Response, render_template, request, redirect, url_for, flash
import sys
sys.path.append("../")
from models import storage
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models.user import User
from models.pan import Pan
from models.salinity import Salinity
import os
from datetime import date, datetime
import pandas as pd
from io import StringIO


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key') # secret key for session management
app.config['SESSION_COOKIE_SECURE'] = True  # or False for HTTP


# # Flask-Login setup for session management
login_manager = LoginManager()
login_manager.init_app(app)
# Redirect users to login page if not authenticated
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    """Load user from the database by user ID (used by Flask-Login)."""
    return storage.get_by_id(User, user_id)

# Define a UserMixin class to bridge with SQLAlchemy user model
class AuthUser(UserMixin):
    """Wrapper for the User class to be compatible with Flask-Login."""
    def __init__(self, user):
        self.id = str(user.id) # Flask-Login requires user IDs as strings
        self.username = user.username
        self.email = user.email

#function to retrive pan.id by the pan_id submited
def get_id_of_pan(pan_id):
    """
    Retrieve the internal ID of a pan by its pan identifier
    """
    pan_objs = storage.all(Pan).values()
    for pan in pan_objs:
        if pan_id == pan.pan_id:
            return pan.id

def generate_pan_ids():
    """
    Generate a list of pan IDs.
    """
    # Initialize an empty list
    t_pan_ids = []
    # Generate Pan IDs from Pan1 to Pan32
    t_pan_ids.extend(f'Pan{i}' for i in range(1, 33))  # 1 to 32
    # Generate Reservoir IDs from R1 to R5
    t_pan_ids.extend(f'R{i}' for i in range(1, 6))  # 1 to 5
    # Add PCR IDs
    t_pan_ids.extend(['PCRA', 'PCRB'])

    return t_pan_ids


def generate_filter_pan_ids(selected_filter):
    """
    Generate a list of pan IDs based on the selected filter.
    """
    # Initialize an empty list
    pan_ids = []

    # Depending on the filter, generate the appropriate pan_ids list
    if selected_filter == 'pan' or selected_filter == '':
        pan_ids.extend(f'Pan{i}' for i in range(1, 33))  # 1 to 32
    if selected_filter == 'reservoir' or selected_filter == '':
        pan_ids.extend(f'R{i}' for i in range(1, 6))  # 1 to 5
    if selected_filter == 'pcr' or selected_filter == '':
        pan_ids.extend(['PCRA', 'PCRB'])

    return pan_ids


@app.route('/')
def index():
    """Redirects to the login page."""
    return render_template('landing_page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login route to authenticate users. Displays login form on GET and 
    handles authentication on POST.
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print(f"Email: {email}, Password: {password}")  # Debugging line

        # Fetch the user from the database
        try:
            user = storage.get_first_by(User, email=email)
        except Exception as e:
            flash('An error occurred while processing your request.', 'danger')
            return render_template('login.html')
        # Check if user exists and if the password is correct
        if user and user.check_password(password):
            auth_user = AuthUser(user)
            login_user(auth_user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.', 'danger')
            return render_template('login.html')  # Render with error message

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    """
    Displays the dashboard with salinity data based on filter and date.
    """
    admin_email = 'desmonddzakago@gmail.com' # Admin email for special permissions
    selected_filter = request.args.get('filter', '') # Filter type (pan, reservoir, PCR)
    selected_date = request.args.get('date', date.today().isoformat()) # Selected date
    date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()

    # Generate pan IDs and retrieve salinity data
    t_pan_ids = generate_pan_ids()

    today_salinity = storage.get_all_by_date(Salinity, date_obj)

    # Organize salinity records
    today_records_dict = {}
    for t_pan_id in t_pan_ids:
        # Filter records by pan/reservoir/PCR
        today_salinity_by_pan = storage.get_all_salinity_by_pan(today_salinity, 'pan_id', t_pan_id)
        # Get the latest entry for the current pan/reservoir/PCR
        today_latest_entry = storage.get_latest_record(today_salinity_by_pan)
        if today_latest_entry:
            # Store the full instance if there's valid data
            today_records_dict[t_pan_id] = today_latest_entry
        else:
            # If no data is available, store "NA" for salinity_level and brine_level
            today_records_dict[t_pan_id] = {
                "salinity_level": "NA",
                "brine_level": "NA"
            }

    pan_ids = generate_filter_pan_ids(selected_filter)
    #fetch all salinity records from today
    salinity_records_today = storage.get_all_by_date(Salinity, date_obj)
    
    # Dictionary to store the latest records for each pan
    latest_records_dict = {}
    for pan_id in pan_ids:
        # Filter records by pan/reservoir/PCR
        salinities_for_current_pan = storage.get_all_salinity_by_pan(salinity_records_today, 'pan_id', pan_id)
        # Get the latest entry for the current pan/reservoir/PCR
        latest_entry = storage.get_latest_record(salinities_for_current_pan)
        if latest_entry:
            # Store the full instance if there's valid data
            latest_records_dict[pan_id] = latest_entry
        else:
            # If no data is available, store "NA" for salinity_level and brine_level
            latest_records_dict[pan_id] = {
                "salinity_level": "NA",
                "brine_level": "NA"
            }

    return render_template('dashboard.html',
                           is_admin=current_user.email == admin_email,
                           latest_salinity_records=latest_records_dict,
                           selected_filter=selected_filter,
                           today_records=today_records_dict,
                           selected_date=selected_date
                           )

@app.route('/report_page', methods=['GET', 'POST'])
@login_required
def report_page():
    """
    Renders the report page, allowing users to filter salinity records by date and type.
    
    - On GET: Displays an empty form for selecting a date and filter type.
    - On POST: Filters salinity records based on the selected date and filter type, 
      and renders the results in the template.
    """
    selected_date = request.args.get('date')
    selected_filter = request.args.get('filterType')
    if request.method == 'POST':
        selected_date = request.form.get('date', date.today().isoformat())
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
        selected_filter = request.form.get('filterType', '')

        pan_ids = generate_filter_pan_ids(selected_filter)

        #fetch all salinity records from today
        salinity_records_by_date = storage.get_all_by_date(Salinity, date_obj)
        
        # Dictionary to store records for each pan
        salinity_records = {}

        for pan_id in pan_ids:
            # Filter records by pan/reservoir/PCR
            salinities_for_pan_id = storage.get_all_salinity_by_pan(salinity_records_by_date, 'pan_id', pan_id)

            if salinities_for_pan_id:
                salinity_records[pan_id] = salinities_for_pan_id
            else:
                salinity_records[pan_id] = [{
                    "salinity_level": "NA",
                    "brine_level": "NA"
                }]
        return render_template('report_page.html',
                               salinity_records=salinity_records,
                               selected_date=selected_date,
                               selected_filter=selected_filter)
    return render_template('report_page.html',
                           salinity_records={},
                           selected_date=selected_date,
                           selected_filter=selected_filter)


@app.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    """
    Handles the creation of an admin user in the application.
    
    - On GET: Displays the admin creation form.
    - On POST: Validates the form inputs and creates an admin user if the environment is set to 'dev' 
      and the provided email is not already registered.
    """
    if request.method == 'POST':
        if os.getenv('FLASK_ENV') != 'dev':
            flash('Access denied.', 'danger')
            return redirect(url_for('login'))

        admin_email = 'desmonddzakago@gmail.com'
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        contact = request.form['contact']
        password = request.form['password']

        # Check if the email already exists
        if storage.get_first_by(User, email=email):
            flash('Email already registered', 'danger')
            return redirect(url_for('create_admin'))
        
        # Create a admin user
        admin_user1 = User(email=email,
                           first_name=firstname,
                           last_name=lastname,
                           username=username,
                           contact_info=contact
                           )
        
        admin_user1.set_password(password)  # Hash the password before storing it

        # Save to the database
        admin_user1.save()

        flash('Admin user created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('create_admin.html')  # Render the form when GET


@app.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    """
    Handles the creation of a new user in the application, accessible only to the admin user.
    - On GET: Displays the user creation form.
    - On POST: Validates form inputs and creates a new user if the current user is an admin and the provided 
      email is not already registered.
    """
    admin_email = 'desmonddzakago@gmail.com'
    if current_user.email != admin_email:
        flash('Access denied. Only admin can create new users.', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        contact = request.form['contact']
        password = request.form['password']

        # Check if the email already exists
        if storage.get_first_by(User, email=email):
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        
        # Creates a user
        new_user = User(email=email,
                           first_name=firstname,
                           last_name=lastname,
                           username=username,
                           contact_info=contact
                           )
        # Hash the password before storing it
        new_user.set_password(password)

        # Save to the database
        new_user.save()

        flash('User created successfully!', 'success')
        return redirect(url_for('login'))
    
    flash('Only admin can create new users.', 'info')
    return render_template('register.html')


@app.route('/data_entry', methods=['GET', 'POST'])
@login_required
def data_entry():
    """
    Handles the data entry page for users.
    - On GET: Displays the data entry form for users to input relevant data.
    """
    if request.method == 'GET':
        return render_template('data_entry.html')
    

@app.route('/add_record', methods=['POST'])
@login_required
def add_record():
    """
    Handles the submission of new salinity and brine level records.
    """
    #get data from form
    salinity_level =int(request.form['salinity'])
    brine_level=int(request.form["brine"])
    id_pan = get_id_of_pan(request.form["pan"])
    brine_attendant_id = current_user.id

    #add record
    salinity_reading = Salinity(
        salinity_level=salinity_level,
        brine_level=brine_level,
        pan_id=id_pan,
        brine_attendant_id=brine_attendant_id
    )

    # Save to the database
    salinity_reading.save()

    # Flash success message
    flash(f'Salinity data for {request.form["pan"]} submitted successfully!', 'success')

    # Redirect to the data entry page or dashboard
    return redirect(url_for('data_entry'))


@app.route('/update_record', methods=['POST'])
@login_required
def update_record():
    """
    Update the latest existing salinity record for a specific pan,
    or create a new one if none exists.
    """
    # Get data from form
    salinity_level = int(request.form['salinity'])
    brine_level = int(request.form["brine"])
    id_pan = get_id_of_pan(request.form["pan"])
    brine_attendant_id = current_user.id

    if id_pan is None:
        flash('Invalid Pan selected!', 'error')
        return redirect(url_for('data_entry'))

    # Fetch today's salinity records and filter by Pan
    salinity_records_today = storage.get_all_by_date(Salinity, date.today())
    salinities_of_pan = storage.get_all_salinity_by_pan(salinity_records_today, 'id', id_pan)

    # Get latest entry
    latest_entry = storage.get_latest_record(salinities_of_pan)

    # Data to be updated
    data = {
        "salinity_level": salinity_level,
        "brine_level": brine_level,
        "pan_id": id_pan,
        "brine_attendant_id": brine_attendant_id
    }

    # Update existing record if found, otherwise create new record
    if latest_entry:
        for key, value in data.items():
            setattr(latest_entry, key, value)
        latest_entry.save()
        flash(f'Salinity data for {request.form["pan"]} updated successfully!', 'success')
    else:
        salinity_reading = Salinity(
            salinity_level=salinity_level,
            brine_level=brine_level,
            pan_id=id_pan,
            brine_attendant_id=brine_attendant_id
        )
        salinity_reading.save()
        flash(f'Salinity data for {request.form["pan"]} submitted successfully!', 'success')

    # Redirect to the data entry page or dashboard
    return redirect(url_for('data_entry'))


@app.route('/handle_selection', methods=['POST'])
@login_required
def handle_selection():
    """
     Handles user selection actions for updating or deleting salinity records.
    """
    action = request.form.get('action')
    selected_pan_ids = request.form.getlist('selected_pan_ids')
    selected_date = request.form.get('selected_date')
    selected_filter = request.form.get('selected_filter')

    if action == 'update' and selected_pan_ids:
        # only one record is allowed for update at a time
        return redirect(url_for('update', pan_id=selected_pan_ids[0]))
    elif action == 'delete' and selected_pan_ids:
        for pan_id in selected_pan_ids:
            record = storage.get_by_id(Salinity, pan_id)
            if record:
                print(record)
                storage.delete(record)
    return redirect(url_for('report_page', date=selected_date, filterType=selected_filter ))


@app.route('/update/<pan_id>', methods=['GET', 'POST'])
@login_required
def update(pan_id):
    """
    Updates the salinity and brine level of a specific pan record.
    """
    record = storage.get_by_id(Salinity, pan_id)
    if request.method == "GET":
        print(record)
        return render_template('update.html', record=record)
    
    if request.method == 'POST':
        print(record)
        # Handle the form submission to update the record
        new_salinity = int(request.form['salinity'])
        setattr(record, "salinity_level", new_salinity)
        new_brine = int(request.form["brine"])
        setattr(record, 'brine_level', new_brine)
            
        #save changes
        record.save()

        flash(f'Salinity data updated successfully!', 'success')
        return redirect(url_for('update', pan_id=record.id))


@app.route('/logout')
@login_required
def logout():
    """
    Logs the current user out of the application.
    """
    logout_user()  # This function logs the user out
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))  # Redirect to the login page


@app.route('/download_csv', methods=['POST'])
@login_required
def download_csv():
    """
    Generates and downloads a CSV file of salinity records filtered by date and pan type
    """

    # Get the selected date and filter from the form
    selected_date = request.form.get('selected_date')
    selected_filter = request.form.get('selected_filter')

    # Check if a date was selected
    if not selected_date:
        return redirect(url_for('report_page'))  
    
    # retrieve by date
    try:
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        return redirect(url_for('report_page')) 
    
    salinity_records_by_date = storage.get_all_by_date(Salinity, date_obj)

    # Create a list to hold all records
    records = []

    pan_ids = generate_filter_pan_ids(selected_filter)

    # Populate the records list with data
    for pan_id in pan_ids:
        salinities_for_pan_id = storage.get_all_salinity_by_pan(salinity_records_by_date, 'pan_id', pan_id)

        if salinities_for_pan_id:
            for record in salinities_for_pan_id:
                records.append({
                    'Pan ID': pan_id,
                    'Date': record.updated_at,
                    'Salinity Level': record.salinity_level,
                    'Brine Level': record.brine_level
                })
        else:
                records.append({
                    'Pan ID': pan_id,
                    'Date': "NA",
                    'Salinity Level': "NA",
                    'Brine Level': "NA"
                })

        
    # Create a DataFrame from the records
    df = pd.DataFrame(records)

    # Create a StringIO buffer
    output = StringIO()

    # Use the to_csv method to write to the response
    df.to_csv(output, index=False)

    # Get the CSV content from the buffer
    csv_content = output.getvalue()

    # Close the StringIO buffer
    output.close()

    # Create a CSV response
    response = Response(csv_content, content_type='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=salinity_records.csv'

    return response


@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes the current database session after each request.
    """
    storage.close()


if __name__ == '__main__':
    app.run(debug=True)
