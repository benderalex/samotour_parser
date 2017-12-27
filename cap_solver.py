from captcha_solver import CaptchaSolver
from captcha_solver.contrib.grab.captcha import solve_captcha
from grab import Grab
from pyquery import PyQuery as pq
from subprocess import call


url = 'http://online.joinup.ua/search_tour'
g = Grab()
response = g.go(url)
body = g.response.body

result = body.find('fcaptcha')

if result > 0:
    sss = pq(body).find('img#icaptcha')
    child = (sss.attr('src'))
    call(["eog", "&"])
    name = raw_input('Enter your name : ')
    print ("Hi %s, Let us be friends!" % name);




