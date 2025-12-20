
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{title}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/css/style.css">
    % if include_js:
        <script src="/static/js/main.js" defer></script>
    % end
</head>
<body>

<header>
    <h1>Enomy-Finances Portal</h1>
    <nav>
        <a href="/">Home</a>
        <a href="/currency">Currency</a>
        <a href="/investment">Investment</a>
    </nav>
</header>

<main>
    % include
</main>

</body>
</html>
