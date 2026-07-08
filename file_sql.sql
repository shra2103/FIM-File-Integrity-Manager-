create database int_file;
use int_file;

create table file_change(
	id int auto_increment primary key,
    file_path varchar(250) not null,
    timestamp timestamp default current_timestamp,
    old_hash varchar(64),
    new_hash varchar(64),
    change_type varchar(50)
);

select * from file_change;
