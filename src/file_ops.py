import os, shutil

def file_update():
    try:

        if os.path.exists("public/"):
            shutil.rmtree("public/")
        shutil.copytree("static/", "public/")

    
    except Exception as e:
        return f"Error: {e}"
