from environs import Env

env = Env()
env.read_env()

MONGO_URI = env.str("MONGO_URI")
DATABASE_NAME = env.str("DATABASE_NAME")
