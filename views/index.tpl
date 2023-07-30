<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Twitterもどき | ホーム</title>
        <link rel="stylesheet" href="/static/css/style.css" type="text/css">
    </head>
    <body>
        <div class="top">
            <div class="left">
                <br>
                <h4 name = "user_id">{{user_id}}</h4><h4>としてログイン中</h4>
                <br>
                <form method="POST" action="/home/search">
                    <label>検索したいユーザー名を入力</label>
                        <br>
                    <input type="text" name="searchname" placeholder="入力">
                        <br>
                    <button type="submit">検索</button>
                </form>
                    <br><br>
                <form method="POST" action="/home/time">
                    <label>検索したい日付を入力</label>
                        <br>
                    <input type="date" name="searchdate">
                        <br>
                    <button type="submit">検索</button>
                </form>
            </div>
            <div class="right">
                <form method="POST" action="/home/return" name="home">
                    <button type="submit" >ホームに戻る</button>
                    <br><br>
                    <button type="submit" formaction="/home/edit">ツイート内容を変更する</button>
                    <br><br>
                    <button type="submit" formaction="/home/delete">ツイートを削除する</button>
                    <br><br>
                    <button type="submit" formaction="/home/user">ユーザー名を変更する</button>
                    <br><br>
                    <button type="submit" formaction="/home/account">アカウントを削除する</button>
                    <br><br>
                    <button type="submit" formaction="/home/password">パスワードを変更する</button>
                    <br><br>
                    <button type="submit" formaction="/home/log">ログを書き出す</button>
                    <br><br>
                    <button type="submit" formaction="/home/logout">ログアウト</button>
                </form>
            </div>
            <div class="main">
                <form method="POST" action="/home/tweet" name="tweet">
                        <br>
                        <p>{{text}}</p>
                        <br>
                    <label>ツイート内容を記入</label>
                        <br>
                    <textarea name="text" maxlength="40" placeholder="ツイート" rows="5" cols="30" required></textarea>
                        <br>
                    <input type="file" name="upload" multiple="multiple">
                        <br>
                    <button type="submit">ツイート</button> 
                        <br><br>
                </form>
                <textarea disabled rows="26" cols="50" STYLE="background-color:skyblue; border:none;">{{textdetail}}</textarea>
            </div>
        </div>
    </body>
</html>