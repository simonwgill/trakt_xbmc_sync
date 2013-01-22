#!/usr/bin/env python

###################### SETTINGS ######################
trakt_username = ''
trakt_password = ''
trakt_apikey = ''

# Array of show slugs to set to unwatched
unwatch_shows = ['how-i-met-your-mother', 'fringe']

#################### END SETTINGS ####################


try:
    import json
except ImportError:
    import simplejson as json
import urllib2, base64, hashlib, copy

def trakt_api(url, params={}):
    '''Connects to trakt.tv api'''
    username = trakt_username
    password = hashlib.sha1(trakt_password).hexdigest()

    params = json.JSONEncoder().encode(params)
    request = urllib2.Request(url, params)
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)

    response = urllib2.urlopen(request).read()
    response = json.JSONDecoder().decode(response)

    return response


def unwatch_show(show_name):
    print '\nGetting TV shows from trakt'

    # Episodes Collection
    url = 'http://api.trakt.tv/show/summary.json/%s/%s/extended' % (trakt_apikey, show_name)
    try:
        show = trakt_api(url)
        show['episodes'] = []
    except Exception as e:
        quit(e)

    print '\nFound %s' % (show['title'])

    for season in show['seasons']:
        for episode in season['episodes']:
            ep = { 'season': episode['season'], 'episode': episode['episode'], 'title': episode['title'] }
            show['episodes'].append(ep)

    url = 'http://api.trakt.tv/show/episode/unseen/%s' % (trakt_apikey)
    params = {}
    params['username'] = trakt_username   
    params['password'] = hashlib.sha1(trakt_password).hexdigest()
    params['tvdb_id'] = show['tvdb_id']
    params['title'] = show['title']
    params['year'] = show['year']
    params['episodes'] = []

    for ep in show['episodes']:
        print '%s-%sx%s-%s' % (show_name, ep['season'], ep['episode'], ep['title'])
        params['episodes'].append({'season': ep['season'], 'episode': ep['episode']})
        trakt_api(url, params)

if __name__ == '__main__':
  for show in unwatch_shows:
    unwatch_show(show)
