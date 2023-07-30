<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Twitterもどき | 変更</title>
        <link rel="stylesheet" href="/static/css/style.css" type="text/css">
    </head>
    <body>
        <div class="change">
            <form action="/home/edit/num" method="POST">
                <p><font color="#ff0000">{{error}}</font></p>
                <br>
                <textarea name="num" style="color:transparent; background-color:skyblue; border:none; pointer-events: none;">{{num}}</textarea>
                <br>
                <label>テキスト内容を変更したい番号を入力</label>
                <br>
                <textarea readonly rows="20" cols="50" STYLE="background-color:skyblue; border:none; pointer-events: none;">{{text}}</textarea>
                <br>
                <input  type="text" name="number" placeholder="入力">
                <br>
                <button type="submit">決定</button>
                <button type="submit" formaction="/re">前に戻る</button>
            </form>
        </div>
    </body>
</html>