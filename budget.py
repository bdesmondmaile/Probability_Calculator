class Category:
    def __init__(self, categories ):
        """ Initialize the instance variables of a Category object. """
        self.ledger = []
        self.category = categories
        self.__balance = 0.0

    def __str__(self):
        """ Returns the string representation for this object """
        ln = (30 - len(self.category)) // 2
        remainder = (30 - len(self.category)) % 2

        obj = "*" * ln + self.category + "*" * ln + "*" * remainder + "\n" # A title of contents of the category. string len = 30. category title is centered in a line of `*` characters.
        if len(self.ledger) == 0:
            return obj
        elif len(self.ledger) == 1:
            obj += self.ledger[-1]["description"][:23].ljust(23) + "{:.2f}".format(self.ledger[-1]["amount"]).rjust(7) +"\n"
            obj += "Total:" + " " + str(self.__balance)
            return obj
        else:
            for i in range(len(self.ledger)):
                obj += self.ledger[i]["description"][:23].ljust(23) + "{:.2f}".format(self.ledger[i]["amount"]).rjust(7) + "\n"
            obj += "Total:" + " " + str(self.__balance)

        return obj

    def deposit(self, amount, description=None):
        """ Add funds to the account. There is no limit
            to the size of the deposit. """
        if description == None:
            description = ""
        self.__balance += float(amount)
        self.ledger.append({'amount': amount, 'description': description})

    def check_funds(self, amount):
        """ Checks for funds before transfer or withdrawal. return false if amount less
        than budget category balance. Return true otherwise. """
        result = False
        if self.__balance - amount >= 0:
            result = True
        return result

    def withdraw(self, amount, description=None):
        """ Deduct funds from the account, if possible. Only completes the withdrawal successfully if
            there are enough funds in the account to fulfill the withdrawal. Return true if successful, false otherwise """
        result = False # withdrwal unsuccesful by default
        if description == None:
            description = ""
        if self.check_funds(amount):
            self.__balance -= amount
            self.ledger.append({'amount': -amount, 'description': description})
            result = True # Withdrawal successful

        return result

    def get_balance(self):
        ''' Returns the current balance of the budget category '''
        return self.__balance

    def transfer(self, amount, category):
        ''' Transfer funds from one budget category to another. '''
        result = False
        if self.check_funds(amount):
            result = True
            msg = "Transfer to" + " " + category.category
            self.withdraw(amount, msg)
            category.deposit(amount, "Transfer from" + " " + self.category)

        return result

def create_spend_chart(categories):
    ''' Displays a bar chart of in percentage spent
        in each category passed in to the function '''
        
    result = "Percentage spent by category\n"
    withdrawal_per_category = [] # stores total withdrawal per category. totals are as per categories.
    percentage_spent = [] # stores percentage of each withdrawal per category over the overall withdrawals. Percentage are stored as per categories.

    for obj in categories:
        sum_withdrawal_per_category = 0
        for dic in obj.ledger:
            if dic["amount"] < 0:
                sum_withdrawal_per_category += dic["amount"]
            else:
                pass
        withdrawal_per_category.append(sum_withdrawal_per_category)
    # calculte withdrawal for eachcategory in percentage.
    for i in withdrawal_per_category:
        percent = i / sum(withdrawal_per_category) * 100
        if percent >= 10:
            percentage_spent.append(int(round(percent, -1)))
        else:
            percentage_spent.append(0)

    i = 100
    while i >= 0:
        var_string = ""
        for item in percentage_spent:
            if item >= i:
                var_string += " o "
            else:
                var_string += "   "
        if i == 0:
            var_string += " "
            result += (str(i)+ "|").rjust(4) + var_string
        else:
            var_string += " "
            result += (str(i)+ "|").rjust(4) + var_string + "\n"
        i -= 10
    #calcutes how many dashes there should be.
    ln = len(percentage_spent)
    dashes = "\n" + "".rjust(4)+ "-" + "-" * ln + "--" * (ln)
    result += dashes + '\n'


    i = 0 # by default the length of the longest category name is zero
    #determine the longest category name.
    for entry in categories:
        if len(entry.category) > 0:
            if i < len(entry.category):
                i = len(entry.category)
    #formats category name in the required format.
    for t in range(i):
        cat_names ="    "
        if t < i-1:
            for j in range(len(categories)):
                if len(categories[j].category) > t:
                    cat_names += ' '+ categories[j].category[t] + ' '
                else:
                    cat_names += " " + " " + " "
            result += cat_names + " " + "\n"
            cat_names += '\n' + "".rjust(4)

        if t == i-1:
            for j in range(len(categories)):
                if len(categories[j].category) > t:
                    cat_names += ' '+ categories[j].category[t] + ' '
                else:
                    cat_names += " " + " " + " "
            result += cat_names + " "

    return result
