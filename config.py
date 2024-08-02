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