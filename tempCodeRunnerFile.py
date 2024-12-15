@app.route('/cancel_booking', methods=['GET', 'POST'])
def cancel_booking():
    if request.method == 'POST':
        # Get user input from the form
        user_email = request.form.get('email')
        user_name = request.form.get('Name')

        # Execute MySQL query to check if booking exists
        cursor = mysql.cursor()
        cursor.execute("DELETE FROM room_bookings WHERE email = %s AND Name = %s", (user_email, user_name))
        affected_rows = cursor.rowcount

        mysql.commit()

        if affected_rows > 0:
            return ("Booking canceled successfully.")
        else:
            return ("No booking found for the provided email and name.")

    return render_template('cancel_bookings.html')

    