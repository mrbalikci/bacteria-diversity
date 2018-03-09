# Interactive Belly Button Biodiversity


An interactive dashboard was created to explore the [Belly Button Biodiversity DataSet](http://robdunnlab.com/projects/belly-button-biodiversity/).

## Flask API Set Up

Used Flask to design an API for the dataset and to serve the HTML and JavaScript required for the dashboard page. 
Sqlite database file and SQLAlchemy inside of the Flask application code was used for the database as JSON file format. 


* Created a template called `index.html` for the dashboard landing page. Used the Bootstrap grid system to create the structure of the dashboard page.

* Created the following routes for the api. 

```python
@app.route("/")
    """Return the dashboard homepage."""
```
```python
@app.route('/names')
    """List of sample names.

    Returns a list of sample names in the format
    [
        "BB_940",
        "BB_941",
        "BB_943",
        "BB_944",
        "BB_945",
        "BB_946",
        "BB_947",
        ...
    ]

    """
```
```python
@app.route('/otu')
    """List of OTU descriptions.

    Returns a list of OTU descriptions in the following format

    [
        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
        "Bacteria",
        "Bacteria",
        "Bacteria",
        ...
    ]
    """ 
```
```python
@app.route('/metadata/<id>')
    """MetaData for a given sample.

    Args: Sample in the format: `BB_940`

    Returns a json dictionary of sample metadata in the format

    {
        AGE: 24,
        BBTYPE: "I",
        ETHNICITY: "Caucasian",
        GENDER: "F",
        LOCATION: "Beaufort/NC",
        SAMPLEID: 940
    }
    """
```
```python
@app.route('/wfreq/<id>')
    """Weekly Washing Frequency as a number.

    Args: Sample in the format: `BB_940`

    Returns an integer value for the weekly washing frequency `WFREQ`
    """
```
```python
@app.route('/samples/<id>')
    """OTU IDs and Sample Values for a given sample.

    Sort the Pandas DataFrame (OTU ID and Sample Value)
    in Descending Order by Sample Value

    Return a list of dictionaries containing sorted lists  for `otu_ids`
    and `sample_values`

    [
        {
            otu_ids: [
                1166,
                2858,
                481,
                ...
            ],
            sample_values: [
                163,
                126,
                113,
                ...
            ]
        }
    ]
    """
```

--- 

## Plotly.js Setup

Used Plotly.js to build interactive charts for the dashboard.

* Used the route `/names` to populate a dropdown select element with the list of sample names.

  * Used `document.getElementById`, `document.createElement` and `append` to populate the create option elements and append them to the dropdown selector.

  * Used the following HTML tag for the dropdown selector

  ```html
  <select id="selDataset" onchange="optionChanged(this.value)"></select>
  ```
  * Created a function called `optionChanged` to handle the change event when a new sample is selected (i.e. fetch data for the newly selected sample).


* Created a PIE chart that uses data from the routes `/samples/<id>` and `/otu` to display the top 10 samples.

  * Used the Sample Value as the values for the PIE chart

  * Used the OTU ID as the labels for the pie chart

  * Used the OTU Description as the hovertext for the chart

  * Used `Plotly.restyle` to update the chart whenever a new sample is selected



* Created a Bubble Chart that uses data from the routes `/samples/<id>` and `/otu` to plot the __Sample Value__ vs the __OTU ID__ for the selected sample.

  * Used the OTU IDs for the x values

  * Used the Sample Values for the y values

  * Used the Sample Values for the marker size

  * Used the OTU IDs for the marker colors 

  * Used the OTU Description Data for the text values

  * Used `Plotly.restyle` to update the chart whenever a new sample is selected



* Displayed the sample metadata from the route `/metadata/<id>`

  * Displayed each key/value pair from the metadata JSON object somewhere on the page

  * Updated the metadata for each sample that is selected

* Finally, deployed the Flask app to Heroku.

