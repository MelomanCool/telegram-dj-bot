# -*- coding: utf-8 -*-

import requests
import json
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger


def tele_post(settings, method, data, files=None):
    return requests.post(
        '{url_base}{token}/{method}'.format(method=method, **settings),
        data=data,
        proxies=settings['proxies'],
        files=files
    )


def send_file(settings, item):
    tele_post(settings,
              'sendPhoto',
              data={'chat_id': item['channel']},
              files={'photo': open('images/{0}'.format(item['image']), 'rb')})
    tele_post(settings,
              'sendAudio',
              data={'chat_id':    item['channel'],
                    'parse_mode': 'Markdown',
                    'caption':    item['caption']},
              files={'audio': open('music/{0}'.format(item['file']), 'rb')})


def send_url(settings, item):
    tele_post(settings,
              'sendPhoto',
              data={'chat_id': item['channel'],
                    'photo':   item['image']})
    tele_post(settings,
              'sendAudio',
              data={'chat_id':    item['channel'],
                    'parse_mode': 'Markdown',
                    'caption':    item['caption']
                    'audio':      item['url']})


def sendPost(settings, item):
    if(item['mode'] == 'file'):
        return send_file(settings, item)
    else:
        return send_file(settings, item)


def schedulePlaylist(settings, playlist, scheduler):
    #lstindex = len(playlist)
    for index, item in enumerate(playlist, start=1):
        date_trigger = DateTrigger(datetime.strptime(item['time'], '%Y.%m.%d %H:%M'))
        scheduler.add_job(lambda item: sendPost(settings, item), date_trigger, kwargs=item)
        print('Job created at ', date_trigger)
        # if index == lstindex:
        #     scheduler.add_job(scheduler.shutdown, 'date', run_date=end_datetime)
    scheduler.start()


def main():
    demo_playlist = json.load(open('playlist.json', 'r'))
    settings = json.load(open('settings.json', 'r'))

    sched = BackgroundScheduler()

    schedulePlaylist(settings, demo_playlist, sched)

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        sched.shutdown()

    print('all jobs are done')


main()
