### Setting `FLASK_ENV`:
1. **Navigate to Render.com** and log in.
2. **Go to your Service Settings**.
3. **Add Environment Variable**:
   - **Key**: `FLASK_ENV`
   - **Value**: `development`

This will ensure that Flask runs in development mode, enabling debug features. Ready to deploy! 🚀

Yes, we can definitely set the port in the environment. This is actually what we’re already doing with the line `port=int(os.environ.get('PORT', 5000))`. Render automatically sets this environment variable so the app binds to the correct port.

You don’t need to manually set the port environment variable unless you have a specific reason. The current setup should work seamlessly.

