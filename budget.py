class Category:

  def __init__(self, name):
    self.name = name
    self.ledger = []
    self.balance = bool(0)
    self.withdrawals = []
    self.deposits = []

  def get_balance(self):
    return self.balance

  def check_funds(self, amount):
    return self.balance >= amount

  def deposit(self, amount, description=''):
    self.balance += amount
    self.ledger.append({"amount": amount, "description": description})
    self.deposits.append(amount)

  def withdraw(self, amount, description=''):
    if self.check_funds(amount) is True:
      self.balance -= amount
      self.withdrawals.append(amount)
      self.ledger.append({"amount": -amount, "description": description})
      return True
    else:
      return False

  def transfer(self, amount, category):
    if self.check_funds(amount) is True:
      self.withdraw(amount, f"Transfer to {category.name}")
      category.deposit(amount, f"Transfer from {self.name}")
      return True
    else:
      return False

  def __str__(self):
    stars = int((30 - len(self.name)) / 2)
    output_text = f"{'*' * stars}{self.name}{'*' * stars}\n"

    for item in self.ledger:
      item_description = item['description'][:23]
      length_of_number = len(str(item['amount'])) if int(
          item['amount']) != item['amount'] else len(str(item['amount'])) + 3
      spaces = 30 - len(item_description) - length_of_number
      text = f"{item['description'][:23]:23}{item['amount']:>7.2f}\n"
      output_text += text

    total = f"Total: {self.get_balance():.2f}"
    output_text += total
    return output_text


def percent_entry(output, percent_list, percent, entry):
  output += str(percent) + '| '
  for entry in percent_list:
    output += (check_percent(100, entry)) + '  '
  output += '\n'


def check_percent(percent, entry):
  if entry >= percent:
    return 'o'
  else:
    return ' '


def create_spend_chart(categories):
  title = "Percentage spent by category\n"
  withdrawals = {
      category.name:
      sum(item["amount"] for item in category.ledger if item["amount"] < 0)
      for category in categories
  }
  total_withdrawals = sum(withdrawals.values())
  percentages = {
      name: (amount / total_withdrawals) * 100
      for name, amount in withdrawals.items()
  }

  chart = title
  for percentage in range(100, -10, -10):
    chart += f"{percentage:>3}| "
    for category in categories:
      if percentages.get(category.name, 0) >= percentage:
        chart += "o  "
      else:
        chart += "   "
    chart += "\n"

  chart += "    -" + "---" * len(categories) + "\n"

  max_length_name = max(len(category.name) for category in categories)
  for i in range(max_length_name):
    chart += "     "
    for category in categories:
      if i < len(category.name):
        chart += category.name[i] + "  "
      else:
        chart += "   "
    chart += "\n"

  return chart.rstrip("\n")
