<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Twitterもどき | 変更</title>
        <link rel="stylesheet" href="/static/css/style.css" type="text/css">
    </head>
    <body>
        <div class="change">
            <form action="/home/text" method="POST">
                <label>テキストを変更してください</label>
                <br>
                <textarea name="number" style="color:transparent; background-color:skyblue; border:none; pointer-events: none;">{{num}}</textarea>
                <br><br>
                <textarea name="text" maxlength="40" placeholder="ツイート" rows="5" cols="30" required>{{text}}</textarea>
                <br>
                <button type="submit">決定</button>
                <button type="submit" formaction="/return">前に戻る</button>
            </form>
        </div>
    </body>
</html>
