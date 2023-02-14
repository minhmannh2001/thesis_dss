from flask import Flask, render_template, request
import pandas as pd
from TOPSIS import search

def get_teacher_info(id):
    teacher_df = pd.read_csv('./../data/teachers.csv', names=['TeacherID', 'TeacherName', 'Major', 'Degrees', 'Fields', 'InterestedFields', 'NumberOfResearches', 'NumberOfAwards'])
    info = teacher_df[teacher_df['TeacherID'] == int(id)]
    return info

def get_teacher_name(id):
    teacher_df = pd.read_csv('./../data/teachers.csv', names=['TeacherID', 'TeacherName', 'Major', 'Degrees', 'Fields', 'InterestedFields', 'NumberOfResearches', 'NumberOfAwards'])
    info = teacher_df[teacher_df['TeacherID'] == int(id)]
    return info['TeacherName'].values[0]

def get_thesis_info(thesis_ids):
    thesis_info = []

    thesis_df = pd.read_csv('./../data/thesises.csv', names=['ThesisID', 'TeacherID', 'Title', 'Description', 'Degree', 'Co-researchers'])

    for id in thesis_ids:
        info = {}
        thesis = thesis_df[thesis_df['ThesisID'] == int(id)]
        info['title'] = thesis['Title'].values[0]
        if str(thesis['Description'].values[0]) == 'nan':
            info['description'] = 'Sẽ được bổ sung thêm'
        else:
            info['description'] = thesis['Description'].values[0]
        if str(thesis['Co-researchers'].values[0]) == 'nan':
            info['coresearchers'] = 'Không có'
        else:
            info['coresearchers'] = thesis['Co-researchers'].values[0]
        info['teacher_id'] = thesis['TeacherID'].values[0]
        info['teacher_name'] = get_teacher_name(thesis['TeacherID'].values[0])
        thesis_info.append(info)
    
    return thesis_info

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/teacher/<id>')
def teacher(id):
    info = get_teacher_info(id)
    print(info)
    teacher_info = {}
    teacher_info['name'] = info['TeacherName'].values[0]
    teacher_info['major'] = info['Major'].values[0]
    teacher_info['degrees'] = info['Degrees'].values[0]
    teacher_info['NumberOfResearches'] = info['NumberOfResearches'].values[0]
    teacher_info['NumberOfAwards'] = info['NumberOfAwards'].values[0]
    teacher_info['Fields'] = info['Fields'].values[0]
    return render_template('teacher.html', info = teacher_info)

@app.route('/result', methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      thesis_ids = search(result)
      print(result)
      thesis_info = get_thesis_info(thesis_ids)
      print(thesis_info)
      return render_template("result.html", thesis_info = thesis_info)

if __name__ == '__main__':
   app.run(debug=True)