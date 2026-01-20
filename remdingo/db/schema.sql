create table users
(
	id serial
		constraint users_pkey
			primary key,
	customer_id varchar(50),
	email varchar(40)
		constraint users_email_key
			unique,
	password varchar(200),
	name varchar,
	website varchar(60),
	created_on timestamp,
	last_login timestamp
);

alter table users owner to postgres;

create sequence reminders_id_seq
	as integer;

alter sequence reminders_id_seq owner to postgres;

create table reminders
(
	id integer default nextval('reminders_id_seq'::regclass) not null
		constraint reminders_pkey
			primary key,
	customer_id varchar(50),
	reminder_date_utc timestamp,
	reminder_date_user timestamp,
	reminder_text varchar(500),
	snooze_number integer,
	ack boolean,
	sms boolean,
	email boolean,
	web boolean,
	"offset" integer,
	tz varchar(300),
	created timestamp
);

alter table reminders owner to postgres;

alter sequence reminders_id_seq owned by reminders.id;

create index reminders_idx
	on reminders (customer_id, reminder_date_utc);

