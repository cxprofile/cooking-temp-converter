from flask import Flask, render_template, request

app = Flask(__name__)

def c_to_f(c):
    return (c * 9/5) + 32

def f_to_c(f):
    return (f - 32) * 5/9

def cooking_label(c):
    if c < 150:
        return "Low heat 🔥"
    elif 150 <= c <= 190:
        return "Moderate heat 🍳"
    else:
        return "High heat 🔥🔥"

@app.route("/blogs")
def blog():
    return render_template("blogs.html")

@app.route("/tools")
def tools():
    return render_template("tools.html")

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    label = None

    if request.method == "POST":
        temp = float(request.form["temp"])
        conversion = request.form["conversion"]

        if conversion == "c_to_f":
            converted = c_to_f(temp)
            result = f"{temp}°C = {converted:.2f}°F"
            label = cooking_label(temp)
        else:
            converted = f_to_c(temp)
            result = f"{temp}°F = {converted:.2f}°C"
            label = cooking_label(converted)

    return render_template("index.html", result=result, label=label)

if __name__ == "__main__":
    app.run()