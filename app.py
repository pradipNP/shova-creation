from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_mail import Mail, Message
import os
import json
import random

app = Flask(__name__)
app.secret_key = 'shova_creation_2025_@secret!'

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'shova1creation2@gmail.com'
app.config['MAIL_PASSWORD'] = 'xjmlvfjxdihmqgts'
app.config['MAIL_DEFAULT_SENDER'] = 'shova1creation2@gmail.com'

mail = Mail(app)

# Rating file path
RATING_FILE = 'ratings.json'


# ===== Utility Functions =====
def load_ratings():
    """Load all ratings from file."""
    if os.path.exists(RATING_FILE):
        with open(RATING_FILE, 'r') as f:
            data = json.load(f)
            return data.get("votes", [])
    return []


def save_rating(rating):
    votes = load_ratings()
    votes.append(int(rating))  # force int
    with open(RATING_FILE, 'w') as f:
        json.dump({"votes": votes}, f)



# ===== Routes =====

@app.route('/')
def index():
    # Load portfolio images
    image_folder = os.path.join(app.static_folder, 'images/portfolio')
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    random.shuffle(image_files)

    # Load ratings
    votes = load_ratings()
    total_votes = len(votes)
    avg_rating = round(sum(votes) / total_votes, 2) if total_votes > 0 else 0

    return render_template('index.html', images=image_files, avg_rating=avg_rating, total_votes=total_votes)


@app.route('/submit-rating', methods=['POST'])
def submit_rating():
    try:
        data = request.get_json()
        rating = int(data.get("rating"))
        if 1 <= rating <= 5:
            save_rating(rating)
            return jsonify({"message": "Rating submitted successfully!"}), 200
        return jsonify({"message": "Invalid rating."}), 400
    except Exception as e:
        return jsonify({"message": "Error submitting rating."}), 500



@app.route('/get-rating')
def get_rating():
    votes = load_ratings()
    int_votes = [int(v) for v in votes if str(v).isdigit()]
    total_votes = len(int_votes)
    average = round(sum(int_votes) / total_votes, 2) if total_votes > 0 else 0
    return jsonify({'average': average, 'count': total_votes})



@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/portfolio')
def portfolio():
    image_folder = os.path.join(app.static_folder, 'images/portfolio')
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    random.shuffle(image_files)
    return render_template('portfolio.html', images=image_files)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if name and email and message:
            try:
                msg = Message('New Contact Form Submission',
                              recipients=['shova1creation2@gmail.com'])
                msg.body = f"""
New message from Shova Creation Website:

Name: {name}
Email: {email}
Message:
{message}
                """
                mail.send(msg)
                flash("Thank you for contacting us! We'll get back to you soon.", 'success')
            except Exception:
                flash("Something went wrong while sending the message. Please try again later.", 'danger')
        else:
            flash("Please fill out all fields.", 'danger')

        return redirect(url_for('contact'))

    return render_template('contact.html')


@app.route('/contact-home', methods=['POST'])
def contact_home():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if name and email and message:
        try:
            msg = Message('New Contact Form Submission (Homepage)',
                          recipients=['shova1creation2@gmail.com'])
            msg.body = f"""
New message from Shova Creation Homepage:

Name: {name}
Email: {email}
Message:
{message}
            """
            mail.send(msg)
            flash("Thank you for contacting us! We'll get back to you soon.", 'success')
        except Exception:
            flash("Something went wrong while sending your message. Please try again later.", 'danger')
    else:
        flash("Please fill out all fields.", 'danger')

    return redirect(url_for('index'))


@app.route('/test-email')
def test_email():
    try:
        msg = Message("Test Email from Shova Creation", recipients=["shova1creation2@gmail.com"])
        msg.body = "This is a test email to verify Flask-Mail."
        mail.send(msg)
        return "Test email sent!"
    except Exception:
        return "Failed to send test email."


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/debug-files")
def debug_files():
    import os
    files = os.listdir("static/images")
    return "<br>".join(files)



# ===== Run Server =====
if __name__ == '__main__':
    app.run(debug=True)
