from django.shortcuts import render
from django.core import serializers
from datetime import datetime, timedelta


from sensor import models
from .proxy import Proxy
from . import utils



def get_latest_sample():
    latest_sample = models.Sample.objects.using('data').latest('date')
    return utils.dateify_sample(latest_sample)

def get_last24hr():
    time_threshold = datetime.now() - timedelta(hours=24)
    results = models.Sample.objects.using('data').filter(date__gt=time_threshold)
    return results

def index(request):
    dates = Proxy.get_dates()
    all_samples = get_last24hr()
    all_samples = list(map(utils.dateify_sample, all_samples))

    temperatures = list(map(lambda sample: sample.temperature, all_samples))
    times = map(lambda sample: sample.time, all_samples)

    min_temp = min(temperatures)
    max_temp = max(temperatures)
    if len(temperatures) > 0:
        avg_temp = sum(temperatures) / len(temperatures)
    else:
        avg_temp = 0

    times = '[' + ', '.join(f'"{t}"' for t in times) + ']'
    temperatures = '[' + ', '.join(str(t) for t in temperatures) + ']'


    return render(request, 'index.html', {
        'dates': dates, 
        'latest_sample': get_latest_sample(),
        'all_samples': all_samples,
        'temperatures': temperatures,
        'times': times,
        'min_temp': min_temp,
        'max_temp': max_temp,
        'avg_temp': avg_temp,
        })


def date(request, date:str):
    dates = Proxy.get_dates()
    weekday = utils.get_weekday(date)
    images = _get_images(date)
    return render(request, 'date.html', {
        'dates': dates,
        'date': date,
        'weekday': weekday,
        'images': images,
        'latest_sample': get_latest_sample()
    })


def image(request, date:str, img:str):
    data = Proxy.get_image(date, img)
    dates = Proxy.get_dates()
    date = _get_image_date(img)
    weekday = utils.get_weekday(date)
    time = _get_image_time(img)
    return render(request, 'image.html', {
        'date': date,
        'time': time,
        'data': data,
        'image': img,
        'weekday': weekday,
        'dates': dates,
        'latest_sample': get_latest_sample()
    })


def next_image(request, date:str, img:str):
    date, img = _next_image(date, img)
    return image(request, date, img)


def prev_image(request, date:str, img:str):
    date, img = _next_image(date, img, next_image=False)
    return image(request, date, img)


def _next_image(date:str, img:str, next_image: bool = True) -> str:
    """ Helper method to get the next image.
        "next" can be either next as future, or previous.
    """
    images = Proxy.get_images(date)
    
    pos = images.index(img)
    direction = 1 if next_image else -1
    new_pos = pos + direction


    if new_pos == len(images) or new_pos < 0:
        dates = Proxy.get_dates()
        date_pos = dates.index(date)

        if new_pos < 0:
            # Go BACK in time
            date_pos -= 1
            new_img_pos = -1

        else:
            # Go FORWARD in time
            date_pos += 1
            if date_pos == len(dates):
                date_pos = -1
            new_img_pos = 0

        date = dates[date_pos]
        img = Proxy.get_images(date)[new_img_pos]
    else:
        img = images[new_pos]
    
    return date, img


def _get_image_date(img: str) -> str:
    return _get_image_name(img).split('_')[0]


def _get_image_time(img: str) -> str:
    return _get_image_name(img).split('_')[1] \
           .replace('-', ':')


def _get_image_name(img: str) -> str:
    return img.split('.jpg')[0]


def _get_images(date:str) -> tuple:
    """ Helper method to get images and create their names. """
    images = Proxy.get_images(date)
    names = map(_get_image_time, images)
    return zip(images, names)