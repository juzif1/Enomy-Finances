% rebase('base.tpl', title='Login', include_js=False)

<h2>Login</h2>

<form method="post">
    <label>Username</label>
    <input type="text" name="username" required>

    <label>Password</label>
    <input type="password" name="password" required>

    <button type="submit">Login</button>
</form>

<p style="text-align:center; margin-top:20px;">
    Don’t have an account?
    <a href="/register">Register here</a>
</p>
