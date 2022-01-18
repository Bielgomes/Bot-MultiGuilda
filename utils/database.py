from pymongo import MongoClient
from dotenv import load_dotenv
import certifi
import os
from datetime import datetime

load_dotenv()

ca = certifi.where()

client = MongoClient(os.getenv("database_connection"), tlsCAFile=ca)
db = client['servers']

# GUILD FUNCTIONS

async def get_prefix(client, ctx):
  guildID = str(ctx.guild.id)

  if guildID in db.list_collection_names():
    collection = db[guildID]
    prefix = collection.find_one({'_id': 0})['prefix']
    return prefix
  else:
    collection = db.create_collection(guildID)
    collection.insert_one({'_id': 0, 'prefix': '!'})
    return '!'

async def change_prefix(guildID : int, nPrefix : str):
  collection = db[str(guildID)]
  prefix = collection.find_one({'_id': 0})['prefix']
  if prefix == nPrefix:
    return False
  collection.update_one({'_id': 0}, {'$set': {'prefix': nPrefix}})

# USER FUNCTIONS

async def create_account(guildID : int, userID : int):
  collection = db[str(guildID)]
  if not collection.find_one({'_id': userID}):
    collection.insert_one({'_id': userID, 'money': 100)
    
 async def get_user_money(guildID : int, userID : int):
  collection = db[str(guildID)]
  await create_account(guildID, userID)
  return collection.find_one({'_id': userID})['money']