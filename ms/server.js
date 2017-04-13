//wget -qO- https://raw.github.com/creationix/nvm/v0.4.0/install.sh | sh
var express = require('express');
var mongoose = require('mongoose');
var bodyParser = require('body-parser');

var MAX = 1000000;
var counter = 0;
var clients = {};
mongoose.Promise = global.Promise;
mongoose.connect("mongodb://localhost:27017/test");
var ImageListSchema = mongoose.Schema({
    id: Number,
    name: String,
    url: String,
    state: Number,
    result: Object
});
var ImageList = mongoose.model('Images', ImageListSchema);

var app = express();
app.use(bodyParser.json());
app.use('/next', function (req, res) {
    if (counter > MAX) {
        res.send({'err': -2});
    }
    else {
        ImageList.findOne({'id': counter}, function (err, d) {
            if (err || d === null)
                res.send({'err': -1, 'counter': counter});
            else if (d['state'] == 1)
                res.send({'err': -1, 'counter': counter});
            else if (d['state'] == 0) {
                res.send({'err': 0, 'id': counter, 'url': d['url']});
            }
            else
                res.send({'err': -1, 'counter': counter});
            counter += 1;
        });
    }
});

app.post('/put', function (req, res) {
    var obj = req.body;
    clients[req.ip] = obj['client'];
    ImageList.findOneAndUpdate({'id': obj['id']}, {'$set': {'result': obj['result'], 'state': 1}}, function (err, ret) {
        if (err)
            res.send({'err': -1});
        else
            res.send({'err': 0});
    });
});

app.use('/set/:counter', function (req, res) {
    counter = Number(req.params.counter);
    res.send({'counter': counter});
});

app.use('/query', function (req, res) {
    res.send({'counter': counter, 'clients': clients});
    clients = {};
});

app.listen('3000', function () {
    console.log('listening');
});