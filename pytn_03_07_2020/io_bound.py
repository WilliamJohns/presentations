import multiprocessing as mp
from multiprocessing.pool import ThreadPool

from time import sleep

import click


def do_something_important(_=None):
    click.echo('Doing something important for 1 second...', nl=False)
    sleep(1)
    click.echo('Done')


def synchronus_handler(iterations, workers=None):
    """
    Results from Dev machine:
    >>> time python io_bound.py sync -i 5 -w 5
    Doing something important for 1 second...Done
    Doing something important for 1 second...Done
    Doing something important for 1 second...Done
    Doing something important for 1 second...Done
    Doing something important for 1 second...Done

    real    0m5.248s
    user    0m0.047s
    sys     0m0.156s
    """
    for _ in range(iterations):
        do_something_important()


def threaded_handler(iterations, workers):
    """
    Results from Dev machine:
    >>> time python io_bound.py thread -i 5 -w 5
    Doing something important for 1 second...Doing something important for 1 second...Doing something important for 1 second...Doing something important for 1 second...Doing something important for 1 second...Done
    Done
    Done
    Done
    Done

    real    0m1.250s
    user    0m0.047s
    sys     0m0.188s
    """
    thread_pool = ThreadPool(workers)

    thread_pool.map(do_something_important, range(iterations))

    thread_pool.close()


def process_handler(iterations, workers):
    """
    Results from Dev machine:
    >>> time python io_bound.py process -i 5 -w 5
    Doing something important for 1 second...Doing something important for 1 second...Doing something important for 1 second...Doing something important for 1 second...Doing something important for 1 second...Done
    Done
    Done
    Done
    Done

    real    0m1.382s
    user    0m0.078s
    sys     0m0.250s
    """
    process_pool = mp.Pool(workers)

    process_pool.map(do_something_important, range(iterations))

    process_pool.close()


HANLDER_MAP = {
    'sync': synchronus_handler,
    'thread': threaded_handler,
    'process': process_handler,
}


@click.command()
@click.argument('mode')
@click.option(
    '-i', '--iterations',
    default=1,
    type=click.INT
)
@click.option(
    '-w', '--workers',
    type=click.INT,
    default=4
)
def execute(mode, iterations, workers):
    HANLDER_MAP[mode](iterations, workers)


if __name__ == "__main__":
    execute()
