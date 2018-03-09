# Dependencies

import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template

app = Flask(__name__)

#################################################
# Database Setup
#################################################

# read sqlite db file
file = os.path.join("db", "belly_button_biodiversity.sqlite")

# create the engine
engine = create_engine(f"sqlite:///{file}")

# reflect the existing db
Base = automap_base()

# reflect all the tables
Base.prepare(engine, reflect=True)

# save tables in db as references

Samples_Metadata = Base.classes.samples_metadata
Otu = Base.classes.otu
Samples = Base.classes.samples

# create the session link
session = Session(engine)

#################################################
# Flask APIs Setup
#################################################

# make the API routes

# The homepage -- index.html
@app.route("/")
def index():
    # return render_template('index.html')

    return render_template('index.html')

# make the list of sample names


@app.route("/names")
def names():

    # get the statements
    state = session.query(Samples).statement
    df = pd.read_sql_query(state, session.bind)
    df.set_index("otu_id", inplace=True)

    return jsonify(list(df.columns))

# list of OTU descriptions


@app.route("/otu")
def otu():

    results = session.query(Otu.lowest_taxonomic_unit_found).all()

    # numpy revel to extract list of tuples into list of descriptions
    otu_list = list(np.ravel(results))

    return jsonify(otu_list)

# MetaData for given sample


@app.route("/metadata/<sample>")
def metadata(sample):

    # select the needed data
    selectData = [Samples_Metadata.SAMPLEID, Samples_Metadata.ETHNICITY,
                  Samples_Metadata.GENDER, Samples_Metadata.AGE,
                  Samples_Metadata.LOCATION, Samples_Metadata.BBTYPE]

    # get rid of BB_ for SAMPLIED
    results = session.query(*selectData).\
        filter(Samples_Metadata.SAMPLEID == sample[3:]).all()

    # make a dictionary out of the info above
    samples_metadata = {}

    for result in results:
        samples_metadata['SAMPLEID'] = result[0]
        samples_metadata['ETHNICITY'] = result[1]
        samples_metadata['GENDER'] = result[2]
        samples_metadata['AGE'] = result[3]
        samples_metadata['LOCATION'] = result[4]
        samples_metadata['BBTYPE'] = result[5]

    return jsonify(samples_metadata)

# Weekly washing freq as a number


@app.route("/wfreq/<sample>")
def wfreg(sample):

    # get rid of BB_
    results = session.query(Samples_Metadata.WFREQ).\
        filter(Samples_Metadata.SAMPLEID == sample[3:]).all()
    wfreg = np.ravel(results)

    return jsonify(int(wfreg[0]))

# Make a dictionary of 'otu_ids' and 'sample_values'


@app.route("/samples/<sample>")
def samples(sample):

    state = session.query(Samples).statement

    df = pd.read_sql_query(state, session.bind)

    # if sample is not there
    if sample not in df.columns:

        return jsonify(f"Warning! Sampl: {sample} Not Found!"), 400
    # return sample value grather than 1
    df = df[df[sample] > 1]

    # sorth the results in descending
    df = df.sort_values(by=sample, ascending=0)

    # format the data as json
    data = [{
        "otu_ids": df[sample].index.values.tolist(),
        "sample_values": df[sample].values.tolist()
    }]

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
