# CS50progress

#### Video Demo: <https://www.youtube.com/watch?v=OAWz0lAsioA>


#### Description:
A terminal calendar displaying CS50 pset submission data.

 The calendar displays each month where we have submitted psets. Dates when pset submissions have been made will have the green font.

<img width="427" height="261" alt="image" src="https://github.com/user-attachments/assets/e74c4859-1b61-49a0-8978-6d8f2b40cb75" />


Built as my final CS50p project

## Requirements
Libraries used:
- BeautifulSoup
- Playwright
    - install playwright chromium browser
    `playwright install chromium`
- Calendar
- Rich
- Re
- Sys

**Status:** First Working Version uploaded.

## Running
In the terminal, run `project.py` with arguments mentioning your username. If your username is `ian`

```bash
python project.py ian
```

## Implementation details
The code is broken up into 
- fetching page
- parsing pset data
- rendering calendar

## Fetching page
get_username
construct_url
get_page

### get_username
Validates user input via sys.argv, and extracts username from sys.argv[1]. Does a sys.exit if no arguments were passed or too many arguments were provided.

### construct_url
Uses extracted username to construct the cs50 submit url

### get_page
This is the meat of the fetching process.

During the concept validation stage, I considered using stored cookies, by copying them manually after inspecting the page, but this quickly proved impractical. The cookies had a session cookie, as well as AWSALB and AWSALBCORS cookies, which kept changing. Eventually I went with Playwright, which enables authenticating with a browser and keeping the context while BeautifulSoup scrapes the page.

Playwright launches a chromium browser and we authenticate with github. Once logged in, playwright waits for the url pattern and once succesful, grabs the html content.

## Parsing data
get_pset_list
- get_pset_name
- get_pset_date

### get_pset_list
calls get_pset_name and get_pset_date to construct a list of dictionaries. Each dictionary has a pset name, and pset date
{
    "pset_name": "outdated",
    "pset_date": "2026-07-10"
}

### get_pset_name
We use BeautifulSoup to search for `<a>` tags, some string methods and regex substitution which gives us our pset name

### get_pset_date
We use some more BeautifulSoup, string methods, f-strings and datetime to retrieve `<span>` with a unique attribute `'data-moment': 'LLLL'` to construct our pset submission date data. We convert it to `datetime.date` which will help us to create the calendar using the calendar module.

## Render calendar
get_year_month_list
build_calendar_data
build_table_data
build_calendar

### get_year_month_list
We iterate through our pset list, and gather the month data for all the month/year in a (month, year) tuple for which we have submitted psets. We will use this with calendar methods to generate the months, into which we will add submission information.

### build_calendar_data
This is a bit of interesting calendar building logic. 

We iterate through the months which we have got in the year_month_list. For each iteration, we also iterate through the days we have in our pset list. If the iteration reaches a day in the month, which exists in the pset list as well, we update that day in the month calendar by formatting it green (to be read by Rich). 

We also delete the pset entry in the pset list so that we dont have to iterate through it again. 

This function also adds the columns for Month and Year which is missing from the calendar data structure we have selected. We then append each row to a new list.

### build_table_data
This function converts our calendar data to rows of strings, which the rich.table module can parse.

### build_calendar
Here we add the headers which display title for month, title for year and days of the week. It then iterates through the list of lists of rows, and inserts each row item into the table. This table data gets passed back to our main function to render our calendar

## main
Our main function uses console.print from rich to parse the calendar rows and we now have our calendar.
