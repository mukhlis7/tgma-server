create table tgmauser(
	id serial primary key,
	fullname text not null,
	username text not null,
	verified boolean not null,
	password text not null
);
