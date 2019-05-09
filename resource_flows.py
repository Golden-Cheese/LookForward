"""
This module contains the implementation of some classes used to manage the income and expenditure of a resource
(money, time,...) """

class Income:
    """
    An object to represent an inflow of a resource. For example, if the resource is money, incomes are monthly
    salaries, annual royalties, or exceptionnal winnings
    """
    def __init__(self, a_label, a_type, an_amount, a_currency, a_date):
        """
        Constructs a new instance of the Income class
        :param a_label: A short description of the income ("salary", "contest prize"... | free time, holiday...)
        :param a_type: The type of income ("Monthly", "Yearly", "Exceptional")
        :param an_amount: the value of the income
        :param a_currency: the currency of the income
        :param a_date: the date when it was perceived
        """
        self.label = a_label
        self.type = a_type
        self.value = an_amount
        self.currency = a_currency
        self.date = a_date

    def __str__(self):
        return "Income (%s); %s\t|\t %.2f %s" % (str(self.type), self.label, self.value, self.currency)

    def to_dict(self):
        return dict(label=self.label, type=self.type, value=self.value, currency=self.currency, date=self.date)


class Expense:
    """
    An object to represent an outflow of a resource. For money, expenses are made on food, rent, ....
    """
    def __init__(self, a_label, a_type, a_category, an_amount, a_currency, a_date):
        """
        Constructs a new instance of the Expense class
        :param a_label: A short description of the expense ("Groceries at Leclerc", "rent", "Electricity bill"
        :param a_type: the type of expense ("Monthly","Exceptional")
        :param a_category: the category to which the expense belongs (food, living, hobbies, clothing,...)
        :param an_amount: the value of the expense
        :param a_currency: the currency of the expense
        :param a_date: the date on which the expense was made
        """
        self.label = a_label
        self.type = a_type
        self.category = a_category
        self.value = an_amount
        self.currency = a_currency
        self.date = a_date

    def __str__(self):
        return "Expense on %s (%s); %s\t|\t %.2f %s" % (
        self.category, str(self.type), self.label, self.value, self.currency)

    def to_dict(self):
        return dict(label=self.label, type=self.type, category=self.category, value=self.value, currency=self.currency,
                    date=self.date)


class Resource:
    """
    An object to represent a resource that can be possessed by a contributor. It can be, for example, time or money.
    For any given project a contributos may possess several resources to give (the contributor can give money ADN
    time to the project)
    """
    def __init__(self, a_type):
        """
        Constructs a nez Instance of the Resource class
        :param a_type: Time or Money
        """
        self.type = a_type
        self.inflows = []
        self.outflows = []
        self.total_income = 0
        self.total_expense = 0
        self.available_value = 0

    def add_income(self, new_income: Income):
        """
        Adds an Income object to its list of in flows of resources and updates total values
        :param new_income: an instance of Income class
        """
        self.inflows.append(new_income)
        self.total_income += new_income.value
        self.available_value = self.total_income - self.total_expense

    def add_expense(self, new_expense: Expense):
        """
        Adds an Expense object to its list of out-flows of resources and updates total values
        :param new_expense: an instance of the Expense class
        :return:
        """
        self.outflows.append(new_expense)
        self.total_expense += new_expense.value
        self.available_value = self.total_income - self.total_expense

    def to_dict(self):
        """
        Returns a dictionary with all incomes and expenses information, as well as total values
        :return: a dict()
        """
        resource_dict = dict(Incomes=[], Expenses=[], inflow_value=self.total_income, outflow_value=self.total_expense, available=self.available_value)
        for i in self.inflows:
            resource_dict["Incomes"].append(i.to_dict())
        for e in self.outflows:
            resource_dict["Expenses"].append(e.to_dict())

        return resource_dict
