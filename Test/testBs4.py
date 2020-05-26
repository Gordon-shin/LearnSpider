'''
-Tag
-NavigableString
-BeautifulSoup
-Comment
'''
from bs4 import BeautifulSoup
file = open("./baidupachong.html","rb")
html = file.read()
bs = BeautifulSoup(html,"html.parser")
print(bs.a.contents)
