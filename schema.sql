create table if not exists users (
    id serial primary key,
    username text unique,
    password text,
    type integer
);

create table if not exists categories (
    id serial primary key,
    category text
);

create table if not exists posts (
    id serial primary key,
    title text,
    content text,
    user_id integer references users,
    category_id integer references categories,
    sent_at timestamp
);