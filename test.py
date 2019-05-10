def consumer():
    status = True
    while True:
        n = yield status
        print "get %s" % n
        if n == 3:
            status = False

def producer(consumer):
    n = 5
    while n > 0:
        yield consumer.send(n)
        n -= 1

if __name__ == '__main__':
    c = consumer()
    c.send(None)
    p = producer(c)
    print p
    for status in p:
        if status == False:
            print "just need 3,4,5"
            break
    print "over"