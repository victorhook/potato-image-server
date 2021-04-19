from datetime import datetime
import os
from pathlib import Path
import pickle


__all__ = ['cache']


CACHE_DIR_NAME = '.cache'
CACHE_FILE_ENDING = '.cache'
LAST_CHANGE_TIME_LIMIT = 10         # In minutes


def get_cache_path(func: callable, *args) -> str:
    """ Returns the absolute path of the cache file. """
    base_path = '/home/victor/coding/web/potato-image-server/potato_image_server/potato_image_server'
    filename = func.__name__ + '_'
    filename += '_'.join([str(arg) for arg in args]).replace(' ', '-')
    filename += CACHE_FILE_ENDING

    return os.path.join(base_path, CACHE_DIR_NAME, filename)


def need_to_update(path: str) -> bool:
    """ Returns if the cache needs to be updated or not. """
    need_update = True
    try:
        last_update = os.path.getmtime(path)
        last_update = datetime.fromtimestamp(last_update)
        now = datetime.now()
        
        time_diff = now - last_update
        time_diff_minutes = int(time_diff.seconds / 60)

        need_update = time_diff_minutes > LAST_CHANGE_TIME_LIMIT

    except FileNotFoundError:
        # Ensure at least directory exists.
        Path(os.path.dirname(path)).mkdir(exist_ok=True)

    return need_update


def save_cache_result(path: str, result: str) -> None:
    with open(path, 'wb') as f:
        pickle.dump(result, f)


def load_cache_result(path: str) -> object:
    with open(path, 'rb') as f:
        return pickle.load(f)


def cache(func: callable):
    
    def wrapper(*args, **kwargs):
        path = get_cache_path(func, *args)

        if need_to_update(path):
            print('Saving cache!')
            result = func(*args, **kwargs)
            save_cache_result(path, result)
        else:
            print('Opening cached')
            result = load_cache_result(path)
        return result

    return wrapper
