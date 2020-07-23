import psycopg2


class Command:

    def run_command(self, query):

        print('query')
        print(query)
        # print(query.get('type'))

        conn = psycopg2.connect(dbname='bot', user='postgres',
                                password='1163524p', host='localhost')
        cursor = conn.cursor()
        command = None

        if query[0] == 'get_telegram_user':
            command = "SELECT COUNT (*) FROM telegram_user WHERE id = {0};".format(query[1])
        elif query[0] == 'add_telegram_user':
            command = "INSERT INTO telegram_user (id) VALUES ({0});".format(query[1])
        elif query[0] == 'audio':
            command = "INSERT INTO audio (file_path, user_id) VALUES ('{0}', {1});".format(query[1], query[2])
        elif query[0] == 'image':
            command = "INSERT INTO image (file_path, user_id) VALUES ('{0}', {1});".format(query[1], query[2])

        try:
            cursor.execute(command)
            if query[0] == 'get_telegram_user':
                return cursor.fetchone()
                # return cursor.fetchall()

            cursor.close()
            conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()
