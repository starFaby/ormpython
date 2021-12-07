from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(70), unique= True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id','title','desccription')

taskSchema = TaskSchema()
tasksSchema = TaskSchema(many=True)

@app.route('/task', methods=['POST'])
def createTask():
    title = request.json['title']
    description = request.json['description']
    newtask = Task(title, description)
    db.session.add(newtask)
    db.session.commit()
    return taskSchema.jsonify(newtask)

@app.route('/task', methods=['GET'])
def allTask():
    allTasks = Task.query.all()
    result = tasksSchema.dump(allTasks)
    return jsonify(result)

@app.route('/task/<id>', methods=['GET'])
def onGetOneTask(id):
    oneTask = Task.query.get(id)
    return taskSchema.jsonify(oneTask)

@app.route('/task/<id>', methods=['PUT'])
def onGetUpdateTask(id):
    task = Task.query.get(id)
    title = request.json['title']
    description = request.json['description']
    task.title = title
    task.description = description
    db.session.commit()
    return taskSchema.jsonify(task)

@app.route('/task/<id>', methods=['DELETE'])
def onGetDeleteTask(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return taskSchema.jsonify(task) 

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message':'binevenido fabystar'})

if __name__ == '__main__':
    app.run(debug=True)