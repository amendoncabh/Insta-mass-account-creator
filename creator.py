from modules.config import Config
from modules.seleniumbot import runbot
from modules.requestbot import runBot
from modules.background_scheduler import schedule

def accountCreator(botType):
    if botType == 1:
        runbot()
    elif botType == 2:
        runBot()
    elif botType == 3:
        schedule(runbot, Config['bot_timing_schedule'])
    else:
        raise Exception("Invalid bot type!")


accountCreator(1)
# accountCreator(Config['bot_type'])
