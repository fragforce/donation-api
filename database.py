import os
from urllib import parse
import psycopg2

import config
import extralife

parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

try:
  conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
  )
except:
  print("Unable to connect to database")

def update_team():
  try:
    T = extralife.team(config.EXTRALIFE_TEAMID)
    cur = conn.cursor()
    SQL = """
      INSERT INTO extralife_team (team_id, name, raised, goal, avatar_url, created)
      VALUES (%s, %s, %s, %s, %s, %s)
      ON CONFLICT(team_id) DO UPDATE
      SET
        name=%s,
        raised=%s,
        goal=%s,
        avatar_url=%s,
        created=%s;
      """
    data = (T.team_id, T.name, T.raised, T.goal, T.avatar_url, T.created, T.name, T.raised, T.goal, T.avatar_url, T.created)
    cur.execute(SQL, data)
    conn.commit()
    return True
  except:
    return False

def create_tables():
  cur = conn.cursor()
  cur.execute("""CREATE TABLE IF NOT EXISTS extralife_team(team_id INT PRIMARY KEY NOT NULL, name TEXT NOT NULL, raised REAL, goal REAL, avatar_url TEXT, created TEXT);""")
  conn.commit()

