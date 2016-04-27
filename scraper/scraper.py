import requests;
from bs4 import BeautifulSoup
import re;
import json;
import math;
import threading;
from threading import Thread;

html_parser = "html.parser";

num_threads = 10;
file_root = 'grad_data_';
file_suffix = ".json";

pn = open("page_no.txt", "w+");


link_id_rx1 = "^normalthread_";
link_id_rx2 = "^stickthread_";
thread_link_rx = "^http://www.1point3acres.com/bbs/thread-\d*-\d-\d.html";

english_rx = r'[\x00-\x7f]+'

links_table_class = "threadlisttableid";
footer_id = "fd_page_bottom";

url = "http://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=82&sortid=164&%1=&sortid=164&page=";

r = requests.get(url + str(1));
tree = BeautifulSoup(r.text, html_parser);

#Total number of pages are in the footer. Should return something ~886
footer = tree.find(id=footer_id).find("div", class_="pg").find("label").find("span");

page_no_limit = int(re.findall(r'\d+', footer.text)[0]);

page_buckets = [];
num_per_bucket = math.ceil((page_no_limit + 1) / num_threads);
buckets = [[]];
pos = 0;
for i in range(1, page_no_limit + 1):
    if i % num_per_bucket == 0:
        pos = pos + 1;
        buckets.append([]);
    buckets[pos].append(i);



def query_pages_in_bucket(bucket, bucket_no):
    pos = 0
    page_no = bucket[pos];
    file_name = file_root + str(bucket_no).zfill(5) + file_suffix;
    fp = open(file_name, "w+");

    while pos < len(bucket):
        page_no = bucket[pos];
        print("Page no: " + str(page_no) + ", bucket: " + str(bucket_no));
        pn.write("Page no: " + str(page_no) + ", bucket: " + str(bucket_no) + "\n");
        pn.flush();
        
        r = requests.get(url + str(page_no));
        tree = BeautifulSoup(r.text, html_parser);
        links = tree.find_all("tbody", id=lambda s: re.compile(link_id_rx1).match(s) or re.compile(link_id_rx2).match(s));

        for link in links:
            link_obj = {};
            link_body = link.find("tr").find("th");

            try:
                user = link.find("td", class_="by").find("a").text;
                if len(user) != 0:
                    link_obj["user"] = user;
            except AttributeError:
                pass;

            #more information in thread, but can't parse yet.
            
            #link of thread must be of a specific format, but there are many links in each table, so get the right one.
            try:
                thread_link = list(filter(lambda x: re.compile(thread_link_rx).match(x["href"]) != None, link_body.find_all("a")))[0]["href"];
                link_obj["url"] = thread_link;

                thread_tree = BeautifulSoup(requests.get(thread_link).text, html_parser);

                #it seems that the header is alawys the first 'u' element on the page. haven't found a case otherwise yet.
                thread_header = thread_tree.find("u");
                thread_content = thread_header.find_parent("div");
                thread_items = thread_content.find_all("li");
                thread_gpa = str(thread_content.find_all(text=re.compile("GPA"))[0]);
                link_obj["gpa"] = re.findall(r'[0-9]\.[0-9]', thread_gpa)[0];
            except IndexError:
                pass;
            except AttributeError:
                pass;
            
            try:
                thread_header = link_body.find("u");
                thread_header_items = re.compile('\]').split(thread_header.text);
                offer_details = thread_header_items[0][1:];
                univ_details = thread_header_items[1][1:];

                #remove any chinese characters
                offer_details = re.compile(english_rx).match(offer_details).group(0);
                univ_details = re.compile(english_rx).match(univ_details).group(0);

                offer_details_items = re.compile('\.').split(offer_details);
                univ_details_items = re.compile('@').split(univ_details);
                
                try:
                    link_obj['year'] = offer_details_items[0];
                    link_obj['degree'] = offer_details_items[1];
                    link_obj['acceptance'] = offer_details_items[2];
                except IndexError:
                    pass;

                try:
                    link_obj['university'] = univ_details_items[len(univ_details_items) - 1];
                    link_obj['majors'] = univ_details_items[0:len(univ_details_items) - 1];
                except IndexError:
                    pass;
                
                try:
                    t_part = link_body.find("b", text=re.compile("^T$")).next_sibling;
                    g_part = link_body.find("b", text=re.compile("^G$")).next_sibling;
                    top_part = link_body.find("font", text=re.compile("Top\d* \d*")).text;
                    top = re.findall(r'\d+', top_part);

                    link_obj['G'] = str(g_part)[2:];
                    link_obj['T'] = str(t_part)[2:];
                    link_obj['top'] = top[0] + '/' + top[1];

                except IndexError:
                    pass;
                except AttributeError:
                    pass;

                #print(link_obj);
                json.dump(link_obj, fp);
                
            except AttributeError:
                continue;
        #break;
        pos = pos + 1; 

    fp.flush();
    fp.close();

#for i in range(0, len(buckets)):
    #threading.Thread(target=query_pages_in_bucket, args=(buckets[i], i+1, )).start();
