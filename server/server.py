from flask import Flask, request, make_response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)


#Student Info Delete Function
def info_del(list, id):
    for i in range(len(list)):
        if list[i]["id"] == id:
            del(list[i])
            return
    return


#Student Info Update Function
def student_info_update(list, id, data):
     for i in range(len(list)):
        if list[i]["id"] == id:
            list[i] = data
            return
     return


#ID Search Function
def id_search(list, id):
    for i in range(len(list)):
        if list[i]["id"] == id:
            return list[i]
    return None


#API Response Function
def response(code: int, message: str, data: any = None):
    body = {"code": code, "message": message, "data": {}}
    if data is not None:
        if hasattr(data, '__dict__'):
            body["data"] = data.__dict__
        else:
            body["data"] = data
    return make_response(json.dumps(body, sort_keys=True, ensure_ascii=False), 200)


#Login
#Login API Construct
@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    if data["username"] == "syc" and data["password"] == "123":
        return response(0, 'Success')
    return response(1000, "Incorrect username or password")


#Students
students = [
              {"id": 1, "name": "Yuchen Shen", "chinese": 99, "math": 98, "english": 97},
              {"id": 2, "name": "Taoran Shen", "chinese": 100, "math": 60, "english": 99},
              {"id": 3, "name": "Guhao Qian", "chinese": 30, "math": 100, "english": 98},
              {"id": 4, "name": "Ziyue Xu", "chinese": 96, "math": 99, "english": 90},
            ]
student_id = 4


#Student List
@app.route('/student_list', methods=['GET'])
def student_list():
    return response(0, "Success", students)


#Student Add
@app.route('/student_add', methods=['POST'])
def student_add():
    global students, student_id
    if str(request.data) == '':
        return response(1, "Parameter Error")
    students_info = {"id": student_id, "name": '', "chinese": 0, "math": 0, "english": 0}
    param = json.loads(request.data)

    if "name" not in param:
        return response(1,"You have to input student name")
    students_info["name"] = param["name"]
    if "chinese" in param:
        students_info["chinese"] = param["chinese"]
    if "math" in param:
        students_info["math"] = param["math"]
    if "english" in param:
        students_info["english"] = param["english"]
    student_id = student_id + 1
    students_info["id"] = student_id
    students.append(students_info)
    return response(0, "Add Success")


#Student Delete
@app.route('/student_del', methods=['POST'])
def student_del():
    global students
    param = json.loads(request.data)
    if str(request.data) == '' or "id" not in param:
        return response(1, "Parameter Error")

    info_del(students, param["id"])
    return response(0, "Delete Success")


#Student Info Edit
@app.route('/student_edit', methods=['POST'])
def student_info_edit():
    global students
    param = json.loads(request.data)
    if str(request.data) == '' or "id" not in param:
        return response(1, "Parameter Error")
    if "name" not in param:
        return response(2, "You have to input Name")
    stu = id_search(students, param["id"])
    if stu is None:
        return response(3, "No that student")
    if "name" in param:
        stu["name"] = param["name"]
    if "chinese" in param:
        stu["chinese"] = param["chinese"]
    if "math" in param:
        stu["math"] = param["math"]
    if "english" in param:
        stu["english"] = param["english"]
    student_info_update(students, param["id"], stu)
    return response(0, "Edit Success")


#Teachers
teachers = [
                {"id": 1, "username": "Mr.Shen", "password": "123"},
           ]
teacher_id = 1


#Teacher List
@app.route('/teacher_list', methods=['GET'])
def teacher_list():
    return response(0, "Success", teachers)


#Teacher Add
@app.route('/teacher_add', methods=['POST'])
def teacher_add():
    global teachers, teacher_id
    if str(request.data) == '':
        return response(1, "Parameter Error")
    teachers_info = {"id": teacher_id, "username": '', "password": ''}
    param = json.loads(request.data)

    if "username" not in param:
        return response(1, "You have to input username")

    if "password" not in param:
        return response(1, "You have to input password")
    teachers_info["username"] = param["username"]
    teachers_info["password"] = param["password"]
    teacher_id = teacher_id + 1
    teachers_info["id"] = teacher_id
    teachers.append(teachers_info)
    return response(0, "Add Success")


#Teacher Delete
@app.route('/teacher_del', methods=['POST'])
def teacher_del():
    global teachers
    param = json.loads(request.data)
    if str(request.data) == '' or "id" not in param:
        return response(1, "Parameter Error")

    info_del(teachers, param["id"])
    return response(0, "Delete Success")


#Student Info Edit
@app.route('/teacher_edit', methods=['POST'])
def teacher_info_edit():
    global teachers
    param = json.loads(request.data)
    if str(request.data) == '' or "id" not in param:
        return response(1, "Parameter Error")
    if "username" not in param:
        return response(2, "You have to input userame")
    tea = id_search(teachers, param["id"])
    if tea is None:
        return response(3, "No that teacher")
    if "username" in param:
        tea["username"] = param["username"]
    if "password" in param:
        tea["password"] = param["password"]
    student_info_update(teachers, param["id"], tea)
    return response(0, "Edit Success")


if __name__ == '__main__':
    app.run(port=9000)