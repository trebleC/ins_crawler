# -*- coding: utf-8 -*-
from lxml import etree
import json
import requests
import time
from pymongo import MongoClient

user_name = 'everyone.is.storyteller'

query_hash=''

headers = { 
            "cookie": "",
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
            "Connection": "keep-alive",
            "Host": "www.instagram.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, sdch, br",
            "accept-language": "zh-CN,zh;q=0.8",
            "X-Instragram-AJAX": "1",
            "X-Requested-With": "XMLHttpRequest",
            "Upgrade-Insecure-Requests": "1",
            }

BASE_URL = 'https://www.instagram.com/'+user_name+'/'
uri = 'https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{cursor}%22%7D'
proxy = {
    'http': 'http://127.0.0.1:1080',
    'https': 'http://127.0.0.1:1080'
}


#存入数据库
def save_mongo(dict):
    conn = MongoClient('localhost', 27017) #地址,端口号
    db = conn.spider    #数据库
    my_set = db.other   #集合
    try:
        my_set.insert(dict)
        print('******************insert database success!*************************')
    except:
        print('###################insert database fail!!#######################')



#获取html
def get_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print('请求网页源代码错误, 错误状态码:', response.status_code)
    except Exception as e:
        print(e)
        return None









def crawler():
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False

        res = requests.get(BASE_URL,headers = headers) 
        html = etree.HTML(res.content.decode()) #获取html
        
        all_js_tags = html.xpath('//script[@type="text/javascript"]/text()') 
        
        
        for js_tag in all_js_tags:
            
            if js_tag.strip().startswith('window._sharedData'): #找到目的script
               
                urls = []
                
                #print('.===========...................................................................................................................................................')
                
                data = js_tag[:-1].split('= {')[1] #去掉window._sharedData
                
                js_data = json.loads('{' + data, encoding='utf-8') #json转字典
                
                
                #用户id
                user_id = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["id"]

                #帖子总数
                page_count = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"][
                     "count"]
                page_count = int((page_count-12 + 12 -1)/12) #计算帖子组数 UP(A/B) = int((A+B-1)/B)
               #贴文内容位置
                edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"][
                     "edges"]
                total_dict = get_data(edges)
                save_mongo(total_dict)
                     
                #刷新标签
                page_info = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]['page_info']

            

                cursor = page_info['end_cursor'] #帖子末尾符号
                flag = page_info['has_next_page'] #data中判断需要异步刷新

                print('.............................................................................\n')
                #print(cursor, flag)
                count=0
                
                while flag:
                    count+=1
                    #url = 'https://www.instagram.com/graphql/query/?query_hash=f2405b236d85e8296cf30347c9f08c2a&variables=%7B%22id%22%3A%224851295731%22%2C%22first%22%3A12%2C%22after%22%3A%22QVFDZ1dseExrVUk2ZHlKNGtYRnRkVUh4OFhiVW9GWjY2U19QNTJqVlU4TlJFdXpmMm5PbDVWaF9LT2M2aUk5eGtwVUJ5b1Y0UWtNNURSZU85Vmw1N2c1dQ%3D%3D%22%7D'
                    url = uri.format(query_hash=query_hash,user_id=user_id,cursor=cursor)
                    response = requests.get(url, headers=headers,timeout=10)
                    print(response.status_code)
                    js_data = response.json()
                    infos = js_data['data']['user']['edge_owner_to_timeline_media']['edges']
                    cursor = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
                    flag = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
                    total_dict = get_data(infos)
                    time.sleep(1)
                    save_mongo(total_dict)  
                    
                    if count==page_count:
                        break
        
                
                #print(cursor, flag)
                
                
                
                # print(new_imgs_url[0])
                # print(new_content[0])
                # print(new_shortcode[0])
                # print(new_counts_comment[0])
                # print(new_counts_like[0])
                # print(new_thumbnail_url[0])


    except Exception as e:
        print("有异常！！！")
        raise e

#获得贴文数据
def get_data(edges):
    total_dict = []
                
    for index,edge in enumerate(edges):
        dict = {}
        dict['time_stamp'] = stamp2date(int(edge["node"]["taken_at_timestamp"])) #时间戳
        dict['imgs_url'] = edge["node"]["display_url"] #图片地址
        try:
            dict['content'] = edge["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"] #正文内容
        except:
            dict['content']=''
        dict['shortcode'] = edge["node"]["shortcode"] #shortcode
        dict['counts_comment'] = edge["node"]["edge_media_to_comment"]["count"] #评论数
        dict['counts_like'] = edge["node"]["edge_media_preview_like"]["count"] #点赞数
        dict['thumbnail_url'] = edge["node"]["thumbnail_resources"][-1]["src"] #缩略图地址
        total_dict.append(dict)
        
    
    print(dict['time_stamp'])
    return total_dict





#时间戳转换为指定格式的日期
def stamp2date(timeStamp):
    # 使用time
    
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
    return otherStyleTime   # 2013--10--10 23:40:00






if __name__ == '__main__':
    crawler()