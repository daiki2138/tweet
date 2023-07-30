from bottle import route, request, run, template, static_file,view
import os
import datetime
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR,'static')

filepath = "./tweet/tweet.sqlite"
filepath_pass = "./tweet/password.sqlite"
filepath_log = "./tweet/log.sqlite"
filepath_DM = "./tweet/DM.sqlite"
path = "./tweet"

#tweetのsqliteがない場合作成する。
if not os.path.exists(filepath):
    connection_text = sqlite3.connect(filepath)
    cursor_text = connection_text.cursor()
    cursor_text.execute("""CREATE TABLE items(
        item_id INTEGER PRIMARY KEY,
        date TEXT,
        user TEXT,
        text TEXT
    )""")
    connection_text.commit()
else:
    connection_text = sqlite3.connect(filepath)
    cursor_text = connection_text.cursor()
    connection_text.commit()

#passwordのsqliteが無い場合作成する。
if not os.path.exists(filepath_pass):
    connection_pass = sqlite3.connect(filepath_pass)
    cursor_pass = connection_pass.cursor()
    cursor_pass.execute("""CREATE TABLE items(
        user INTEGER PRIMARY KEY,
        user_id TEXT,
        password TEXT
    )""")
    connection_pass.commit()
else:
    connection_pass = sqlite3.connect(filepath_pass)
    cursor_pass = connection_pass.cursor()
    connection_pass.commit()

#logのsqliteが無い場合作成する。
if not os.path.exists(filepath_log):
    connection_log = sqlite3.connect(filepath_log)
    cursor_log = connection_log.cursor()
    cursor_log.execute("""CREATE TABLE items(
        log_id INTEGER PRIMARY KEY,
        date TEXT,
        user TEXT,
        detail TEXT
    )""")
    connection_log.commit()
else:
    connection_log = sqlite3.connect(filepath_log)
    cursor_log = connection_log.cursor()
    connection_log.commit()

#CSSの指定。
@route('/static/css/<filename:path>')
def return_static(filename):
    return static_file(filename, root = f'{STATIC_DIR}/css')

#標準でログイン画面に移動する。
@route('/')
def root():
    return template('main',error="")

#アカウント新規作成ボタンした場合、registrationのページに飛びアカウント作成ページに飛ぶ。
@route('/create',method="POST")
def create():
    return template('registration',error="")

#新規作成ページで入力されたユーザー名とパスワードを後で変更できる様にpasswordのsqliteに書き込む。
@route('/create/registration',method="POST")
def registration():
    user = request.forms.getunicode('user_id')
    password = request.forms.getunicode('password')
    cursor_pass.execute("SELECT * FROM items")
    result = cursor_pass.fetchall()
    for i in result:
        if user == i[1]:
            return template('registration',error="すでにそのユーザー名は使用されています。")         
    dt_now = datetime.datetime.now()
    time = dt_now.strftime('%Y年%m月%d日 %H時%M分%S秒')
    detail = "新規登録しました。\n"
    cursor_log.execute('INSERT INTO items (date,user,detail) VALUES (?,?,?)',(time,user,detail))
    cursor_pass.execute('INSERT INTO items (user_id,password) VALUES (?,?)',(user,password))
    connection_log.commit()
    connection_pass.commit()
    return template('main',error="登録が完了しました")

#入力されたユーザー名とパスワードが合っているかpasswordのsqliteで確認。
#合っていればツイート画面を表示、間違っていればログイン画面に移動。
@route('/home',method="POST")
def home():
    global user
    user = request.forms.getunicode('user_id')
    password = request.forms.getunicode('password')
    cursor_pass.execute('SELECT * FROM items WHERE user_id=?',(user,))
    result = cursor_pass.fetchone()
    if str(result) == "None":
        return template('main',error="ユーザー名またはパスワードが間違っています。もう一度入力しなおしてください。")
    elif result[2] == password:
        detail = "ログインしました。\n"
        dt_now = datetime.datetime.now()
        time = dt_now.strftime('%Y年%m月%d日 %H時%M分%S秒')
        cursor_log.execute('INSERT INTO items (date,user,detail) VALUES (?,?,?)',(time,user,detail))
        connection_log.commit()
        if os.path.exists('./tweet/tweet.txt'):
            with open("./tweet/tweet.txt","r",encoding='UTF-8') as file:
                textdetail = file.read()
                return template('index',textdetail=textdetail,user_id=user,text="")
        else:
            return template('index',textdetail="                 書き込みはありません",user_id=str(user),text="")
    else:
        return template('main',error="ユーザー名またはパスワードが間違っています。もう一度入力しなおしてください")

