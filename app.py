from flask import Flask, render_template, request, jsonify
import queue 
import typerscript

app = Flask(__name__)

log_queue = queue.Queue()

def log_writer(message):
    log_queue.put(message)

@app.route('/', methods=['GET'])
def index():
    return app.redirect("/migration")

@app.route('/migration', methods=['GET', 'POST'])
def migration():
    if request.method == 'POST':
        domain = request.form['domain']
        numeros = request.form['numeros'].split(',')
        max_value = int(request.form['max'])
        
        result = typerscript.exportSilae(domain, numeros, max_value)
        return jsonify(result)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)