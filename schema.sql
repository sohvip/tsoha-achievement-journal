create table if not exists users (
    id serial primary key,
    username text unique,
    password text,
    type integer
);