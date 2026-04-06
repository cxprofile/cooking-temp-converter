from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.message import EmailMessage
import os 
from dotenv import load_dotenv

from flask import Flask, request, send_file, render_template
import pandas as pd
from io import StringIO, BytesIO


app = Flask(__name__)
app.secret_key = "secretwapprender"  # required for flash messages

# --- Conversion Functions ---
def c_to_f(c):
    return (c * 9/5) + 32

def f_to_c(f):
    return (f - 32) * 5/9

def g_to_kg(f):
    return (f/1000)

def kg_to_g(f):
    return (f*1000)

def g_to_lbs(f):
    return (f/1453.6)

def lbs_to_g(f):
    return (f*1453.6)

def kg_to_lbs(f):
    return (f*2.205)

def lbs_to_kg(f):
    return (f/2.205)

def g_to_oz(f):
    return (f/28.35)

def oz_to_g(f):
    return (f*28.35)

def cups_to_ml(f):
    return (f/236.6)

def ml_to_cups(f):
    return (f*236.6)

def cooking_label(c):
    if c < 150:
        return "Low heat 🔥"
    elif 150 <= c <= 190:
        return "Moderate heat 🍳"
    else:
        return "High heat 🔥🔥"


# --- CSV Transformation Logic ---
def transform_csv(file_stream):
    df = pd.read_csv(file_stream)

    if df.empty:
        raise ValueError("CSV is empty")

    # Simple mapping (adjust to your needs)
    df = df.rename(columns={
        "Name": "contact_name",
        "InvoiceDate": "invoice_date",
        "DueDate": "due_date",
        "Description": "description",
        "Quantity": "quantity",
        "UnitAmount": "unit_amount"
    })

    required = ["contact_name", "invoice_date", "due_date", "description", "quantity", "unit_amount"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # Normalize
    df["invoice_date"] = pd.to_datetime(df["invoice_date"]).dt.strftime("%d/%m/%Y")
    df["due_date"] = pd.to_datetime(df["due_date"]).dt.strftime("%d/%m/%Y")
    df["quantity"] = df["quantity"].fillna(1).astype(float)
    df["unit_amount"] = df["unit_amount"].astype(float).round(2)

    df["account_code"] = "200"
    df["tax_type"] = "GST on Income"
    df["currency"] = "NZD"
    df["invoice_number"] = [f"INV-{i+1:04d}" for i in range(len(df))]

    # Xero format
    output = pd.DataFrame()
    output["ContactName"] = df["contact_name"]
    output["EmailAddress"] = ""
    output["InvoiceNumber"] = df["invoice_number"]
    output["InvoiceDate"] = df["invoice_date"]
    output["DueDate"] = df["due_date"]
    output["Description"] = df["description"]
    output["Quantity"] = df["quantity"]
    output["UnitAmount"] = df["unit_amount"]
    output["AccountCode"] = df["account_code"]
    output["TaxType"] = df["tax_type"]
    output["Reference"] = ""
    output["Currency"] = df["currency"]
    return output

@app.route("/convert-csv-to-xero")
def convertcsv():
    return render_template("convert-csv-to-xero.html")

@app.route("/convert-csv-to-xero-csv", methods=["POST"])
def converttoxero():
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]

    try:
        df = transform_csv(file)
    except Exception as e:
        return str(e), 400

    # Convert DataFrame to CSV in memory
    buffer = StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    return send_file(
        BytesIO(buffer.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="converted.csv"
    )

@app.route("/180c-to-fahrenheit")
def page_180():
    return render_template("180c.html")

@app.route("/<temp>")
def dynamic_temp(temp):
    if temp == "180c-to-fahrenheit":
        value = "180°C = 350°F"
        use = "Perfect for cakes, cookies, and baking."
    elif temp == "200c-to-fahrenheit":
        value = "200°C = 392°F"
        use = "Great for roasting and crispy dishes."
    else:
        return "Not found", 404

    return render_template("temp_page.html", value=value, use=use)

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
                <p style="padding-left:10px;text-align:left">Great for beginners building full-stack apps.</p>

            <h2>2. Netlify</h2>
                <p style="padding-left:10px;text-align:left">Perfect for blogs and static sites.</p>

            <h2>3. Cloudflare Pages</h2>
                <p style="padding-left:10px;text-align:left">Best free hosting with unlimited bandwidth.</p>

            <h2>4. Railway</h2>
                <p style="padding-left:10px;text-align:left">Fast prototyping and deployment.</p>

            <h2>5. Vercel</h2>
                <p style="padding-left:10px;text-align:left">Best for frontend developers.</p>
        """
    },
    "free-hosting-pros-cons":{
        "title": "Pros and Cons of Free Web Hosting",
        "content": """
            <h1>Pros and Cons of Free Hosting for Beginners (2026 Guide)</h1>
            <h2>Pros:</h2>
            <ul style="text-align:left">
                <li>Zero Cost
                    <p style="text-align:left">You don’t pay anything to get started </p>
                    <p style="text-align:left">Perfect for beginners, students, and side projects</p>
                </li>
                <li>Easy Setup. Most platforms offer:
                    <p style="text-align:left">One-click deploy </p>
                    <p style="text-align:left">Githb integration</p>
                    <p style="text-align:left">Simple Dashboards </p>
                </li>
                <li>Great for learning and testing
                    <p style="text-align:left">Practice coding and test ideas</p>
                    <p style="text-align:left">Building portfolio </p>
                </li>
                <li>No Commitment
                    <p style="text-align:left">No contracts and you can stop at anytime</p>
                </li>
                <li>Basic Tools included like:
                    <p style="text-align:left">SSL</p>
                    <p style="text-align:left">Website Builder </p>
                    <p style="text-align:left">Git Integration </p>
                </li>
            </ul>
            <h2>Cons:</h2>
            <ul>
                <li>Slow Performance
                    <p style="text-align:left">Servers are shared with many users 
                    <p style="text-align:left">Can be slow and laggy</p>
                </li>
                <li>Sites might go offline
                    <p style="text-align:left">Sleep after inactivity" </p>
                </li>
                <li>Limited Resource
                    <p style="text-align:left">Storage Limits can be strict </p>
                    <p style="text-align:left">Bandwidth and CPU can be limited </p>
                </li>
                <li> Weak security and support
                    <p style="text-align:left">Limited security features </p>
                    <p style="text-align:left">No customer support </p>
                </li>
                <li> Hidden Upsells
                    <p style="text-align:left">You'll be pushed to upgrade </p>
                </li>

            </ul>
        """
    }
   }

    article = articles.get(slug)

    if not article:
            return "Article not found", 404

    return render_template("article.html", article=article)


@app.route("/privacy")
def privacy():
    return render_template("privacy-policy.html")


@app.route("/terms")
def terms_of_service():
    return render_template("terms.html")

@app.route("/tools")
def tools():
    return render_template("tools.html")

# New contact page route
@app.route("/contact")
def contact():
    load_dotenv()
    runenv = os.getenv("WHEREAMI")
    return render_template("contact.html", runenv=runenv)

@app.route("/send-message", methods=["POST"])
def send_message():
    label=""
    try:
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Create the email
        load_dotenv()
        email_user = os.getenv("EMAIL_USER")
        email_pwd = os.getenv("EMAIL_PWD")
        smtp_host = os.getenv("SMTP_HOST")
        #print(email_user)
        #print(email_pwd)

        msg = EmailMessage()
        msg['Subject'] = f'New message from {name}'
        msg['From'] = email_user
        msg['To'] = 'admin@conversiontoolshub.com'
        msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")

        # Send email via SMTP
        with smtplib.SMTP(smtp_host, 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(email_user, email_pwd) #nycteeytynvmixzu
            server.send_message(msg)
        label="email sent."
        #flash("Your message was sent successfully!", "success")
    except Exception as e:
        #print(e)
        #print(email_user)
        #print(email_pwd)
        label="There was an error sending your message. Please try again later."
        #flash("There was an error sending your message. Please try again.", "error")

    return render_template("contact.html", label=label)

@app.route("/cooking-measurement-tips")
def cooking_measurement_tips():
    return render_template("cooking-measurement-tips.html")

@app.route("/grams-vs-cups")
def grams_vs_cups():
    return render_template("grams-vs-cups.html")

@app.route("/grams-vs-ounce")
def gramsvsoz():
    return render_template("grams-vs-ounce.html")

@app.route("/grams-to-ounce/<string:subpage>", methods=["GET", "POST"])
def weightConverter(subpage):
    result = None
    if request.method == "POST":
        temp = float(request.form["temp"])
        conversion = request.form["conversion"]

        if conversion == "g_to_oz":
            converted = g_to_oz(temp)
            result = f"{temp} g = {converted:.6f} oz"
        elif conversion == "oz_to_g":
            converted = oz_to_g(temp)
            result = f"{temp} oz = {converted:.6f} g"
        elif conversion == "g_to_lbs":
            converted = g_to_lbs(temp)
            result = f"{temp} g = {converted:.6f} lbs"
        elif conversion == "lbs_to_g":
            converted = lbs_to_g(temp)
            result = f"{temp} lbs = {converted:.6f} g"
        elif conversion == "cups_to_ml":
            converted = cups_to_ml(temp)
            result = f"{temp} cups = {converted:.6f} ml"
        elif conversion == "ml_to_cups": 
            converted = ml_to_cups(temp)
            result = f"{temp} ml = {converted:.6f} cups"
        else:
            pass

    return render_template("grams-to-ounce.html", result=result, defselect=subpage)

@app.route("/cooking-conversion-tools", methods=["GET", "POST"])
def cookingConverter():
    #return render_template("cooking-converters.html")
    result = None
    if request.method == "POST":
        temp = float(request.form["temp"])
        conversion = request.form["conversion"]

        if conversion == "g_to_kg":
            converted = g_to_kg(temp)
            result = f"{temp} g = {converted:.5f} Kg"
        elif conversion == "kg_to_g":
            converted = kg_to_g(temp)
            result = f"{temp} Kg = {converted:.5f} g"
        elif conversion == "g_to_lbs":
            converted = g_to_lbs(temp)
            result = f"{temp} g = {converted:.5f} lbs"
        elif conversion == "lbs_to_g":
            converted = lbs_to_g(temp)
            result = f"{temp} lbs = {converted:.5f} g"
        elif conversion == "lbs_to_kg":
            converted = lbs_to_kg(temp)
            result = f"{temp} lbs = {converted:.5f} Kg"
        elif conversion == "kg_to_lbs": 
            converted = kg_to_lbs(temp)
            result = f"{temp} Kg = {converted:.5f} lbs"
        else:
            pass

    return render_template("cooking-converters.html", result=result)


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