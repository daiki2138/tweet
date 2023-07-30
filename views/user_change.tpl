<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Twitterもどき | ユーザー名変更</title>
        <link rel="stylesheet" href="/static/css/style.css" type="text/css">
    </head>
    <body>
        <div class="change">
            <form method="POST" action="/home/user/decide">
                <h3>ユーザー名を変更します。</h3><br>
                <p><font color="#ff0000">{{text}}</font></p>
                <p>新しいユーザー名を入力</p><input type="text" name="user_id" placeholder="ユーザー名" required><br>
                <p>パスワードを入力</p><input type="password" name="password" placeholder="パスワード" required><br>
                <button type"submit">決定</button>
            <form>
        </div>
    </body>
</html>