from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = 'deepak'
DB_NAME = 'notepad'

DATABASE = MongoClient()[DB_NAME]
POSTS = DATABASE.posts
IDS = DATABASE.ids
SETTINGS_COLLECTION = DATABASE.settings

DEBUG = True