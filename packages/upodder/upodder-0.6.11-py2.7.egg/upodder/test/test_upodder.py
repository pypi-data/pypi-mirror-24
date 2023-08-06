import unittest
import shutil

from upodder import upodder

BASEDIR = '/tmp/upodder_testing'

class TestUpodder(unittest.TestCase):
    feeds = [
                "https://www.relay.fm/clockwise/feed",
                "http://popupchinese.com/feeds/custom/sinica",
                "http://www.radiolab.org/feeds/podcast/",
                "http://99percentinvisible.org/feed/",
                "http://chaosradio.ccc.de/chaosradio-latest.rss",
                "http://djfm.ca/?feed=rss2",
                "http://feeds.feedburner.com/Sebastien-bHouseFromIbiza/",
                "http://alternativlos.org/ogg.rss",
                "http://www.sovereignman.com/feed/",
                "http://neusprech.org/feed/",
                "http://www.davidbarrkirtley.com/podcast/geeksguideshow.xml",
                "http://www.cbc.ca/cmlink/1.2919550",
                "http://feeds.feedburner.com/binaergewitter-podcast-opus",
                "http://podcastfeeds.nbcnews.com/audio/podcast/MSNBC-MADDOW-NETCAST-M4V.xml",
                "http://feeds.feedburner.com/uhhyeahdude/podcast",
            ]

    def setUp(self):
        upodder.args.no_download = True
        upodder.args.mark_seen = False
        upodder.args.oldness = 720
        upodder.args.basedir = BASEDIR
        upodder.init()

    def tearDown(cls):
        shutil.rmtree(BASEDIR);

class TestFeedProcessing(TestUpodder):
    def test_feedparsing(self):
        for f in self.feeds:
            upodder.process_feed(f)

    def test_mark_seen(self):
        upodder.args.mark_seen = True
        for f in self.feeds:
            upodder.process_feed(f)

        self.assertGreater(upodder.SeenEntry.select().count(), 5)


class TestFailingFeeds(TestUpodder):
    def test_failing_feed(self):
        upodder.process_feed('http://www.google.com')

if __name__ == '__main__':
    unittest.main()
