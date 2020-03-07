import multiprocessing as mp
from multiprocessing.pool import ThreadPool

from pathlib import Path
from random import randint
from time import sleep

import click
import h5py


def synchronus_handler(iterations, workers=None):
    """
    Results from Dev machine:
    >>> time python cpu_bound.py sync -i 5
    Found 6 instances of b'mezzo' in 10,000 files
    Found 11 instances of b'radioparadise' in 10,000 files
    Found 2 instances of b'female power voice' in 10,000 files
    Found 2 instances of b'mezz 2005' in 10,000 files
    Found 2 instances of b'alternative invaders' in 10,000 files

    real    1m52.473s
    user    1m44.578s
    sys     0m8.953s
    """
    data_path = Path('./')
    with open('MillionSongSubset/AdditionalFiles/subset_unique_terms.txt', 'r') as f:
        unique_terms = [
            line.strip().encode()
            for line in f.readlines()
        ]

    for _ in range(iterations):
        found_count = 0
        artist_term = unique_terms.pop(randint(0, len(unique_terms)-1))
        data_files = data_path.rglob('data/**/*.h5')
        for data_file in data_files:
            with h5py.File(str(data_file), 'r') as f:
                if artist_term in f['metadata']['artist_terms']:
                    found_count += 1
        click.echo(f'Found {found_count} instances of {artist_term} in 10,000 files')


def thread_worker(payload):
    file_path, term = payload
    found_count = 0
    with h5py.File(str(file_path), 'r') as f:
        if term in f['metadata']['artist_terms']:
            found_count += 1
    return found_count


def threaded_handler(iterations, workers):
    """
    Results from Dev machine:
    >>> time python cpu_bound.py thread -i 5 -w 4
    Found 53 instances of b'freakbeat' in 10,000 files
    Found 9 instances of b'antifa' in 10,000 files
    Found 1 instances of b'turntablist' in 10,000 files
    Found 13 instances of b'artist' in 10,000 files
    Found 1 instances of b'sharp' in 10,000 files

    real    2m11.376s
    user    1m57.000s
    sys     0m19.547s
    """
    data_path = Path('./')
    thread_pool = ThreadPool(workers)
    with open('MillionSongSubset/AdditionalFiles/subset_unique_terms.txt', 'r') as f:
        unique_terms = [
            line.strip().encode()
            for line in f.readlines()
        ]

    def _payload_generator(term):
        data_files = data_path.rglob('data/**/*.h5')
        for data_file in data_files:
            yield data_file, term

    for _ in range(iterations):
        found_count = 0
        artist_term = unique_terms.pop(randint(0, len(unique_terms)-1))
        final_count = sum(thread_pool.map(thread_worker, _payload_generator(artist_term)))
        click.echo(f'Found {final_count} instances of {artist_term} in 10,000 files')

    thread_pool.close()


def process_handler(iterations, workers):
    """
    Results from Dev machine:
    >>> time python cpu_bound.py process -i 5 -w 4
    Found 7 instances of b'vinyl' in 10,000 files
    Found 93 instances of b'afro-cuban jazz' in 10,000 files
    Found 2 instances of b'deejay' in 10,000 files
    Found 3 instances of b'hard style' in 10,000 files
    Found 4 instances of b'southern gothic' in 10,000 files

    real    0m31.743s
    user    1m48.000s
    sys     0m11.938s
    """
    data_path = Path('./')
    process_pool = mp.Pool(workers)
    with open('MillionSongSubset/AdditionalFiles/subset_unique_terms.txt', 'r') as f:
        unique_terms = [
            line.strip().encode()
            for line in f.readlines()
        ]

    def _payload_generator(term):
        data_files = data_path.rglob('data/**/*.h5')
        for data_file in data_files:
            yield data_file, term

    for _ in range(iterations):
        found_count = 0
        artist_term = unique_terms.pop(randint(0, len(unique_terms)-1))
        final_count = sum(process_pool.map(thread_worker, _payload_generator(artist_term)))
        click.echo(f'Found {final_count} instances of {artist_term} in 10,000 files')

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
    default=100,
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
