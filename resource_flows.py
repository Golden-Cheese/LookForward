class Income:

    def __init__(self, a_label, a_type, an_amount, a_currency, a_date):
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
    def __init__(self, a_label, a_type, a_category, an_amount, a_currency, a_date):
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
    def __init__(self, a_type):
        self.type = a_type
        self.inflows = []
        self.outflows = []
        self.total_income = 0
        self.total_expense = 0
        self.available_value = 0

    def add_income(self, new_income: Income):
        self.inflows.append(new_income)
        self.total_income += new_income.value
        self.available_value = self.total_income - self.total_expense

    def add_expense(self, new_expense: Expense):
        self.outflows.append(new_expense)
        self.total_expense += new_expense.value
        self.available_value = self.total_income - self.total_expense

    def to_dict(self):
        resource_dict = dict(Incomes=[], Expenses=[], inflow_value=self.total_income, outflow_value=self.total_expense, available=self.available_value)
        for i in self.inflows:
            resource_dict["Incomes"].append(i.to_dict())
        for e in self.outflows:
            resource_dict["Expenses"].append(e.to_dict())

        return resource_dict
