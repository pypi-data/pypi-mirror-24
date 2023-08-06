from pystas import logpista
import random
import time

@logpista
def sample(bla):
    print 'aca!'
    if random.random()<0.05:
        raise Exception("bla")
    if random.random()<0.05:
        raise RuntimeError("shit")


class A:
    @logpista
    def test(self):
        print 'bla'
        time.sleep(random.random()*3)

A().test()
for x in xrange(random.randint(1,7)):
    sample(2)
for x in xrange(random.randint(1,2)):
    A().test()
for x in xrange(random.randint(1,2)):
    sample(2)
