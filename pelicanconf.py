AUTHOR = 'kienlt'
SITENAME = "Kienlt's notebook"
SITEURL = ""

PATH = "content"

TIMEZONE = 'Asia/Ho_Chi_Minh'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = True
RECENT_ARTICLES_COUNT = 20
THEME = 'themes/elegant'  # https://github.com/Pelican-Elegant/elegant
# Show only titles on the index page
SUMMARY_MAX_LENGTH = 0
STATIC_PATHS = ['static', 'images']
