
let express = require('express'),
    http = require('http'),
    path = require('path'),
    bodyParser = require('body-parser'),
    app = express();

app.set('views', path.join(__dirname, '/views'));
app.set('view engine', 'hbs');
app.use(bodyParser.json())

app.get('/', (req, res) => {
    res.render('index');
});

app.post('/', (req, res) => {
    let packet = req.body;
    
    console.log(packet);

    res.end();
});

http.createServer(app).listen(3000);