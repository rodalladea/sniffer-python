
let express = require('express'),
    http = require('http'),
    path = require('path'),
    bodyParser = require('body-parser'),
    app = express(),
    { PythonShell } = require('python-shell');    

let python_process;

app.set('views', path.join(__dirname, '/views'));
app.set('view engine', 'hbs');
app.use(bodyParser.json())

app.get('/inicia', (req, res) => {
    pyshell = new PythonShell('sniffer.py'); 

    pyshell.end(function (err) {
        if (err) {
            console.log(err);
        }
    });
    python_process = pyshell.childProcess;

    res.send('Inicia');
});

app.get('/para', (req, res) => {
    python_process.kill('SIGINT');
    res.send('Para');
});

app.post('/', (req, res) => {
    let packet = req.body;
    
    console.log(packet);

    res.end();
});

http.createServer(app).listen(3000);