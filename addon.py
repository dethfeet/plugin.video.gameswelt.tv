from xbmcswift2 import Plugin
from resources.lib import scraper


plugin = Plugin()


@plugin.route('/')
def index():
    items = []
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
    
    
@plugin.route('/video/<videoId>/')
def show_video(videoId):
    quality = plugin.get_setting('quality', choices=('SD', 'HD'))
    video_url = scraper.get_video_urls(videoId)[quality]
    return plugin.set_resolved_url(video_url)

if __name__ == '__main__':
    plugin.run()
