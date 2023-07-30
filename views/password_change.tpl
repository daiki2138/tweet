<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Twitterもどき | パスワード変更</title>
        <link rel="stylesheet" href="/static/css/style.css" type="text/css">
    </head>
    <body>
        <div class="change">
            <form method="POST" action="/home/password/change">
                <h3>パスワードを変更します。</h3><br>
                <p><font color="#ff0000">{{text}}</font></p>
                <p>変更後のパスワードを入力</p><input type="text" name="newpass" placeholder="新パスワード" required>
                <p>変更前のパスワードを入力</p><input type="password" name="password" placeholder="旧パスワード" required><br>
                <button type"submit">変更</button>
            <form>
        </div>
    </body>
</html>