#ツイートで入力された文字と日時を取得、テキストファイルに書き込むと同時にsqliteファイルに書き込み、後で編集可能にしておく。
@route('/home/tweet',method="POST")
def tweet():
    dt_now = datetime.datetime.now()
    time = dt_now.strftime('%Y年%m月%d日 %H時%M分%S秒')
    text = request.forms.getunicode('text')
    filename = "./tweet/tweet.txt"
    with open(filename,"a",encoding='UTF-8',newline='') as file:
        file.write(time+" ツイート "+"\nユーザー名 "+str(user)+"\n"+"ツイート内容"+"\n")
        for i in text:
            file.write(i)
        file.write("\n"+"\n")
    detail = text+"とツイートしました。\n"
    cursor_log.execute('INSERT INTO items (date,user,detail) VALUES (?,?,?)',(time,str(user),detail))
    cursor_text.execute('INSERT INTO items (date,user,text) VALUES (?,?,?)',(time,str(user),text))
    connection_log.commit()
    connection_text.commit()
    with open("./tweet/tweet.txt","r",encoding='UTF-8') as file:
        textdetail = file.read()
        return template('index',textdetail=textdetail,user_id=user,text="")    

#時間でソートし、テキストファイルにソート結果を表示させる。
#時間でソートできなかった場合、全てのツイートを表示させる。
@route('/home/time',method="POST")
def time():
    time = request.forms.getunicode('searchdate')
    time = time[:4]+"年"+time[5:7]+"月"+time[-2:]+"日"
    cursor_text.execute('SELECT * FROM items WHERE date like ?', (time+'%',))
    result = cursor_text.fetchall()
    if result == []:
        with open("./tweet/tweet.txt","r",encoding='UTF-8') as file:
            textdetail = file.read()
        return template('index',textdetail=textdetail,user_id=user,text="検索したユーザー名はいませんでした。")
    else:
        with open('./tweet/result.txt',"w",encoding='UTF-8',newline='') as file:
            for i in result:
                file.write(i[1]+" ツイート"+"\nユーザー名 "+i[2]+"\nツイート内容 \n"+i[3]+"\n\n")
        with open('./tweet/result.txt',"r",encoding='UTF-8') as file:
            textdetail = file.read()
        return template('index',textdetail=textdetail,user_id=user,text="")

#ユーザー名でソートし、テキストファイルにソート結果を表示させる。
#ユーザー名でソートできなかった場合、全てのツイートを表示させる。
@route('/home/search',method="POST")
def search():
    user_id = request.forms.getunicode('searchname')
    cursor_text.execute('SELECT * FROM items WHERE user=?',(user_id,))
    connection_text.commit()
    result = cursor_text.fetchall()
    if result == []:
        with open("./tweet/tweet.txt","r",encoding='UTF-8') as file:
            textdetail = file.read()
        return template('index',textdetail=textdetail,user_id=user,text="検索した日付にツイートしたユーザーはいませんでした。")
    else:
        with open('./tweet/result.txt',"w",encoding='UTF-8',newline='') as file:
            for i in result:
                file.write(i[1]+" ツイート"+"\nユーザー名 "+i[2]+"\nツイート内容 \n"+i[3]+"\n\n")
        with open('./tweet/result.txt',"r",encoding='UTF-8') as file:
            textdetail = file.read()
        return template('index',textdetail=textdetail,user_id=user,text="")

