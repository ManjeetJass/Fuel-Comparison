from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
import pandas as pd
from pathlib import Path
import os


class SearchForm(FlaskForm):
    # Get Data #
    data_folder = Path(os.getcwd() + "/static/data")

    bd = pd.read_csv(data_folder / "brand.csv")
    brandsCode = bd.values.tolist()

    pt = pd.read_csv(data_folder / "product.csv")
    productCode = pt.values.tolist()

    pr = pd.read_csv(data_folder / "perth_suburbs.csv")
    suburbCode = pr.values.tolist()

    SURROUNDING_CHOICES = [('yes', 'Yes'), ('no', 'No')]

    """Search form."""
    product = SelectField('Product', choices=productCode, default=2)
    brand = SelectField('Brand', choices=brandsCode)
    suburbs = SelectField('Suburbs', choices=suburbCode, default='Queens Park')
    surrounding = SelectField('Surrounding Suburbs', choices=SURROUNDING_CHOICES, default=0)
    submit = SubmitField('Submit')
