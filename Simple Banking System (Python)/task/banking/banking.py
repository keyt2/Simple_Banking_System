import random
import sqlite3

dict = {}

def check_luhn(card_number: str):
    control_number = list(card_number[:len(card_number)-1])
    for i in range(0, len(control_number), 2):
        control_number[i] = str(int(control_number[i]) * 2)
        if int(control_number[i]) > 9:
            control_number[i] = str(int(control_number[i]) - 9)
    checksum = 0
    for i in range(len(control_number)):
        checksum += int(control_number[i])
    last_digit = 10 - checksum % 10
    if last_digit == 10:
        last_digit = 0
    if card_number[len(card_number)-1] == str(last_digit):
        return True
    else:
        return False

def menu2(card_number, cur, conn):
    x = 1
    while True:
        x = int(input("\n1. Balance\n2. Add income\n3. Do tranfer\n"
                      "4. Close account\n5. Log out\n0. Exit"))
        if x == 1:
            cur.execute("SELECT balance FROM card WHERE number == " + card_number + ";")
            print(f"\nBalance: {str(cur.fetchone())}\n")
        elif x == 2:
            x = input("\nEnter income:\n")
            cur.execute("UPDATE card SET balance = balance + " + x + " WHERE number == " + card_number + ";")
            conn.commit()
        elif x == 3:
            print("\nTransfer\n")
            transfer_card = input("Enter card number:\n")
            if not check_luhn(transfer_card):
                print("\nProbably you made a mistake in the card number. Please try again!\n")
            elif transfer_card == card_number:
                print("\nYou can't transfer money to the same account!\n")
            else:
                cur.execute('SELECT pin FROM card WHERE number == ' + transfer_card + ';')
                result = cur.fetchone()
                if result is None:
                    print("\nSuch a card does not exist.\n")
                else:
                    amount = int(input("\nEnter how much money you want to transfer:\n"))
                    cur.execute('SELECT balance FROM card WHERE number == ' + card_number + ";")
                    result = str(cur.fetchone())
                    result = int(result[1:len(result)-2])
                    if result < amount:
                        print('\nNot enough money!\n')
                    else:
                        cur.execute('UPDATE card SET balance = balance - ' + str(amount) + ' WHERE number == ' + card_number + ';')
                        cur.execute('UPDATE card SET balance = balance + ' + str(amount) + ' WHERE number == ' + transfer_card + ';')
                        conn.commit()
        elif x == 4:
            cur.execute('DELETE FROM card WHERE number == ' + card_number + ';')
            conn.commit()
        elif x == 5:
            print("\nYou have successfully logged out!\n")
            return 1
        elif x == 0:
            return 0


def menu():
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS card ("
                "id INTEGER PRIMARY KEY,"
                "number TEXT,"
                "pin TEXT,"
                "balance INTEGER DEFAULT 0);")
    conn.commit()
    x = 1
    while x != 0: 
        x = int(input("\n1. Create an account\n2. Log into account\n0. Exit\n"))
        card_number = '400000'
        pin = str(random.randint(0,9))
        if x==1:
            for _ in range(1,10):
                card_number += str(random.randint(0,9))
            control_number = list(card_number)
            for i in range(0, len(control_number), 2):
                control_number[i] = str(int(control_number[i]) * 2)
                if int(control_number[i]) > 9:
                    control_number[i] = str(int(control_number[i]) - 9)
            checksum = 0
            for i in range(len(control_number)):
                checksum += int(control_number[i])
            last_digit = 10 - checksum % 10
            if last_digit==10:
                last_digit = 0
            card_number += str(last_digit)
            for _ in range(1,4):
                pin += str(random.randint(0,9))
            dict[card_number] = pin
            print(f"\nYour card has been created\nYour card number:\n{card_number}\nYour card PIN:\n{pin}")
            cur.execute('INSERT INTO card (number, pin) VALUES (' + card_number + ', ' + pin + ');')
            conn.commit()
        elif x==2:
            card = input("Enter your card number:")
            pin = input("Enter your PIN:")
            cur.execute('SELECT pin FROM card WHERE number == ' + card + ';')
            result = str(cur.fetchone())
            if result is None or result is False or pin not in result:
                print("Wrong card number or PIN!")
            else:
                print("You have successfully logged in!")
                x = menu2(card, cur, conn)
        if x==3:
            print("\nBye!\n")

menu()