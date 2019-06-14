from django.test import TestCase

# Create your tests here.


with open('/home/kiosk/Downloads/冯提莫-知否知否.mp3','rb') as f1,open('/home/kiosk/Downloads/1.mp3','wb') as f2:
    f2.write(f1.read())
