from flask import Flask, render_template, redirect, url_for, session, request
import random
import json
import ast
# from pyarabic.araby import normalize_ligature
from verbs_list import verbs_list, current_counter
from vocab_list import vocabulary_list
from html_helpers import capitalize_each_word, combine_list, capitalize_first_word

mee_stem = "می‌"
b_stem = "ب"

pronouns = {"they/them": { "written": "آنها", "spoken": "اونا" },
            "you (respectful)": { "written": "شما", "spoken": "" },
            "we": { "written": "ما", "spoken": "" },
            "he/she": { "written": "او", "spoken": "اون" },
            "you": { "written": "تو", "spoken": "" },
            "me": { "written": "من", "spoken": "" }}

html_tenses = ["Present Tense", "Simple Past", "Past Progressive", "Present Perfect", "Past Perfect", "Future Tense", "Imperative", "Subjunctive"]

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

present_perfect_tense = {"me": { "written": "ه‌ام", "spoken": "م" },
                    "you": { "written": "ه‌ای", "spoken": "ی" },
                    "he/she": { "written": "ه است", "spoken": "ه" },
                    "we": { "written": "ه‌ایم", "spoken": "یم" },
                    "you (respectful)": { "written": "ه‌اید", "spoken": "ین" },
                    "they/them": { "written": "ه‌اند", "spoken": "ن" }}

past_perfect_tense = {"me": { "written": "ه بودم", "spoken": "" },
                    "you": { "written": "ه بودی", "spoken": "" },
                    "he/she": { "written": "ه بود", "spoken": "" },
                    "we": { "written": "ه بودیم", "spoken": "" },
                    "you (respectful)": { "written": "ه بودید", "spoken": "ه بودین" },
                    "they/them": { "written": "ه بودند", "spoken": "ه بودن" }}

# optimized by removing spoken, since future only used in written
future_tense = {"me": { "written": "خواهم" },
                    "you": { "written": "خواهی" },
                    "he/she": { "written": "خواهد" },
                    "we": { "written": "خواهیم" },
                    "you (respectful)": { "written": "خواهید" },
                    "they/them": { "written": "خواهند" }}

# imperative same as present except for you
imperative_tense = present_tense.copy()
imperative_tense["you"] = { "written": "", "spoken": "" }

# subjunctive conjugations is the same as present tense

# root used for each tense
roots = {"Present Tense": "Pres. Stem", "Simple Past": "Past Stem", "Past Progressive": "Past Stem", 
            "Present Perfect": "Past Stem", "Past Perfect": "Past Stem", "Future Tense": "Past Stem",
            "Imperative": "Pres. Stem", "Subjunctive": "Pres. Stem"}

# beginning used for each tense
beginnings = {"Present Tense": mee_stem, "Simple Past": "", "Past Progressive": mee_stem, "Present Perfect": "", 
              "Past Perfect": "", "Future Tense": "", "Imperative": b_stem, "Subjunctive": b_stem}

# all tense conjugations
tenses = {"Present Tense": present_tense, "Simple Past": past_tense, "Past Progressive": past_tense, 
            "Present Perfect": present_perfect_tense, "Past Perfect": past_perfect_tense, "Future Tense": future_tense,
            "Imperative": imperative_tense, "Subjunctive": present_tense}



app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.jinja_env.filters['capitalize_each_word'] = capitalize_each_word
app.jinja_env.filters['combine_list'] = combine_list
app.jinja_env.filters['capitalize_first_word'] = capitalize_first_word


