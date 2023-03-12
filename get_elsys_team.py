# postgreSQL database connection

import psycopg2
from dotenv import load_dotenv
import os

class Teams:
    def __init__(self):
        # config db - env

        load_dotenv('.env.db.local')

        USERNAME = os.getenv('USERNAME')
        PASSWORD = os.getenv('PASSWORD')
        HOST = os.getenv('HOST')
        PORT = os.getenv('PORT')
        DATABASE = os.getenv('DATABASE')
        SSLMODE = os.getenv('SSLMODE')

        # connect to the database

        conn = None

        try:
            conn = psycopg2.connect(user = USERNAME,
                                    password = PASSWORD,
                                    host = HOST,
                                    port = PORT,
                                    database = DATABASE,
                                    sslmode = SSLMODE)
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
            print("Make sure you have the correct credentials in .env.db.local file")
            print(USERNAME, PASSWORD, HOST, PORT, DATABASE, SSLMODE, sep='\n')
            exit(-1)

        # create a cursor

        cur = conn.cursor()

        # make an array for every team and add the emails of the team members

        cur.execute('SELECT id, name FROM teams WHERE id != 1')
        teams = cur.fetchall()

        # print the results

        self.emails = []

        for team in teams:
            print(f"[GETTING] Team {team[0]}: {team[1]}")
            cur.execute(f'SELECT elsys_email, concat(first_name, \' \', last_name) FROM users WHERE team_id = {team[0]} AND deleted_at IS NULL')
            temp = cur.fetchall()
            # remove double spaces and spaces at the end
            for i in range(len(temp)):
                temp[i] = (temp[i][0], temp[i][1].replace("  ", " ").strip())
            
            self.emails.append(temp)
            
        # close the communication with the PostgreSQL

        cur.close()
        conn.close()

        # print the results

        for i in range(len(self.emails)):
            print(f"[TEAM {i+1}]")
            for email in self.emails[i]:
                print(email[0])

    def get_team_emails(self, id):
        return self.emails[id-2] # compensate for the first team - admin team





