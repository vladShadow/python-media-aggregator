import psycopg2
from config import config

def get_connection():
    db = psycopg2.connect(config.DATABASE_STRING)
    return db


def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute('''DROP TABLE IF EXISTS users CASCADE ;
                 DROP TABLE IF EXISTS profiles CASCADE ;
                 DROP TABLE IF EXISTS criterias CASCADE ;
                 DROP TABLE IF EXISTS posts CASCADE ;
                 DROP TABLE IF EXISTS seen_posts CASCADE ;
                 DROP TABLE IF EXISTS files CASCADE ;
              ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
    user_id             int  primary key,
    user_name           text,
    curr_state          text,
    registration_date   text,
    last_activity       text
     );''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS profiles (
    profile_id          serial  primary key,
    user_id             int,
    profile_type        text,
    profile_name        text,
    
    foreign key(user_id) references users(user_id)
    );''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS criterias (
    criteria_id         serial primary key,
    profile_id          int,
    criteria_type       text,
    criteria_value      int,
    
    foreign key(profile_id) references profiles(profile_id)
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS posts (
    post_id             int primary key,
    profile_type        text,
    profile_name        text,
    publication_date    text,
    download_date       text

    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS seen_posts (
    seen_post_id        int primary key,
    user_id             int,
    post_id             int,
    view_date           text,
    
    foreign key(user_id) references users(user_id),
    foreign key(post_id) references posts(post_id)
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS files (
    path                text primary key,
    post_id             int,
    
    foreign key(post_id) references posts(post_id)
    )
    ''')
    
    c.execute('''INSERT INTO users (user_id, user_name, curr_state) VALUES
                (402027899, \'Vlood\', \'main_menu\')''')

    conn.commit()


def insert_user(user_id, user_name, curr_state, registration_date, last_activity):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute(
            'INSERT INTO users (user_id, user_name, curr_state, last_activity, registration_date) VALUES (%s, %s, %s, %s, %s)',
            (user_id, user_name, curr_state, last_activity, registration_date)
        )
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        print('User already exists')


def update_state(user_id, user_name, curr_state, last_activity):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'UPDATE users SET user_name = %s, curr_state = %s, last_activity = %s WHERE user_id = %s',
        (user_name, curr_state, last_activity, user_id)
    )
    conn.commit()

    print(user_name + ' at ' + curr_state)


def get_state(user_id: str):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute(
            'SELECT curr_state FROM users WHERE user_id = %s',
            (user_id,)
        )

        q = c.fetchone()
        return q[0]

    except TypeError:
        return 'NoneType error on state fetch'


def insert_profile(user_id, profile_type, profile_name):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO profiles (user_id, profile_type, profile_name) VALUES (%s, %s, %s)',
        (user_id, profile_type, profile_name)
    )
    conn.commit()


def get_profile_id(profile_type, profile_name):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute(
            'SELECT profile_id FROM profiles WHERE profile_type = %s and profile_name = %s',
            (profile_type, profile_name)
        )
        
        q = c.fetchone()
        return q[0]

    except TypeError:
        return 'NoneType error on profile get'


def insert_criteria(profile_id, criteria_type, criteria_value):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO criterias (profile_id, criteria_type, criteria_value) VALUES (%s, %s, %s)',
        (profile_id, criteria_type, criteria_value)
    )
    conn.commit()