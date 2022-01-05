
import basicfunction
import pytest
# @pytest.mark.filterwarnings('ignore::DeprecationWarning')

@pytest.fixture
def init_bnk_acc_0():
    return basicfunction.BankAccount()

@pytest.fixture
def init_bnk_acc_val():
    return basicfunction.BankAccount(2)

@pytest.mark.parametrize("n1 ,n2, sol", [
    (6,6,36),
    (9,9,81)
])
def test_multiply(n1, n2, sol):
    print("testing out function")
    assert basicfunction.multiply(n1,n2) == sol


def test_initial_amt(init_bnk_acc_val):
    
    assert init_bnk_acc_val.balance == 2

def test_def_amt(init_bnk_acc_0):
    assert init_bnk_acc_0.balance == 0

def test_bnk_withdraw(init_bnk_acc_val):
    init_bnk_acc_val.withdraw(2)
    assert init_bnk_acc_val.balance == 0

def test_bnk_deposit(init_bnk_acc_val):
    init_bnk_acc_val.deposit(2)
    assert init_bnk_acc_val.balance == 4

def test_bnk_collect_interest(init_bnk_acc_val):
    init_bnk_acc_val.deposit(2)
    init_bnk_acc_val.collect_interest()
    assert init_bnk_acc_val.balance == 4.4

@pytest.mark.parametrize("n1 ,n2, slide", [
    (100,10,92),
    (50,12,40),

])
def test_bank_tran(init_bnk_acc_val, n1, n2, slide): # start with 2
    init_bnk_acc_val.deposit(n1)
    init_bnk_acc_val.withdraw(n2)
    assert init_bnk_acc_val.balance == slide


def test_broke(init_bnk_acc_0):
    with pytest.raises(basicfunction.Broke):
        init_bnk_acc_0.withdraw(10)
