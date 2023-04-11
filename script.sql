create table source_files (
	id integer PRIMARY KEY autoincrement,
	filename varchar(255) NOT NULL,
	processed datetime
);

create table streamers (
	id integer autoincrement,
	name varchar(255) PRIMARY KEY NOT NULL,
	viewingTime integer,
	airTime integer,
    peakViews integer,
    averageVies integer,
    subscribers integer,
	source_file integer NOT NULL,
	CONSTRAINT fk_source_files
	FOREIGN KEY (source_file)
	REFERENCES source_files(id)
	ON DELETE CASCADE
);