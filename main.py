from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import json
# from pyarabic.araby import normalize_ligature

# with open('data/vocabulary.json') as f:
    # vocabulary_list = json.load(f)

verb_list = [    
    {
        "english": "to think",
        "infinitive": "فکر کردن",
        "present_root": [
            "فکر", "ک"    # note that the first or zeroth object is from right to left
        ]
    }
]


vocabulary_list = [
    {
        "english": "door",
        "farsi": {
            "written": "در",
            "spoken": ""
        }
    },
        {
        "english": "door",
        "farsi": {
            "written": "در",
            "spoken": ""
        }
    },
    {
        "english": "door",
        "farsi": {
            "written": "در",
            "spoken": ""
        }
    },
    {
        "english": "door",
        "farsi": {
            "written": "در",
            "spoken": ""
        }
    },
    {
        "english": "door",
        "farsi": {
            "written": "در",
            "spoken": ""
        }
    }
]

pronouns = {
    "me": {
        "written": "من",
        "spoken": ""
    },
    "you": {
        "written": "تو",
        "spoken": ""
    },
    "he/she": {
        "written": "او",
        "spoken": "اون"
    },
    "we": {
        "written": "ما",
        "spoken": ""
    },
    "you (respectful)": {
        "written": "شما",
        "spoken": ""
    },
    "they/them": {
        "written": "آنها",
        "spoken": "اونا"
    }
}

# present stem creation
# present_tense = []
# for verb in verb_list:












app = Flask(__name__)


@app.route('/test')
def test():
    stem = "رو"
    beginning = "می‌"
    end = "م"

    test_var = beginning + stem + end

    return render_template("test.html", test_var = test_var)


@app.route('/')
def splash():
    return render_template("splash.html")


@app.route('/vocabulary')
def vocabulary():
    return render_template("vocabulary.html", vocabulary=vocabulary_list)



# @app.route('/book/new/', methods=['GET', 'POST'])
# def newBook():
#     if request.method == 'POST':
#         new_name = request.form['name']
#         # check if there's a number missing between 1 through max
#         max_num = list(range(1,len(books)+1))
#         current_nums = []
#         for book in books:
#             current_nums.append(int(book['id']))
        
#         # get new id num
#         diff = [x for x in max_num if x not in current_nums]
#         if diff != []:
#             new_id = diff[0]
#         else:
#             new_id = len(books) + 1
        
#         # add to books
#         books.append({'title': new_name, 'id': str(new_id)})
#         return redirect(url_for('showBook'))
#     else:
#         return render_template('newBook.html')



# @app.route('/book/<int:book_id>/edit/', methods=['GET','POST'])
# def editBook(book_id):
#     if request.method == 'POST':
#         new_name = request.form['name']
#         for book in books:
#             if int(book['id']) == int(book_id):
#                 book['title'] = new_name
#                 break
#         return redirect(url_for('showBook'))
#     else:
#         single_book = {}
#         for oneBook in books:
#             if int(oneBook['id']) == int(book_id) :
#                 single_book = oneBook
#         return render_template('editBook.html', single_book = single_book)

	
# @app.route('/book/<int:book_id>/delete/', methods = ['GET', 'POST'])
# def deleteBook(book_id):
#     if request.method == 'POST':
#         for book in books:
#             if int(book['id']) == int(book_id):
#                 books.remove(book)
#                 break
#         return redirect(url_for('showBook'))
#     else:
#         single_book = {}
#         for oneBook in books:
#             if int(oneBook['id']) == book_id :
#                 single_book = oneBook
#         return render_template('deleteBook.html', single_book = single_book)


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
	

