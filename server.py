from flask import Flask, jsonify, request
app = Flask(__name__)

global tasks
tasks = {}
global task_id  
task_id = 0

class Tarefas:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.removed = 0

@app.route('/Tarefa', methods = ['GET'])
def getTarefa():
    print("aaa")
    print(tasks)
    resp = {}
    for i in range(task_id):
        print(tasks[i])
        if not tasks[i]['removed']:
            resp[i] = {"name" : tasks[i]['name'], "description" : tasks[i]['description']}
        
    return jsonify({"status":"success", "data":resp})

@app.route('/Tarefa', methods = ['POST'])
def addTarefa():
    global task_id
    name = request.form['name']
    description = request.form['description']
    task = Tarefas(name, description)
    tasks[task_id] = task.__dict__
    print(tasks)
    task_id+=1
    return jsonify({"status":"success", "data":"INSERTEDTASK"})
    
@app.route('/Tarefa/<id>', methods = ['GET'])
def getTarefaById(id):
    try:
        print(id)
        print(tasks[int(id)])
        if (tasks[int(id)]['removed']):
            return jsonify({"status":"fail", "data":"TASKREMOVED"}),404
    except KeyError:
        return jsonify({"status":"error", "data":"KeyError"}),404
    else:
        return jsonify({"status":"success", "data":tasks[int(id)]})

@app.route('/Tarefa/<id>', methods = ['PUT'])
def updateTarefa(id):
    try:
        if (tasks[int(id)]['removed']):
            return jsonify({"status":"fail", "data":"TASKREMOVED"}),404
    except KeyError:
        return jsonify({"status":"error", "data":"KeyError"}),404
    else:
        name = request.form['name']
        description = request.form['description']
        tasks[int(id)]['name'] = name
        tasks[int(id)]["description"] = description
        return jsonify({"status":"success", "data":"UPDATEDTASK"})


@app.route('/Tarefa/<id>', methods = ['DELETE'])
def deleteTarefa(id):
    try:
        tasks[int(id)]['removed'] = 1
    except KeyError:
        return jsonify({"status":"error", "data":"KeyError"}),404
    else:
        return jsonify({"status":"success", "data":"TASKremoved"})


@app.route('/healthcheck')
def statusCheck():
    return "", 200    

if __name__ == '__main__':
    app.run()