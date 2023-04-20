from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import json
# from pyarabic.araby import normalize_ligature

mee_stem = "می‌"

pronouns = {"me": { "written": "من", "spoken": "" },
            "you": { "written": "تو", "spoken": "" },
            "he/she": { "written": "او", "spoken": "اون" },
            "we": { "written": "ما", "spoken": "" },
            "you (respectful)": { "written": "شما", "spoken": "" },
            "they/them": { "written": "آنها", "spoken": "اونا" }
}


present_tense = {"me": { "written": "م", "spoken": "" },
                "you": { "written": "ی", "spoken": "" },
                "he/she": { "written": "د", "spoken": "ه" },
                "we": { "written": "یم", "spoken": "" },
                "you (respectful)": { "written": "ید", "spoken": "ین" },
                "they/them": { "written": "ند", "spoken": "ن" }
}

# simple past same as present except for he/she
past_tense = present_tense.copy()
past_tense = past_tense["he/she"] = { "written": "", "spoken": "" }
# past progressive simple to make as well

present_perfect_tense = {"me": { "written": "ه‌ام", "spoken": "" },
                    "you": { "written": "ه‌ای", "spoken": "ی" },
                    "he/she": { "written": "ه‌اد", "spoken": "ه" },
                    "we": { "written": "ه‌ایم", "spoken": "یم" },
                    "you (respectful)": { "written": "ه‌اید", "spoken": "ین" },
                    "they/them": { "written": "ه‌اند", "spoken": "ن" }
}

# NEED TO FIX THESE TWO  TENSES
past_perfect_tense = {"me": { "written": "ه‌ام", "spoken": "" },
                    "you": { "written": "ه‌ای", "spoken": "ی" },
                    "he/she": { "written": "ه‌اد", "spoken": "ه" },
                    "we": { "written": "ه‌ایم", "spoken": "یم" },
                    "you (respectful)": { "written": "ه‌اید", "spoken": "ین" },
                    "they/them": { "written": "ه‌اند", "spoken": "ن" }
}

future_tense = {"me": { "written": "ه‌ام", "spoken": "" },
                    "you": { "written": "ه‌ای", "spoken": "ی" },
                    "he/she": { "written": "ه‌اد", "spoken": "ه" },
                    "we": { "written": "ه‌ایم", "spoken": "یم" },
                    "you (respectful)": { "written": "ه‌اید", "spoken": "ین" },
                    "they/them": { "written": "ه‌اند", "spoken": "ن" }
}

tenses = [present_tense, past_tense, past_tense, present_perfect_tense, past_perfect_tense, future_tense]

verbs_list = [    
    {
        "english": "to think",
        "infinitive": "فکر کردن",
        "present_root": {"written": ["فکر", "ک"], "spoken": [] }   # note that the first or zeroth object is from right to left
    },
        {
        "english": "to go",
        "infinitive": "رفتن",
        "present_root": {"written": ["رو"], "spoken": ["ر"] }
    },
        {
        "english": "to go by foot/walk",
        "infinitive": "پیاده رفتن",
        "present_root": {"written": ["پیاده", "رو"], "spoken":  ["پیاده", "ر"] }
    },
        {
        "english": "to go by foot (for people) \n to move (for automobiles)",
        "infinitive": "ره رفتن",
        "present_root": {"written": ["ره", "رو"], "spoken":  ["ره", "ر"] }
    },
]



vocabulary_list = [
    {
        "english": "door",
        "farsi": { "written": "در", "spoken": "" }
    },
        {
        "english": "door",
        "farsi": { "written": "در", "spoken": "" }
    }
]



# for item in verbs_list:
#     print(item)
#     print(item["english"])
#     print(item.infinitive)



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

print(verbs_list)
@app.route('/vocabulary')
def vocabulary():
    return render_template("vocabulary.html", vocabulary=vocabulary_list)


@app.route('/verbs')
def verbs():
    return render_template("verbs.html", verbs=verbs_list)

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
	

