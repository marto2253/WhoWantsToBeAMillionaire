import sqlite3


class Database:

    def __init__(self):
        self.conn = sqlite3.connect('millionaire.db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS questions (
        question text, a1 text, a2 text, a3 text, a4 text, right_answer text)
        """)
        self.conn.commit()

    def insert_record(self, question, a1, a2, a3, a4, right_answer):
        self.c.execute("INSERT INTO questions VALUES (?, ?, ?, ?, ?, ?)", (question, a1, a2, a3, a4, right_answer))
        self.conn.commit()

    def show_question(self, number):
        self.c.execute("SELECT question FROM questions WHERE rowid = (?)", (number,))
        row = self.c.fetchall()

        return row

    def show_answers(self, number: int):
        self.c.execute("SELECT a1, a2, a3 ,a4 FROM questions WHERE rowid = (?)", (number,))
        row = self.c.fetchall()

        return row

    def view(self):
        self.c.execute("SELECT rowid, * FROM questions")
        rows = self.c.fetchall()

        return rows

    def delete_record(self, number):
        self.c.execute("DELETE FROM questions WHERE rowid = (?)", (number,))
        self.conn.commit()

    def right_answers(self):
        list_with_answers = []
        self.c.execute("SELECT right_answer FROM questions")
        items = self.c.fetchall()
        for item in items:
            list_with_answers.append(item[0])

        return list_with_answers

    def get_right_answer(self, q: str):
        self.c.execute("SELECT right_answer FROM questions WHERE question = (?)", (q,))
        items = self.c.fetchall()

        return items[0][0]

    def __del__(self):
        self.conn.close()
