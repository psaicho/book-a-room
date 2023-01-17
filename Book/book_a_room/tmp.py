# from django.utils.timezone import now
#
# print(now().date())



from datetime import date, datetime
today = date.today().strftime("%Y-%m-%d")
print(today)
date_s = '2023-01-06'
date = datetime.strptime(date_s, '%Y-%m-%d')
print(date)

if today > date:
    print('wwww')