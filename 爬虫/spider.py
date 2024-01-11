import csv
import os
import random
import re
import pandas as pd
import pymysql
import requests
from parsel import Selector
from sqlalchemy import create_engine, text

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/豆瓣')


class Spider:
    def __init__(self):
        self.spiderUrl = 'https://m.douban.com/rexxar/api/v2/movie/recommend'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.57',
            'Referer': 'https: // movie.douban.com / explore'

        }
        self.page = 0

    def init(self):
        if not os.path.exists('./tempDate.csv'):
            with open('./tempDate.csv', 'w', newline='', encoding='utf-8') as writer_f:
                writer = csv.writer(writer_f)
                writer.writerow(
                    ['电影导演', '电影评分', '电影名字', '电影演员', '电影封面', '电影详细链接', '电影类型',
                     '电影制片国家', '语言', '电影上映时间', '电影片长', '短评个数', '星级', '电影简介',
                     '电影短评(短评用户, 短评评分,短评时间)', '图片列表', '预告片链接'])

        # try:
        #     conn = pymysql.connect(host='localhost', user='root', password='123456', db='豆瓣')
        #     cursor = conn.cursor()
        #     sql = '''CREATE TABLE movies (
        #                 id INT PRIMARY KEY AUTO_INCREMENT,
        #                 电影导演                                text   null,
        #                 电影评分                                text null,
        #                 电影名字                                text   null,
        #                 电影演员                                text   null,
        #                 电影封面                                text   null,
        #                 电影详细链接                            text   null,
        #                 电影类型                                text   null,
        #                 电影制片国家                            text   null,
        #                 语言                                    text   null,
        #                 电影上映时间                            text   null,
        #                 电影片长                                text   null,
        #                 短评个数                                text null,
        #                 星级                                    text   null,
        #                 电影简介                                text   null,
        #                 `电影短评(短评用户, 短评评分,短评时间)` text   null,
        #                 图片列表                                text   null,
        #                 预告片链接                              text   null
        #             )'''
        #     cursor.execute(sql)
        # except:
        #     pass
        if not os.path.exists('./spiderPage.txt'):
            with open('spiderPage.txt', 'w', encoding='utf-8') as f:
                f.write('0\n')

    def get_page(self):
        with open('spiderPage.txt', 'r', encoding='utf-8') as r_f:
            return r_f.readlines()[-1].strip()

    def set_page(self, new_page):
        with open('spiderPage.txt', 'a', encoding='utf-8') as w_f:
            w_f.write(str(new_page) + '\n')

    def spiderMain(self):
        page = self.get_page()
        tags = ['喜剧', '爱情', '动作', '科幻', '动画', '悬疑', '犯罪', '惊悚', '冒险', '历史', '奇幻', '恐怖', '战争',
                '传记',
                '歌舞', '武侠', '情色', '灾难', '西部', '纪录片', '短片']
        for tag in tags:
            print(tag)
            params = {
                'start': int(page) * 20,
                'count': 10,
                'tags': tag

            }
            respJson = requests.get(self.spiderUrl, params=params, headers=self.headers).json()
            a = 1
            respJson = respJson['items']
            resultList = []
            for index, item in enumerate(respJson):
                try:

                    movieData = []
                    # 电影小标题
                    # if 'card_subtitle' in item:
                    #     movie_card_subtitle = item['card_subtitle']
                    #     movie_card_subtitle = {'电影小标题': movie_card_subtitle}
                    #     movieData.append(movie_card_subtitle)
                    # 判断是否为电影列表
                    # print(type(item['card']))
                    if 'card' in item and item['card'] == 'subject':
                        print('正在爬取第{}页,第{}条'.format(int(page) + 1, a))
                        a += 1
                        # 电影名字
                        if 'title' in item:
                            movie_title = item['title']
                            movie_title = {'电影名字': movie_title}
                            print(movie_title)
                            movieData.append(movie_title)

                            # 电影评分
                        if 'rating' in item and 'value' in item['rating']:
                            movie_rating = item['rating']['value']
                            movie_rating = {'电影评分': movie_rating}

                            movieData.append(movie_rating)

                            # 电影封面
                        if 'photos' in item and len(item['photos']) > 0:
                            movie_photos = item['pic']['large']
                            movie_photos = {'电影封面': movie_photos}

                            movieData.append(movie_photos)

                            # 电影的详情链接
                        if 'id' in item:
                            url = 'https://movie.douban.com/subject/' + item['id']
                            movie_url = {'电影详情链接': url}

                            movieData.append(movie_url)

                        movieTail = requests.get(url, headers=self.headers).text
                        select = Selector(movieTail)
                        main = select.xpath('//*[@id="info"]')
                        # 导演
                        movie_director = main.xpath('//*[@rel="v:directedBy"][1]//text()').get()
                        movie_director = {'电影导演': movie_director}
                        movieData.append(movie_director)
                        # 演员
                        movie_actors = main.xpath('//*[@class="actor"]//a/text()').getall()

                        movie_actors = {'电影演员': ','.join(movie_actors)}
                        movieData.append(movie_actors)
                        # 电影类型
                        movie_type = main.xpath('//*[@property="v:genre"]//text()').getall()
                        movie_type = {'电影类型': ','.join(movie_type)}
                        movieData.append(movie_type)
                        # 电影上映时间
                        movie_release_time = main.xpath('//*[@property="v:initialReleaseDate"]/text()').getall()
                        movie_release_time = {'电影上映时间': ''.join(movie_release_time)}
                        movieData.append(movie_release_time)
                        # 电影制片国家
                        movie_country = main.xpath('text()').getall()
                        texts = []
                        for text in movie_country:
                            if text.strip() != '' and text.strip() != "/":
                                texts.append(text.strip())
                        movie_country = texts[0].split(' / ')
                        movie_country = {'电影制片国家': ','.join(movie_country)}
                        movieData.append(movie_country)
                        # 电影语言
                        movie_language = texts[1].split(' / ')
                        movie_language = {'电影语言': ','.join(movie_language)}
                        movieData.append(movie_language)
                        # 电影片长
                        movie_length = main.xpath('//*[@property="v:runtime"]/text()').get()
                        movie_length = {'电影片长': movie_length}
                        movieData.append(movie_length)
                        # 短评个数
                        movie_comment_num = select.xpath(
                            '//*[@id="comments-section"]/div[1]//span[@class="pl"]/a/text()').get()[
                                            3:-2]
                        movie_comment_num = {'短评个数': movie_comment_num}
                        movieData.append(movie_comment_num)
                        # 电影星级占比
                        movie_stars = select.xpath(
                            '//*[@id="interest_sectl"]//*[@class="rating_per"][1]/text()').getall()
                        movie_stars = [i.strip() for i in movie_stars]
                        movie_stars = {'电影星级占比': ''.join(movie_stars)}
                        movieData.append(movie_stars)
                        # 电影简介
                        movie_summary = select.xpath(
                            '//*[@id="link-report-intra"]/span[@property="v:summary"]/text()').getall()
                        summary = []
                        for i in movie_summary:
                            if i.strip():
                                summary.append(i.strip())
                        movie_summary = ''.join(summary)
                        movie_summary = {'电影简介': movie_summary}
                        movieData.append(movie_summary)

                        # 电影短评
                        movie_comments = []
                        comments = select.xpath('//*[@id="hot-comments"]//*[@class="short"]/text()').getall()
                        users = select.xpath('//*[@id="hot-comments"]//*[@class="comment-info"]/a/text()').getall()
                        try:
                            stars = select.xpath('//*[@class="comment-info"]/span[2]/@class').getall()
                        except:
                            stars = ['暂无']
                        times = select.xpath('//*[@class="comment-time "]/text()').getall()
                        for comment, user, star, time in zip(comments, users, stars, times):
                            movie_comments.append({
                                '短评内容': comment,
                                '短评用户': user,

                                '短评时间': time.strip()
                            })
                        movie_comments = {'电影短评': movie_comments}
                        movieData.append(movie_comments)
                        # 图片列表
                        movie_images = select.xpath('//a[@class="related-pic-video"]/@style').getall()
                        # 从style属性中提取背景图像URL
                        movie_image_url = movie_images[0].split('url(')[1].split(')')[0]
                        movie_images = {'图片列表': movie_image_url}
                        movieData.append(movie_images)
                        # 预告片链接
                        try:
                            movie_trailer = select.xpath(
                                '//ul[@class="related-pic-bd  "]/li[@class="label-trailer"]/a/@href').getall()
                            trailer = requests.get(movie_trailer[0], headers=self.headers).text
                            movie_trailer = Selector(text=trailer).xpath('//source/@src').get()
                            movie_trailer = {'预告片链接': movie_trailer}
                        except:
                            movie_trailer = {'预告片链接': '暂无'}
                        movieData.append(movie_trailer)
                        # 导演 movie_director 演员 movie_actors 类型 movie_type 上映时间 movie_release_time 制片国家 movie_country
                        # 语言 movie_language 片长 movie_length 短评个数 movie_comments_num 星级占比
                        # 电影简介 movie_summary 电影图片 movie_images 预告片 movie_trailer 电影评论 movie_comments
                        DateList = [movieData[4]['电影导演'], movieData[1]['电影评分'], movieData[0]['电影名字'],
                                    movieData[5]['电影演员'],
                                    movieData[2]['电影封面'], movieData[3]['电影详情链接'], movieData[6]['电影类型'],
                                    movieData[8]['电影制片国家'], movieData[9]['电影语言'],
                                    movieData[7]['电影上映时间'],
                                    movieData[10]['电影片长'], movieData[11]['短评个数'], movieData[12]['电影星级占比'],
                                    movieData[13]['电影简介'],
                                    movieData[14]['电影短评'], movieData[15]['图片列表'], movieData[16]['预告片链接']]
                        resultList.append(DateList)


                except:
                    print("出现问题")
            self.save_to_csv(resultList)
            self.clear_csv()
        self.set_page(int(page) + 1)
        self.spiderMain()

    def save_to_csv(self, resultList):
        # 中文注释
        with open('tempDate.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for rowDate in resultList:
                writer.writerow(rowDate)

    def clear_csv(self):
        df = pd.read_csv('tempDate.csv', encoding='utf-8')
        df.fillna("暂无", inplace=True)
        df.drop_duplicates(subset=["电影名字"], inplace=True)  # 删除重复行，基于"电影名字"列
        df.to_csv('tempDate.csv', index=False)  # 将清理过的数据保存回原始的CSV文件
        self.save_to_sql(df)

    def save_to_sql(self, df):
        pd.read_csv('tempDate.csv', encoding='utf-8')
        df.to_sql('movies', con=engine, if_exists='replace', index=False)
        # self.clear_sql_duplicates()


if __name__ == '__main__':
    SpiderObj = Spider()
    SpiderObj.init()
    SpiderObj.spiderMain()
