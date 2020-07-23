import psycopg2
from env import environment


env = environment.Environment().get_env()


def migrate():
    conn = psycopg2.connect(dbname=env['POSTGRES_DB_NAME'], user=env['POSTGRES_DB_USER'],
                            password=env['POSTGRES_DB_PASSWORD'], host=env['POSTGRES_DB_HOST'])
    cursor = conn.cursor()
    conn.autocommit = True

    commands = (
        """
          CREATE TABLE telegram_user (
            id INT PRIMARY KEY NOT NULL
          );
        """,
        """ 
          CREATE SEQUENCE tg_audio_messages_seq;
        """,
        """
          CREATE TABLE IF NOT EXISTS audio (
            id CHAR(24) NOT NULL DEFAULT TRIM('audio_message_' || nextval('tg_audio_messages_seq')),
            file_path VARCHAR(255) NOT NULL,
            user_id INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES telegram_user(id)
          );
          """,
        """
          ALTER SEQUENCE tg_audio_messages_seq OWNED BY audio.id;
        """,
        """ 
          CREATE SEQUENCE tg_image_seq;
        """,
        """
          CREATE TABLE IF NOT EXISTS image (
            id CHAR(24) NOT NULL DEFAULT TRIM('image_' || nextval('tg_image_seq')),
            file_path VARCHAR(255) NOT NULL,
            user_id INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES telegram_user(id)
          );
          """,
        """
          ALTER SEQUENCE tg_image_seq OWNED BY image.id;
        """,
    )

    try:
        for command in commands:
            cursor.execute(command)

        cursor.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    migrate()
