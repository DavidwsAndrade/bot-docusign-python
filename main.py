import os
from bot_docusign import BotDocuSign
from logger import Logger
from driver import Driver

if __name__ == "__main__":
    user_email = os.getenv("USER_EMAIL")
    user_passw = os.getenv("USER_PSWD")
    logger = Logger.setup()
    driver = Driver.setup()
    bot = BotDocuSign(user_email, user_passw, logger, driver)
    bot.run()
