import pytest

def test_equal_or_not():
    assert 3==3
    assert 3!=2
    assert 4==4

def test_isinstance():
    assert isinstance('this is string',str)
    assert not isinstance('10',int)

def test_boolean():
    validated=True
    assert validated is True
    assert validated is not False
    assert ('hello'=='world') is False

def test_type():
    assert type('str' is str)
    assert type(10 is not str)

def test_gt_lt():
    assert 2 >1
    assert 11 < 15

def test_list():
    l1=[1,12,3,4,5]
    tem=[False,False]

    assert 1 in l1
    assert tem is not True
    assert all(l1)
    assert not any(tem)


class organization:
    def __init__(self,First_name,Last_name,Org_name,Experince):
        self.First_name = First_name
        self.Last_name = Last_name
        self.Org_name = Org_name
        self.Experince = Experince

@pytest.fixture
def defualt_employee():
    return organization('Shrikrishna','Jagtap','IBM',3.5)

def test_person_intialization(defualt_employee):
    
    assert defualt_employee.First_name == 'Shrikrishna','First name should be shrikrishna'
    assert defualt_employee.Last_name == 'Jagtap','Last name should be jagtap'
    assert defualt_employee.Org_name == 'IBM','Organization name should be IBM'
    assert defualt_employee.Experince == 3.5,'Experince should 3 to 5'


