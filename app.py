from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Route to display the form
@app.route('/', methods=['GET'])
def input_form():
    """Displays the user input form."""
    return render_template('input_form.html')


# Route to handle the submitted form data
@app.route('/submit', methods=['POST'])
def submit_data():
    """Handles the form submission and retrieves data."""
    if request.method == 'POST':
        # Accessing form data using the 'name' attributes from the HTML form
        user_name = request.form.get('user_name', 'N/A')  # .get() is safer, provides default if key missing
        message_prompt = request.form.get('message_prompt')

        # --- Backend Processing ---
        # At this point, you have 'user_name' and 'message_prompt'
        # You can now:
        # 1. Process this data (e.g., generate emails based on the prompt)
        # 2. Store it in a database
        # 3. Call other functions/APIs
        # etc.

        print("---- Data Received at Backend ----")
        print(f"User Name: {user_name}")
        print(f"Message Prompt: {message_prompt}")
        print("---------------------------------")

        # For demonstration, let's pass the data back to the form template
        # In a real application, you might redirect to a success page or another part of your app.
        # return redirect(url_for('input_form')) # Simple redirect
        return render_template('input_form.html',
                               submitted_name=user_name,
                               submitted_prompt=message_prompt)

    # If someone tries to access /submit via GET, redirect them to the form
    return redirect(url_for('input_form'))

if __name__ == '__main__':
    # Setting debug=True is useful for development as it provides detailed error pages
    # and auto-reloads the server when you make code changes.
    # Port can be changed if 5000 is in use.
    app.run(debug=True, port=5001)