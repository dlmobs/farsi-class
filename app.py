from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import random
import json
import ast
# from pyarabic.araby import normalize_ligature
from verbs_vocab_list import verbs_list, vocabulary_list

mee_stem = "می‌"

# may be deleted: 
pronouns = {"me": { "written": "من", "spoken": "" },
            "you": { "written": "تو", "spoken": "" },
            "he/she": { "written": "او", "spoken": "اون" },
            "we": { "written": "ما", "spoken": "" },
            "you (respectful)": { "written": "شما", "spoken": "" },
            "they/them": { "written": "آنها", "spoken": "اونا" }}

# for html files
html_pronouns = {"me": "من",
            "you": "تو",
            "he/she": "او (اون)",
            "we": "ما",
            "you (respectful)": "شما",
            "they/them": "آنها (اونا)"}

html_tenses = [["Present Tense", "Simple Past"], ["Past Progressive", "Present Perfect"], ["Past Perfect", "Future Tense"]]

# tense set up
present_tense = {"me": { "written": "م", "spoken": "" },
                "you": { "written": "ی", "spoken": "" },
                "he/she": { "written": "د", "spoken": "ه" },
                "we": { "written": "یم", "spoken": "" },
                "you (respectful)": { "written": "ید", "spoken": "ین" },
                "they/them": { "written": "ند", "spoken": "ن" }}

# simple past same as present except for he/she
past_tense = present_tense.copy()
past_tense["he/she"] = { "written": "", "spoken": "" }

present_perfect_tense = {"me": { "written": "ه‌ام", "spoken": "" },
                    "you": { "written": "ه‌ای", "spoken": "ی" },
                    "he/she": { "written": "ه است", "spoken": "ه" },
                    "we": { "written": "ه‌ایم", "spoken": "یم" },
                    "you (respectful)": { "written": "ه‌اید", "spoken": "ین" },
                    "they/them": { "written": "ه‌اند", "spoken": "ن" }}

past_perfect_tense = {"me": { "written": "ه بودم", "spoken": "" },
                    "you": { "written": "ه بودی", "spoken": "" },
                    "he/she": { "written": "ه بود", "spoken": "" },
                    "we": { "written": "ه بودیم", "spoken": "" },
                    "you (respectful)": { "written": "ه یودید", "spoken": "ه بودین" },
                    "they/them": { "written": "ه بودند", "spoken": "ه بودن" }}

# optimized by removing spoken, since future only used in written
future_tense = {"me": { "written": "خواهم" },
                    "you": { "written": "خواهی" },
                    "he/she": { "written": "خواهد" },
                    "we": { "written": "خواهیم" },
                    "you (respectful)": { "written": "خواهید" },
                    "they/them": { "written": "خواهند" }}


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# root used for each tense
roots = {"Present Tense": "present_root", "Simple Past": "past_root", "Past Progressive": "past_root", 
            "Present Perfect": "past_root", "Past Perfect": "past_root", "Future Tense": "past_root"}

tenses = {"Present Tense": present_tense, "Simple Past": past_tense, "Past Progressive": past_tense, 
            "Present Perfect": present_perfect_tense, "Past Perfect": past_perfect_tense, "Future Tense": future_tense}

def capitalize_each_word(s):
    ''' perform capitalization for a given english phrase in frontend call '''
    return ' '.join(word.capitalize() for word in s.split())

app.jinja_env.filters['capitalize_each_word'] = capitalize_each_word


# example word_dict
    # {
    #     "counter": 1,
    #     "english": "to think",
    #     "infinitive": "فکر کردن",
    #     "present_root": {"written": ["فکر", "کن"], "spoken": [] },    * note that the first or zeroth object is from right to left *
    #     "past_root": {"written": ["ره", "رو"], "spoken":  ["ره", "ر"] }   
    # }

def single_verb_conjugations(word_dict):
    ''' conjugate a given verb '''

    # loop through each tense
    for tense_name, tense_conjugations in tenses.items():
        # a single tense conjugation for all pronouns
        verb_tense_conjugations = {}
        root_needed = roots[tense_name]

        # written and spoken form of the root
        w_s_root = word_dict[root_needed]

        # loop through each pronoun and it's ending
        for pronoun, pronoun_endings in tense_conjugations.items():
            # completed written and spoken conjugation
            completed_conj = {"written": "", "spoken": ""}

            # key_w_s is "written" or "spoken"
            # conjugation is the written and spoken endings, so it can be empty
            for key_w_s, conjugation in pronoun_endings.items():

                # originally running under the assumption that if there is no spoken form of stem, there is no spoken form conjugation for any. false
                # corner case: verb doesn't have spoken form but spoken for present for conjugation
                # solution: only create stem if not empty (first item always written so never empty). keeps second empty item from replacing first
                if w_s_root[key_w_s] != []:
                    root = w_s_root[key_w_s]            # stem string (written or spoken stem)

                    # root is a list of the root. sometimes two worded root

                # if the conjugation doesn't have a spoken form, then conjugation is empty
                fully_conj_verb = ""
                if conjugation != "":
                    # performed this way to avoid adding a space at the end of full_conj_verb and run into issues with strip function and farsi characters
                    for i, word in enumerate(root):
                        # add first word if a 2+ word verb
                        if i == 0 and len(root) > 1:
                            fully_conj_verb = word + " "
                        # add second word
                        else:
                            if tense_name == "Present Tense" or tense_name == "Past Progressive":
                                fully_conj_verb = fully_conj_verb + mee_stem + word + conjugation
                            elif tense_name == "Future Tense":
                                fully_conj_verb = fully_conj_verb + conjugation + " " + word
                            # simple past, present perfect, past perfect
                            else:
                                fully_conj_verb = fully_conj_verb + word + conjugation

                    # add parenthesis
                    if key_w_s == "spoken":
                        fully_conj_verb = "(" + fully_conj_verb + ")"
                    completed_conj[key_w_s] = fully_conj_verb

            # add it to the respective conjugations for the tense
            verb_tense_conjugations[pronoun] = completed_conj

        # update word_dict with present tense ones
        word_dict[tense_name] = verb_tense_conjugations
    
    return word_dict


# app routes
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

# about page
@app.route('/about')
def about():
    return render_template("about.html")

# vocabulary list page
@app.route('/vocabulary-list')
def vocabulary():
    return render_template("vocabulary.html", vocabulary=vocabulary_list)

# verbs list page
@app.route('/verb-list')
def verbs():
    return render_template("verbs.html", verbs=verbs_list)

# specific verb page with all the conjugations
@app.route('/verbs/<int:index>')
def single_verb(index):
    word_dict_str = session.get('word_dict')
    word_dict = ast.literal_eval(word_dict_str)
    word_dict_tenses = single_verb_conjugations(word_dict)

    return render_template('single_verb.html', word_dict=word_dict_tenses, pronouns_dict=html_pronouns, tense_order = html_tenses)

# redirct/helper route for specific verb page
@app.route('/set_word_dict/<word_dict>')
def set_word_dict(word_dict):
    session['word_dict'] = word_dict
    word_dict_for_counter = ast.literal_eval(word_dict)
    return redirect(url_for('single_verb', index=word_dict_for_counter["counter"]))


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)