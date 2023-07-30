<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Twitterもどき | ログの書き出し</title>
        <link rel="stylesheet" href="/static/css/style.css" type="text/css">
    </head>
    <body>
        <div class="change">
            <form method="POST" action="/home/log/export">
                <h3>ログを書き出します。<br>書き出したファイルはlog.txtとして書き出されます。</h3><br>
                <p><font color="#ff0000">{{text}}</font></p>
                <p>管理パスワードを入力</p><input type="password" name="password" placeholder="パスワード" required><br>
                <button type"submit">書き出し</button>
            <form>
        </div>
    </body>
</html>