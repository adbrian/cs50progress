import calendar
import re
import sys
from datetime import date, datetime

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from rich.console import Console
from rich.table import Table


def main():
    username = get_username(sys.argv)
    soup = get_page(construct_url(username))
    pset_list = get_pset_list(soup)
    year_month_list = get_year_month_list(pset_list)
    calendar_data = build_calendar_data(year_month_list, pset_list)
    console = Console()
    table_data_str = build_table_data_str(calendar_data)

    pset_calendar_table = build_calendar(table_data_str)
    console.print(pset_calendar_table)


def get_username(args):
    if len(args) == 2:
        return args[1]
    sys.exit("Incorrect number of arguments")


def construct_url(user):
    page_url = f"https://submit.cs50.io/users/{user}"
    return page_url

def get_page(page_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(page_url)
        if "github.com" in page.url:
            print("Login in browser")
            page.wait_for_url("**/submit.cs50.io/**", timeout=120000)
        html = page.content()
        context.close()
        browser.close()
        return BeautifulSoup(html, "lxml")


def get_pset_list(soup):
    ps_list = []
    for item in soup.find_all("li"):
        ps_dict = {"pset_name": get_pset_name(item), "pset_date": get_pset_date(item)}
        ps_list.append(ps_dict)
    ps_list.reverse()
    return ps_list


def get_pset_name(item):
    a_tag = item.a.text.strip()
    ps_name = re.sub(r".*/", "", a_tag)
    return ps_name


def get_pset_date(item):
    ps_date = item.find(attrs={"data-moment": "LLLL"}).text.strip()
    d = ps_date.replace(',', '').split(' ')
    ps_str_dt = f"{d[3]}-{d[1]}-{d[2]}"
    ps_dt_dt = datetime.strptime(ps_str_dt, "%Y-%B-%d").date()
    return ps_dt_dt


def get_year_month_list(ps_list):
    year_month_list = []
    for ps in ps_list:
        ps_year_month = (ps["pset_date"].year, ps["pset_date"].month)
        if ps_year_month not in year_month_list:
            year_month_list.append(ps_year_month)
    return year_month_list


def build_calendar_data(month_list, ps_list):
    cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
    color = "spring_green2"
    cal_rows = []
    for year_month in month_list:
        year, month = year_month
        for week_days in cal.monthdayscalendar(year, month):
            for i, day in enumerate(week_days):
                for j, pset in enumerate(ps_list):
                    if day != 0 and pset.get("pset_date") == date(year, month, day):
                        week_days[i] = f"[{color}]{week_days[i]}[/{color}]"
                        del ps_list[j]
            if 1 in week_days:
                week_days.insert(0, calendar.month_abbr[month].upper())
                week_days.append(year)
            else:
                week_days.insert(0, " ")
                week_days.append(" ")
            cal_rows.append(week_days)
    return cal_rows


def build_table_data_str(cal_data):
    str_rows = []
    for row in cal_data:
        single_row = []
        for item in row:
            single_row.append(str(item))
        str_rows.append(single_row)
    return str_rows


def build_calendar(str_rows):
    table = Table("MNTH", "SU", "MO", "TU", "WE", "TH", "FR", "SA", "YEAR")
    for row in str_rows:
        table.add_row(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]
        )
    return table


if __name__ == "__main__":
    main()
