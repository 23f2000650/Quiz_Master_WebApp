from flask import Blueprint, request, jsonify , current_app
from model import db, Subject, Chapter, Quiz, Question , User ,QuizResult
from flask_cors import CORS
from flask_jwt_extended import jwt_required
from sqlalchemy import func


admin_bp = Blueprint('admin_bp', __name__)
CORS(admin_bp)


#--------------dashborad data----------------

@admin_bp.route('/allquiz', methods=['GET'])
@jwt_required()
def dashboard_data():
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


#--------------subject crud----------------

@admin_bp.route('/subject/new', methods=['POST'])
@jwt_required()
def create_subject():
    data=request.json
    subject = Subject(name=data['name'],description=data['description'],credit=data['credits'])
    db.session.add(subject)
    db.session.commit()
    return jsonify({'message':'Subject created successfully!'}),200

@admin_bp.route('/subject/<int:sub_id>', methods=['GET'])
@jwt_required()
def get_subject(sub_id):
    subject = Subject.query.get(sub_id)
    data = {
        "id": subject.id,
        "name": subject.name,
        "description": subject.description,
        "credits": subject.credit,
    }
    return jsonify(data),200

@admin_bp.route('/subject/<int:sub_id>', methods=['POST'])
@jwt_required()
def edit_subject(sub_id):
    data = request.json
    subject = Subject.query.get(sub_id)
    subject.name = data['name']
    subject.description = data['description']
    subject.credit = data['credits']
    db.session.commit()
    return jsonify({'message':'Subject updated successfully!'}),200


@admin_bp.route('/subject/<int:sub_id>', methods=['DELETE'])
@jwt_required()
def subjectDelete(sub_id):
    subject = Subject.query.get(sub_id)
    db.session.delete(subject)
    db.session.commit()
    return jsonify({'message':'Subject deleted successfully!'}),200


#--------------chapter crud----------------


@admin_bp.route('/chapters/<int:cid>', methods=['GET'])
@jwt_required()
def get_chapters(cid):
    chapter = Chapter.query.get(cid)
    data = {
        "id": chapter.id,
        "title": chapter.name,
        "description": chapter.description,
        "subject_id": chapter.subject_id
    }
    return jsonify(data),200    


@admin_bp.route('/subject/<int:id>/chapters', methods=['POST'])
@jwt_required()
def new_chapter(id):
    data = request.json
    
    chapter = Chapter(subject_id=id, name=data['title'], description=data['description'])
    db.session.add(chapter)
    db.session.commit()
    return jsonify({"message": "Chapter created successfully!"})


@admin_bp.route('/chapters/<int:cid>', methods=['PUT'])
@jwt_required()
def edit_chapter(cid):
    data = request.json
    chapter = Chapter.query.get(cid)
    chapter.name = data['title']
    chapter.description = data['description']
    db.session.commit()
    return jsonify({"message": "Chapter updated successfully!"})

@admin_bp.route('/subject/<int:sid>/chapter/<int:cid>', methods=['DELETE']) 
@jwt_required()
def chapterDelete(sid,cid):
    chapter = Chapter.query.get(cid)
    db.session.delete(chapter)
    db.session.commit()
    return jsonify({"message": "Subject deleted successfully!"})


#--------------quiz crud----------------

@admin_bp.route('/quizzes', methods=['GET'])
@jwt_required()
def allquiz():
    quizzes = Quiz.query.all()
    data = []
    for quiz in quizzes:
        data.append({
            "id": quiz.id,
            "name": quiz.name,
            "description": quiz.description,
            "chapter_id": quiz.chapter_id,
            "time_duration": quiz.time_duration,
            "deadline": quiz.deadline,
            "one_attempt_only": quiz.one_attempt_only
        })
    return jsonify(data)

@admin_bp.route('/quiz/<int:qid>', methods=['GET'])
@jwt_required()
def get_quiz(qid):
    quiz = Quiz.query.get(qid)
    data = {
        "id": quiz.id,
        "name": quiz.name,
        "description": quiz.description,
        "chapter_id": quiz.chapter_id,
        "duration": quiz.time_duration
    }
    return jsonify(data),200



@admin_bp.route('/subject/<int:sid>/chapter/<int:cid>/new', methods=['POST'])
@jwt_required()
def newquiz(sid,cid):
    data = request.json
    quiz = Quiz(name=data['name'], description=data['description'], chapter_id=cid,time_duration=data['duration'])
    db.session.add(quiz)
    db.session.commit()
    with current_app.app_context():
        from app import trigger_mail  # Import inside function to avoid circular import
        trigger_mail()
    return jsonify({"message": "Quiz created successfully!"})


@admin_bp.route('/quiz/<int:qid>', methods=['PUT'])
@jwt_required()
def editquiz(qid):
    data = request.json
    quiz = Quiz.query.get(qid)
    quiz.name = data['name']
    quiz.description = data['description']
    quiz.time_duration = data['duration']
    db.session.commit()
    return jsonify({"message": "Quiz updated successfully!"})



@admin_bp.route('/subject/<int:sid>/chapter/<int:cid>/quiz/<int:qid>', methods=['DELETE'])
@jwt_required()
def deletequiz(sid,cid,qid):
    quiz = Quiz.query.get(qid)
    db.session.delete(quiz)
    db.session.commit()
    return jsonify({"message": "Quiz deleted successfully!"})



