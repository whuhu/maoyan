import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl

txt = open(r'maoyan.txt','r',encoding='utf-8')
data = []
#读取txt
for line in txt.readlines():
    line = line.replace('\n','')
    data.append(eval(line))

pairs = []
#将字符串转化为字典形式
for item in data:
    movie = item['title']
    strlist = item['actor'].split(',')
    for i in strlist:
        pairs.append((i,movie))


index = [j[0] for j in pairs]
data = [j[1] for j in pairs]
dfl = pd.DataFrame({'演员':index, '电影名称':data})


#转化为dataframe结构
result = dfl.groupby('演员', as_index=False).count()
result = result.sort_values(by='电影名称',ascending = False)
result.columns = ['演员', '参演电影数量']
print(result)

#使用中文
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False

#top100电影中拍摄影片最多的10名演员
result1 = result[0:10]
plt.figure()
result1.plot(x='演员', kind='bar')
plt.savefig('most', dpi=1200)