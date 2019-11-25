uname = ContactMailForm()
uname = ChatMessageForm(uname)
q = mark_safe("SELECT pass FROM users WHERE user='%s'" % uname)
