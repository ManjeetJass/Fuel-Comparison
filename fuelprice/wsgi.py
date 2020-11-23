from flask import Flask, render_template, request, flash
from flask_wtf import CSRFProtect
import os
import checkfuelprice as fp
import settings as settings
import search_view as sv


# print("Current path: ", os.getcwd())
app = Flask(__name__)
app.config.from_object(settings.Config)
csrf = CSRFProtect(app)


@app.route('/', methods=('GET', 'POST'))
def search():
    form = sv.SearchForm(request.form)

    if form.validate_on_submit():
        if form.suburbs.data == '-1':
            flash('Please select suburb.', 'error')
            return render_template('search.html', form=form)

        if form.brand.data == '0':
            brand = 'All brands'
        else:
            brand = dict(form.brand.choices).get(int(form.brand.data))

        if form.surrounding.data == 'yes':
            surrounding = 'Yes'
        else:
            surrounding = 'No'

        selected_value = {
            'Product': dict(form.product.choices).get(int(form.product.data)),
            'Suburb': form.suburbs.data,
            'Brand': brand,
            'Surrounding': surrounding
        }

        df = fp.get_data(form.product.data, form.suburbs.data, form.brand.data, form.surrounding.data)
        return render_template('result.html', fuel_price=df, form=form, selected_value=selected_value)
    # else:
    #     print('Form error.', form.errors)
    return render_template('search.html', form=form)


@app.route('/result')
def success():
    return render_template('result.html')


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    app.run()
