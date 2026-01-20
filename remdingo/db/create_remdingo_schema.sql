-- Remdingo Database Setup Script
-- Run this script against your PostgreSQL server to create the database and tables

-- Create the database (run this separately if needed, or connect to postgres database first)
-- Note: You cannot run CREATE DATABASE inside a transaction block
-- Run this command first: CREATE DATABASE remdingodb;

-- Then connect to remdingodb and run the rest:

-- Create reminders sequence
CREATE SEQUENCE IF NOT EXISTS reminders_id_seq AS INTEGER;

-- Create reminders table
CREATE TABLE IF NOT EXISTS reminders
(
    id INTEGER DEFAULT nextval('reminders_id_seq'::regclass) NOT NULL
        CONSTRAINT reminders_pkey PRIMARY KEY,
    customer_id VARCHAR(50),
    reminder_date_utc TIMESTAMP,
    reminder_date_user TIMESTAMP,
    reminder_text VARCHAR(500),
    snooze_number INTEGER DEFAULT 0,
    ack BOOLEAN DEFAULT FALSE,
    sms BOOLEAN DEFAULT FALSE,
    email BOOLEAN DEFAULT FALSE,
    web BOOLEAN DEFAULT TRUE,
    "offset" INTEGER DEFAULT 0,
    tz VARCHAR(300),
    created TIMESTAMP
);

-- Set sequence ownership
ALTER SEQUENCE reminders_id_seq OWNED BY reminders.id;

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS reminders_idx ON reminders (customer_id, reminder_date_utc);

