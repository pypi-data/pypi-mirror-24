from pystas import logpista
import random
import time


@logpista
def a_function_with_strange_behavior(bla):
    print 'will I crash?',
    if random.random() < 0.05:
        print 'yes..'
        raise Exception("bla")
    if random.random() < 0.05:
        print 'yes..'
        raise RuntimeError("shit")
    print 'no! :-)'


class SomeClass:
    @logpista
    def some_interesting_method(self):
        print 'hold on..'
        time.sleep(random.random()*3)

for x in xrange(random.randint(1, 7)):
    a_function_with_strange_behavior(2)
for x in xrange(random.randint(1, 2)):
    A().some_interesting_method()
for x in xrange(random.randint(1, 2)):
    a_function_with_strange_behavior(2)
