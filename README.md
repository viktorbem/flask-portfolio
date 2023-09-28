# Personal Portfolio with Flask

<br>

### Getting started:

- Clone this repository
```bash
git clone git@github.com:viktorbem/flask-portfolio.git
```
- Install dependencies
```bash
pip install -r requirements.txt
sudo apt install wkhtmltopdf
```
- Run the app
```bash
flask run 
```

<br>

### Heroku deployment

It's necessary to include the `wkhtmltopdf` buildpack, e.g. via Heroku CLI:
```bash
heroku buildpacks:add https://github.com/dscout/wkhtmltopdf-buildpack.git
```