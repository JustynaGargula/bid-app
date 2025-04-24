const sqlite3 = require("sqlite3");
const Tender = require(("../models/Tender"))

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

function addTender( tender, callback) {
    const sql =  'INSERT INTO tenders (name, company, description, tender_start_time, tender_finish_time, max_budget) VALUES (?, ?, ?, ?, ?, ?)';
    db.run(sql, tender.toArray(), (err) => {
        if (err) {
            console.error('Błąd dodawania danych:', err.message);
            return callback(err);
        } else {
            console.log('Dodano dane do tabeli.');
            tender.id = this.lastID
            return callback(null, tender);
        }
    });
}

module.exports = {
    addTender
};