#ソート後などで再び全員のツイートを表示する。
@route('/home/return',method="POST")
def root():
    if os.path.exists('./tweet/tweet.txt'):
        with open("./tweet/tweet.txt","r",encoding='UTF-8') as file:
            textdetail = file.read()
            return template('index',textdetail=textdetail,user_id=user,text="")
    else:
        return template('index',textdetail="                 書き込みはありません",user_id=user,text="")

#ツイート内容を変更する場合にsqliteファイルを使用しユーザー名でソートし、ツイート一覧を表示する。
@route('/home/edit',method="POST")
def change():
    cursor_text.execute('SELECT * FROM items WHERE user=?',(str(user),))
    result = cursor_text.fetchall()
    ls = []
    with open('./tweet/result.txt',"w",encoding='UTF-8',newline='') as file:
        for i in result:
            file.write("No."+str(i[0])+"  "+i[1]+" ツイート内容 "+i[3]+"\n")
            ls.append(i[0])
    with open('./tweet/result.txt',"r",encoding='UTF-8') as file:
            textdetail = file.read()
    return template('change',text=textdetail,error="",num=ls)

#前のページを表示する。
@route('/re',method="POST")
def re():
    return template('index')    

#選択した番号でソートしテキスト内容を表示させる。
#選択した番号がない場合、番号を選択しなおす。
@route('/home/edit/num',method="POST")
def nun():
    number = request.forms.getunicode('number')
    num = request.forms.getunicode('num')
    for i in num:
        if i == number:
            cursor_text.execute('SELECT * FROM items WHERE item_id=?',(i,))
            result = cursor_text.fetchone()
            textdetail = result[3]
            return template('edit',text=textdetail,num=i)
    with open('./tweet/result.txt',"r",encoding='UTF-8') as file:
        textdetail = file.read()
    return template('change',text=textdetail,error="検索した番号が正しくありません 番号を入力しなおしてください。",num=num)

#ツイート内容変更ページから選択画面に戻る。
@route('/return',method="POST")
def re():
    cursor_text.execute('SELECT * FROM items WHERE user=?',(str(user),))
    result = cursor_text.fetchall()
    ls = []
    with open('./tweet/result.txt',"w",encoding='UTF-8',newline='') as file:
        for i in result:
            file.write("No."+str(i[0])+"  "+i[1]+" ツイート内容 "+i[3]+"\n")
            ls.append(i[0])
    with open('./tweet/result.txt',"r",encoding='UTF-8') as file:
            textdetail = file.read()
    return template('change',text=textdetail,error="",num=ls)

#変更したテキストをsqliteファイルに更新する。
#変更に伴い、tweetのテキストファイルを書き直す。
#変更内容をテキストファイルに書き込む。
@route('/home/text',method="POST")
def text():
    text = request.forms.getunicode('text')
    num = request.forms.getunicode('number')
    cursor_text.execute('SELECT * FROM items WHERE item_id=?',(str(num),))
    before = cursor_text.fetchone()
    dt_now = datetime.datetime.now()
    time = dt_now.strftime('%Y年%m月%d日 %H時%M分%S秒')
    detail = before[3]+"から"+text+"へ変更しました。\n"
    cursor_log.execute('INSERT INTO items (date,user,detail) VALUES (?,?,?)',(time,str(user),detail))
    cursor_text.execute("UPDATE items SET text=? WHERE item_id=?",(text,num))
    cursor_text.execute("SELECT * FROM items")
    result = cursor_text.fetchall()
    with open('./tweet/tweet.txt',"w",encoding='UTF-8',newline='') as file:
            for i in result:
                file.write(i[1]+" ツイート"+"\nユーザー名 "+i[2]+"\nツイート内容 \n"+i[3]+"\n\n")
    connection_log.commit()
    connection_text.commit()
    with open('./tweet/tweet.txt',"r",encoding='UTF-8') as file:
            textdetail = file.read()
    return template('index',textdetail=textdetail,user_id=user,text="変更が完了しました。")

