import re
from collections import Counter
from 项目.App.utils.utils import *

"""
获取首页数据
    电影个数
    豆瓣最高评分
    出场最多的演员
    制片国家最多数
    电影种类个数
    电影语言最多数
"""


def getHomeData():
    # 1.电影个数
    maxMovieLen = len(df)
    # 2.评分最高
    maxRate = df['电影评分'].max()
    # 3.出场最多演员
    actorsList = typeList('电影演员')
    # 只能查一个,如果多个同样多的值只会取第一个
    # maxActor = max(actorsList, key=actorsList.count)
    maxActors = Counter(actorsList)

    if maxActors.most_common()[0][0] == '暂无':
        # get the second most common actor if it's '暂无'
        maxActors = maxActors.most_common(2)[1]
    else:
        # get the first most common actor if it's not '暂无'
        maxActors = maxActors.most_common(1)[0]
    strActors = maxActors[0]
    strActorsNumber = str(maxActors[1])
    # 4.制片国家最多数
    countryList = typeList('电影制片国家')
    maxCountry = Counter(countryList).most_common(1)
    strCountry = maxCountry[0][0] + ':' + str(maxCountry[0][1])
    # 5.电影种类最多
    movieTypeList = typeList('电影类型')
    maxType = Counter(movieTypeList).most_common(1)
    # strType = maxType[0][0] + ':' + str(maxType[0][1])
    maxTypeLen = len(Counter(movieTypeList))

    # 6.电影语言最多数
    languageList = typeList('语言')
    maxLanguage = Counter(languageList).most_common(1)
    strLanguage = maxLanguage[0][0] + ':' + str(maxLanguage[0][1])
    return maxMovieLen, maxRate, strActors, strActorsNumber, strCountry, maxTypeLen, strLanguage


"""
获取echarts需要的数据
电影种类饼状图
"""


def getTypesEcharDate():
    movieTypeList = typeList('电影类型')
    movieTypeDict = dict(Counter(movieTypeList))
    movieType = []
    for index, value in movieTypeDict.items():
        movieType.append({'name': index, 'value': value})
    return movieType


"""
获取echarts需要的数据
电影评分折线图
"""


def getRatesEcharDate():
    movieRatesList = typeList('电影评分')
    movieRatesDict = dict(Counter(movieRatesList).most_common())
    sorted_counter = sorted(movieRatesDict.items(), key=lambda x: float(x[0]))
    keys = [str(item[0]) for item in sorted_counter]
    values = [item[1] for item in sorted_counter]
    return keys, values


"""
电影详情信息
"""
def getTableData():
    TableDatas = []
    for TableData in df.values:
        TableData[3] = ','.join(TableData[3].split(',')[0:5])
        TableDatas.append(TableData)
    return TableDatas


def getTime():
    Datas = df.values
    times = []
    for data in Datas:
        time = data[9][0:4]
        times.append(time)
    counter_time = Counter(times).most_common()
    sort_time = sorted(counter_time, key=lambda x: int(x[0]))
    x = [x[0] for x in sort_time]
    y = [y[1] for y in sort_time]
    return x, y


"""
电影时长
"""
def getLength():
    Datas = df.values
    lengths = []
    for data in Datas:
        length = data[10]
        numbers = re.findall(r'\d+', length)
        for i in numbers:
            lengths.append(int(i))
    movie_length = []
    a = 0
    b = 0
    c = 0
    d = 0
    for length in lengths:
        if length < 60:
            a += 1
        elif length > 60 and length < 90:
            b += 1
        elif length > 90 and length < 120:
            c += 1
        else:
            d += 1

    movie_length.append({'value': a, 'name': '<60分钟'})
    movie_length.append({'value': b, 'name': '60-90分钟'})
    movie_length.append({'value': c, 'name': '90-120分钟'})
    movie_length.append({'value': d, 'name': '>120分钟'})
    return movie_length


"""
搜索页面默认为第一个
"""
def searchMovie():
    searchMovies = []
    searchMovies.append(df.values[0])
    return searchMovies


"""

"""
def searchMovieByWord(searchWord):
    searchMovies = []
    for i in df.values:
        if i[2].find(searchWord) != -1:
            searchMovies.append(i)
    return searchMovies


def getmovieType():
    movieTypeList = list(set(typeList('电影类型')))
    return movieTypeList


def searchMovieByType(searchType):
    searchMovies = []
    for i in df.values:
        if i[6].find(searchType) != -1:
            searchMovies.append(list(i))
    rate_movies = []
    for i in searchMovies:
        rate_movies.append(i[1])
    rate = Counter(rate_movies).most_common()
    sort_rate = sorted(rate, key=lambda x: float(x[0]))
    x = [x[0] for x in sort_rate]
    y = [y[1] for y in sort_rate]
    return x, y


def getRateLevel(searchWord):
    name = searchMovieByWord(searchWord)[0][2]
    RateLevel = searchMovieByWord(searchWord)[0][12].split('%')[0:5]
    RateLevel = [float(i) for i in RateLevel]
    RateLevels = [
        {'value': RateLevel[0], 'name': '5星'},
        {'value': RateLevel[1], 'name': '4星'},
        {'value': RateLevel[2], 'name': '3星'},
        {'value': RateLevel[3], 'name': '2星'},
        {'value': RateLevel[4], 'name': '1星'}
    ]
    print(name)
    return name, RateLevels


def getYearRate():
    Data = df.values
    years = set(df['电影上映时间'].values)
    list_year = []
    x = []
    y = []
    for year in years:
        list_year.append(int(year[0:4]))
    list_year = sorted(list(set(list_year)))
    for i in list_year:
        averRate = df[df['电影上映时间'].str.contains(str(i))]['电影评分'].mean()
        year = i
        x.append(year)
        y.append(averRate)

    return x, y


if __name__ == '__main__':
    # getHomeData()
    # getTypesEcharDate()
    # getRatesEcharDate()
    # getTableData()
    getTime()
    # getLength()
    # getRateLevel('长津湖')
    # getYearRate()
