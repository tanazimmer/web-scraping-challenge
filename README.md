# web-scraping-challenge

Create a Jupyter Notebook file called mission_to_mars.ipynb and use this to complete all of your scraping and analysis tasks. The following outlines what you need to scrape.
```
url = 'https://mars.nasa.gov/news/'

browser.visit(url)
html = browser.html
soup = bs(html, 'html.parser')
```

Start by converting your Jupyter notebook into a Python script called scrape_mars.py with a function called scrape that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.
```
def scrape_info():
    browser = init_browser()
```
    
Next, create a route called /scrape that will import your scrape_mars.py script and call your scrape function. (app.py)
```
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")
 ```

Create a template HTML file called index.html that will take the mars data dictionary and display all of the data in the appropriate HTML elements.
```
 <div class="row">
          <div class="col-md-12">
              <h3>Latest Mars News</h3>
                <h4>{{mars_data.first_title}}</h4>
                    <p>{{mars_data.first_paragraph}}</p>
          </div>
        </div>

        <div class ="row">
            <div class = "col-md-8">
                <h3>Mars Image</h3>
                <img src = "{{mars_data.image_url}}" alt ="Image of Mars">
            </div>
        </div>
        
        <div class ="row">
            <div class = "col-md-12">
                <h3>Mars Hemispheres</h3>

                {% for hemisphere in mars_data.hemis_df %}
                    <div class = "col-md-6">
                        <div class = "thumbnail">
                            <img src = "{{hemis_df}}">
                                <h3>{{hemis_df.Title}}</h3>
                            </div>
                        </div>
                {% endfor %}
                    </div>
```
