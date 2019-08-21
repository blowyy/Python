# coding=utf-8
'''
data : 2019-8-6
author : 不正经程序员
goal : 数据的可视化
'''

# 导入Style类，用于定义样式风格
from pyecharts import Style
# 导入Geo组件，用于生成地理坐标类图
from pyecharts import Geo
import json
# 导入Geo组件，用于生成柱状图
from pyecharts import Bar, Line, Overlap, Funnel
# 导入Counter类，用于统计值出现的次数
from collections import Counter
import pandas as pd

import fileinput,re

# # 设置全局主题风格
# from pyecharts import configure
# configure(global_theme='wonderland')

# 数据可视化

# 存放分值
scores = []
scores_luhan = []
# 存放性别
genders = []

dates = []

positive_text = ""
negative_text = ""

luhan_positive_text = ""
luhan_negative_text = ""

def is_float(str):
    try:
        float(str)
    except:
        return False
    else:
        return True

def render():
    global positive_text
    global negative_text
    global luhan_positive_text
    global luhan_negative_text
    # 获取评论中所有城市
    cities = []
    with open('shanghai.csv', mode='r', encoding='utf-8') as f:
        rows = f.readlines()
        for row in rows[1:]:
            if row.count(',') != 7:
                continue
            elements = row.split(',')
            time = elements[0]
            gender = elements[3]
            city = elements[4]
            comment = elements[7]
            score = elements[6]
            if not is_float(score):
                continue
            if '鹿晗' in comment:
                scores_luhan.append(float(score) * 2)
                if float(score) * 2 == 10:
                    luhan_positive_text += comment
                elif float(score) * 2 == 1:
                    luhan_negative_text += comment
            if city != '':  # 去掉城市名为空的值
                cities.append(city)
            if score != '':
                scores.append(float(score) * 2)
                if float(score) * 2 == 10:
                    positive_text += comment
                elif float(score) * 2 == 1:
                    negative_text += comment
            if gender != '':
                genders.append(gender)

            if time != '':
                dates.append(time)

    # print(positive_text)
    # print(negative_text)

    with open("positive_text.txt","w", encoding='utf-8') as f:
        f.write(positive_text)
    
    with open("negative_text.txt","w", encoding='utf-8') as f:
        f.write(negative_text)
    
    with open("luhan_positive_text.txt","w", encoding='utf-8') as f:
        f.write(luhan_positive_text)
    
    with open("luhan_negative_text.txt","w", encoding='utf-8') as f:
        f.write(luhan_negative_text)

    # 对城市数据和坐标文件中的地名进行处理
    handle(cities)

    data = Counter(cities).most_common()  # 使用Counter类统计出现的次数，并转换为元组列表
    score_data = Counter(scores).most_common()  # 使用Counter类统计出现的次数，并转换为元组列表
    # 按0-10进行排序
    score_data = sorted(score_data)
    
    score_data_luhan = Counter(scores_luhan).most_common()  # 使用Counter类统计出现的次数，并转换为元组列表
    # 按0-10进行排序
    score_data_luhan = sorted(score_data_luhan)

    gender_data = Counter(genders).most_common()  # 使用Counter类统计出现的次数，并转换为元组列表
    print(gender_data)
    
    date_data = Counter(dates).most_common()
    # 按日期进行排序
    date_data = sorted(date_data)
    # print(data)
    # 定义样式
    style = Style(
        title_color='#fff',
        title_pos='center',
        width=800,
        height=600,
        background_color='#404a59'
    )

    # 根据城市数据生成地理坐标图
    geo = Geo('观众地理分布', '数据来源：不正经程序员-采集自猫眼', **style.init_style)
    attr, value = geo.cast(data)
    geo.add('', attr, value, visual_range=[0, 600],
            visual_text_color='#fff', symbol_size=7,
            is_visualmap=True, is_piecewise=True, visual_split_number=10)
    geo.render(
        'picture\观众地理分布-地理坐标图.html')

    # 根据城市数据生成柱状图
    data_top20 = Counter(cities).most_common(20)  # 返回出现次数最多的20条
    bar = Bar('观众来源排行TOP20', '数据来源：不正经程序员-采集自猫眼',
              title_pos='center', width=1200, height=600)
    attr, value = bar.cast(data_top20)
    bar.add('', attr, value, is_visualmap=False, visual_range=[0, 3500], visual_text_color='#fff', is_more_utils=True,
            is_label_show=True)
    bar.render('picture\观众来源排行-柱状图.html')

    # 根据评分数据生成柱状图
    bar = Bar('各段评分数量', '数据来源：不正经程序员-采集自猫眼',
              title_pos='center', width=900, height=600)
    attr, value = bar.cast(score_data)
    # line = Line()
    # line.add('', attr, value)
    bar.add('', attr, value, is_visualmap=True, visual_range=[0, 3500], visual_text_color='#fff', is_more_utils=True,
            is_label_show=True)
    overlap = Overlap()
    overlap.add(bar)
    # overlap.add(line)
    overlap.show_config()
    overlap.render(
        'picture\评分数量-柱状图.html')

    # 根据评分数据生成柱状图
    bar = Bar('评论带有鹿晗的各段评分数量', '数据来源：不正经程序员-采集自猫眼',
              title_pos='center', width=900, height=600)
    attr, value = bar.cast(score_data_luhan)
    # line = Line()
    # line.add('', attr, value)
    bar.add('', attr, value, is_visualmap=True, visual_range=[0, 3500], visual_text_color='#fff', is_more_utils=True,
            is_label_show=True)
    overlap = Overlap()
    overlap.add(bar)
    # overlap.add(line)
    overlap.show_config()
    overlap.render(
        'picture\评论带有鹿晗的各段评分数量-柱状图.html')

    # 根据评分数据生成柱状图
    bar = Bar('评价人数走势图', '数据来源：不正经程序员-采集自猫眼',
              title_pos='center', width=1200, height=600)
    attr, value = bar.cast(date_data)
    # line = Line()
    # line.add('', attr, value)
    bar.add('', attr, value, is_visualmap=True,  xaxis_rotate=30,visual_range=[0, 3500], visual_text_color='#fff', is_more_utils=True,
            is_label_show=True)
    overlap = Overlap()
    overlap.add(bar)
    # overlap.add(line)
    overlap.show_config()
    overlap.render(
        'picture\评价人数走势图.html')

    from pyecharts import Pie
    # 设置主标题与副标题，标题设置居中，设置宽度为900
    pie = Pie("观众性别分布图", "数据来源：不正经程序员-采集自猫眼",title_pos='center',width=900)
    attr, value = geo.cast(gender_data)
    # 加入数据，设置坐标位置为【25，50】，上方的colums选项取消显示
    pie.add("", ["其他","男","女"], value ,visual_range=[0, 3500],is_legend_show=False, is_label_show=True)

    # 保存图表
    pie.render('picture\观众性别分布图.html')

