import requests
from memory_profiler import profile
from bs4 import BeautifulSoup
from parse_cfg import URL, HEADERS, URL_for_evenodd


# getting html code
def get_html(URL, HEADERS):
    r = requests.get(URL, headers=HEADERS).text
    return r

# returns faculty name from cathedra name. Ex: СМ13 -> СМ
def get_front_marker(string):
    result = ''
    for letter in string:
        try:
            int(letter)
            return result
        except:
            result += letter
    return result

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
        empty_flag = True
        #   parsing schedule
        table_all = day_soup.find_all('tr')
        for i in range(2, len(table_all)):
            lessons_soup = BeautifulSoup(str(table_all[i]), 'lxml')
            lessons = lessons_soup.find_all('td')
            #   if there are a lessons that are held only on even/odd weeks, html code changes, so, we should check this out
            if len(lessons) == 2:
                lesson = BeautifulSoup(str(lessons[1]), 'lxml').find('td', colspan="2").get_text().strip()
                #   if there are no lessons, returning array just with a day name
                if lesson == 'Самостоятельная работа каф.':
                    daily_schedule = [day_name]
                    break
                empty_flag = False
                #   appending 2 similar lessons for more comfortable enumeration of array
                daily_schedule += [lesson] * 2
            else:
                lesson_even = BeautifulSoup(str(lessons[1]), 'lxml').find('td', class_="text-info-bold").get_text()
                lesson_odd = BeautifulSoup(str(lessons[2]), 'lxml').find('td', class_="text-primary").get_text()
                if lesson_even != ' ' or lesson_odd != ' ':
                    empty_flag = False
                daily_schedule.append(lesson_even)
                daily_schedule.append(lesson_odd)
        if empty_flag:
            daily_schedule = [day_name]
        schedule.append(daily_schedule)
    return schedule

#   getting department url
def get_group_url(URL, HEADERS, depart_name):
    html = get_html(URL, HEADERS)
    faculties_soup = BeautifulSoup(html, 'lxml')
    faculties = faculties_soup.find_all('a')
    group_url = None
    for faculty in faculties:
        faculty_soup = BeautifulSoup(str(faculty), 'lxml')
        if depart_name == faculty_soup.get_text().strip():
            link = faculty_soup.a['href']
            group_url = 'https://lks.bmstu.ru' + link

    if group_url:
        return group_url
    else:
        return 'Error occurred. Check the spelling of department name or text the developer @turrrrrrboUl'

def get_depart_names(URL, HEADERS, fac_name):
    html = get_html(URL, HEADERS)
    faculties_soup = BeautifulSoup(html, 'lxml')
    departs = faculties_soup.find_all('h4', class_='')
    result_departs = []
    for depart in departs:
        depart_txt = depart.get_text()
        front_marker = get_front_marker(depart_txt)
        if front_marker == fac_name:
            result_departs.append(depart.get_text())
    if result_departs == []:
        print('Error occurred in get_depart_names(). Please check faculty name spelling.')
        return None
    else:
        return result_departs

def groups_name_array(URL, HEADERS, dep_name):
    html = get_html(URL, HEADERS)
    faculties_soup = BeautifulSoup(html, 'lxml')
    faculties = faculties_soup.find_all('a', class_="btn btn-primary col-1 rounded schedule-indent")
    for i in range(len(faculties)):
        faculties[i] = faculties[i].get_text().strip()
    groups = []
    for j in range(len(faculties)):
        if faculties[j][:faculties[j].index('-')] == dep_name:
            groups.append(faculties[j])
    if groups != []:
        return groups
    else:
        print('Error occurred in groups_name_array(). Department not found or '
              'there are no active groups in the department')
        return False

def even_odd_check(URL_for_evenodd, HEADERS):
    html = get_html(URL_for_evenodd, HEADERS)
    soup = BeautifulSoup(html, 'lxml')
    week_num = soup.find('i').get_text()
    if week_num[week_num.index(',') + 1:].strip() == 'числитель':
        return 0
        print(0)
    else:
        return 1
        print(1)



# dep_name = 'ЮР-53'
# depart_url = get_group_url(URL, HEADERS, dep_name)
# schedule = get_schedule(depart_url, HEADERS)
# print(schedule)
print(groups_name_array(URL, HEADERS, 'АК3'))
# print(get_depart_names(URL, HEADERS, 'ИУ'))
# print(even_odd_check(URL_for_evenodd, HEADERS))