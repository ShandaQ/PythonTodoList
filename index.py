from flask import Flask, render_template, request, redirect

import pg

db = pg.DB(dbname='todoList')

app = Flask('OurApp')

@app.route('/')
def form():
    query = db.query('''select * from todolist order by  completiondate asc''')

    tasks = query.namedresult()
    undone_Task = 0
    for row in tasks:
        if row.complete == False:
            undone_Task += 1
    print tasks
    return render_template(
        'todo.html',
        tasks = query.namedresult(),
        undone_Task = undone_Task
    )

@app.route('/add_task', methods=['POST'])
def add_task():
    content = request.form['content']
    completion_date = request.form['completion_date']

    db.insert('todolist', content=content, completiondate=completion_date, complete=False)

    return redirect('/')

@app.route('/edit_tasks', methods=['POST'])
def edit_task():
    task_list =request.form.keys()
    task_list.sort()
    print task_list
    list_len = len(task_list) - 1
    if task_list[list_len] == 'complete':
        print 'The complete button was pressed'
        for i in task_list:
            if i != 'complete':
                db.update('todolist', {'id': i, 'complete': True})
    elif task_list[list_len] == 'delete':
        for i in task_list:
            if i != 'delete':
                db.delete('todolist', {'id': i})
        print 'The delete button was pressed'
    else:
        for i in task_list:
            if i != 'notComplete':
                db.update('todolist', {'id': i, 'complete': False})

    return redirect('/')

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
