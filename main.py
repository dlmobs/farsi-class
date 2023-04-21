from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import random
import json
import ast
# from pyarabic.araby import normalize_ligature

mee_stem = "می‌"

pronouns = {"me": { "written": "من", "spoken": "" },
            "you": { "written": "تو", "spoken": "" },
            "he/she": { "written": "او", "spoken": "اون" },
            "we": { "written": "ما", "spoken": "" },
            "you (respectful)": { "written": "شما", "spoken": "" },
            "they/them": { "written": "آنها", "spoken": "اونا" }}

html_pronouns = {"me": "من",
            "you": "تو",
            "he/she": "او (اون)",
            "we": "ما",
            "you (respectful)": "شما",
            "they/them": "آنها (اونا)"}


present_tense = {"me": { "written": "م", "spoken": "" },
                "you": { "written": "ی", "spoken": "" },
                "he/she": { "written": "د", "spoken": "ه" },
                "we": { "written": "یم", "spoken": "" },
                "you (respectful)": { "written": "ید", "spoken": "ین" },
                "they/them": { "written": "ند", "spoken": "ن" }}

# simple past same as present except for he/she
past_tense = present_tense.copy()
past_tense["he/she"] = { "written": "", "spoken": "" }
# past progressive simple to make as well

present_perfect_tense = {"me": { "written": "ه‌ام", "spoken": "" },
                    "you": { "written": "ه‌ای", "spoken": "ی" },
                    "he/she": { "written": "ه‌اد", "spoken": "ه" },
                    "we": { "written": "ه‌ایم", "spoken": "یم" },
                    "you (respectful)": { "written": "ه‌اید", "spoken": "ین" },
                    "they/them": { "written": "ه‌اند", "spoken": "ن" }}

# NEED TO FIX THESE TWO  TENSES
past_perfect_tense = {"me": { "written": "ه‌ام", "spoken": "" },
                    "you": { "written": "ه‌ای", "spoken": "ی" },
                    "he/she": { "written": "ه‌اد", "spoken": "ه" },
                    "we": { "written": "ه‌ایم", "spoken": "یم" },
                    "you (respectful)": { "written": "ه‌اید", "spoken": "ین" },
                    "they/them": { "written": "ه‌اند", "spoken": "ن" }}

future_tense = {"me": { "written": "ه‌ام", "spoken": "" },
                    "you": { "written": "ه‌ای", "spoken": "ی" },
                    "he/she": { "written": "ه‌اد", "spoken": "ه" },
                    "we": { "written": "ه‌ایم", "spoken": "یم" },
                    "you (respectful)": { "written": "ه‌اید", "spoken": "ین" },
                    "they/them": { "written": "ه‌اند", "spoken": "ن" }}

tenses = {"Present Tense": present_tense, "Simple Past": past_tense, "Past Progressive": past_tense, 
            "Present Perfect": present_perfect_tense, "Past Perfect": past_perfect_tense, "Future Tense": future_tense}

verbs_list = [    
    {
        "counter": 1,
        "english": "to think",
        "infinitive": "فکر کردن",
        "present_root": {"written": ["فکر", "کن"], "spoken": [] },   # note that the first or zeroth object is from right to left
        "past_root": {"written": ["ره", "رو"], "spoken":  ["ره", "ر"] }   
    },
    {
        "counter": 2,
        "english": "to go",
        "infinitive": "رفتن",
        "present_root": {"written": ["رو"], "spoken": ["ر"] },
        "past_root": {"written": ["ره", "رو"], "spoken":  ["ره", "ر"] }
    },
    {
        "counter": 3,
        "english": "to go by foot/walk",
        "infinitive": "پیاده رفتن",
        "present_root": {"written": ["پیاده", "رو"], "spoken":  ["پیاده", "ر"] },
        "past_root": {"written": ["ره", "رو"], "spoken":  ["ره", "ر"] }
    },
    {
        "counter": 4,
        "english": "to go by foot (for people), \n\n to move (for automobiles)",
        "infinitive": "ره رفتن",
        "present_root": {"written": ["ره", "رو"], "spoken":  ["ره", "ر"] },
        "past_root": {"written": ["ره", "رو"], "spoken":  ["ره", "ر"] }
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


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


def capitalize_each_word(s):
    return ' '.join(word.capitalize() for word in s.split())

app.jinja_env.filters['capitalize_each_word'] = capitalize_each_word



@app.route('/test')
def test():
    stem = "رو"
    beginning = "می‌"
    end = "م"

    test_var = beginning + stem + end

    return render_template("test.html", test_var = test_var)

# splash page
@app.route('/')
def splash():
    return render_template("splash.html")

# vocabulary list page
@app.route('/vocabulary')
def vocabulary():
    return render_template("vocabulary.html", vocabulary=vocabulary_list)

# verbs list page
@app.route('/verbs')
def verbs():
    return render_template("verbs.html", verbs=verbs_list)

# specific verb page with all the conjugations
@app.route('/verbs/<int:index>')
def single_verb(index):
    word_dict_str = session.get('word_dict')
    word_dict = ast.literal_eval(word_dict_str)
    word_conjugations = {}

    # present tense set up
    present_tense_conjugations = {}
    for pronoun, pronoun_conj in present_tense.items():
        # written and spoken conjugation
        completed_conj = {}
        # key_w_s is "written" or "spoken"
        # conjugation is the written and spoken endings, so it can be empty
        for key_w_s, conjugation in pronoun_conj.items():
            completed_conj[key_w_s] = ""

            # originally running under the assumption that if there is no spoken form of stem, there is no spoken form conjugation for any. false
            # corner case: verb doesn't have spoken form but spoken for present for conjugation
            # solution: only create stem if not empty (first item always written so never empty). keeps second empty item from replacing first
            if word_dict["present_root"][key_w_s] != []:
                present_stem = word_dict["present_root"][key_w_s]   # stem string (written or spoken stem)

            # if the conjugation has a spoken form
            fully_conj_verb = ""
            if conjugation != "":
                # performed this way to avoid adding a space at the end of full_conj_verb and run into issues with strip function and farsi characters
                for i, word in enumerate(present_stem):
                    # add first word if a 2+ word verb
                    if i == 0 and len(present_stem) > 1:
                        fully_conj_verb = word + " "
                    # add second word
                    else:
                        fully_conj_verb = fully_conj_verb + mee_stem + word + conjugation
                        # print("second word added", fully_conj_verb)
                
                if key_w_s == "spoken":
                    fully_conj_verb = "(" + fully_conj_verb + ")"
                completed_conj[key_w_s] = fully_conj_verb



        # add it to the present tense conjugations
        present_tense_conjugations[pronoun] = completed_conj

    # update word_conjugations with present tense ones
    word_conjugations["present_t"] = present_tense_conjugations
    print(completed_conj)

    word_dict["present_tense"] = present_tense_conjugations


    return render_template('single_verb.html', word_dict=word_dict, pronouns_dict=html_pronouns)


@app.route('/set_word_dict/<word_dict>')
def set_word_dict(word_dict):
    session['word_dict'] = word_dict
    word_dict_for_counter = ast.literal_eval(word_dict)
    return redirect(url_for('single_verb', index=word_dict_for_counter["counter"]))

 
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
	

