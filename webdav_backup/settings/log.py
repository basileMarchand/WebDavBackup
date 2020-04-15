import logging

class Log(logging.Logger):

    __instance = None

    def __init__(self, level=logging.INFO):
        super(Log, self).__init__(level)

        screen = logging.StreamHandler()
        screen.setLevel(level)
        self.addHandler(screen)
        formatter_screen = logging.Formatter('[%(levelname)-8s] :: %(message)s')
        screen.setFormatter(formatter_screen)

    @staticmethod
    def Instance():
        if Log.__instance is None:
            Log.__instance = Log()
        return Log.__instance

    @staticmethod
    def Info(msg: str):
        Log.Instance().info( msg )

    @staticmethod 
    def Warning(msg: str):
        Log.Instance().warning( msg )

    @staticmethod 
    def Debug(msg: str):
        Log.Instance().debug( msg )

    @staticmethod
    def Error(msg: str):
        Log.Instance().error( msg )
        raise Exception

    