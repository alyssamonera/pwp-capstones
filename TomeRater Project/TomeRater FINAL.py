class User(object):
    def __init__(self, name, email):
        self.name = name.title()
        self.email = email
        self.money_spent = 0
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        return "Your email has been updated."

    def get_money_spent(self):
        return self.money_spent

    def __repr__(self):
        return "User: {name}, Email: {email}, Books read: {books}".format(name = self.name, email = self.email, books = len(self.books.keys()))
        
    def __eq__(self, other_user):
        if (self.name == other_user.name) and (self.email == other_user.email):
            return True
        else:
            return False
       
    def read_book(self, book, rating=None):
        if rating != None:
            if rating < 0 or rating > 4:
                return "Invalid Rating"
            else:
                self.books[book] = rating
                self.money_spent += book.price
        else:
            self.books[book] = rating
            self.money_spent += book.price

        
#I decided to tweak this so that it doesn't include books that don't have a rating, since leaving the rating as "None" is an option.
    def get_average_rating(self):
        sum_of_ratings = 0
        total_number_of_rated_books = 0
        for value in self.books.values():
            if type(value) == int:
                sum_of_ratings += value
                total_number_of_rated_books += 1
        avg_of_ratings = sum_of_ratings / total_number_of_rated_books
        return avg_of_ratings
        
class Book(object):
    def __init__(self, title, isbn, price):
        self.title = title.title()
        self.isbn = isbn
        self.price = price
        self.ratings = []
        
    def get_title(self):
        return self.title
    
    def get_isbn(self):
        return self.isbn
    
    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        return "ISBN has been updated."
    
    def add_rating(self, rating):
        if (rating >= 0) and (rating <= 4):
            self.ratings.append(rating)
            return "Rating added."
        else:
            return "Invalid Rating"
        
    def __eq__(self, other_book):
        if (self.title == other_book.title) and (self.isbn == other_book.isbn):
            return True
        else:
            return False

#I decided to write an error message in case someone tried to access the average ratings of an unrated book.        
    def get_average_rating(self):
        if len(self.ratings) > 0:
            sum_of_rates = 0
            for rate in self.ratings:
                sum_of_rates += rate
            avg_of_rates = sum_of_rates / len(self.ratings)
            return avg_of_rates
        else:
            return "This book has not been rated, yet."
    
    def __hash__(self):
        return hash((self.title,	self.isbn))

#Since Fiction and Non-Fiction have repr dunder methods, I decided to give one to Book as well, in case a book falls under neither Fiction nor Non-Fiction.
    def __repr__(self):
        return "{title}".format(title=self.title)
        
class Fiction(Book):
    def __init__(self, title, author, isbn, price):
        super().__init__(title, isbn, price)
        self.author = author.title()
        
    def get_author(self):
        return self.author
    
    def __repr__(self):
        return "{title} by {author}".format(title = self.title, author = self.author)
    
class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level
        
    def get_subject(self):
        return self.subject
    
    def get_level(self):
        return self.level
    
    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title = self.title, level = self.level, subject = self.subject)
    
class TomeRater:
#Self.users = user emails:User objects; Self.books = Book objects:# users who have read it
    def __init__(self):
        self.users = {}
        self.books = {}
        
    def create_book(self, title, isbn, price):
        new_book = Book(title, isbn, price)
        self.books[new_book] = 0
        return new_book
    
    def create_novel(self, title, author, isbn, price):
        new_novel = Fiction(title, author, isbn, price)
        self.books[new_novel] = 0
        return new_novel
    
    def create_non_fiction(self, title, subject, level, isbn, price):
        new_nonfic = Non_Fiction(title, subject, level, isbn, price)
        self.books[new_nonfic] = 0
        return new_nonfic
    
    def add_book_to_user(self, book, email, rating=None):
        if email in self.users.keys():
            current_user = self.users[email]
            current_user.read_book(book, rating)
            if rating != None:
                if 0 <= rating <= 4:
                    book.add_rating(rating)
                else:
                    return "Invalid Rating"
            if book in self.books:
                self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            return "No user with email {email}!".format(email=email)
        
    def add_user(self, name, email, books=None):
        new_user = User(name, email)
        self.users[email] = new_user
        if books != None:
            for book in books:
                self.add_book_to_user(book, email)
        return new_user

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def most_read_book(self):
        most_read_value = 0
        most_read_book = "none"
        for book in self.books.keys():
            if self.books[book] > most_read_value:
                most_read_value = self.books[book]
                most_read_book = book
        return most_read_book

    def highest_rated_book(self):
        highest_avg = 0
        best_book = "none"
        for book in self.books.keys():
            if len(book.ratings) > 0:
                if book.get_average_rating() > highest_avg:
                    highest_avg = book.get_average_rating()
                    best_book = book
            else:
                continue
        return best_book

    def most_positive_user(self):
        highest_avg = 0
        most_positive = "none"
        for user in self.users.values():
            if user.get_average_rating() > highest_avg:
                highest_avg = user.get_average_rating()
                most_positive = user
        return most_positive

    def get_n_most_expensive_books(self, n):
        highest_price = 0
        list_of_prices = []
        list_of_books = []
        priciest_books = []
        for book in self.books.keys():
            list_of_prices.append(book.price)
            list_of_books.append(book)
        prices_and_books = {key:value for key, value in zip(list_of_prices, list_of_books)}
        sorted_prices = sorted(list_of_prices)
        priciest_prices = sorted_prices[-n:]
        for price in priciest_prices:
            priciest_books.append(prices_and_books[price])
        return priciest_books

    def get_worth_of_user(self, user_email):
        worth = self.users[user_email].money_spent
        return worth
