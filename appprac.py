from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)

SECRET_KEY = 'SPARTA'

client = MongoClient('52.78.96.228', 27017, username="test", password="test")

db = client.hanghaegram

    # 처음 화면
@app.route('/')
def home():
    return render_template('index.html')

    # 카테고리 페이지로 이동
@app.route('/category')
def login():
    msg = request.args.get("msg")
    return render_template('category.html', msg=msg)

    #회원가입 페이지로 이동
@app.route('/signup')
def register():
    msg = request.args.get("msg")
    return render_template('signup.html', msg=msg)

    # 로그인
@app.route('/sign_in', methods=['POST'])
def sign_in():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면 메세지 띄우기
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

    # 회원가입 정보 db에 저장
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
        "profile_pic": "",                                          # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
        "profile_info": ""                                          # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

    # 회원가입 할때 중복 확인
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})




# 상세페이지(pet) 랜더링
@app.route('/pet')
def showing():
# DB에서 클리이언트가 작성한 정보 받아오기
    articles = list(db.pet.find({}, {"_id": False}))
# 리턴값으로 상세페이지와 Jinja2 방식으로 DB정보 전송
    return render_template("pet.html", articles=articles, )
# 상세페이지(pet) 게시물 등록
@app.route('/pet/posts', methods=['POST'])
def saving():
#이름, 코멘트 ,파일을 클라이언트로 부터 받아옴
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    file = request.files["file_give"]
# 여러가지 확장자를 가진 파일을 저장하고 들고오기 위해서 작성
    extension = file.filename.split('.')[-1]
# 게시물 작성시간을 클라이언트 페이지에 보여주기 위해서 설정
    now = datetime.now()
    nowtime = now.strftime('%H시 %M분 %S초 / %Y년 %m월 %d일')
# 파일을 static에 저장할 때, 파일이름을 업로드 시간으로 하는 것
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
#파일 이름 정하기, 및 파일 저장 (f를 써서 글을 간단히 만들기)
    filename = f'file-{mytime}'
    save_to = f'static/image/{filename}.{extension}'
    file.save(save_to)
#DB에 이름, 코멘트, **파일경로**, 업로드시간, 좋아요 0 으로 저장
    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'file': f'{filename}.{extension}',
        'upload_time': nowtime,
        'like':0
    }

    db.pet.insert_one(doc)

    return jsonify({'msg': '정상적으로 저장되었습니다.'})
# 상세페이지(pet) 좋아요 올리기
@app.route('/pet/like', methods=['POST'])
def like_pet():
# 업로드 시간을 클라이언트로 부터 받아오고 DB에서 해당 이름을 가진 정보 꺼내오기
    time_receive = request.form['time_give']
    target_star = db.pet.find_one({'upload_time': time_receive})
# 받아온 정보에서 'like'의 숫자 추가하기
    current_like = target_star['like']
    new_like = current_like + 1
# 이것을 DB에 넣고 클라이언트에게 완료 메세지 보내기
    db.pet.update_one({'upload_time': time_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '좋아요 완료!'})


# 상세페이지(daily) 랜더링 -> 상세페이지(pet)을 참고하세요 ↑
@app.route('/daily')
def showing2():

    articles = list(db.daily.find({}, {"_id": False}))

    return render_template("daily.html", articles=articles, )
# 상세페이지(daily) 게시물 등록 -> 상세페이지(pet)을 참고하세요 ↑
@app.route('/daily/posts', methods=['POST'])
def saving2():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    now = datetime.now()
    nowtime = now.strftime('%H시 %M분 %S초 / %Y년 %m월 %d일')

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'

    save_to = f'static/image/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'file': f'{filename}.{extension}',
        'upload_time': nowtime,
        'like': 0
    }

    db.daily.insert_one(doc)

    return jsonify({'msg': '정상적으로 저장되었습니다.'})
