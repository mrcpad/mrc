# -*- coding: gbk -*-


import wrapt




def logginginfo(level):
    print(level)
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        print(2)
        print(wrapped)
        print(args)
        print(kwargs)
        print(wrapped(*args, **kwargs))
        import logging
        logging.basicConfig(level=logging.INFO,
                            filename='service.log',
                            filemode='a',
                            format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

        #print "[{level}]: enter function {func}()".format(level=level, func=wrapped.__name__)
        logging.info("[{level}]: enter function {func}()".format(level=level, func=wrapped.__name__))
        return wrapped(*args, **kwargs)
    return wrapper
@logginginfo('INFO')
def test(a):
    print(a)
    return 10*a

print(test(5))