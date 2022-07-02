#!/usr/bin/python3.9

print('Content-type:text/html\r\n\r')
print('<html lang="en">')
print('  <head>')
print('    <title>')
print('PostgreSQL Authorization File Generator')
print('     </title>')
#print('    <link rel="stylesheet" href="entry.css">')
print('   </head>')
print('  <body>')
  
from os import environ

if 'QUERY_STRING' in environ and environ['QUERY_STRING'] != '':
  print('    <p>')
  #print('Passed ', environ['QUERY_STRING'])
  #print('      <br>')
  parts = environ['QUERY_STRING'].split('&')
  partsNo = len(parts)
  #print(partsNo, ' parts')
  partCount = 0
  #print('      <ol>')
  partDict = {}
  while partCount < partsNo:
    #print('        <li>\n',parts[partCount])
    cleavage = parts[partCount].split('=')
    partDict[cleavage[0]] = cleavage[1]
    partCount += 1
  #print('       </ol>')
  #print('Built dictionary ', partDict)
  filename = ''
  username = ''
  password = ''
  db = ''
  if 'filename' not in partDict or partDict['filename'] == '':
    print('A filename is needed.')
  else:
    filename = partDict['filename']
  if 'username' not in partDict or partDict['username'] == '':
    print('A username is needed.')
  else:
    username = partDict['username']
  if 'password' not in partDict or partDict['password'] == '':
    print('A password is needed.')
  else:
    password = partDict['password']
  if 'db' not in partDict or partDict['db'] == '':
    print('A database is needed.')
  else:
    db = partDict['db']
  if filename != '' and username != '' and password != '' and db != '':
    contents = 'user="' + username + '"\n'
    contents += 'password="' + password + '"\n'
    contents += 'dbname="' + db + '"\n'
    
    try:
      authfile = open(filename, 'w')
      authfile.write(contents)
      authfile.close()
      print('authorization file written')
    except OSError:
      print('could not open ', filename, ' for writing')
      print('suggest touching and setting permissions to universal write')
    
    importError = False
    try:
      import psycopg2
    except ImportError:
      print('could not import psycopg2')
      importError = True
    
    connectError = False
    if not importError:
      try:
        connection = psycopg2.connect(dbname=db, user=username,
			password=password)
        print('<br>connected to database')
      except psyscopg2.Error:
        print('could not connect to database')
        connectError = True
    
    if not connectError:
      cursor = connection.cursor()
      query = "select tablename from pg_catalog.pg_tables where tableowner ="
      query += " '" + username + "'"
      cursor.execute(query)
      if cursor.rowcount == 0:
        print('<br>no tables')
      else:
        print('<br>Tables:')
        print('      <ul>')
        for record in cursor:
          print('        <li>')
          print(record[0])
        print('       </ul>')

  print('     </p>')

print('    <form action="generate-authfile.py">')
print('      <label for="filename">')
print('File name:')
print('       </label>')
print('      <input type="text" id="filename" name="filename"')
print(' value="auth.txt">')
print('      <br>')
print('      <label for="username">')
print('User name:')
print('       </label>')
print('      <input type="text" id="username" name="username">')
print('      <br>')
print('      <label for="password">')
print('Password:')
print('       </label>')
print('      <input type="text" id="password" name="password">')
print('      <br>')
print('      <label for="password">')
print('Database:')
print('       </label>')
print('      <input type="text" id="db" name="db">')
print('      <br>')
print('      <input type="submit" id="submit"')
print('       name="submit" value="Enter">')
print('     </form>')
print('   </body>')
print(' </html>')
