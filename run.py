from flaskblog import app   #flaskblog = __init__.py 

if __name__ == "__main__":
    app.run(debug='True')   #if we remove debug part, we'll have to restart again to reload, debug will show changes with just reload
