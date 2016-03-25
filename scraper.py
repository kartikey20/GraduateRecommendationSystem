import requests;
from bs4 import BeautifulSoup
import re;

class Scraper(object):
    def get_forum_links(self, panel):
        #fonts = summary_panel.find_all("font", text = re.compile("^201"));

        year = "";
        link_map = {};
        for child in panel.contents:
            try:
                if child.name == 'font':
                    year = child.text;
                    link_map[year] = [];

                if child.name == 'a':
                    link_map[year].append({child.text : child['href']});
            except AttributeError:
                pass

        print link_map;

    def __init__(self):
    	summary_panel_class = "xg2";
    	url = "http://www.1point3acres.com/bbs/forum-177-1.html";


    	r = requests.get(url);
    	tree = BeautifulSoup(r.text);

    	summary_panel = tree.find_all(class_=summary_panel_class)[0];
        self.get_forum_links(summary_panel);


if __name__  == "__main__":
    imdb = Scraper();