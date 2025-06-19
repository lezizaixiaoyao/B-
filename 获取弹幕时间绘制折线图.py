#导入模块
import requests
from bs4 import BeautifulSoup
#url链接和请求头
url="https://comment.bilibili.com/30069294516.xml"
headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
         "Referer":"https://www.bilibili.com/video/BV1YmJizREst",
         "origin": "https://www.bilibili.com/",
        }
#获取响应
response=requests.get(url,headers=headers)
response.raise_for_status()  # 检查请求是否成功（状态码不是 200），会抛出异常
#设置响应内容的编码为自动检测的编码
response.encoding=response.apparent_encoding
#将响应内容转为字符串
xml=response.text
#添加解析器
soup=BeautifulSoup(xml,'lxml')
#寻找节点，查找所有<d>标签，这些标签包含弹幕信息（如果你是完全没接触过爬虫的朋友可以稍微了解一下web的组成）
content_all=soup.find_all(name='d')
#将节点内容组成列表：timeList是一个包含所有弹幕出现时间的列表，每个元素是一个浮点数，表示弹幕出现的时间
timeList=[]
for comment in content_all:
    #提取p属性的值，该值包含弹幕的时间等信息
    data=comment.attrs['p']
    #通过逗号分隔提取第一个元素作为弹幕出现的时间
    time=data.split(",")[0]
    timeList.append(float(time))
    #最后打印前 10 条弹幕的时间数据用来验证数据提取的逻辑是否正确
print(f"提取到的弹幕时间数据：{timeList[:10]}")
#新建一个字典，用于存储每个时间段的弹幕数量
subtitlesDict={}
#循环 25 次，每次计算一个 30 秒的时间段，格式为start-end
for x in range(25):
    # 将30*x+1赋值给变量start
    start=30*x+1
    # 将30*(x+1)赋值给变量end
    end=30*(x+1)
    # 格式化start和end
    # 用短横线相连，赋值给segment_range
    segment_range = f"{start}-{end}"
    # 将segment_range作为字典subtitlesDict的键,添加进字典中
    # 将字典中键所对应的值设置为0
    subtitlesDict[segment_range] = 0

# for循环遍历字典subtitlesDict所有的键
for subtitle in subtitlesDict.keys():

    # 使用split()分隔字典的键获取第一项，赋值给变量start_key
    start_key = subtitle.split("-")[0]

    # 使用split()分隔字典的键获取第二项，赋值给变量end_key
    end_key = subtitle.split("-")[1]
    # for循环遍历列表timeList，每次循环将一个弹幕时间赋值给变量 item
    for item in timeList:

        # 如果弹幕分布时间在整型start_key和整型end_key之间
        if int(start_key)<= item <= int(end_key):

            # 将字典中键所对应的值累加
            subtitlesDict[subtitle] = subtitlesDict[subtitle] + 1
#pyecharts 是一个用于生成 Echarts 图表的 Python 库，Echarts 是一个强大的 JavaScript 可视化库，Line 是 pyecharts 中的一个类，专门用于创建折线图。这里从 pyecharts.charts 模块中导入 Line 类，以便后续创建折线图对象
from pyecharts.charts import Line
# 使用Line()创建Line对象，赋值给line
line = Line()
# line.add_xaxis() 是 Line 对象的一个方法，用于向折线图中添加 X 轴数据
line.add_xaxis(list(subtitlesDict.keys()))

# add_yaxis() 是 Line 对象的一个方法，用于向折线图中添加 Y 轴数据系列，第一个参数 "弹幕数" 是这个数据系列的名称，会在折线图的图例中显示
# 第二个参数 list(subtitlesDict.values()) 是 Y 轴的数据，代表每个时间段对应的弹幕数量。
line.add_yaxis("弹幕数", list(subtitlesDict.values()))

# 使用render()函数存储文件，设置文件名为line.html
line.render("line.html")

# 使用print输出success
print("success")
