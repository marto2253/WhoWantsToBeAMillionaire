import tkinter as tk
from PIL import ImageTk, Image
import tkinter.font as tkFont
import tkinter.ttk as ttk
from database import Database
import tkinter.messagebox as mb
import random
database = Database()


class Game:

    def __init__(self):

        # Create the application window.
        self.window = tk.Tk()
        self.window.geometry("720x520")
        self.window.resizable(False, False)
        self.window.title("Who wants to be a millionaire")

        # Create a notebook with two tabs (Game and Database tab).
        self.style = ttk.Style()
        self.style.layout("TNotebook", [])  # remove the border of the notebook.
        self.notebook = self.create_notebook()

        self.game_frame = self.game_frame()  # create a frame which contains the game widgets
        self.database_frame = self.database_frame()  # create a frame which contains the database widgets

        self.background = ImageTk.PhotoImage(Image.open("pictures/final_bg1.png"))  # game frame background image.
        self.background_label = self.create_background_label()  # set the game frame background image.

        # Adding the frames to the notebook.
        self.notebook.add(self.game_frame, text='Game')
        self.notebook.add(self.database_frame, text='Database')

        # The text(rewards) listed on the rewards label.
        self.rewards = {
            '15': '100 000', '14': '  50 000', '13': '  30 000', '12': '  20 000', '11': '  10 000', '10': '  5 000',
            '9': '    3 000', '8': '    2 000', '7': '    1 500', '6': '    1 000', '5': '      500',
            '4': '      400', '3': '      300', '2': '      200', '1': '      100',
        }

        # Game tab widgets and some of their functionalities.
        self.question_label = self.create_question_label()
        self.rewards_label = self.create_reward_label()

        self.left_button = self.create_left_button()
        self.down_left_button = self.create_down_left_button()
        self.right_button = self.create_right_button()
        self.down_right_button = self.create_down_right_button()

        #  Initialize the binding of the buttons.
        self.binded_buttons = self.bind_buttons(self.left_button, self.down_left_button,
                                                self.right_button, self.down_right_button)

        self.call_friend_image = tk.PhotoImage(file='pictures/call_a_friend.png')  # Call a friend button image.
        self.fifty_fifty_image = tk.PhotoImage(file='pictures/fifty_fifty.png')  # 50/50 button image.
        self.ask_the_audience_image = tk.PhotoImage(file='pictures/audience.png')  # Ask the audience button image.
        self.progress_bar = self.create_progress_bars()  # create the progress bars for the ask the audience joker.
        self.take_money_image = tk.PhotoImage(file='pictures/take_money.png')  # Take money button image.

        self.call_friend_button = self.call_a_friend_button()
        self.ask_the_audience_button = self.ask_the_audience()
        self.fifty_fifty_button = self.fifty_fifty()
        self.take_money_button = self.take_money()

        # Database tab widgets.
        self.list_box = self.create_list_box()
        self.question_entry = self.create_question_entry()
        self.answer_A_entry = self.create_answer_A_entry()
        self.answer_B_entry = self.create_answer_B_entry()
        self.answer_C_entry = self.create_answer_C_entry()
        self.answer_D_entry = self.create_answer_D_entry()
        self.right_answer = self.create_right_answer()
        self.view_all_button = self.create_view_all_button()
        self.delete_entry_button = self.create_delete_entry_button()
        self.submit_entry_button = self.create_submit_entry_button()
        self.scroll_bars = self.create_scroll_bars()

        # Others
        self.q_number = 1  # the number of the currect question.
        self.rewards_label[14].configure(bg='orange')  # initiate the orange color of the first question.

    def create_notebook(self):
        notebook = ttk.Notebook(self.window)
        notebook.pack(expand=True)

        return notebook

    def game_frame(self):
        frame = tk.Frame(self.notebook)
        frame.pack(expand=True, fill='both')

        return frame

    def database_frame(self):
        frame = tk.Frame(self.notebook)
        frame.pack(expand=True, fill='both')

        return frame

    def create_background_label(self):
        label = tk.Label(self.game_frame, image=self.background)
        label.pack(expand=True)

        return label

    def create_question_label(self):
        label = tk.Label(self.game_frame, height=3, width=62, bg='#2c1ba5', text=database.show_question(1)[0][0],
                         fg='white', anchor=tk.W, font='Helvetica, 11', justify=tk.LEFT, wraplength=555, bd=0)
        label.place(x=75, y=303)

        return label

    def create_left_button(self):
        left_button = tk.Button(self.game_frame, text=database.show_answers(1)[0][0],
                                width=32, bg='#2c1ba5', fg='white', bd=0, font='Helvetica, 9', anchor=tk.W,
                                activebackground='#2c1ba5')
        left_button.place(x=103, y=397)

        return left_button

    def create_down_left_button(self):
        down_left_button = tk.Button(self.game_frame, text=database.show_answers(1)[0][1],
                                     width=32, bg='#2c1ba5', fg='white', bd=0, font='Helvetica, 9', anchor=tk.W,
                                     activebackground='#2c1ba5')
        down_left_button.place(x=103, y=446)

        return down_left_button

    def create_right_button(self):
        right_button = tk.Button(self.game_frame, text=database.show_answers(1)[0][2],
                                 width=32, bg='#2c1ba5', fg='white', bd=0, font='Helvetica, 9', anchor=tk.W,
                                 activebackground='#2c1ba5')
        right_button.place(x=425, y=397)

        return right_button

    def create_down_right_button(self):
        down_right_button = tk.Button(self.game_frame, text=database.show_answers(1)[0][3],
                                      width=32, bg='#2c1ba5', fg='white', bd=0, font='Helvetica, 9', anchor=tk.W,
                                      activebackground='#2c1ba5')
        down_right_button.place(x=425, y=446)

        return down_right_button

    def remove_progressbar(self):  # remove the progress bar of ask the audience joker after it has been used.
        for i in range(4):
            self.progress_bar[0][i].place_forget()
            self.progress_bar[1][i].place_forget()

    def create_progress_bars(self):

        all_p_bars = []
        all_labels = []
        label_text = ['A:', 'B:', 'C:', 'D:']
        for i in range(4):
            label = tk.Label(self.game_frame, text=label_text[i], bg='#2c1ba5', fg='white')
            progress_bar = ttk.Progressbar(self.game_frame, orient=tk.VERTICAL, length=100)
            all_p_bars.append(progress_bar)
            all_labels.append(label)

        return all_p_bars, all_labels

    #  the functionality behind ask the audience joker. It makes the progress bars visible and display their value.
    def progress_bar_functionality(self):
        x, y = 130, 160
        for i in range(4):
            self.progress_bar[0][i].place(x=x, y=y)
            self.progress_bar[1][i].place(x=x + 2, y=260)
            x += 30
        left = False
        right = False
        down_left = False
        down_right = False
        # the following loop checks if the answer is correct and whether it has been checked already.
        while not left and not right and not down_right and not down_left:
            if self.left_button['text'] not in database.right_answers() and not left:
                left = True
                self.progress_bar[0][0].config(value=20)
            elif self.left_button['text'] in database.right_answers() and not left:
                left = True
                self.progress_bar[0][0].config(value=80)
            if self.right_button['text'] not in database.right_answers() and not right:
                right = True
                self.progress_bar[0][2].config(value=35)
            elif self.right_button['text'] in database.right_answers() and not right:
                right = True
                self.progress_bar[0][2].config(value=80)
            if self.down_left_button['text'] not in database.right_answers() and not down_left:
                down_left = True
                self.progress_bar[0][1].config(value=50)
            elif self.down_left_button['text'] in database.right_answers() and not down_left:
                down_left = True
                self.progress_bar[0][1].config(value=80)
            if self.down_right_button['text'] not in database.right_answers() and not down_right:
                down_right = True
                self.progress_bar[0][3].config(value=40)
            elif self.down_right_button['text'] in database.right_answers() and not down_right:
                down_right = True
                self.progress_bar[0][3].config(value=80)

        self.ask_the_audience_button.configure(state=tk.DISABLED)  # disables the button after it has been used.

    def ask_the_audience(self):

        button = tk.Button(self.game_frame, image=self.ask_the_audience_image, borderwidth=0, bg='#2c1ba5',
                           activebackground='#2c1ba5', command=self.progress_bar_functionality)
        button.place(x=15, y=150)

        return button

    def call_a_friend_functionality(self):
        question = self.question_label["text"]
        suggestion = tk.StringVar()

        # the following code gives diversity. There is 0.2% chance of the 'friend' not knowing the answer.
        number = random.randint(1, 5)
        if number != 1:
            suggestion.set(f'I believe the right answer should be: {database.get_right_answer(question)}')
        else:
            suggestion.set(f'I am not sure about this one, sorry.')

        # creates the MB, which shows the joker's message.
        message_box = mb.showinfo("Call from a friend", suggestion.get())

        self.call_friend_button.configure(state=tk.DISABLED)  # disables the button after it has been used.

        return message_box

    def call_a_friend_button(self):

        button = tk.Button(self.game_frame, image=self.call_friend_image, borderwidth=0, bg='#2c1ba5',
                           activebackground='#2c1ba5', command=self.call_a_friend_functionality)
        button.place(x=15, y=10)

        return button

    def fifty_fifty_functionality(self):
        counter = 0
        left = False
        right = False
        down_left = False
        down_right = False
        #  the loop iterates through the answers and checks if the current asnwer is correct or not.
        #  If it is correct is omits it and removes the next two incorrect ones.
        while counter != 2:
            if self.left_button['text'] not in database.right_answers() and left != True:
                self.left_button['text'] = ''
                left = True
                counter += 1
            elif self.right_button['text'] not in database.right_answers() and right != True:
                self.right_button['text'] = ''
                right = True
                counter += 1
            elif self.down_left_button['text'] not in database.right_answers() and down_left != True:
                self.down_left_button['text'] = ''
                down_left = True
                counter += 1
            elif self.down_right_button['text'] not in database.right_answers() and down_right != True:
                self.down_right_button['text'] = ''
                down_right = True
                counter += 1

        self.fifty_fifty_button.configure(state=tk.DISABLED)

    def fifty_fifty(self):
        button = tk.Button(self.game_frame, image=self.fifty_fifty_image, borderwidth=0, bg='#2c1ba5',
                           activebackground='#2c1ba5', command=self.fifty_fifty_functionality)
        button.place(x=15, y=80)

        return button

    #  servers the purpose as a 'restart' of the game. Whenever the player gets an answer wrong or wins a certain price
    #  he is asked if he would like to try the game one more time and if he agrees, the following code resets the game.
    def restart(self):
        self.question_label['text'] = database.show_question(self.q_number)[0][0]
        self.left_button['text'] = database.show_answers(self.q_number)[0][0]
        self.down_left_button['text'] = database.show_answers(self.q_number)[0][1]
        self.right_button['text'] = database.show_answers(self.q_number)[0][2]
        self.down_right_button['text'] = database.show_answers(self.q_number)[0][3]
        self.fifty_fifty_button.configure(state=tk.NORMAL)
        self.ask_the_audience_button.configure(state=tk.NORMAL)
        self.call_friend_button.configure(state=tk.NORMAL)
        self.remove_progressbar()

    def take_money_functionality(self):
        price = self.rewards_label[16 - self.q_number]["text"][-7:]
        message_box = mb.askquestion('Congratulations!', f'You walk away with: {str(price).replace(" ", "") + "$"}'
                                                         '\nDo you want to try again?')
        if message_box == 'yes':
            self.rewards_label[15 - self.q_number].configure(bg='#6158ac')
            self.rewards_label[14].configure(bg='orange')
            self.q_number = 1
            self.restart()
        else:
            exit()

    def take_money(self):

        button = tk.Button(self.game_frame, image=self.take_money_image, borderwidth=0, bg='#2c1ba5',
                           activebackground='#2c1ba5', command=self.take_money_functionality)
        button.place(x=15, y=220)

        return button

    # If you give a wrong asnwer. The following codes prompts a MB asking if you'd like to try again.
    def wrong_asnwer(self):
        message_box = mb.askquestion("GAME OVER :(", "Do you want to try again?")
        return message_box

    # If you win the big price. The following codes prompts a MB asking if you'd like to try again.
    def win_game(self):
        message_box = mb.askquestion('Congratulations!!!', 'You have won the big price of 100 000$!'
                                                           '\nDo you want to play again?')
        return message_box

    # the functionality behind the click of each answer button. It takes the event of clicking and depending on
    # which button has been clicked it takes its text(answer) and checks if the answer is correct or not.
    # Based on the answer the game might continue, or you would have to begin again from the beginning.
    def button_click(self, event):
        clicked_b = event.widget  # the event of clicking a button
        b_value = clicked_b['text']  # getting the text of the clicked button.
        if b_value in database.right_answers():  # checks if the answer is correct
            self.q_number += 1
            self.rewards_label[14].configure(bg='#6158ac')  # updates the color of the rewards label.
            self.rewards_label[16 - self.q_number].configure(bg='#6158ac')  # updates the color of the rewards label.
            self.rewards_label[15 - self.q_number].configure(bg='orange')  # updates the color of the rewards label.
            if self.q_number > 15:  # checks if you have answered the last question.
                if self.win_game() == 'no':  # prompts the MB and based on your answer restarts or exits the game.
                    exit()
                else:
                    self.q_number = 1
                    self.restart()
            # updates the question label and buttons' texts with the next question and answers.
            self.question_label['text'] = database.show_question(self.q_number)[0][0]
            self.left_button['text'] = database.show_answers(self.q_number)[0][0]
            self.down_left_button['text'] = database.show_answers(self.q_number)[0][1]
            self.right_button['text'] = database.show_answers(self.q_number)[0][2]
            self.down_right_button['text'] = database.show_answers(self.q_number)[0][3]
            self.remove_progressbar()
        else:  # if the answer is incorrect prompts a MB which ask you if you'd like to try again or exit.
            if self.wrong_asnwer() == 'no':
                exit()
            else:
                self.rewards_label[15 - self.q_number].configure(bg='#6158ac')
                self.rewards_label[14].configure(bg='orange')
                self.q_number = 1
                self.restart()

    # the binding of the buttons.
    def bind_buttons(self, left_button, down_left_button, right_button, down_right_button):
        left_button.bind('<Button-1>', self.button_click)
        down_left_button.bind('<Button-1>', self.button_click)
        right_button.bind('<Button-1>', self.button_click)
        down_right_button.bind('<Button-1>', self.button_click)

    def create_reward_label(self):
        x_axis = 510
        y_axis = 10
        all_labels = []
        for num, price in self.rewards.items():  # the loop creates 15 labels, each for each reward.
            t = num + '            ' + price
            label = tk.Label(self.game_frame, text=t, width=20, anchor=tk.W, bd=1, bg='#6158ac')
            font_config = tkFont.Font(family='Arial', size=11, weight='bold')
            label.configure(font=font_config)
            label.place(x=x_axis, y=y_axis)
            y_axis += 18
            all_labels.append(label)

        return all_labels

    # Database tab widgets and functionalities.
    def create_question_entry(self):
        label = tk.Label(self.database_frame, text='Enter your question below.')
        label.place(x=50, y=20)
        entry = tk.Entry(self.database_frame, width=80)
        entry.place(x=50, y=40)

        return entry

    def create_answer_A_entry(self):
        label = tk.Label(self.database_frame, text='A:')
        label.place(x=60, y=80)
        entry = tk.Entry(self.database_frame, width=30)
        entry.place(x=80, y=80)

        return entry, label

    def create_answer_B_entry(self):
        label = tk.Label(self.database_frame, text='B:')
        label.place(x=60, y=120)
        entry = tk.Entry(self.database_frame, width=30)
        entry.place(x=80, y=120)

        return entry, label

    def create_answer_C_entry(self):
        label = tk.Label(self.database_frame, text='C:')
        label.place(x=330, y=80)
        entry = tk.Entry(self.database_frame, width=30)
        entry.place(x=350, y=80)

        return entry, label

    def create_answer_D_entry(self):
        label = tk.Label(self.database_frame, text='D:')
        label.place(x=330, y=120)
        entry = tk.Entry(self.database_frame, width=30)
        entry.place(x=350, y=120)

        return entry, label

    def create_right_answer(self):  # Create an option menu for the player to choose which answer is the correct one.
        options = self.answer_A_entry[1]['text'], self.answer_B_entry[1]['text'], \
                  self.answer_C_entry[1]['text'], self.answer_D_entry[1]['text']
        label = tk.Label(self.database_frame, text='Choose the right answer.')
        label.place(x=80, y=160)
        name = tk.StringVar()
        name.set('Answers')
        options = tk.OptionMenu(self.database_frame, name, *options)
        options.place(x=80, y=180)
        return options, name

    def submit_entry_button_functionality(self):
        if self.question_entry.get() != '' and self.answer_A_entry[0].get() != '' and \
                self.answer_B_entry[0].get() != '' and self.answer_C_entry[0].get() != '' and \
                self.answer_D_entry[0].get() != '':

            if self.right_answer[1].get() == 'A:':
                database.insert_record(self.question_entry.get(), self.answer_A_entry[0].get(),
                                       self.answer_B_entry[0].get(), self.answer_C_entry[0].get(),
                                       self.answer_D_entry[0].get(), self.answer_A_entry[0].get())
            elif self.right_answer[1].get() == 'B:':
                database.insert_record(self.question_entry.get(), self.answer_A_entry[0].get(),
                                       self.answer_B_entry[0].get(), self.answer_C_entry[0].get(),
                                       self.answer_D_entry[0].get(), self.answer_B_entry[0].get())
            elif self.right_answer[1].get() == 'C:':
                database.insert_record(self.question_entry.get(), self.answer_A_entry[0].get(),
                                       self.answer_B_entry[0].get(), self.answer_C_entry[0].get(),
                                       self.answer_D_entry[0].get(), self.answer_C_entry[0].get())
            elif self.right_answer[1].get() == 'D:':
                database.insert_record(self.question_entry.get(), self.answer_A_entry[0].get(),
                                       self.answer_B_entry[0].get(), self.answer_C_entry[0].get(),
                                       self.answer_D_entry[0].get(), self.answer_D_entry[0].get())

            #  deletes the submited answers/question from the entry widgets.
            self.question_entry.delete(0, tk.END)
            self.answer_A_entry[0].delete(0, tk.END)
            self.answer_B_entry[0].delete(0, tk.END)
            self.answer_C_entry[0].delete(0, tk.END)
            self.answer_D_entry[0].delete(0, tk.END)

    def create_submit_entry_button(self):
        button = tk.Button(self.database_frame, text='Submit', width=10, command=self.submit_entry_button_functionality)
        button.place(x=580, y=80)

        return button

    def delete_entry_button_functionality(self):
        selected = str(self.list_box.curselection()[0])
        index = self.list_box.get(selected)[0]
        database.delete_record(index)

    def create_delete_entry_button(self):
        button = tk.Button(self.database_frame, text='Delete', width=10, command=self.delete_entry_button_functionality)
        button.place(x=580, y=290)

        return button

    def create_list_box(self):
        label = tk.Label(self.database_frame, text='List of all questions and answers.')
        label.place(x=50, y=230)
        list_box = tk.Listbox(self.database_frame, height=10, width=80)
        list_box.place(x=50, y=250)

        return list_box

    def create_scroll_bars(self):
        sb1 = tk.Scrollbar(self.database_frame, command=self.list_box.yview)
        sb1.place(x=540, y=300)
        sb2 = tk.Scrollbar(self.database_frame, orient='horizontal',command=self.list_box.xview)
        sb2.place(x=250, y=420)
        self.list_box.configure(xscrollcommand=sb2.set, yscrollcommand=sb1.set)

        return sb1, sb2

    def viel_all_functionality(self):
        self.list_box.delete(0, tk.END)
        for row in database.view():
            self.list_box.insert(tk.END, row)

    def create_view_all_button(self):
        button = tk.Button(self.database_frame, text='View all', width=10, command=self.viel_all_functionality)
        button.place(x=580, y=250)

        return button

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    game = Game()
    game.run()
