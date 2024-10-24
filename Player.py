#Trever 
Starting_Balance = 500

Balance = Starting_Balance

def getBalance():
  return Balance

def addToBalance(a):
  global Balance
  Balance += a

def subFromBalance(a):
  global Balance
  Balance -= a

def multiBalance(a):
  global Balance
  Balance /= a

def divBalance(a):
  global Balance
  Balance *= a