def single_verb_conjugations(word_dict):
    ''' conjugate a given verb '''

    # loop through each tense
    for tense_name, tense_conjugations in tenses.items():
        # a single tense conjugation for all pronouns
        verb_tense_conjugations = {}
        root_needed = roots[tense_name]

        # written and spoken form of the root
        w_s_roots = word_dict[root_needed]

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
                if w_s_roots[key_w_s] != []:
                    root = w_s_roots[key_w_s]            # stem string (written or spoken stem)
                    # root is a list of the root. sometimes two worded root

                # if the conjugation doesn't have a spoken form, then conjugation is empty
                # if no conjugation and stem spoken form, then full conjugation stays as ""
                fully_conj_verb = ""
                if conjugation != "" or w_s_roots[key_w_s] != []:
                    # loop through each word in a given root. some can be two words
                    for i, word in enumerate(root):
                        # add first word if a 2+ word verb
                        if i == 0 and len(root) > 1:
                            fully_conj_verb = word + " "
                        # add second word
                        else:
                            if tense_name == "Present Tense":
                                # if Pres. Stem has spoken form, need to use the written endings for conjugation
                                if conjugation == "":
                                    conjugation = pronoun_endings["written"]
                                fully_conj_verb = fully_conj_verb + mee_stem + word + conjugation
                            elif tense_name == "Imperative":
                                # do not use spoken stem for you conj. no you spoken for imperative
                                if pronoun == "you" and key_w_s == "spoken":
                                    break
                                fully_conj_verb = fully_conj_verb + b_stem + word + conjugation
                            elif tense_name == "Subjunctive":
                                # if Pres. Stem has spoken form, need to use the written endings for conjugation
                                if conjugation == "":
                                    conjugation = pronoun_endings["written"]
                                fully_conj_verb = fully_conj_verb + b_stem + word + conjugation
                            elif tense_name == "Past Progressive":
                                fully_conj_verb = fully_conj_verb + mee_stem + word + conjugation
                            elif tense_name == "Future Tense":
                                fully_conj_verb = fully_conj_verb + conjugation + " " + word
                            # simple past, present perfect, past perfect
                            else:
                                fully_conj_verb = fully_conj_verb + word + conjugation

                    completed_conj[key_w_s] = fully_conj_verb

            # add it to the respective conjugations for the tense
            verb_tense_conjugations[pronoun] = completed_conj

        # update word_dict with present tense ones
        # word_dict[tense_name] = dict(list(reversed(list(verb_tense_conjugations.items()))))
        word_dict[tense_name] = verb_tense_conjugations
    
    return word_dict


def conjugation_formulas():
    ''' conjugation formulas for conjugation page '''
    formulas = {}

    # loop through each tense
    for tense_name, tense_conjs in tenses.items():
        needed_root = roots[tense_name]
        needed_beg = beginnings[tense_name]

        tense_formulas = {}

        # loop through each pronoun and its dict of conjugations (w,s)
        for pronoun, w_s_conj in tense_conjs.items():
            w_s_conj_formula = w_s_conj.copy()
            ending = w_s_conj["written"]

            if tense_name == "Future Tense":
                single_formula =  ending + " " + needed_root
            else:
                single_formula = ending + " + " + needed_root + " + " + needed_beg

            single_formula = single_formula.strip(' + ')
            w_s_conj_formula["written"] = single_formula

            tense_formulas[pronoun] = w_s_conj_formula

        formulas[tense_name] = dict(list(reversed(list(tense_formulas.items()))))
    
    return formulas


# app routes
# splash page
@app.route('/')
def splash():
    return render_template("splash.html")

# about page
@app.route('/about')
def about():
    return render_template("about.html")

# login page
@app.route('/login')
def login_page():
    return render_template("login.html")

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
    return render_template('single_verb.html', word_dict=word_dict_tenses, tense_order=html_tenses, pronouns_dict=pronouns)

# redirct/helper route for specific verb page
@app.route('/set_word_dict/<word_dict>')
def set_word_dict(word_dict):
    session['word_dict'] = word_dict
    word_dict_for_counter = ast.literal_eval(word_dict)
    return redirect(url_for('single_verb', index=word_dict_for_counter["counter"]))

# conjugations page
@app.route('/tenses')
def tenses_page():
    conj_formulas = conjugation_formulas()
    return render_template("conjugations.html", conj_formulas=conj_formulas, tenses=html_tenses, pronouns=pronouns)

# exceptions page
@app.route('/exceptions')
def exceptions_page():
    return render_template("exceptions.html")


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0')