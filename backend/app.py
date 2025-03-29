from flask import Flask, jsonify, request, Response
from model import db, User , QuizResult , Quiz
from api.admin.admin import admin_bp
from api.user.user import user_bp
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_mail import Message, Mail
from dotenv import load_dotenv
from celery import Celery
import os
import csv
import io


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize database
with app.app_context():
    db.init_app(app)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "fallback_secret_key")
jwt = JWTManager(app)


app.config['broker_url'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/1'

# Mail Configurations
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL')  # Email from .env
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')  # Password from .env

mail=Mail(app)

def make_celery(app):
    celery = Celery(
        "app",
        broker=app.config['broker_url'],
        backend=app.config['result_backend'],
        include=['celery_worker']  # Ensures tasks from celery_worker are included
    )
    celery.conf.update(app.config)
    return celery

celery = make_celery(app)
import celery_worker

# Register Blueprints

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')

@app.route('/')
def home():
    return "Welcome to Quiz App server"


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS,PUT,DELETE")
    return response

# User login route (Generates JWT token)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=username).first()

    if user:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token, role=user.role, user=user.id), 200

    return jsonify(msg="Invalid credentials"), 401

# Protected route testing JWT
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(msg=f"Hello {current_user}, you have access!"), 200

#-----------celery task-------------------

@celery.task
def send_email(subject, recipient, body):
    with app.app_context():
        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient])
        msg.html = body  # Sending email in HTML format
        mail.send(msg)
    return f"Email sent to {recipient}"

@app.route('/send-mail')
def trigger_mail():
    # Import User model (adjust based on your structure)
    with app.app_context():
        users = User.query.filter_by(role="user").all()
        recipients = [user.email for user in users]

        if not recipients:
            return "No users found with role 'user'."

        email_body = """
        <html>
        <body>
            <h2 style="color: #2E86C1;">New Quiz Alert! 🎉</h2>
            <p>A new quiz has been added. Test your skills and improve your knowledge.</p>
            <p><strong>Click the link below to start:</strong></p>
            <a href="http://localhost:8080/" 
               style="display: inline-block; padding: 10px 20px; font-size: 16px; 
                      background-color: #28a745; color: white; text-decoration: none; 
                      border-radius: 5px;">Take the Quiz</a>
            <p>Happy Learning! 🚀</p>
        </body>
        </html>
        """

        for recipient in recipients:
            send_email.delay("New Quiz Alert!", recipient, email_body)

    return "Emails are being sent asynchronously!"




#------------------ CSV Upload ------------------

@app.route('/admin/download_csv/<int:user_id>')
def admin_download_csv(user_id):
    # Fetch user details
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Fetch quiz results for the user
    results = (
        db.session.query(
            QuizResult.id,
            Quiz.name.label("quiz_name"),
            QuizResult.quiz_id,
            QuizResult.marks_scored,
            QuizResult.total_marks,
            QuizResult.completed_at
        )
        .join(Quiz, Quiz.id == QuizResult.quiz_id)
        .filter(QuizResult.user_id == user_id)
        .all()
    )

    # Create in-memory CSV buffer
    output = io.StringIO()
    writer = csv.writer(output)

    # Write User Details Header
    writer.writerow(["User ID", "Name", "Email", "Date of Birth", "Qualification", "Role"])
    writer.writerow([user.id, user.name, user.email, user.dob, user.qualification, user.role])

    # Add a separator row
    writer.writerow([])  
    writer.writerow(["Quiz Attempts"])
    
    # Write Quiz Details Header
    writer.writerow(["Result ID", "Quiz Name", "Quiz ID", "Marks Scored", "Total Marks", "Completed At"])
    
    # Write Quiz Results Data
    for r in results:
        completed_at = r.completed_at.strftime("%Y-%m-%d %H:%M:%S") if r.completed_at else ""
        writer.writerow([r.id, r.quiz_name, r.quiz_id, r.marks_scored, r.total_marks, completed_at])

    # Move cursor to the start
    output.seek(0)

    # Return response with CSV file
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=user_{user_id}_details.csv"}
    )


@app.route('/user/<int:user_id>/download_csv')
def user_download_csv(user_id):
    # Fetch all quiz results for the user
    results = (
        db.session.query(
            QuizResult.id,
            Quiz.name.label("quiz_name"),
            QuizResult.quiz_id,
            QuizResult.marks_scored,
            QuizResult.total_marks,
            QuizResult.completed_at
        )
        .join(Quiz, Quiz.id == QuizResult.quiz_id)
        .filter(QuizResult.user_id == user_id)
        .all()
    )

    if not results:
        return jsonify({"message": "No results found for this user"}), 404

    # Create in-memory CSV buffer
    output = io.StringIO()
    writer = csv.writer(output)

    # Write CSV headers
    writer.writerow(["Result ID", "Quiz Name", "Quiz ID", "Marks Scored", "Total Marks", "Completed At"])

    # Write quiz results data
    for r in results:
        completed_at = r.completed_at.strftime("%Y-%m-%d %H:%M:%S") if r.completed_at else ""
        writer.writerow([r.id, r.quiz_name, r.quiz_id, r.marks_scored, r.total_marks, completed_at])

    # Move cursor to the start
    output.seek(0)

    # Return response with CSV file
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=user_{user_id}_quiz_results.csv"}
    )


if __name__ == "__main__":
    app.run(debug=True, port=8000)
