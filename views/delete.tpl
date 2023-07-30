<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Twitterもどき | 削除</title>
        <link rel="stylesheet" href="/static/css/style.css" type="text/css">
    </head>
    <body>
        <div class="change">
            <form action="/home/delete/decide" method="POST">
                <h2>削除するツイートの番号とパスワードを入力してください</h2>
                <br>
                <p><font color="#ff0000">{{error}}</font></p>
                <br>
                <textarea name="num" style="color:transparent; background-color:skyblue; border:none; pointer-events: none;">{{num}}</textarea>
                <br>
                <textarea disabled rows="20" cols="50" STYLE="background-color:skyblue; border:none; pointer-events: none;">{{text}}</textarea>
                <br>
                <p>削除したいツイート番号</p><input type="text" name="delete" placeholder="番号" required>
                <br>
                <p>パスワード</p><input type="password" name="password" placeholder="パスワード" required minlength="8">
                <br>
                <button type"submit">削除</button>
            </form>
        <div>
    </body>
</html>