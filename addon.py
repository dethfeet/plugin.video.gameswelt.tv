from xbmcswift2 import Plugin
from resources.lib import scraper


plugin = Plugin()


@plugin.route('/')
def index():
    items = []
    #Suche
    items.append({
        'label': 'Search',
        'path': plugin.url_for(
            endpoint='search',
        ),
        'is_playable': False
        })
    #Kategorien
    for category in scraper.get_categories():
        items.append({
        'label': category['title'],
        'path': plugin.url_for(
            endpoint='show_category',
            path=category['path'],
        ),
        'thumbnail': category['thumb'],
        'is_playable': False
        })
    return plugin.finish(items)

    
@plugin.route('/category/<path>/')
def show_category(path):
    items = []
    for video in scraper.get_videos(path):
        if video['type'] == 'video':
            items.append({
            'label': video['title'],
            'path': plugin.url_for(
                endpoint='show_video',
                videoId=video['parameter'],),
            'thumbnail': video['thumb'],
            'info':{'plot': video['teaser']},
            'is_playable': True
            })
        elif video['type'] == 'category':
            items.append({
            'label': video['title'],
            'path': plugin.url_for(
                endpoint='show_category',
                path=video['parameter'],),
            'is_playable': False
            })
    return plugin.finish(items)

@plugin.route('/search/')
def search():
    search_string = plugin.keyboard(heading='Search')
    if search_string:
        url = plugin.url_for(
            'show_category',
            path=scraper.get_search_path(search_string)
        )
        return plugin.redirect(url)  
    return False
    
@plugin.route('/video/<videoId>/')
def show_video(videoId):
    quality = plugin.get_setting('quality', choices=('SD', 'HD'))
    video_url = scraper.get_video_urls(videoId)[quality]
    return plugin.set_resolved_url(video_url)

if __name__ == '__main__':
    plugin.run()
