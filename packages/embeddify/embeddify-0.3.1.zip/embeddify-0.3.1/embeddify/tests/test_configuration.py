from embeddify import Embedder, YouTube

def test_generic_youtube():
    embedder = Embedder(width=200)
    assert embedder("https://www.youtube.com/watch?v=2wii8hfNkzE") == """<iframe width="200" height="113" src="https://www.youtube.com/embed/2wii8hfNkzE?feature=oembed" frameborder="0" allowfullscreen></iframe>"""

def test_generic_slideshare():
    embedder = Embedder(width=200)
    assert embedder("http://de.slideshare.net/mrtopf/open-government-vortrag-aachen").startswith("""<iframe src="https://www.slideshare.net/slideshow/embed_code/key/3wGhGoN6QUw5lR" """)

def test_plugin_specific_config():
    cfg = {
        'youtube' : {'width' : 200 },
        'slideshare' : {'width' : 500 }
    }
    embedder = Embedder(plugin_config=cfg)
    assert embedder("https://www.youtube.com/watch?v=2wii8hfNkzE").startswith("""<iframe width="200" height="113" src="https://www.youtube.com/embed/2wii8hfNkzE?feature=oembed""")

    assert embedder("http://de.slideshare.net/mrtopf/open-government-vortrag-aachen").startswith("""<iframe src="https://www.slideshare.net/slideshow/embed_code/key/3wGhGoN6QUw5lR" width="427" height="356" """)

def test_plugin_selection():
    """only use youtube"""
    embedder = Embedder(plugins = [YouTube()])
    assert embedder("https://www.youtube.com/watch?v=2wii8hfNkzE") == """<iframe width="560" height="315" src="https://www.youtube.com/embed/2wii8hfNkzE?feature=oembed" frameborder="0" allowfullscreen></iframe>"""
    assert embedder("http://de.slideshare.net/mrtopf/open-government-vortrag-aachen") == "http://de.slideshare.net/mrtopf/open-government-vortrag-aachen"

def test_by_call_configuration():
    embedder = Embedder(width=400)
    assert embedder.plugin_config['youtube'] == dict(width=400)
    assert embedder("https://www.youtube.com/watch?v=2wii8hfNkzE", width=200) == """<iframe width="200" height="113" src="https://www.youtube.com/embed/2wii8hfNkzE?feature=oembed" frameborder="0" allowfullscreen></iframe>"""
    assert embedder.plugin_config['youtube'] == dict(width=400)


def test_autoplay():
    embedder = Embedder(autoplay=True)
    result = embedder("http://vimeo.com/6791752")
    assert result.startswith("""<iframe src="https://player.vimeo.com/video/6791752?autoplay=1" width="420" height="315" """)
    result = embedder("https://www.youtube.com/watch?v=SC93q4tZeNI")
    assert result == """<iframe width="560" height="315" src="https://www.youtube.com/embed/SC93q4tZeNI?feature=oembed&autoplay=1" frameborder="0" allowfullscreen></iframe>"""


def test_params():
    embedder = Embedder()
    result = embedder("http://vimeo.com/6791752", params=dict(autoplay=True))
    assert result.startswith("""<iframe src="https://player.vimeo.com/video/6791752?autoplay=1" width="420" height="315" """)
