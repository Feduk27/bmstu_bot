URL = 'https://lks.bmstu.ru/schedule/list'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
    'accept': '*/*'}

# It is possible to check if the week is even/odd only after going to some group's schedule.
# So lets just use 1st group's URL.
URL_for_evenodd = 'https://lks.bmstu.ru/schedule/f987f700-8a79-11ec-b81a-0de102063aa5'