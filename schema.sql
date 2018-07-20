create table if not exists guest(
 no integer primary key autoincrement,
 name string not null,
 subject string not null,
 content string not null,
 regdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP


);
