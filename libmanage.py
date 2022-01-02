#library management system using Python and MYSQL
#by Khushi Aggarwal 
import mysql.connector
#mysql library using xampp apache web server

# admin's password
password = '00000'

# defining functions
def insert_book():
    global cursor
    bookname = input("Enter bookname to Insert book: ")
    author = input("Enter Book's Author: ")
    genre = input("Enter Genre: ")
    quantity = int(input("Enter quantity: "))
    query = "INSERT into books(bookname,author,genre,quantity)" \
        "VALUES(%s,%s,%s,%s)"
        
    val = (bookname,author,genre,quantity)
    try:
        cursor.execute(query,val)
        con.commit()
        print(f"Book {bookname} has been added")
    except:
        con.rollback()
        print("Something went Wrong please try again later...")

def delete_book():
    global cursor
    bookname = input("Enter bookname to Delete book: ")
    query = "DELETE FROM books WHERE bookname=%s"
    val = (bookname)
    try:
        cursor.execute(query,val)
        con.commit()
        print(f"Book {bookname} has been deleted")
    except:
        con.rollback()
        print("Something went Wrong please try again later...")

def update_quantity():
    global cursor
    bookname = input("Enter bookname to Edit Quantity: ")
    new_quantity = int(input("Enter New Quantity: "))
    query = """ UPDATE books  
    SET quantity=(%s)
    WHERE bookname=(%s)"""
    val = (new_quantity,bookname)
    try:
        cursor.execute(query,val)
        con.commit()
        print(f"Quantity of Book {bookname} has been changed to {new_quantity}")
    except:
        con.rollback()
        print("Something went Wrong please try again later...")

def change_genre():
    global cursor
    bookname = input("Enter bookname to Edit Genre: ")
    new_genre = input("Enter New genre: ")
    query = """ UPDATE books  
    SET genre=(%s)
    WHERE bookname=(%s)"""
    val = (new_genre,bookname)
    try:
        cursor.execute(query,val)
        con.commit()
        print(f"Genre of Book {bookname} has been changed to {new_genre}")
    except:
        con.rollback()
        print("Something went Wrong please try again later...")

def search_book():
    available_book()
    bookname = input("Enter bookname to search: ")
    query = "SELECT * from books WHERE bookname=%s"
    val = (bookname,)
    try:
        cursor.execute(query,val)
        books_record = cursor.fetchone()
        print("BOOKNAME | AUTHOR | GENRE | QUANTITY")  
        for book_details in books_record:
            print(" |", book_details, end = "")
    except:
        con.rollback()
        print("Book Not Found!")

def available_book():
    global cursor
    print("ALL AVAILABLE BOOKS")
    print("BOOKNAME | AUTHOR | GENRE  | QUANTITY ")
    cursor.execute("Select * from books;")
    books_record = cursor.fetchall()
    for book_details in books_record:
        print(book_details)

def issue_book():
    global cursor
    reg_no = input("Enter your Registration Number: ")
    name = input("Enter your Name: ")
    bookname = input("Enter bookname to issue: ")
    issuedate = input("Enter issue date: ")
    query = "INSERT into issue(`Registration No.`, `Student Name`, `Book Name`, `Issue Date`)" \
        "VALUES(%s,%s,%s,%s)"
    val = (reg_no, name, bookname, issuedate)
    try:
        cursor.execute(query,val)
        con.commit()
        print(f"Book {bookname} has been Issued to {name}")
        book_up(bookname,-1)
    except:
        con.rollback()
        print("Something went Wrong please try again later...")
    
def return_book():
    global cursor
    reg_no = input("Enter your Registration Number: ")
    name = input("Enter your Name: ")
    bookname = input("Enter bookname to return: ")
    returndate = input("Enter return date: ")
    query = "INSERT into return(`Registration No.`, `Student Name`, `Book Name`, `Return Date`)" \
        "VALUES(%s,%s,%s,%s)"
    val = (reg_no, name, bookname, returndate)
    try:
        cursor.execute(query,val)
        con.commit()
        print(f"Book {bookname} has been Returned by {name}")
        book_up(bookname,1)
    except:
        con.rollback()
        print("Something went Wrong please try again later...")

def book_up(bookname, upquantity):
    global cursor
    query = "Select quantity from books Where bookname=%s"
    val = (bookname,)
    try:
        cursor.execute(query,val)
        quan = cursor.fetchone()
        total = quan[0] +upquantity
        query2 = "UPDATE books SET quantity = %s WHERE bookname = %s"
        val2 = (total, bookname)
        cursor.execute(query2, val2)
        con.commit()
    except:
        con.rollback()
        print("Something went Wrong please try again later...")

#connect to database
con = mysql.connector.connect(
    user = 'root',
    passwd='',
    host='localhost',
    database='library')
if con.is_connected:
    cursor = con.cursor()

#Menu 
print('*****Welcome to Library Management system*****')
user = input('Confirm User type \n 1.Client\n 2.Admin\n')
if user == '1':
    print('Enter your choice to perform User operations \n 1.Search\n 2.Issue Book\n 3.Return Book\n')
    options = 'Y'
    while options == 'Y':
        choice = input('Enter Choice: ')
        if choice == '1':
            search_book()
        elif choice == '2':
            issue_book()
        elif choice == '3':
            return_book()
        else:
            print("Wrong choice..")
        options = input("\nDo you wish to continue... (Y/N)").upper()
    
    print("Thank You for using My Library Management system")

if user == '2':
    pass_check = input("Enter Admin Password To Procced: ")
    if pass_check == password:
        print('Enter your choice to perform Admin operation \n 1.Add New Book\n 2.Delete book\n 3.Update quantity\n 4.Change Genre\n 5.Search Book ')
        options = 'Y'
        while options == 'Y':
            option = input("Enter Option: ")
            if option == '1':
                insert_book()
            elif option == '2':
                delete_book()
            elif option == '3':
                update_quantity()
            elif option == '4':
                change_genre()
            elif option == '5':
                search_book()
            else:
                print("Wrong input!!")
            options = input("\nDo you wish to continue? (Y/N)").upper()

        print("signing out of admin....")
            
    else:
        print("Wrong Password! \n [+] session expired: try later")

con.close()