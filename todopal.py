from todotxt import *
import pandas as pd
import telebot
from datetime import date
from tools import *
import os

cwd = os.getcwd()
keys = open_keys( cwd+"/secret.yaml" )
bot = telebot.TeleBot(keys["Bot Token"])
user_id = keys["User ID"]
todos = TodoFile(keys["Todo File"])
todos.load()

todo_df = pd.DataFrame.from_records([todo.to_dict() for todo in todos.todo_entries])

todo_df["threshold"] = pd.to_datetime( todo_df["threshold"], errors="coerce" )
todo_df["due"] = pd.to_datetime( todo_df["due"], errors="coerce" )

def ping_should_be_working_on(uid, df):
    today = date.today().strftime("%d/%m/%Y")
    mask = ((today>df["threshold"]) & (df["due"]>today))
    df = df.loc[mask]
    result = "You should be working on:\n"+df.to_string()
    bot.send_message(uid, result)

def ping_too_late(uid, df):
    today = date.today().strftime("%d/%m/%Y")
    mask = (df["due"]<today)
    df = df.loc[mask]
    result = "Too late for:\n"+df.to_string()
    bot.send_message(uid, result)

ping_should_be_working_on(user_id, todo_df)
ping_too_late(user_id, todo_df)