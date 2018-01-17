from flask import Flask, render_template, render_template_string, request
import crawler
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')


@app.route('/crawl', methods=['POST'])
def login():
    if request.method == 'POST':
        page = crawler.render_page(request.form.get('url', None), request.form.get('recursive', None))
        return render_template_string(page)
    else:
        error = 'Invalid method'
        # the code below is executed if the request method was GET
        return render_template('error.html', error=error)

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80)