#削除するユーザー名でツイートをソートし、一覧を表示する。
@route('/home/delete',method="POST")
def delete():
    cursor_text.execute('SELECT * FROM items WHERE user=?',(str(user),))
    result = cursor_text.fetchall()
    ls = []
    with open('./tweet/result.txt',"w",encoding='UTF-8',newline='') as file:
        for i in result:
            file.write("No."+str(i[0])+"  "+i[1]+" ツイート内容 "+i[3]+"\n")
            ls.append(i[0])
    with open('./tweet/result.txt',"r",encoding='UTF-8') as file:
            textdetail = file.read()
    return template('delete',error="",text=textdetail,num=ls)

#パスワードと入力された番号がそれぞれ一致したら、削除してホームに戻る。
#パスワードが間違っていたら選択画面に戻し、番号が一致しなかったら、選択画面にもどす。
#削除したときにログも残しておく。
@route('/home/delete/decide',method="POST")
def delete():
    number = request.forms.getunicode('delete')
    num = request.forms.getunicode('num')
    password = request.forms.getunicode('password')
    cursor_pass.execute('SELECT * FROM items WHERE user_id=?',(str(user),))
    result = cursor_pass.fetchone()
    if result[2] != password:
        with open('./tweet/result.txt',"r",encoding='UTF-8') as file:
            textdetail = file.read()
        return template('delete',text=textdetail,error="入力したパスワードが正しくありません。",num=num)
    for i in num:
        if i == number:
            cursor_text.execute('SELECT * FROM items WHERE item_id=?',(i,))
            result_before = cursor_text.fetchone()
            dt_now = datetime.datetime.now()
            time = dt_now.strftime('%Y年%m月%d日 %H時%M分%S秒')
            detail = result_before[3] + "を削除しました\n"
            cursor_log.execute('INSERT INTO items (date,user,detail) VALUES (?,?,?)',(time,str(user),detail))
            connection_log.commit()
            cursor_text.execute('delete FROM items WHERE item_id=?',(i,))
            connection_text.commit()
            cursor_text.execute('SELECT * FROM items')
            result = cursor_text.fetchall()
            with open('./tweet/tweet.txt',"w",encoding='UTF-8',newline='') as file:
                for i in result:
                    file.write(i[1]+" ツイート"+"\nユーザー名 "+i[2]+"\nツイート内容 \n"+i[3]+"\n\n")
            with open('./tweet/tweet.txt',"r",encoding='UTF-8') as file:
                textdetail = file.read()
            return template('index',textdetail=textdetail,user_id=user,text="ツイート削除が完了しました。")
    with open('./tweet/result.txt',"r",encoding='UTF-8') as file:
        textdetail = file.read()
    return template('delete',text=textdetail,error="検索した番号が正しくありません 番号を入力しなおしてください。",num=num)


#パスワード変更画面に移動
@route('/home/password',method="POST")
def p_change():
    return template('password_change',text="")

#前のパスワードが合っていれば新しいパスワードに変更し、再ログインさせる。
#パスワードが合っていない場合は、変更画面に戻る。
@route('/home/password/change',method="POST")
def chenge():
    old = request.forms.getunicode('password')
    new = request.forms.getunicode('newpass')
    cursor_pass.execute('SELECT * FROM items WHERE user_id=?',(str(user),))
    password = cursor_pass.fetchone()
    if password[2] == old:
        dt_now = datetime.datetime.now()
        time = dt_now.strftime('%Y年%m月%d日 %H時%M分%S秒')
        detail = "パスワードを変更しました。\n"
        cursor_log.execute('INSERT INTO items (date,user,detail) VALUES (?,?,?)',(time,str(user),detail))
        cursor_pass.execute("UPDATE items SET password=? WHERE user_id=?",(new,str(user)))
        connection_log.commit()
        connection_pass.commit()
        return template('main',error="パスワードの変更が完了しました。ログインしなおしてください。")
    else:
        return template('user_change',text="パスワードが違います。")

#ユーザー名変更画面に移動
@route('/home/user',method="POST")
def change():
    return template('user_change',text="")

