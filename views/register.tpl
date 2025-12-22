% rebase('base.tpl', title='Register', include_js=False)

<h2>Create Account</h2>

<form method="post">
    <label>Username</label>
    <input type="text" name="username" required>

    <label>Password</label>
    <input type="password" name="password" required>

    <button type="submit">Register</button>
</form>

<p style="text-align:center; margin-top:20px;">
    Already have an account?
    <a href="/login">Login</a>
</p>
