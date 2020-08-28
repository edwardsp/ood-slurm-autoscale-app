from flask import Flask, render_template, url_for
import glob
MyApp = Flask(__name__, static_url_path="", static_folder="public")

helpers = {
    "dashboard_title": "Open OnDemand",
    "dashboard_url": "/pun/sys/dashboard/",
    "title": "Autoscale Log"
}

@MyApp.route("/")
def view_autoscale_log():
    items = []
    try:
        with open("/var/log/slurm/autoscale.log") as file:
            items = [ 
                [ x.strip() for x in line.split("#") ] 
                for line in file.readlines() 
            ]
    except IOError:
        pass
    
    return render_template('index.html', items=items, **helpers)

@MyApp.route("/<log>")
def view_azlog(log):
    g = glob.glob("/var/log/slurm/*_"+log+".log")
    if len(g):
        with open(g[0]) as file:
            content = file.read()
    else:
        content = "<empty_file>"

    return render_template('azlog.html', content=content, **helpers)

if __name__ == "__main__":
	MyApp.run()
