from app import app, mail, celery  # Import Flask app and mail from app.py
from celery.schedules import crontab
from flask_mail import Message
from model import db, User, QuizResult , Quiz
from datetime import datetime, timedelta

# Periodic Task Scheduling
celery.conf.beat_schedule = {
    "daily-reminder": {
        "task": "celery_worker.send_daily_email",
        "schedule": crontab(minute=00,hour=00),  # Runs daily at midnight
    },
    "every-minute-task": {
        "task": "celery_worker.send_periodic_email",
        "schedule": crontab(minute=0, hour=0, day_of_month=1),  # Run on the first day of every month
    }
}
celery.conf.timezone = "Asia/Kolkata"


@celery.task(name='celery_worker.send_daily_email')
def send_daily_email():
    """Send daily reminders to users who haven't attempted all available quizzes."""
    with app.app_context():
        total_quizzes = Quiz.query.count()  # Get total number of quizzes

        if total_quizzes == 0:
            print("No quizzes available. Skipping email reminders.")
            return "No quizzes available."

        users = User.query.filter_by(role="user").all()

        for user in users:
            attempted_quiz_count = db.session.query(QuizResult.quiz_id).filter(
                QuizResult.user_id == user.id
            ).distinct().count()  # Count distinct quizzes attempted by the user

            if attempted_quiz_count < total_quizzes:  # If the user has not attempted all quizzes
                msg = Message(
                        "Daily Quiz Reminder",
                        sender=app.config['MAIL_USERNAME'],
                        recipients=[user.email],
                        html=f"""\
                        <html>
                            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                                <h2 style="color: #007bff;">Hello {user.name},</h2>
                                <p>You haven't attempted all available quizzes yet!</p>
                                <p><strong>{total_quizzes - attempted_quiz_count} quizzes</strong> are waiting for you.</p>
                                <p>
                                    <a href="http://localhost:8080/" 
                                    style="display: inline-block; padding: 10px 20px; color: white; background-color: #28a745; 
                                            text-decoration: none; border-radius: 5px;">
                                        Take a Quiz Now
                                    </a>
                                </p>
                                <p>Happy learning!</p>
                            </body>
                        </html>"""
                    )
                try:
                    mail.send(msg)
                    print(f"Email sent to {user.email}")
                except Exception as e:
                    print(f"Failed to send email to {user.email}: {str(e)}")

    return "Daily reminders sent successfully."

@celery.task(name='celery_worker.send_periodic_email')
def send_periodic_email():
    """Task that runs every minute (e.g., for monitoring)."""
    with app.app_context():
        users = User.query.filter_by(role="user").all()
        for user in users:
            quiz_attempts = db.session.query(QuizResult).filter_by(user_id=user.id).all()
            total_quizzes = len(quiz_attempts)
            marks_scored= sum(qr.marks_scored for qr in quiz_attempts)
            total_score = sum(qr.total_marks for qr in quiz_attempts)
            avg_score = marks_scored / total_score  if total_quizzes > 0 else 0
            
            msg = Message(
                f"Monthly Quiz Report - {user.name}",
                sender=app.config['MAIL_USERNAME'],
                recipients=[user.email],
                html=f"""\
                <html>
                    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                        <h2 style="color: #007bff;">Hello {user.name},</h2>
                        <p>Here’s your <strong>monthly quiz performance</strong> summary:</p>
                        <ul>
                            <li><strong>Quizzes Taken:</strong> {total_quizzes}</li>
                            <li><strong>Marks Scored:</strong> {marks_scored}</li>
                            <li><strong>Total Score:</strong> {total_score}</li>
                            <li><strong>Average Score:</strong> {(avg_score * 100):.2f}%</li>
                        </ul>
                        <p>Keep practicing and improve your skills!</p>
                        <p>
                            <a href="http://localhost:8080/" 
                            style="display: inline-block; padding: 10px 20px; color: white; background-color: #28a745; 
                                    text-decoration: none; border-radius: 5px;">
                                Take More Quizzes
                            </a>
                        </p>
                        <p>Happy Learning!</p>
                    </body>
                </html>"""
            )
            try:
                mail.send(msg)
                print(f"Email sent to {user.email}")
            except Exception as e:
                print(f"Failed to send email to {user.email}: {str(e)}")


    return "Monthly reports sent successfully"


