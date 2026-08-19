import pytest
from project import get_username, construct_url, get_pset_list, get_pset_name, get_pset_date, get_year_month_list, build_calendar_data
from bs4 import BeautifulSoup
import datetime


TEST_HTML_LI = '<li><a href="https://submit.cs50.io/users/test_user/cs50/problems/2022/python/watch">cs50/problems/2022/python/watch</a><span data-moment="LLLL">Wednesday, July 29, 2026 1:32 AM IST</span></li>'
TEST_SOUP = BeautifulSoup(TEST_HTML_LI, 'lxml')
TEST_PSET_LIST = [{'pset_name': 'scrabble', 'pset_date': datetime.date(2024, 4, 16)}, {'pset_name': 'jar', 'pset_date': datetime.date(2026, 8, 11)}, {'pset_name': 'shirtificate', 'pset_date': datetime.date(2026, 8, 12)}]


def test_valid_args():
    assert get_username(["python.py", "ian"]) == "ian"

def test_missing_args():
    with pytest.raises(SystemExit):
        get_username(["python.py"])

def test_too_many_args():
    with pytest.raises(SystemExit):
        get_username(["python.py", "ian", "ianovich"])

def test_construct_url():
    assert construct_url("ian") == "https://submit.cs50.io/users/ian"

def test_get_pset_list():
    with open("html_test.html") as file:
        soup = BeautifulSoup(file, "lxml")
        assert get_pset_list(soup) == [{'pset_name': 'caesar', 'pset_date': datetime.date(2024, 4, 25)}, {'pset_name': 'grocery', 'pset_date': datetime.date(2026, 7, 9)}, {'pset_name': 'outdated', 'pset_date': datetime.date(2026, 7, 10)}]
        assert type(get_pset_list(soup)[0].get("pset_date")) == datetime.date

def test_get_pset_name():
    assert get_pset_name(TEST_SOUP) == "watch"

def test_get_pset_date():
    assert get_pset_date(TEST_SOUP) == datetime.date(2026, 7, 29)

def test_get_year_month_list():
    assert get_year_month_list(TEST_PSET_LIST) == [(2024, 4), (2026, 8)]