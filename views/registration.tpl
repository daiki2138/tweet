<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Twitterもどき | 登録画面</title>
        <link rel="stylesheet" href="/static/css/style.css" type="text/css">
    </head>
    <body>
        <div class="change">
            <form action="/create/registration" method="POST">
                <h2>登録画面</h2>
                <br>
                <p><font color="#ff0000">{{error}}</font></p>
                <br>
                <p>ユーザー名</p><input type="text" name="user_id" placeholder="ユーザー名" required>
                <br>
                <p>パスワード</p><input type="text" name="password" placeholder="パスワード" required minlength="8"><p><font color="#ff0000">８文字以上</font></p>
                <br>
                <button type"submit">登録</button>
            </form>
        <div>
    </body>
</html>