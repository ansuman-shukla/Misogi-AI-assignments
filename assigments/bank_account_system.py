class ValidationError(Exception):
    pass


class Account:
    _total_accounts = 0
    _bank_name = "Default Bank"
    _minimum_balance = 0
    
    def __init__(self, account_id, account_holder, initial_balance=0):
        self._validate_account_creation(account_id, account_holder, initial_balance)
        self._account_id = account_id
        self._account_holder = account_holder
        self._balance = initial_balance
        Account._total_accounts += 1
    
    def _validate_account_creation(self, account_id, account_holder, initial_balance):
        if not account_id:
            raise ValidationError("Account ID cannot be empty")
        if not account_holder:
            raise ValidationError("Account holder name cannot be empty")
        if initial_balance < self._minimum_balance:
            raise ValidationError(f"Initial balance must be at least {self._minimum_balance}")
    
    @property
    def account_id(self):
        return self._account_id
    
    @property
    def account_holder(self):
        return self._account_holder
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def bank_name(self):
        return Account._bank_name
    
    def get_balance(self):
        return self._balance
    
    def deposit(self, amount):
        if amount <= 0:
            return False
        self._balance += amount
        return True
    
    def withdraw(self, amount):
        if amount <= 0:
            return False
        if self._balance >= amount:
            self._balance -= amount
            return True
        return False
    
    @classmethod
    def get_total_accounts(cls):
        return cls._total_accounts
    
    @classmethod
    def set_bank_name(cls, name):
        cls._bank_name = name
    
    @classmethod
    def set_minimum_balance(cls, amount):
        cls._minimum_balance = amount
    
    def __str__(self):
        return f"Account({self._account_id}, {self._account_holder}, Balance: {self._balance})"
    
    def __repr__(self):
        return f"{self.__class__.__name__}('{self._account_id}', '{self._account_holder}', {self._balance})"


class SavingsAccount(Account):
    def __init__(self, account_id, account_holder, initial_balance=0, interest_rate=2.5):
        super().__init__(account_id, account_holder, initial_balance)
        self._interest_rate = interest_rate
    
    @property
    def interest_rate(self):
        return self._interest_rate
    
    def set_interest_rate(self, rate):
        if rate >= 0:
            self._interest_rate = rate
    
    def calculate_monthly_interest(self):
        monthly_rate = self._interest_rate / 100 / 12
        return self._balance * monthly_rate
    
    def apply_monthly_interest(self):
        interest = self.calculate_monthly_interest()
        self._balance += interest
        return interest


class CheckingAccount(Account):
    def __init__(self, account_id, account_holder, initial_balance=0, overdraft_limit=200):
        super().__init__(account_id, account_holder, initial_balance)
        self._overdraft_limit = overdraft_limit
    
    @property
    def overdraft_limit(self):
        return self._overdraft_limit
    
    def set_overdraft_limit(self, limit):
        if limit >= 0:
            self._overdraft_limit = limit
    
    def withdraw(self, amount):
        if amount <= 0:
            return False
        available_balance = self._balance + self._overdraft_limit
        if available_balance >= amount:
            self._balance -= amount
            return True
        return False
    
    def get_available_balance(self):
        return self._balance + self._overdraft_limit


if __name__ == "__main__":
    savings_account = SavingsAccount("SA001", "Alice Johnson", 1000, 2.5)
    checking_account = CheckingAccount("CA001", "Bob Smith", 500, 200)
    
    print(f"Savings Account: {savings_account}")
    print(f"Checking Account: {checking_account}")
    
    print(f"Savings balance before: {savings_account.get_balance()}")
    savings_account.deposit(500)
    print(f"After depositing $500: {savings_account.get_balance()}")
    
    withdrawal_result = savings_account.withdraw(200)
    print(f"Withdrawal result: {withdrawal_result}")
    print(f"Balance after withdrawal: {savings_account.get_balance()}")
    
    print(f"Checking balance: {checking_account.get_balance()}")
    overdraft_result = checking_account.withdraw(600)
    print(f"Overdraft withdrawal: {overdraft_result}")
    print(f"Balance after overdraft: {checking_account.get_balance()}")
    
    interest_earned = savings_account.calculate_monthly_interest()
    print(f"Monthly interest earned: {interest_earned}")
    
    print(f"Total accounts created: {Account.get_total_accounts()}")
    print(f"Bank name: {Account.bank_name}")
    
    Account.set_bank_name("New National Bank")
    Account.set_minimum_balance(100)
    
    try:
        invalid_account = SavingsAccount("SA002", "", -100, 1.5)
    except ValidationError as e:
        print(f"Validation error: {e}")
