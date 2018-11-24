from lxml import etree
import urllib.request as url
import urllib.error as ure
import os,time,json,re,random

ua = open('user-agents.txt','rt',1,'utf-8','ignore')
user_agent = ua.readlines()

class therad():

    def get(link):
        while True:
            try:
                therad = url.Request(link)
                try:
                    therad.add_header('User-Agent',(random.choice(user_agent)).replace('\n',''))
                    therad.add_header('Referer','https://tieba.baidu.com')
                except:
                    pass
                finally:
                    therad_read = url.urlopen(therad)
            except ure as status:
                print("Access Tieba Error!Please Check the link you input!Error Reason:\n%s" % (str(status)))
                pass
            except:
                print("Unkonwn Error!")
                pass
            else:
                break
        therad_list = etree.HTML((therad_read.read()).decode())
        therad_list = therad_list.xpath('//div[@class="l_post l_post_bright j_l_post clearfix  "]')
        for per_floor in therad_list:
            for i in per_floor.xpath('.//span[@class="tail-info"]/text()'):
                if i.find('楼') != -1:
                    floor = 'floor_' + str((i.replace('楼','')))
                else:
                    pass
                
            #floor = 'floor_' + str(((per_floor.xpath('.//span[@class="tail-info"]/text()'))[0]).replace('楼',''))
            author = (json.loads((per_floor.xpath('./@data-field'))[0]))['author']['user_name']
            main_text = per_floor.xpath('.//div[@class="d_post_content j_d_post_content "]//text()')
            for a in per_floor.xpath('.//div[@class="d_post_content j_d_post_content "]//a//text()'):
                try:
                    a_place = (main_text.index(a,))
                except:
                    pass
                else:
                    try:
                        main_text[a_place + 1]
                    except:
                        main_text[a_place - 1] = main_text[a_place - 1] + main_text[a_place]
                        del main_text[a_place]
                    else:
                        main_text[a_place - 1] = main_text[a_place - 1] + main_text[a_place] + main_text[a_place + 1]
                        del main_text[a_place + 1]
                        del main_text[a_place]
            for img in per_floor.xpath('.//div[@class="d_post_content j_d_post_content "]//img[@class="BDE_Image"]/@src'):
                print(img)
            final_text = ''
            for br in main_text:
                final_text += '\n' + br
            print(floor,author,final_text)

therad.get('https://tieba.baidu.com/p/1766018024')