<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Twitterもどき | アカウント削除</title>
        <link rel="stylesheet" href="/static/css/style.css" type="text/css">
    </head>
    <body>
        <div class="change">
            <form method="POST" action="/home/account/delete">
                <h3>アカウントを削除します。<br>よろしければユーザー名とパスワードを入力してください。</h3><br>
                <p><font color="#ff0000">{{text}}</font></p>
                <p>ユーザー名を入力</p><input type="text" name="user_id" placeholder="ユーザー名" required><br>
                <p>パスワードを入力</p><input type="password" name="password" placeholder="パスワード" required><br>
                <button type"submit">削除</button>
            <form>
        </div>
    </body>
</html>