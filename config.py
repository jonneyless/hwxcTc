from environs import Env

env = Env()
env.read_env()

mysqlInfo = {
    "host": env.str("DB_HOST", "3.1.50.237"),
    "db": env.str("DB_DATABASE", "welcome"),
    "user": env.str("DB_USER", "sync"),
    "passwd": env.str("DB_PASS", "pcKyxHZzHcz35D33"),
    "port": env.int("DB_PORT", 3306),
}

redisInfo = {
    "host": env.str("REDIS_HOST", "127.0.0.1"),
    "port": env.int("REDIS_PORT", 6379),
}

bot_token = env.str('BOT_TOKEN', "5556519757:AAHrQvrSfsS-I20cgTVorxuBHFkN4IwtqRY")
bot_tg_id = env.int('BOT_ID', 5556519757)
bot_url = "https://api.telegram.org/bot%s/" % bot_token

welcome_bot_token = env.str('WELCOME_BOT_TOKEN', "5759299188:AAHSTq6xbLEb9oWFBkLonFtn3nDLzLkR_EE")
welcome_bot_url = "https://api.telegram.org/bot%s/" % welcome_bot_token