# 상세페이지(daily) 좋아요 올리기 -> 상세페이지(pet)을 참고하세요 ↑
@app.route('/daily/like', methods=['POST'])
def like_daily():
    time_receive = request.form['time_give']
    target_star = db.daily.find_one({'upload_time': time_receive})

    current_like = target_star['like']
    new_like = current_like + 1

    db.daily.update_one({'upload_time': time_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '좋아요 완료!'})


# 상세페이지(exercise) 랜더링 -> 상세페이지(pet)을 참고하세요 ↑
@app.route('/exercise')
def showing3():

    articles = list(db.exercise.find({}, {"_id": False}))

    return render_template("exercise.html", articles=articles, )
# 상세페이지(exercise) 게시물 등록 -> 상세페이지(pet)을 참고하세요 ↑
@app.route('/exercise/posts', methods=['POST'])
def saving3():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    now = datetime.now()
    nowtime = now.strftime('%H시 %M분 %S초 / %Y년 %m월 %d일')

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'

    save_to = f'static/image/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'file': f'{filename}.{extension}',
        'upload_time': nowtime,
        'like': 0
    }

    db.exercise.insert_one(doc)

    return jsonify({'msg': '정상적으로 저장되었습니다.'})
# 상세페이지(exercise) 좋아요 올리기 -> 상세페이지(pet)을 참고하세요 ↑
@app.route('/exercise/like', methods=['POST'])
def like_exercise():
    time_receive = request.form['time_give']
    target_star = db.exercise.find_one({'upload_time': time_receive})

    current_like = target_star['like']
    new_like = current_like + 1

    db.exercise.update_one({'upload_time': time_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '좋아요 완료!'})


# 상세페이지(food) 랜더링 -> 상세페이지(pet)을 참고하세요 ↑
@app.route('/food')
def showing4():

    articles = list(db.food.find({}, {"_id": False}))

    return render_template("food.html", articles=articles, )
# 상세페이지(food) 게시물 등록 -> 상세페이지(pet)을 참고하세요 ↑
@app.route('/food/posts', methods=['POST'])
def saving4():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    now = datetime.now()
    nowtime = now.strftime('%H시 %M분 %S초 / %Y년 %m월 %d일')

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'

    save_to = f'static/image/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'file': f'{filename}.{extension}',
        'upload_time': nowtime,
        'like': 0
    }

    db.food.insert_one(doc)

    return jsonify({'msg': '정상적으로 저장되었습니다.'})
# 상세페이지(food) 좋아요 올리기 -> 상세페이지(pet)을 참고하세요 ↑
@app.route('/food/like', methods=['POST'])
def like_food():
    time_receive = request.form['time_give']
    target_star = db.food.find_one({'upload_time': time_receive})

    current_like = target_star['like']
    new_like = current_like + 1

    db.food.update_one({'upload_time': time_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '좋아요 완료!'})


# 상세페이지(trip) 랜더링 -> 상세페이지(pet)을 참고하세요 ↑
@app.route('/trip')
def showing5():

    articles = list(db.trip.find({}, {"_id": False}))

    return render_template("trip.html", articles=articles, )
# 상세페이지(trip) 게시물 등록 -> 상세페이지(pet)을 참고하세요 ↑
@app.route('/trip/posts', methods=['POST'])
def saving5():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    now = datetime.now()
    nowtime = now.strftime('%H시 %M분 %S초 / %Y년 %m월 %d일')

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'

    save_to = f'static/image/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'file': f'{filename}.{extension}',
        'upload_time': nowtime,
        'like': 0
    }

    db.trip.insert_one(doc)

    return jsonify({'msg': '정상적으로 저장되었습니다.'})
# 상세페이지(trip) 좋아요 올리기 -> 상세페이지(pet)을 참고하세요 ↑
@app.route('/trip/like', methods=['POST'])
def like_trip():
    time_receive = request.form['time_give']
    target_star = db.trip.find_one({'upload_time': time_receive})

    current_like = target_star['like']
    new_like = current_like + 1

    db.trip.update_one({'upload_time': time_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '좋아요 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)