# 处理地名数据，解决坐标文件中找不到地名的问题
def handle(cities):
    # print(len(cities), len(set(cities)))

    # 获取坐标文件中所有地名
    data = None
    with open(
            'D:\programs\Python37\Lib\site-packages\pyecharts\datasets\city_coordinates.json',
            mode='r', encoding='utf-8') as f:
        data = json.loads(f.read())  # 将str转换为json

    # 循环判断处理
    data_new = data.copy()  # 拷贝所有地名数据
    for city in set(cities):  # 使用set去重
        # 处理地名为空的数据
        if city == '':
            while city in cities:
                cities.remove(city)
        count = 0
        for k in data.keys():
            count += 1
            if k == city:
                break
            if k.startswith(city):  # 处理简写的地名，如 达州市 简写为 达州
                # print(k, city)
                data_new[city] = data[k]
                break
            if k.startswith(city[0:-1]) and len(city) >= 3:  # 处理行政变更的地名，如县改区 或 县改市等
                data_new[city] = data[k]
                break
        # 处理不存在的地名
        if count == len(data):
            while city in cities:
                cities.remove(city)

    # print(len(data), len(data_new))

    # 写入覆盖坐标文件
    with open(
            'D:\programs\Python37\Lib\site-packages\pyecharts\datasets\city_coordinates.json',
            mode='w', encoding='utf-8') as f:
        f.write(json.dumps(data_new, ensure_ascii=False))  # 将json转换为str

def view_piaofang():
    attr = []
    piaofang_data = []
    paipianbi_data = []
    shangzuolv_data = []


    with open('piaofang.csv', 'r') as f:
        rows = f.readlines()
        for row in rows[1:]:
            if row.count(',') != 3:
                continue
            elements = row.split(',')
            attr.append(elements[0])
            piaofang_data.append(elements[1])
            paipianbi_data.append(elements[2])
            shangzuolv_data.append(elements[3])
    # 根据评分数据生成柱状图
    bar = Bar('票房走势图', '数据来源：不正经程序员-采集自猫眼',
    title_pos='center', width=1200, height=600)
    # line = Line()
    # line.add('', attr, value)
    bar.add('', attr, piaofang_data, is_visualmap=True, visual_range=[0, 3500], visual_text_color='#fff', is_more_utils=True,
    is_label_show=True, mark_line=["average"], is_fill = True,is_smooth=True, xaxis_name = '上映日期', yaxis_name = '当日票房（万）'
    ,yaxis_name_pos = 'end')
    bar.render('picture\票房走势图.html')

    # print(paipianbi_data)
    # 根据评分数据生成柱状图
    line = Line('拍片比-上座率走势图', '数据来源：不正经程序员-采集自猫眼',
    title_pos='center', width=1200, height=600)
    # line = Line()
    # line.add('', attr, value)
    line.add('拍片比', attr, paipianbi_data, is_more_utils=True,is_fill=True,legend_pos = 'right',legend_top = 320,
    is_label_show=True, mark_line=["average"])
    line.add('上座率', attr, shangzuolv_data, is_more_utils=True,legend_pos = 'right', mark_line=["average"],
    is_label_show=True, is_smooth=True, xaxis_name = '上映日期', is_fill=True, yaxis_name = '百分比（%）' ,yaxis_name_pos = 'end')
    line.render('picture\拍片比-上座率走势图.html')