#パスワードが合っていれば新しいユーザー名に変更し、再ログインさせる。
#ツイートのユーザー名の所も変更しておく。
#パスワードが合っていない場合は、変更画面に戻る。
@route('/home/user/decide',method="POST")
def user():
    user_password = request.forms.getunicode('password')
    user_id = request.forms.getunicode('user_id')
    cursor_pass.execute('SELECT * FROM items WHERE user_id=?',(str(user),))
    password = cursor_pass.fetchone()
    if password[2] == user_password:
        cursor_pass.execute("UPDATE items SET user_id=? WHERE password=?",(user_id,user_password))
        cursor_text.execute('SELECT * FROM items WHERE user=?',(str(user),))
        result = cursor_text.fetchall()
        for i in result:
            cursor_text.execute("UPDATE items SET user=? WHERE item_id=?",(user_id,i[0]))
        cursor_text.execute("SELECT * FROM items")
        result = cursor_text.fetchall()
        with open('./tweet/tweet.txt',"w",encoding='UTF-8',newline='') as file:
                for i in result:
                    file.write(i[1]+" ツイート"+"\nユーザー名 "+i[2]+"\nツイート内容 \n"+i[3]+"\n\n")
        dt_now = datetime.datetime.now()
        time = dt_now.strftime('%Y年%m月%d日 %H時%M分%S秒')
        detail = "ユーザー名を"+user_id+"に変更しました。\n"
        cursor_log.execute('INSERT INTO items (date,user,detail) VALUES (?,?,?)',(time,str(user),detail))
        connection_log.commit()
        connection_pass.commit()
        connection_text.commit()
        return template('main',error="ユーザー名の変更が完了しました。ログインしなおしてください。")
    else:
        return template('user_change',text="パスワードが違います。")
        
#アカウント削除ページに移動する。
@route('/home/account',method="POST")
def account():
    return template('account_delete',text="")

#ユーザー名とパスワードが一致していたら、アカウントを削除し、ログイン画面に戻す。
#一致していなければ、エラーを表示させる。
#ログにも書き込んでおく。
@route('/home/account/delete',method="POST")
def account_delete():
    user_password = request.forms.getunicode('password')
    user_id = request.forms.getunicode('user_id')
    if user_id != str(user):
        return template('account_delete',error="ユーザー名が一致しません。入力しなおしてください。")
    cursor_pass.execute('SELECT * FROM items WHERE user_id=?',(user_id,))
    result = cursor_pass.fetchone()
    if user_password == result[2]:
        cursor_pass.execute('delete FROM items WHERE user_id=?',(user_id,))
        dt_now = datetime.datetime.now()
        time = dt_now.strftime('%Y年%m月%d日 %H時%M分%S秒')
        detail = "アカウントを削除しました。\n"
        cursor_log.execute('INSERT INTO items (date,user,detail) VALUES (?,?,?)',(time,str(user),detail))
        connection_log.commit()
        return template('main',error="アカウントは削除されました。")
    else:
        return template('account_delete',text="パスワードが一致しません。入力しなおしてください。")
    connection_pass.commit()

#ログアウトする。
@route('/home/logout',method="POST")
def logout():
    dt_now = datetime.datetime.now()
    time = dt_now.strftime('%Y年%m月%d日 %H時%M分%S秒')
    detail = "ログアウトしました。\n"
    cursor_log.execute('INSERT INTO items (date,user,detail) VALUES (?,?,?)',(time,str(user),detail))
    connection_log.commit()
    return template('main',error="")

#ログ書き出し画面に移動
@route('/home/log',method="POST")
def export():
    return template('master',text="")

#これまでの管理ログをテキストファイルに書き込む。
@route('/home/log/export',method="POST")
def export():
    password = request.forms.getunicode('password')
    if password == "tWJyEpnQiu8tBLT3MadZW6TNz":
        cursor_log.execute("SELECT * FROM items")
        result = cursor_log.fetchall()
        with open('./log.txt',"w",encoding='UTF-8',newline='') as file:
            for i in result:
                file.write(i[1]+"\n"+i[2]+"さんが\n"+i[3]+"\n")
        connection_log.commit()
        with open('./tweet/tweet.txt',"r",encoding='UTF-8') as file:
            textdetail = file.read()
        return template('index',text="書き込みが完了しました。",user_id=user,textdetail=textdetail)
    else:
        return template('master',text="パスワードが違います。")

run(host='localhost', port=8080)
