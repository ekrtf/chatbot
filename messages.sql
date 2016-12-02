
drop table if exists messages;
create table messages (
	'messageId' integer primary key autoincrement,
	'userId' text not null,
	'text' text not null,
	'timestamp' text not null
);