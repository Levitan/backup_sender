#!/usr/bin/python
# -*- coding: utf-8 -*-
# backup_sender.py
#
# Copyright 2014 Vitaly Levitan <vlevitan91@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#

import sys, os, ftplib, md5, cgi, zipfile
def main():
  # Парсим GET параметры
  args = cgi.FieldStorage()
  login = args['login'].value
  passwd = args['pass'].value
  # Проверяем пасс
  if hashSum(passwd) != 'MD5_SUMM':
    print "Pass is incorrect" # Нужна ТОЛЬКО для отладки!!!
    sys.exit()
  site_name = 'SITE_NAME'
  # Задаём имена файлов
  back_name = 'full_dump.tar.gz'
  db_file = 'dump.sql'
  # параметры подключения к базе
  db_host = 'localhost'
  db_user = 'db_user'
  db_pass = 'db_pass'
  db_name = 'db_name'
  # параметры подключения к FTP
  ftp_host = 'PUT_A_FTP_HOST_HERE'
  ftp_user = login
  ftp_pass = passwd
  # Имя сайта
  site_name = 'site.ru'
  
  dumpDB(db_user, db_pass, db_host, db_name, db_file) # Снимаем базу
  packFiles(back_name) # Пакуем всё в один архив
  sendFiles(ftp_host, ftp_user, ftp_pass, back_name)
  
  # Удаляем бекап, что бы врагу не досталось
  os.remove(back_name)
  os.remove(db_file)
  print "Finish" # Нужна ТОЛЬКО для отладки!!!
  
  
def hashSum(val):
  m = md5.new()
  m.update(val)
  return m.hexdigest()

def dumpDB(user, passwd, host, name, dbFile):
  os.system('mysqldump -u'+user+' -p'+passwd+' -h'+host+' '+name+' > '+dbFile)

def packFiles(fileArc):
  zf = zipfile.ZipFile(fileArc, 'w')
  for d, dirs, files in os.walk(os.getcwd()):
    for f in files:
      print os.path.join(d,f)
      if f != fileArc:
	zf.write(os.path.join(d, f))
  zf.close()
  
def sendFiles(host, user, passwd, fileArc):
  ftpCon = ftplib.FTP(host, user, passwd, site)
  ftpCon.set_pasv(True)
  ftpCon.mkd(site)
  ftpCon.cwd(site)
  ftpCon.storbinary('STOR '+fileArc, open(fileArc, 'rb'))
  ftpCon.quit()
  
  
if __name__=='__main__':
  print "Content-Type: text/html\r\n\r\n"
  main()
  sys.exit()