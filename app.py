#app.py
from flask import Flask, render_template, redirect, request, flash
from dbhelper import *
import os

app = Flask(__name__)
uploadfolder = 'static/img/'
app.config['SECRET_KEY'] = '!@#$%^'
app.config['UPLOAD_FOLDER'] = uploadfolder

def get_users() -> object:
	return getall_records('registrations')

def get_user(idno:str) -> object:
	return getone_record('registrations', idno=idno)

def substringer(s, phrase):
    i = s.find(phrase)
    return s[i + len(phrase):] if i != -1 else ''

@app.route('/register', methods=['POST'])
def register():
    idno: str = request.form['idno']
    lastname: str = request.form['lastname']
    firstname: str = request.form['firstname']
    course: str = request.form['course']
    level: str = request.form['level']
    flag: str = request.form['flag']
    file: object = request.files['uploadimage']

    # Validate that idno contains only digits
    if not idno.isdigit():
        flash("Error: ID Number must contain only digits!", 'error')  # Red for error
        return redirect('/')

    existing_user = get_user(idno)
    
    # Check if the user already exists
    if existing_user and flag == '0':  
        flash(f"User ID '{idno}' already exists!", 'warning')
        return redirect('/') 

    imagename = ''
    if file.filename != '':
        filename, extension = os.path.splitext(file.filename)
        imagename = os.path.join(uploadfolder, f'{filename}{idno}{extension}')
    
    try:
        ok: bool = False
        if flag == '0':  # Register new user
            if file.filename != '':
                ok = add_record('registrations', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level, image=imagename)
            else:
                ok = add_record('registrations', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level)
            
            # Flash message for registration success or failure
            msg: str = "New User Registered!" if ok else "Error Registering User!"
            flash(msg, 'success' if ok else 'error')  # Green for success, red for error
            
        else:  # Update existing user
            if file.filename != '':
                ok = update_record('registrations', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level, image=imagename)
            else:
                ok = update_record('registrations', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level)
            
            # Flash message for update success or failure
            msg: str = "User Updated Successfully!" if ok else "Error Updating User!"
            flash(msg, 'success' if ok else 'error')  # Green for success, red for error
        
        if file.filename != '' and ok:
            file.save(imagename)
    except Exception as e:
        flash(f"File Saving Error: {e}", 'error')  # Red for file saving errors
        print(e)
    
    return redirect('/')

@app.route('/delete_user', methods=['POST'])
def delete_user():
    idno: str = request.form['idno']
    imagename: str = get_user(idno)[0]['image']
    ok: bool = delete_record('registrations', idno=idno)
    
    # Flash message based on the outcome of deletion
    if ok:
        message: str = "User Deleted: User deleted successfully!"
        flash(message, 'success')  # Green for success
    else:
        message: str = "Error Deleting User: Something went wrong"
        flash(message, 'error')  # Red for error
    
    try:
        if os.path.exists(imagename):
            os.remove(imagename)
    except Exception as e:
        flash(f"Error within '/delete_user': File path error", 'error')  # Red for file errors
        print(e)
    
    return redirect('/')



@app.route('/')
def index():
    users = get_users()  # Ensure this is fetching data correctly
    return render_template('index.html', pagetitle='Registration', users=users)


if __name__ == '__main__':
	app.run(debug=True)
	