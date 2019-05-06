import re
import mysql.connector as mariadb
import xlrd
import pandas as pd
sheets_dict = pd.read_excel('output.xlsx')
print("done")

db = mariadb.connect(user='matchmaker_admin', password='csProject411!',database='matchmaker_a')
cursor = db.cursor()

spq="""INSERT INTO users (age,body_type,diet,drinks,education,ethnicity,height,income,job,location,offspring,religion,orientation,pets,sex,speaks,password,name,email) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
for index, row in sheets_dict.iterrows():
    print("id: "+str(row['a']))
    cursor.execute(spq, [str(row['b']),str(row['c']),str(row['d']),str(row['e']),str(row['f']),str(row['g']),str(row['h']),str(row['i']),str(row['j']),str(row['k']),str(row['l']),str(row['m']),str(row['n']),str(row['o']),str(row['p']),str(row['q']),str(row['r']),str(row['s']),str(row['t'])])
    db.commit()