def avg():
    df = pd.read_csv('final_out.csv', error_bad_lines=False)
    df.round(2)
    # 根据日期统计各天的平均值，并保留两位小数
    date_score_avg = df.groupby('date')['score'].mean().round(2)*2
    # 根据评分数据生成柱状图

    bar = Line('评分走势图', '数据来源：不正经程序员-采集自猫眼',
              title_pos='center', width=1500, height=600)
    # line = Line()
    # line.add('', attr, value)
    bar.add('', date_score_avg.index, date_score_avg.values, is_visualmap=True, visual_range=[0, 3500], visual_text_color='#fff', is_more_utils=True,
            is_label_show=True, xaxis_interval=0, xaxis_rotate=30, mark_line=["average"])
    overlap = Overlap()
    overlap.add(bar)
    # overlap.add(line)
    overlap.show_config()
    overlap.render(
        'picture\评分走势图.html')
        
    # 根据日期统计各天的平均值，并保留两位小数
    date_positive_prob_avg = df.groupby('date')['positive_prob'].mean().round(2)
    bar = Bar('评论情感指数走势图', '数据来源：不正经程序员-采集自猫眼',
              title_pos='center', width=1500, height=600)
    # line = Line()
    # line.add('', attr, value)
    bar.add('', date_positive_prob_avg.index, date_positive_prob_avg.values, is_visualmap=False, visual_range=[0, 3500], visual_text_color='#fff', is_more_utils=True,
            is_label_show=True, xaxis_interval=0, xaxis_rotate=30, mark_line=["average"])
    overlap = Overlap()
    overlap.add(bar)
    # overlap.add(line)
    overlap.show_config()
    overlap.render(
        'picture\评论情感指数走势图.html')

def word_cloud():
    import jieba
    import numpy
    from PIL import Image
    from wordcloud import WordCloud
    stopwords = [line.strip() for line in open('static\stopwords.txt', 'r', encoding='utf-8').readlines()] 
    # jieba 分词
    f = open('luhan_positive_text.txt', encoding='utf-8').read()

    wordlist = jieba.cut(f, cut_all=True)
    wl_space_split = " ".join(wordlist)

    my_wordcloud = WordCloud(
        background_color='white',   #背景设置为白色
        font_path='static\simkai.ttf',             #字体
        max_words=2000,              #最大显示的关键词数量
        # stopwords=STOPWORDS,        #使用上面导入停用词表
        max_font_size=250,          #最大字体
        random_state=30,            #设置随机状态数，及配色的方案数
        height=660,                 #如果使用默认图片，则可以设置高
        margin=2,                   #图片属性
        width=1000,                 #设置宽
        stopwords=stopwords,
        collocations=False,         #是否包括两个词的搭配
        # mask=alice_coloring       #如果使用自定义图片，则导入上面我们读入的numpy类型数据
    ).generate(wl_space_split)

    my_wordcloud.to_file('picture\\luhan_positive_text.png')
    
    # jieba 分词
    f = open('luhan_negative_text.txt', encoding='utf-8').read()
    wordlist = jieba.cut(f, cut_all=True)
    wl_space_split = " ".join(wordlist)

    # width,height,margin 可以设置图片属性
    # generate 可以对全部文本进行自动分词，但是他对中文支持不好，所以这里我们使用 jieba 先进行了分词
    # 通过 font_path 参数来设置字体集
    # 通过 mask 参数 来设置词云形状
    my_wordcloud = WordCloud(
        background_color='black',   #背景设置为白色
        font_path='static\simkai.ttf',             #字体
        max_words=2000,              #最大显示的关键词数量
        # stopwords=STOPWORDS,        #使用上面导入停用词表
        max_font_size=250,          #最大字体
        random_state=30,            #设置随机状态数，及配色的方案数
        height=660,                 #如果使用默认图片，则可以设置高
        margin=2,                   #图片属性
        width=1000,                 #设置宽
        stopwords=stopwords,
        collocations=False,         #是否包括两个词的搭配
        # mask=alice_coloring       #如果使用自定义图片，则导入上面我们读入的numpy类型数据
    ).generate(wl_space_split)
    my_wordcloud.to_file('picture\\luhan_negative_text.png')

render()
avg()
# word_cloud()
view_piaofang()
