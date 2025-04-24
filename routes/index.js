var express = require('express');
var router = express.Router();
const sqlite3 = require('sqlite3');

const db = new sqlite3.Database('../bid_database.db', (err) => {
  if (err) {
    console.error('Błąd połączenia z bazą danych:', err.message);
  } else {
    console.log('Połączono z bazą danych SQLite.');
  }
});

db.run(`
  CREATE TABLE IF NOT EXISTS tenders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    company TEXT,
    description TEXT,
    tender_start_time DATETIME,
    tender_finish_time DATETIME,
    max_budget FLOAT
  )
`, (err) => {
  if (err) {
    console.error('Błąd tworzenia tabeli "tenders":', err.message);
  } else {
    console.log('Tabela "tenders" została utworzona lub już istnieje.');
  }
});

db.run(`
  CREATE TABLE IF NOT EXISTS bids (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tender_id INTEGER,
    name TEXT,
    bid_value FLOAT,
    bid_time DATETIME
  )
`, (err) => {
  if (err) {
    console.error('Błąd tworzenia tabeli "bids":', err.message);
  } else {
    console.log('Tabela "bids" została utworzona lub już istnieje.');
  }
});

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Przetargi' });
});

router.get('/tenders-list', (req, res) => {
  res.render('./pages/tenders-list');
});

router.get('/finished-tenders-list', (req, res) => {
  res.render('./pages/finished-tenders-list');
});

router.get('/new-tender', (req, res) => {
  res.render('./pages/new-tender');
});

module.exports = router;
