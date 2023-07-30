<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Twitterもどき | ログイン</title>
        <link rel="stylesheet" href="/static/css/style.css" type="text/css">
    </head>
    <body>
        <div class="change">
            <form method="POST" action="/home">
                <h2>Twitterもどきへようこそ<br>ログインは下記からお願いします</h2>
                <br>
                <p><font color="#ff0000">{{error}}</font></p>
                <br>
                <input type="text" name="user_id" placeholder="ユーザー名">
                <br>
                <input type="password" name="password" placeholder="パスワード">
                <br>
                <button type"submit">ログイン</button>
                <button type="submit" formaction="/create">新規作成はこちら</button>
            </form>
        <div>
    </body>
</html>