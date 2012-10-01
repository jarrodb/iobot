from tornado.ioloop import IOLoop
from iobot import IOBot

def main():
    ib = IOBot(
        host = 'senor.crunchybueno.com',
        nick = 'iono',
        char = '#',
        owner = 'norf',
        port = 6667,
        initial_chans = ['#norf'],
        )

    ib.register(['echo','stock'])

    IOLoop.instance().start()

if __name__ == '__main__':
    main()

