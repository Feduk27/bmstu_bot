import requests
from memory_profiler import profile
from bs4 import BeautifulSoup
from parse_cfg import URL, HEADERS


# getting html code
def get_html(URL, HEADERS):
    r = requests.get(URL, headers=HEADERS).text
    return r



# parsing schedule and info about current week from university website
def get_schedule(URL, HEADERS):
    schedule = []
    html = get_html(URL, HEADERS)
    soup = BeautifulSoup(html, 'lxml')
    week = soup.find_all('table', class_="table table-bordered text-center")
    for day in week:
        day_soup = BeautifulSoup(str(day), 'lxml')
        #   getting name of the day of the week
        day_name = day_soup.find('strong').get_text()
        daily_schedule = [day_name]

        #   parsing schedule
        table_all = day_soup.find_all('tr')
        for i in range(2, len(table_all)):
            lessons_soup = BeautifulSoup(str(table_all[i]), 'lxml')
            lessons = lessons_soup.find_all('td')
            #   if there are a lessons that are held only on even/odd weeks, html code changes, so, we should check this out
            if len(lessons) == 2:
                lesson = BeautifulSoup(str(lessons[1]), 'lxml').find('td', colspan="2").get_text()
                #   if there are no lessons, returning array just with a day name
                if lesson == 'Самостоятельная работа каф.   ':
                    daily_schedule = [day_name]
                    break
                #   appending 2 similar lessons for more comfortable enumeration of array
                daily_schedule += [lesson] * 2
            else:
                daily_schedule.append(BeautifulSoup(str(lessons[1]), 'lxml').find('td', class_="text-info-bold").get_text())
                daily_schedule.append(BeautifulSoup(str(lessons[2]), 'lxml').find('td', class_="text-primary").get_text())
        schedule.append(daily_schedule)
    return schedule

#   getting department url
def get_depart_url(URL, HEADERS, depart_name):
    html = get_html(URL, HEADERS)
    faculties_soup = BeautifulSoup(html, 'lxml')
    faculties = faculties_soup.find_all('a')
    depart_url = None
    for faculty in faculties:
        faculty_soup = BeautifulSoup(str(faculty), 'lxml')
        try:
            if depart_name == faculty_soup.get_text().strip():
                link = faculty_soup.a['href']
                depart_url = 'https://lks.bmstu.ru' + link
        except:
            pass
    if depart_url:
        return depart_url
    else:
        return 'Error occurred. Check the spelling of department name or text the developer @turrrrrrboUl'

dep_name = 'ЛТ10-11Б'
depart_url = get_depart_url(URL, HEADERS, dep_name)
schedule = get_schedule(depart_url, HEADERS)
print(schedule)