@admin_bp.route('/quizzes/<int:qid>', methods=['DELETE'])
@jwt_required()
def deletequiz_onqid(qid):
    quiz = Quiz.query.get(qid)
    db.session.delete(quiz)
    db.session.commit()
    return jsonify({"message": "Quiz deleted successfully!"}) 


#--------------question crud----------------


@admin_bp.route('/quiz/<int:qid>/questions', methods=['GET'])
@jwt_required()
def get_questions(qid):
    questions = Question.query.filter_by(quiz_id=qid).all()
    quiz = Quiz.query.get(qid)
    quiz_name = quiz.name
    data = []
    for question in questions:
        data.append({
            "quiz_name" : quiz.name,
            "id": question.id,
            "quiz_id": question.quiz_id,
            "question": question.question,
            "option_a": question.option_a,
            "option_b": question.option_b,
            "option_c": question.option_c,
            "option_d": question.option_d,
            "answer": question.answer
        })
    return jsonify(data),200


@admin_bp.route('/questions/new', methods=['POST'])
@jwt_required()
def add_question():
    data = request.json
    print(data)
    question = Question(
        quiz_id=data['quizId'],
        question=data['text'],
        option_a=data['options'][0],
        option_b=data['options'][1],
        option_c=data['options'][2],
        option_d=data['options'][3],
        answer=data['correctOption']
    )
    db.session.add(question)
    db.session.commit()
    return jsonify({"message": "Question created successfully!"}), 201



@admin_bp.route('/questions/<int:question_id>', methods=['DELETE'])
@jwt_required()
def delete_questions(question_id):
    question = Question.query.get(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question deleted successfully!"}),200

@admin_bp.route('/questions/<int:question_id>', methods=['PUT'])
@jwt_required()
def edit_questions(question_id):
    data = request.json
    question = Question.query.get(question_id)
    question.question = data['text']
    question.option_a = data['options'][0]
    question.option_b = data['options'][1]
    question.option_c = data['options'][2]
    question.option_d = data['options'][3]
    question.answer = data['correctOption']
    db.session.commit()
    return jsonify({"message": "Question updated successfully!"}), 200


#--------------user details----------------
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.filter_by(role='user').all()
    data = []
    for user in users:
        data.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "dob": user.dob,
            "qualification": user.qualification
        })
    return jsonify(data),200


@admin_bp.route('/users/<int:uid>', methods=['DELETE'])
@jwt_required()
def delete_user(uid):
    user = User.query.get(uid)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}),200



#----------admin summary----------------


@admin_bp.route("/summary", methods=["GET"])
@jwt_required()
def admin_dashboard():
    total_users = User.query.count()
    total_subjects = Subject.query.count()
    total_chapters = Chapter.query.count()
    total_quizzes = Quiz.query.count()

    # Count quizzes taken by each user
    user_quiz_count = (
        db.session.query(User.name, func.count(QuizResult.id))
        .join(QuizResult, QuizResult.user_id == User.id)
        .group_by(User.id)
        .all()
    )

    # Subject-wise performance
    subject_performance = (
        db.session.query(Subject.name, func.count(QuizResult.id), func.avg(QuizResult.marks_scored))
        .join(Chapter, Chapter.subject_id == Subject.id)
        .join(Quiz, Quiz.chapter_id == Chapter.id)
        .join(QuizResult, QuizResult.quiz_id == Quiz.id)
        .group_by(Subject.id)
        .all()
    )

    # Chapter-wise performance
    chapter_performance = (
        db.session.query(Chapter.name, func.count(QuizResult.id), func.avg(QuizResult.marks_scored))
        .join(Quiz, Quiz.chapter_id == Chapter.id)
        .join(QuizResult, QuizResult.quiz_id == Quiz.id)
        .group_by(Chapter.id)
        .all()
    )

    # Recent quiz results
    recent_results = (
        db.session.query(User.name, Quiz.name, QuizResult.marks_scored, QuizResult.completed_at)
        .join(QuizResult, QuizResult.user_id == User.id)
        .join(Quiz, Quiz.id == QuizResult.quiz_id)
        .order_by(QuizResult.completed_at.desc())
        .limit(5)
        .all()
    )

    # Average score across all quizzes
    avg_score = db.session.query(func.avg(QuizResult.marks_scored)).scalar()

    response_data = {
        "total_users": total_users,
        "total_subjects": total_subjects,
        "total_chapters": total_chapters,
        "total_quizzes": total_quizzes,
        "user_performance": [{"user": u, "quizzes_attempted": c} for u, c in user_quiz_count],
        "subject_performance": [{"subject": s, "attempts": a, "avg_score": round(avg or 0, 2)} for s, a, avg in subject_performance],
        "chapter_performance": [{"chapter": c, "attempts": a, "avg_score": round(avg or 0, 2)} for c, a, avg in chapter_performance],
        "recent_results": [{"user": u, "quiz": q, "score": s, "completed_at": c.strftime('%Y-%m-%d %H:%M')} for u, q, s, c in recent_results],
        "average_score": round(avg_score or 0, 2),
    }

    return jsonify(response_data)


