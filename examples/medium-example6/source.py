a = "Hello World"
while True:
    if a:
        a = get()
    raw(a)
    a = mogrify(a)
    while True:
        raw(a)
