from pymongo import MongoClient
from local_databaseconfig import host

database = MongoClient(host=host)

bmi = database["BMI"]