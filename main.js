
let express = require('express'),
    http = require('http'),
    path = require('path'),
    bodyParser = require('body-parser'),
    app = express(),
    { PythonShell } = require('python-shell'),
    Pacotes = require('./model/Pacote');

let python_process;

app.use(express.static(path.join(__dirname, 'public')));

app.set('views', path.join(__dirname, '/views'));
app.set('view engine', 'hbs');
app.use(bodyParser.json());

app.get('/inicia', (req, res) => {
    pyshell = new PythonShell('sniffer.py'); 

    pyshell.end(function (err) {
        if (err) {
            console.log(err);
        }
    });
    python_process = pyshell.childProcess;

    res.render('index');
});

app.get('/para', (req, res) => {
    python_process.kill('SIGINT');
    res.send('Para');
});

app.get('/list', (req, res) => {
    Pacotes.find({}, 0).then(result => {

        res.render('index', { test: result });
    });
});

app.post('/', (req, res) => {
    var pacote = new Pacotes(req.body);
    pacote.save();

    res.end();
});

http.createServer(app).listen(3000);