from flask import Flask, render_template, request, redirect, url_for
import bcrypt
import pymysql
import pymysql.cursors
from flask import session



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12ad34cfShiva#'
app.config['MYSQL_DB'] = 'hotel_management'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' 

mysql = pymysql.connect(host=app.config['MYSQL_HOST'],
                        user=app.config['MYSQL_USER'],
                        password=app.config['MYSQL_PASSWORD'],
                        db=app.config['MYSQL_DB'],
                        cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        FullName = request.form['FullName']
        DateOfBirth = request.form['DateOfBirth']
        Address = request.form['Address']
        Phone = request.form['Phone']
        Email = request.form['Email']
        Password = request.form['Password']
        ID_proof = request.form['ID_proof']
        hashed_password = bcrypt. hashpw(Password.encode('utf-8'), bcrypt.gensalt())
        # Create MySQL connection
        cursor = mysql.cursor()
        # Execute query to insert data
        cursor.execute("INSERT INTO useres (FullName, DateOfBirth, Address, Phone, Email, Password, ID_proof) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                     (FullName, DateOfBirth, Address, Phone, Email, hashed_password , ID_proof))

        # Commit changes to database
        mysql.commit()

        # Close cursor
        cursor.close()  

        return 'You are now logged in! Welcome to Hotel AATHITYAM'

    return render_template('signup.html')



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        Email = request.form.get('Email')
        Password = request.form.get('Password')

        if not Email or not Password:
            return "Please enter your correct Email and password."

        cursor = mysql.cursor()
        cursor.execute("SELECT * FROM useres WHERE Email= %s", (Email,))
        user = cursor.fetchone()
        if user:
            session['Email'] = Email
            return "You are existing user. Continue to book a room"
            
        else:
            return "User does not exist. Please sign up."

    return render_template('login.html')


    
@app.route('/book_room', methods=['GET', 'POST'])
def book_room():
    
    if request.method == 'POST':
        Booking_type = request.form['Booking_type']
        room_type = request.form['room_type']
        check_in = request.form['check_in']
        check_out = request.form['check_out']
        Name = request.form['Name']
        phone_number = request.form['phone_number']
        Address = request.form['Address']
        ID_proof = request.form['ID_proof']
        no_of_people = request.form['no_of_people']
        payment_mode = request.form['payment_mode']
        email = request.form['email']
        location = request.form['location']
        cursor = mysql.cursor()
        cursor.execute("INSERT INTO room_bookings(Booking_type, room_type, check_in, check_out, Name, phone_number, Address, ID_proof, no_of_people, payment_mode,email,location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",
                       (Booking_type, room_type, check_in, check_out, Name, phone_number, Address, ID_proof, no_of_people, payment_mode,email,location))
        mysql.commit()
        cursor.close()

        return 'Congratulations You have successfully booked your Room WELCOME TO HOTEL AATHITYAM. We are happy that you choose us looking for you to give best hospitality. '
     
    return render_template('room_booking.html')

@app.route('/staff_details',methods=['GET', 'POST'])
def staff_details():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM staff_details")
    data = cursor.fetchall()
    return render_template('staff_details.html', data=data)



@app.route('/cusines',methods=['GET', 'POST'])
def cusines():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM food_menu")
    data = cursor.fetchall()
    return render_template('food_menu.html', data=data)

@app.route('/our_rooms')
def our_rooms():
    return render_template("our_rooms.html")

@app.route('/amenities')
def features():
    return render_template("amenities.html")

@app.route('/contact_us', methods=['GET','POST'])
def contact_us():
    if request.method == 'POST':
        Name = request.form.get('Name')
        email = request.form.get('email')
        with mysql.cursor() as cursor:
            sql = "SELECT * FROM room_bookings WHERE Name=%s AND email=%s"
            cursor.execute(sql, (Name, email))
            result = cursor.fetchone()

        if result:
            return 'Thank You for your valuable feedback. Hope you have enjoyed your stay and we look forwaard for you comeback!!!'
        else:
            return 'Sorry! Please book a room. Feedback can only be given by the people who booked or stayed in our hotel. Regrets for any inconvienience .'
    
    return render_template('contact_us.html')




@app.route('/hotel_branch',methods=['GET', 'POST'])
def hotel_branch():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM hotel_branch")
    data = cursor.fetchall()
    return render_template('hotel_branch.html', data=data)

    
@app.route('/rooms',methods=['GET', 'POST'])
def rooms():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM rooms")
    data = cursor.fetchall()
    return render_template('rooms.html', data=data)

@app.route('/cancel_booking', methods=['GET', 'POST'])
def cancel_booking():
    if request.method == 'POST':
        # Get user input from the form
        user_name = request.form.get('Name')
        user_email = request.form.get('email')  # Ensure the case of 'Name' matches the form field name

        # Construct the SQL query to fetch the tuple
        with mysql.cursor() as cursor:
            select_query = "SELECT * FROM room_bookings WHERE Name = %s AND email = %s"
            cursor.execute(select_query, (user_name, user_email))
            booking_data = cursor.fetchone()

            # If a booking exists, delete it
            if booking_data:
                delete_query = "DELETE FROM room_bookings WHERE Name = %s AND email = %s"
                cursor.execute(delete_query, (user_name, user_email))
                mysql.commit()
                return "Room booking has been canceled."
            else:
                return "No bookings found for the provided name and email."

    return render_template('cancel_bookings.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)


