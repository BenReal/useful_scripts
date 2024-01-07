import codecs
import csv
import re
import pandas as pd
import requests
import time
import copy

# 处理目录页面 + 爬虫

class SatSpider:
    # 爬虫类
    def __init__(self, df, savefile, patterns):
        self.headers = {"User-Agent":"Chrome/27.0.1453.116"}
        self.df = df
        self.savefile = savefile
        self.patterns = patterns

    def getParsePage(self):
        # 爬取页面， 并进行解析和保存
        df_new = self.df
        row = ['Nation','Type / Application','Operator','Contractors','Equipment','Configuration','Propulsion','Power','Lifetime','Mass','Orbit']
        for i in row:
            df_new[i] = None
        k = 0
        for i in range(len(self.df)):            
            # print(df_new.iloc[i,6])
            df_new.iloc[i,6] = str(df_new.iloc[i,6]).strip()
            k += 1
            print(k)
            # if k > 5:
            #     break
            link = df_new.iloc[i,1]
            # print(link)
            if link and type(link) == str:
                res = requests.get(link, headers=self.headers)
                res.encoding = "utf-8"
                html = res.text
                # print(html)
                for j in range(len(row)):
                    try:
                        t = re.findall(self.patterns[j], html)[0]
                        m = re.findall('">[\s\S]*?</td>',t)[0]
                        m = m[2:-5]
                    except:
                        m = 'fail_to_get'
                        print(link,self.patterns[j])
                    # print(m)
                    df_new.iloc[i,j+8] = m
                time.sleep(1)

        df_new.to_excel(self.savefile)


if __name__ == '__main__':
    infile = '2019.html'
    sat_list_file = '2019_new.xlsx'
    outfile = 'sat2019_new.xlsx'
    patterns = ['<td class="rcont" id="sdnat">[\s\S]*?</td>',
    '<td class="rcont" id="sdtyp">[\s\S]*?</td>',
    '<td class="rcont" id="sdope">[\s\S]*?</td>',
    '<td class="rcont" id="sdcon">[\s\S]*?</td>',
    '<td class="rcont" id="sdequ">[\s\S]*?</td>',
    '<td class="rcont" id="sdcnf">[\s\S]*?</td>',
    '<td class="rcont" id="sdpro">[\s\S]*?</td>',
    '<td class="rcont" id="sdpow">[\s\S]*?</td>',
    '<td class="rcont" id="sdlif">[\s\S]*?</td>',
    '<td class="rcont" id="sdmas">[\s\S]*?</td>',
    '<td class="rcont" id="sdorb">[\s\S]*?</td>']
    columns1 = ['Payload','url_payload','ID','Date','Launch Vehicle','url_launchveicles','Site','Remark']
    # columns2 = ['Nation','Type / Application','Operator','Contractors','Equipment','Configuration','Propulsion','Power','Lifetime','Mass','Orbit']

    # 处理卫星列表数据，并组成 dataframe 数据结构
    with codecs.open(infile, 'r', encoding='utf8', errors="ignore") as fin:
        lines = fin.readlines()
        alltext = ''.join(lines)
        trs = re.findall(r'<tr[\s\S]*?</tr>', alltext)
        sat_list = []
        for tr in trs:
            temp = []
            tds = re.findall(r'<td[\s\S]*?</td>', tr)
            tds = [td[4:-5].strip() for td in tds]
            if len(tds) > 5:
                urls = tds[2].split('br>')
                urls = [url.strip() for url in urls]
                for ele in urls:
                    temp.append([ele,'NA'] + tds[:2] + [tds[3]] + ['NA'] + tds[4:])
            sat_list.extend(temp)

        for i in sat_list:
            if '<a href' in i[0]:
                url1 = re.findall('https://.*?"',i[0])[0][:-1]
                i[1] = url1
                name1 = re.findall('">.*?<',i[0])[0][2:-1] 
                i[0] = name1
                print(url1)
            else:
                i[1] = ''
            tmp = copy.copy(i[3].split('.'))
            tmp.reverse()
            i[3] = '-'.join(tmp)
            if '<a href' in i[4]:
                url2 = re.findall('https://.*?"',i[4])[0][:-1]
                i[5] = url2
                name2 = re.findall('">.*?<',i[4])[0][2:-1] 
                i[4] = name2
                print(url2) 
            else:
                i[5] = ''


        df = pd.DataFrame(sat_list, columns = columns1)
        df.to_excel(sat_list_file)
        print(df) 
    

    # for i in df['url']:
    #     print(type(i))
    # 爬虫
    spider = SatSpider(df, outfile, patterns)
    spider.getParsePage()

