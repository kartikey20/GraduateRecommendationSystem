import requests;
from bs4 import BeautifulSoup
import re;

summary_panel_class = "xg2";
url = "http://www.1point3acres.com/bbs/forum-177-1.html";
r = requests.get(url);
tree = BeautifulSoup(r.text);
summary_panel = tree.find_all(class_=summary_panel_class)[0];

#fonts = summary_panel.find_all("font", text = re.compile("^201"));

year = "";
link_map = {};
year_re = re.compile("^201.");
for child in summary_panel.contents:
    try:
        if year_re.match(child.text):
            year = child.text;
            link_map[year] = [];

        elif child.name == 'a':
            link_map[year].append({'name' : child.text , 'link' : child['href'], "threads" : []});
    except AttributeError:
        pass

    #print link_map;

url_match = re.compile("^http://www.1point3acres.com");
for year in link_map:
    for major in link_map[year]:
        r = requests.get(major['link'])
        soup = BeautifulSoup(r.text);
        #soup.find(id="threadstamp").find_parent("div").find("table");
        table = soup.select(".t_fsz .t_f")[0];
        links = table.find_all("a");
        for link in links:
            try:
                if url_match.match(link["href"]):
                    try:
                        thread_dict = {};
                        thread_dict["link"] = link["href"];

                        r = requests.get(link["href"]);
                        thread = BeautifulSoup(r.text);
                        post = thread.select(".pcb")[0];
                        
                        title = post.find("u");
                        thread_dict["title"] = title.text;

                        thread_dict["points"] = [];
                        points = post.find_all("li");
                        for point in points:
                            thread_dict["points"].append(point.text);
                    except IndexError:
                        pass;

                    major["threads"].append(thread_dict);
            except KeyError:
                pass;
            print major["threads"];
        break;
    break;

print link_map;