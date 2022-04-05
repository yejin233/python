from flask import Flask,render_template,request
import sqlite3
from flask import url_for

app = Flask(__name__)

con1 = sqlite3.connect("user.db")

cur1= con1.cursor()
# sql = "CREATE TABLE lkx1(USER VARCHAR(20),PASSWD INT);"
# cur1.execute(sql)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/index')
def home():
    #return render_template("index.html")
    return index()


@app.route('/movie')
def movie():
    datalist  = []
    con = sqlite3.connect("movie.db")
    cur = con.cursor()
    sql = "select * from movie250"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()
    print(datalist)
    return render_template("movie.html",movies = datalist)



@app.route('/score')
def score():
    score = []  #评分
    num = []    #每个评分所统计出的电影数量
    con = sqlite3.connect("movie.db")
    cur = con.cursor()
    sql = "select score,count(score) from movie250 group by score"
    data = cur.execute(sql)
    for item in data:
        score.append(str(item[0]))
        num.append(item[1])

    cur.close()
    con.close()
    return render_template("score.html",score= score,num=num)
@app.route('/wor')
def word1():
    return render_template("侧边导航栏.html")
@app.route('/word')
def word():
    return render_template("word.html")

@app.route('/team')
def team():
    return render_template("team.html")
@app.route('/hello',methods=["GET","post"])
def hello():
    #登录检查
    con2 = sqlite3.connect("user.db")

    cur2= con2.cursor()
  
    if request.method=='POST':
        
        user1=request.form.get('user')
        pass1=int(request.form.get('pasword'))
        # print(type(user1))
        # print(user1)
        # print(pass1)
        # print(type(pass1))
        oo=f"select PASSWD from lkx where USER='{user1}'"
        data=cur2.execute(oo)
        #oo="select * from lkx;"
        ##print(cur2.execute(oo)[1])
        tt=[]
        for dat in data:
            tt.append(dat)
        print(tt)
        ee=[]
        for i in range(len(tt)):
            ee.append(tt[i][0])
        print(ee)
        if user1 in ee:
            print("1")
            return render_template("word.html")
            
        cur2.close()
        con2.commit()
        con2.close()
    
    return render_template("bilibili登录.html")

@app.route('/oo')
def oo():
    t="""<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>手机充电</title>
	<link rel="stylesheet" href="./33.CSS">
	 <script src="echarts.js">
	</script>
</head>
<body>
	<div class="battery">
		<div class="cover">
			
		</div>
	</div>
	<script type="text/javascript">
      // 基于准备好的dom，初始化echarts实例
      var myChart = echarts.init(document.getElementById('main'));

      // 指定图表的配置项和数据
      var option = {
        title: {
          text: 'ECharts 入门示例'
        },
        tooltip: {},
        legend: {
          data: ['销量']
        },
        xAxis: {
          data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
        },
        yAxis: {},
        series: [
          {
            name: '销量',
            type: 'bar',
            data: [5, 20, 36, 10, 10, 20]
          }
        ]
      };

      // 使用刚指定的配置项和数据显示图表。
      myChart.setOption(option);
    </script>
    <div id="main" style="width: 600px;height:400px;"></div>
    <script type="text/javascript">
      // 基于准备好的dom，初始化echarts实例
      var myChart = echarts.init(document.getElementById('main'));

      // 指定图表的配置项和数据
      var option = {
        title: {
          text: 'ECharts 入门示例'
        },
        tooltip: {},
        legend: {
          data: ['销量']
        },
        xAxis: {
          data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
        },
        yAxis: {},
        series: [
          {
            name: '销量',
            type: 'bar',
            data: [5, 20, 36, 10, 10, 20]
          }
        ]
      };

      // 使用刚指定的配置项和数据显示图表。
      myChart.setOption(option);
    </script>
</body>
</html>"""
    return t#直接输入网页源码

if __name__ == '__main__':
    with app.test_request_context():
        url_for('static', filename='style.css')
    app.run()
    
