
import json
import logging
import sys
import time
import subprocess
import telepot
#from urllib import request
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import os

# store the TOKEN for the Telegram Bot
TOKEN = '763104210:AAFmqH_denR6_EN1qVxfEBBQaE7M9SY9ZV8'


def run_sqlplus(sqlplus_script):
    """
    Run a sql command or group of commands against
    a database using sqlplus.
    """
    p = subprocess.Popen(['sqlplus ','/nolog'],stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (stdout,stderr) = p.communicate(sqlplus_script.encode('utf-8'))
    stdout_lines = stdout.decode('utf-8').split("\n")

    return stdout_lines

def on_chat_message(msg):
    name    = msg["from"]["first_name"]
    content_type, chat_type, chat_id = telepot.glance(msg)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='POS today', callback_data='postoday')],
                   [InlineKeyboardButton(text='Laporan Kasir Harian', callback_data='kasirharian')],
                   [InlineKeyboardButton(text='Laporan Penjualan', callback_data='rpt_sales')],
                   [InlineKeyboardButton(text='Laporan Void', callback_data='kasir')],
                   [InlineKeyboardButton(text='Penjualan per PLU', callback_data='ultra')],
                   [InlineKeyboardButton(text='Penjualan Per Waiter', callback_data='flameA')],
                   [InlineKeyboardButton(text='Lain-lain', callback_data='flameD')]
               ])

    bot.sendMessage(chat_id, 'Selamat Datang di IRS Bot!'.format(name), reply_markup=keyboard)

#The function on_callback_query pprocess the data from Thingspeak and react according to the pushed button
def on_callback_query(msg):
    # istore in a variable the response from  GET response
    #response = request.urlopen('qui il link del vostro canale thingspeak')
    # get the json data from the request
    #data = response.read().decode('utf-8')

    # convert the string in dictionary
    #data_dict = json.loads(data)

    #separate the value that you need
    #feeds = data_dict['feeds']

    #let it react to the press of the button
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    if(query_data == 'postoday'):

        sqlplus_script="""
                set colsep ,
                set headsep off
                set pagesize 0
                set trimspool on
                spool d:\salesybplu.txt

                connect IRS/IRS041972@ASTRO
                select * from uom_mst;
                exit

                """

        bot.sendMessage(from_id, parse_mode='HTML', text='<b>Laporan Penjualan per PLU</b>')

        sqlplus_output = run_sqlplus(sqlplus_script)
        #for line in sqlplus_output:
        #    print(line)
        
        f = open('d:\salesybplu.txt', 'rb')  
        bot.sendDocument(from_id, f)

        '''
            'text' => 'Success! Your Telegram account with name <b>'.$first_name.' '.$last_name.'</b> has been added into iBridge data!.%0ABack to <a href= \n"https://ibridgeapp.com/home \n">iBridge</a>',
            'parse_mode' => 'HTML'
        '''

    elif(query_data == 'kasirharian'):
        command = " D:\\Data\\RESTO\\ASTRO\\IRS\\run_batch.hta "  # the shell command
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #Launch the shell command:
        output, error = process.communicate()

        time.sleep(20)

        # JANGAN BUAT NAMA FILE DEPAN NYA r 
        f = open('d:\kasir_harian.txt', 'rb')  
        bot.sendDocument(from_id, f)

    elif(query_data == 'rpt_sales'):
        sqlplus_script ="""
                connect IRS/IRS041972@ASTRO                
                @D:\Data\IRSPython\Telegram\item_mst.sql
            """ 

        sqlplus_output = run_sqlplus(sqlplus_script)
        print(sqlplus_output[0])        
        f = open('d:\item_mst.html', 'rb')  
        bot.sendDocument(from_id, f)

    elif(query_data == 'ultra'):
        bot.sendMessage(from_id, text="C qualcosa ad una distanza di: ")

    elif(query_data == 'flameA'):
        bot.sendMessage(from_id, text='Il sensore di luce misura: ')

    elif(query_data == 'flameD'):

        if(feeds[1]['field6'] == '0'):
            bot.sendMessage(from_id, text="Non  fiamma in casa")

        elif(feeds[1]['field6'] == '1'):
            bot.sendMessage(from_id, text="ATTENZIONE CPRESENZA DI FIAMMA IN CASA!")

#initialize the functions
bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
