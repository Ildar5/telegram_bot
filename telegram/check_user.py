from postgres_command import command


class CheckUser:

    def __init__(self):
        self.cd = command.Command()

    def check_user_exist(self, user_id):
        query = ['get_telegram_user', user_id]
        get = self.cd.run_command(query)
        if get[0] == 0:
            add_user = ['add_telegram_user', user_id]
            self.cd.run_command(add_user)
