from flask import Flask, render_template, request, g, url_for, redirect
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing
from flaskext.mysql import MySQL

# python 엔터
# >>> from guest import init_db(); init_db() 한줄로 쓸때는 세미 콜론


DATABASE = "guest.db"# 대문자 상수형변수 한번 값을 정하면 불변
#.sql문서에 한글 주석을 달면 안된다


app = Flask(__name__)#__를 쓰는건 파이썬 내부 변수
app.config.from_object(__name__)#config 환경을 설정하다
app.config.from_envvar("GUEST_SETTINGS", silent=True)#조용히 환경설정 정보를 가져오라



def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with connect_db() as db:
        with app.open_resource('schema.sql', mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():#요청이 있기전에 준비
    g.db = connect_db()

@app.teardown_request
def teardown_request(Exception):
    if hasattr(g,'db'):# 속성을 가졌느냐
        g.db.close()#끝 자원을 해제한다


DEBUG = True

# http://localhost:5000/
# @app 는 데코레이터라고 함
@app.route("/")
def index():
    return render_template("index.html")

# http://localhost:5000/hello
@app.route("/write", methods=['GET','POST'])#디폴트값은 GET만 있는거 그래서 위에것은 생략
def write():
    if request.method =='POST':
        subject = request.form['subject']
        name = request.form['name']
        content = request.form['content']
        print('이름=', name, "제목=",subject,"내용=", content)
        sql="""insert into guest(name,subject,content) values(?,?,?)"""
        #insert into guest(name,subject,content) values('"+ name + "', '" + subject + "', '" + content + "')
        data = [ name, subject, content ]          #db2= connect_db()# 1 단계 : 연결
        g.db.execute(sql, data)           #메모리상에 처리 # 2단계: 명령 # 3단계: 결과
        #print(result.lastrowid)                    #0아니면 저장성공 0이면 실패
        
        #if result.lastrowid != 0 :
        #    s = "저장 성공"
        #else:
        #    s="에러발생"
        g.db.commit()                              #적용#print("성공은1, 실패는0, ok=",ok)
        return redirect(url_for("list"))
    else:
        return render_template("writeform.html")
#http://localhost:5000/list    
@app.route("/list")
def list():
    sql = "select * from guest order by no desc"
    cur = g.db.execute(sql)
    #print(cur.fetchall()) 
    guests= [dict(no=row[0], name=row[1], subject=row[2], content=row[3], regdate=row[4] ) for row in cur.fetchall()]        #fetchall() 다가져와라
    print(guests)
    return render_template("list.html", guests=guests)

#http://localhost:5000/layout
@app.route("/layout")
def layout():
    return render_template("layout.html")

@app.route("/test1")
def test1():
    user1 = { "url" : "hong.com","username":"홍길동"}
    user2 = { "url" : "jang.com","username":"장길산"}
    user3 = { "url" : "im.com","username":"임꺽정"}
    users = [user1,user2,user3]
    return render_template("test1.html", users=users)

if __name__ == "__main__":
    app.debug=True
    app.run()

# create table guestbook(
#     no int primary auto_increment,
#     name varchar(10) not null,
#     subject varchar(50) not null,
#     content varchar(500) not null,
#     regdate datetime default current_timestamp
# )