from flask import Blueprint, request
from flask import jsonify
from model import db, User, Quiz, QuizResult , Subject , Chapter , Question
from datetime import datetime
from flask_cors import CORS
from flask_jwt_extended import jwt_required,get_jwt_identity


user_bp = Blueprint('user_bp', __name__)
CORS(user_bp)

@user_bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == "OPTIONS":  # Handle preflight request
        return _build_cors_prelight_response()
    
    data = request.json
    if 'dob' in data:
        data['dob'] = datetime.strptime(data['dob'], "%Y-%m-%d").date()

    new_user = User(
        name=data['name'],
        email=data['email'],
        dob=data['dob'],
        qualification=data['qualification'],
        role=data['role'],
        password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    
    response = jsonify({"message": "User created successfully!"})
    return _build_cors_actual_response(response)

def _build_cors_prelight_response():
    response = jsonify({"message": "CORS preflight response"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response

def _build_cors_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response

@user_bp.route('/quizzes', methods=['GET'])
@jwt_required()
def get_quizzes():
    current_user = get_jwt_identity()
    
    # Debugging print statements
    print(f"User ID: {current_user}")  
    print(f"Request Headers: {request.headers}")
    
    if not current_user:
        return jsonify({"msg": "Invalid or missing token"}), 401

    subjects = Subject.query.all()
    data = []
    
    for subject in subjects:
        subject_data = {
            "subject_id": subject.id,
            "title": subject.name,
            "chapters": []
        }
        
        for chapter in subject.chapters:
            chapter_data = {
                "chapter_id": chapter.id,
                "title": chapter.name,
                "quizzes": []
            }
            
            for quiz in chapter.quizzes:
                quiz_data = {
                    "id": quiz.id,
                    "title": quiz.name,
                    "description": quiz.description,
                    "duration": quiz.time_duration
                }
                chapter_data["quizzes"].append(quiz_data)
            
            subject_data["chapters"].append(chapter_data)
        
        data.append(subject_data)
    
    return jsonify(data)


@user_bp.route('/quiz/<int:qid>', methods=['GET'])
@jwt_required()
def get_quiz_questions(qid):
    questions = Question.query.filter_by(quiz_id=qid).all()  # Fetch all questions for the given quiz_id
    quiz=Quiz.query.filter_by(id=qid).first()
    time=quiz.time_duration
    if not questions:
        return jsonify({"message": "No questions found for this quiz"}), 404

    response = []
    for q in questions:
        response.append({
            "question_id": q.id,
            "time" : time,
            "question": q.question,
            "option_a": q.option_a,
            "option_b": q.option_b,
            "option_c": q.option_c,
            "option_d": q.option_d,
            "answer": q.answer
        })

    return jsonify(response), 200

@user_bp.route('/quiz/submit', methods=['POST'])
@jwt_required()
def user_results():
    data = request.json

    # Extract data from JSON request
    user_id = data.get('user_id')
    quiz_id = data.get('qid')  # Updated key name from 'quiz_id' to 'qid'
    score = data.get('score')
    total_marks = data.get('total_marks')
    #time_taken = data.get('time_taken')
    date_of_completion_str = data.get('date_of_completion')
    if date_of_completion_str:
        date_of_completion = datetime.fromisoformat(date_of_completion_str.rstrip('Z'))  # Convert from string to datetime
    else:
        date_of_completion = datetime.utcnow()

    # Create a new quiz result entry
    new_result = QuizResult(
        user_id=user_id,
        quiz_id=quiz_id,
        marks_scored=score,
        total_marks=total_marks,
        #time_taken=time_taken,
        completed_at=date_of_completion
    )

    db.session.add(new_result)
    db.session.commit()

    return jsonify({"message": "Quiz result submitted successfully!"}), 200



@user_bp.route('/<int:userid>/quiz/results', methods=['GET'])
@jwt_required()
def get_user_results(userid):
    results = QuizResult.query.filter_by(user_id=userid).all()
    if not results:
        return jsonify({"message": "No results found for this user"}), 404
    
    
    response = []
    for r in results:
        quiz=Quiz.query.filter_by(id=r.quiz_id).first()
        
        response.append({
            "result_id": r.id,
            "quiz_name": quiz.name,
            "quiz_id": r.quiz_id,
            "marks_scored": r.marks_scored,
            "total_marks": r.total_marks,
            "completed_at": r.completed_at
        })
        print(response)
    return jsonify(response), 200



# ||---------------------- Dashboard Routes ----------------------||

@user_bp.route('<int:user_id>/stats', methods=['GET'])
def get_user_stats(user_id):
    user_id = user_id  # Assuming user_id is passed as a query parameter
    total_quizzes = Quiz.query.count()
    completed_quizzes = (
        db.session.query(QuizResult.quiz_id)
        .filter_by(user_id=user_id)
        .distinct()
        .count()
    )
    #average_score = db.session.query(db.func.avg(QuizResult.marks_scored)).filter_by(user_id=user_id).scalar()
    best_performance = db.session.query(QuizResult).filter(
        QuizResult.user_id == user_id,
        QuizResult.marks_scored == db.session.query(db.func.max(QuizResult.marks_scored))
        .filter(QuizResult.user_id == user_id)
        .scalar()
        ).first()    
    print(completed_quizzes,best_performance)
    return jsonify({
            "totalQuizzes": total_quizzes,
            "completed": completed_quizzes,
            "bestPerformance": best_performance.marks_scored if best_performance else 'N/A',
            "totalMarks": best_performance.total_marks if best_performance and best_performance.total_marks else 'N/A'
        }), 200
    
    
@user_bp.route('/quizzes/upcoming', methods=['GET'])
def get_upcoming_quizzes():
    # Fetch upcoming quizzes logic
    quizzes = Quiz.query.filter().limit(5).all()
    response = []
    for quiz in quizzes:
        response.append({
            "id": quiz.id,
            "title": quiz.name,
            "description": quiz.description,
            
            "duration": quiz.time_duration
        })
    return jsonify(response), 200

@user_bp.route('<int:user_id>/results/recent', methods=['GET'])
def get_recent_results(user_id):
    user_id = user_id  # Assuming user_id is passed as a query parameter
    results = QuizResult.query.filter_by(user_id=user_id).order_by(QuizResult.completed_at.desc()).limit(5).all()
    response = []
    for result in results:
        quiz = Quiz.query.get(result.quiz_id)
        response.append({
            "id": result.id,
            "quizTitle": quiz.name,
            "date": result.completed_at,
            "score": result.marks_scored,
            "totalMarks": result.total_marks,
            "status": "Passed" if result.marks_scored >= 50 else "Failed"
        })
    return jsonify(response), 200



#-----------user summary----------------

from flask import request
from sqlalchemy.orm import joinedload

@user_bp.route('/summary/<int:user_id>', methods=['GET'])
@jwt_required()
def user_performance(user_id):
    user_id = user_id
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    user = User.query.options(joinedload(User.quiz_results).joinedload(QuizResult.quiz)).filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    total_attempts = len(user.quiz_results)
    avg_score = sum(result.marks_scored or 0 for result in user.quiz_results) / total_attempts if total_attempts else 0

    subject_performance = {}
    chapter_performance = {}
    recent_performance = []
    
    for result in user.quiz_results:
        quiz = result.quiz
        chapter = quiz.chapter
        subject = chapter.subject
        
        # Subject-wise performance
        if subject.name not in subject_performance:
            subject_performance[subject.name] = {"attempts": 0, "total_score": 0}
        subject_performance[subject.name]["attempts"] += 1
        subject_performance[subject.name]["total_score"] += result.marks_scored or 0
        
        # Chapter-wise performance
        if chapter.name not in chapter_performance:
            chapter_performance[chapter.name] = {"attempts": 0, "total_score": 0}
        chapter_performance[chapter.name]["attempts"] += 1
        chapter_performance[chapter.name]["total_score"] += result.marks_scored or 0

        # Recent quiz performance
        recent_performance.append({
            "quiz_name": quiz.name,
            "score": result.marks_scored,
            "total": result.total_marks,
            "completed_at": result.completed_at.strftime("%Y-%m-%d %H:%M")
        })
    
    subject_performance = {
        k: {"avg_score": v["total_score"] / v["attempts"]} for k, v in subject_performance.items()
    }
    chapter_performance = {
        k: {"avg_score": v["total_score"] / v["attempts"]} for k, v in chapter_performance.items()
    }
    
    return jsonify({
        "total_attempts": total_attempts,
        "avg_score": avg_score,
        "subject_performance": subject_performance,
        "chapter_performance": chapter_performance,
        "recent_performance": recent_performance[:5]  # Last 5 quizzes
    })

