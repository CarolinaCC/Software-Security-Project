request = "ola"
uname = QueryDict(request)
q = mogrify("SELECT pass FROM users WHERE user='%s'" % uname)
