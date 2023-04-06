import pymysql
from app import app
from db import mysql
from flask import jsonify
from flask import flash, request

#from werkzeug import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash



############User################

@app.route('/login', methods=['GET','POST'])
def login():
	conn = None
	cursor = None
	try:
		_json = request.json
		_name = _json['name']
		_password = _json['pwd']
		# validate the received values
		if _name and _password and request.method == 'POST':
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT user_id id, user_name name, user_email email, user_password pwd FROM tbl_user WHERE user_name=%s ", (_name))
			data = cursor.fetchone()
			if data:
				hashpwd=data['pwd']
				if check_password_hash(hashpwd, _password):
					resp = jsonify(data)
					resp.status_code = 200
					return resp
				else:
					return not_found()
			else:
				return not_found()

		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()



@app.route('/add', methods=['POST'])
def add_user():
	conn = None
	cursor = None
	try:
		_json = request.json
		_name = _json['name']
		_email = _json['email']
		_password = _json['pwd']
		_type = _json['type']
		_contact = _json['contact']
		# validate the received values
		if _name and _email and _password and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "INSERT INTO tbl_user(user_name, user_email, user_password, user_type, user_contact) VALUES(%s, %s, %s, %s, %s)"
			data = (_name, _email, _hashed_password, _type, _contact)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/examadd', methods=['POST'])
def add_exam():
	conn = None
	cursor = None
	try:
		_json = request.json
		_examName = _json['examName']
		_examType = _json['examType']
		_startDate = _json['startDate']
		_examStatus = _json['examStatus']
		_examPaperId = _json['examPaperId']
		_examReportId = _json['examReportId']
		_examCreator = _json['examCreator']
		
		# validate the received values
		if _examName and _examType and _startDate and _examStatus and _examPaperId and _examReportId and _examStatus and _examCreator and request.method == 'POST':
			# save edits
			sql = "INSERT INTO exams(ExamName, ExamType, StartDate, ExamStatus, ExamPaperId, ExamReportId, ExamCreator) VALUES(%s, %s, %s, %s, %s, %s, %s)"
			data = (_examName, _examType, _startDate, _examStatus, _examPaperId, _examReportId, _examCreator)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Exam added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/users')
def users():
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT user_id id, user_name name, user_email email, user_password pwd, user_type type, user_contact contact FROM tbl_user")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/user/<int:id>')
def user(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT user_id id, user_name name, user_email email, user_password pwd, user_type type, user_contact contact FROM tbl_user WHERE user_id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()



@app.route('/update', methods=['PUT'])
def update_user():
	conn = None
	cursor = None
	try:
		_json = request.json
		_id = _json['id']
		_name = _json['name']
		_email = _json['email']
		_password = _json['pwd']
		_type = _json['type']
		_contact = _json['contact']		
		# validate the received values
		if _name and _email and _password and _id and request.method == 'PUT':
			#hash new password
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "UPDATE tbl_user SET user_name=%s, user_email=%s, user_password=%s, user_type=%s, user_contact=%s WHERE user_id=%s"
			data = (_name, _email, _hashed_password, _type, _contact, _id)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()



		
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM tbl_user WHERE user_id=%s", (id,))
		conn.commit()
		resp = jsonify('User deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
		return not_found()
	finally:
		cursor.close() 
		conn.close()
		


############Exam#################################

#  StartTime startTime, EndTime endTime
@app.route('/exams')
def exams():
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT ExamID examID, ExamName examName, ExamType examType, StartDate startDate, ExamStatus examStatus, ExamPaperId examPaperId, ExamReportId examReportId, ExamCreator examCreator FROM exams")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


@app.route('/exam/<int:id>')
def exam(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT ExamID examID, ExamName examName, ExamType examType, StartDate startDate, ExamStatus examStatus, ExamPaperId examPaperId, ExamReportId examReportId, ExamCreator examCreator FROM exams WHERE ExamID=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


		
@app.route('/examedit', methods=['PUT'])
def update_exam():
	conn = None
	cursor = None
	try:
		_json = request.json
		_examID = _json['examID']
		_examName = _json['examName']
		_examType = _json['examType']
		_startDate = _json['startDate']
		_examStatus = _json['examStatus']
		_examPaperId = _json['examPaperId']
		_examReportId = _json['examReportId']
		_examCreator = _json['examCreator']		
		# validate the received values
		if _examName and _examType and _examStatus and _examCreator and request.method == 'PUT':
			# save edits
			sql = "UPDATE exams SET ExamName=%s, ExamType=%s, StartDate=%s, ExamStatus=%s, ExamPaperId=%s, ExamReportId=%s, ExamCreator=%s WHERE ExamID=%s"
			data = (_examName, _examType, _startDate, _examStatus, _examPaperId, _examReportId, _examCreator, _examID)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


@app.route('/examdelete/<int:id>', methods=['DELETE'])
def delete_exam(id):
	conn = None
	cursor = None
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM exams WHERE ExamID=%s", (id,))
		conn.commit()
		resp = jsonify('Exam deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
		return not_found()
	finally:
		cursor.close() 
		conn.close()
		

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp	

if __name__ == "__main__":
    app.run()