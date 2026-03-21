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
 articles = [
  {
    "title": "Top 5 Cheap Hosting Platforms",
    "slug": "cheap-hosting"
  },
  {
    "title": "Pros and Cons of Free Web Hosting",
    "slug": "free-hosting-pros-cons"
  }
 ]
 return render_template("blogs.html", articles=articles)

@app.route("/blogs/<slug>")
def article(slug):
    articles = {
    "cheap-hosting": {
        "title": "Top 5 Cheap Hosting Platforms",
        "content": """
            <h1>Top 5 Cheap Hosting Platforms for Beginners (2026 Guide)</h1>

            <p>If you're building small tools or side projects, you don’t need expensive hosting.</p>

            <h2>1. Render</h2>
                <p style="padding-left:10px">Great for beginners building full-stack apps.</p>

            <h2>2. Netlify</h2>
                <p style="padding-left:10px">Perfect for blogs and static sites.</p>

            <h2>3. Cloudflare Pages</h2>
                <p style="padding-left:10px">Best free hosting with unlimited bandwidth.</p>

            <h2>4. Railway</h2>
                <p style="padding-left:10px">Fast prototyping and deployment.</p>

            <h2>5. Vercel</h2>
                <p style="padding-left:10px">Best for frontend developers.</p>
        """
    },
    "free-hosting-pros-cons":{
        "title": "Pros and Cons of Free Web Hosting",
        "content": """
            <h1>Pros and Cons of Free Hosting for Beginners (2026 Guide)</h1>
            <h2>Pros:</h2>
            <ul>
                <li>Zero Cost
                    <p>	You don’t pay anything to get started </p>
                    <p> Perfect for beginners, students, and side projects</p>
                </li>
                <li>Easy Setup. Most platforms offer:
                    <p>	One-click deploy </p>
                    <p> Githb integration</p>
                    <p> Simple Dashboards </p>
                </li>
                <li>Great for learning and testing
                    <p>	Practice coding and test ideas</p>
                    <p> Building portfolio </p>
                </li>
                <li>No Commitment
                    <p>	No contracts and you can stop at anytime</p>
                </li>
                <li>Basic Tools included like:
                    <p>	SSL</p>
                    <p> Website Builder </p>
                    <p> Git Integration </p>
                </li>
            </ul>
            <h2>Cons:</h2>
            <ul>
                <li>Slow Performance
                    <p>	Servers are shared with many users </p>
                    <p> Can be slow and laggy</p>
                </li>
                <li>Sites might go offline
                    <p>	"Sleep after inactivity" </p>
                </li>
                <li>Limited Resource
                    <p>	Storage Limits can be strict </p>
                    <p> Bandwidth and CPU can be limited </p>
                </li>
                <li> Weak security and support
                    <p> Limited security features </p>
                    <p> No customer support </p>
                </li>
                <li> Hidden Upsells
                    <p> You'll be pushed to upgrade </p>
                </li>

            </ul>
        """
    }
   }

    article = articles.get(slug)

    if not article:
            return "Article not found", 404

    return render_template("article.html", article=article)


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