# pages/views.py
import pandas as pd
from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView
from keras.models import load_model


def formPageView(request):
    return render(request, 'form.html')


def aboutPageView(request):
    # return request object and specify page.
    return render(request, 'about.html')


def formPost(request):
    predList = ["Age",
                "Previously_Insured",
                "Annual_Premium",
                "Vintage",
                "Gender_Female", "Gender_Male",
                "Vehicle_Age_1-2 Year", "Vehicle_Age_< 1 Year", "Vehicle_Age_> 2 Years",
                "Vehicle_Damage_No", "Vehicle_Damage_Yes"]

    try:
        age = request.POST['age']

        gender = request.POST['gender']
        print(gender)
        if int(gender) == 0:
            gen_f, gen_m = 0, 1
        else:
            gen_f, gen_m = 1, 0

        v_age = request.POST['V_AGE']
        if v_age == 0:
            v_age_less_1, v_age_1_2, v_age_2_plus = 1, 0, 0
        elif v_age == 1:
            v_age_less_1, v_age_1_2, v_age_2_plus = 0, 1, 0
        else:
            v_age_less_1, v_age_1_2, v_age_2_plus = 0, 0, 1

        v_damage = request.POST['v_damage']
        if v_damage == 0:
            v_damage_y, v_damage_n = 0, 1
        else:
            v_damage_y, v_damage_n = 1, 0

        insured = request.POST['insured']

        premium = request.POST['premium']

        vintage = request.POST['vintage']

    except:
        return render(request, 'form.html', {
            'err': ""
        })
    return HttpResponseRedirect(reverse('results', kwargs={"age": age, "insured": insured, "premium": premium,
                                                           "vintage": vintage, "gen_f": gen_f, "gen_m": gen_m,
                                                           "v_age_1_2": v_age_1_2, "v_age_less_1": v_age_less_1,
                                                           "v_age_2_plus": v_age_2_plus,
                                                           "v_damage_n": v_damage_n, "v_damage_y": v_damage_y}, ))


def resultsPageView(request, age, insured, premium, vintage, gen_f, gen_m,
                    v_age_1_2, v_age_less_1, v_age_2_plus,
                    v_damage_n, v_damage_y):
    gender_text = "F" if gen_f else "M"
    age_text = str(age) + " years old"
    premium_text = "$"+str(premium)
    vintage_text = str(vintage) + " days"
    v_age_text = "Less than 1 year" if v_age_less_1 else "1 to 2 years" if v_age_1_2 else "More than 2 years"
    v_damage_text = "Yes" if v_damage_y else "No"
    insured_text = "Yes" if insured else "No"

    loadelModel = load_model('./model.h5')

    df = pd.DataFrame([{"Age": age, "Previously_Insured": insured, "Annual_Premium": premium,
                        "Vintage": vintage, "Gender_Female": gen_f, "Gender_Male": gen_m,
                        "Vehicle_Age_1-2 Year": v_age_1_2, "Vehicle_Age_< 1 Year": v_age_less_1,
                        "Vehicle_Age_> 2 Years": v_age_2_plus,
                        "Vehicle_Damage_No": v_damage_n, "Vehicle_Damage_Yes": v_damage_y}])
    print(df)

    singlePrediction = loadelModel.predict(df) > 0.5

    pred_part = "likely" if singlePrediction > 0.5 else "unlikely"
    pred_text = "It is " + pred_part + " that the customer will be interested in vehicular insurance under the same" \
                                       " company."
    return render(request, 'results.html', {'gender': gender_text, 'age': age_text, 'insured': insured_text,
                                            'premium': premium_text, 'vintage': vintage_text,
                                            'v_damage': v_damage_text, 'v_age': v_age_text, 'pred': pred_text})
