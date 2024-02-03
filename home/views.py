from .forms import SuggestionForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from .forms import SchoolSignUpForm
from django.http import HttpResponse
from .managers import CustomUserManager
from .forms import GovernmentSignUpForm
from home.models import contactEnquiry
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Count
from .forms import DistrictSignUpForm
from .models import Suggestion
from .models import SuggestionDis
from .models import Suggestion_state_to_sch
from .models import SchoolYearData
from .forms import SuggestionDistForm
from .forms import SuggestionStateToSchForm
from .models import DropoutPrediction  # Import the model for storing predictions
from sklearn.neighbors import KNeighborsClassifier
# from django.template.loader import get_template
# from xhtml2pdf import pisa

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from .models import CustomUser
from .forms import SchoolYearDataForm
from django.contrib import messages
from operator import itemgetter

# Manually create some sample data

# Create your views here.

def index(request):
    return render(request,'index.html')

def school_index(request):
    if request.user.is_anonymous or not request.user.is_school_user or not request.user.is_approved:
        return redirect("/login")
        
    user_dist = request.user.District
    user_school = request.user.username
    user_state = request.user.state
    
    username=request.user.username
    suggestions = SuggestionDis.objects.filter(district_name__iexact=user_dist,school_name__iexact=username)
    suggestions_G_to_S = Suggestion_state_to_sch.objects.filter(school_name__iexact=user_school,state_name__iexact=user_state)
    
      
    enquiries = contactEnquiry.objects.filter(user=request.user)
    school_data = SchoolYearData.objects.filter(school=request.user,district=request.user.District)
    context = {'enquiries': enquiries, 'suggestions': suggestions,'suggestions_G_to_S':suggestions_G_to_S,'school_data':school_data,'enquiries':enquiries}
    return render(request, 'school_index.html', context)

def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)

        
        if user is not None and user.is_school_user and user.is_approved:
            login(request,user)
            user_dist = request.user.District
            user_school = request.user.username
            user_state = request.user.state
            username=request.user.username
            suggestions = SuggestionDis.objects.filter(district_name__iexact=user_dist,school_name__iexact=username)
            suggestions_G_to_S = Suggestion_state_to_sch.objects.filter(school_name__iexact=user_school,state_name__iexact=user_state)
            enquiries = contactEnquiry.objects.filter(user=request.user)
            school_data = SchoolYearData.objects.filter(school=request.user,district=request.user.District)
            return render(request,'school_index.html',{
                'suggestions': suggestions,
                'school_data':school_data,
                'suggestions_G_to_S':suggestions_G_to_S,
                'enquiries':enquiries,
            })
        else:
            return render(request, 'School-login.html')

    return render(request, 'School-login.html')

def logoutUser(request):
   logout(request)
   return redirect("/login")


def gov_index(request):

    if request.user.is_anonymous or not request.user.is_government_user :
        return redirect("/logingov")
    
    year=2023
    user_state = request.user.state
    school_data = SchoolYearData.objects.filter(
        year=year,
        state=request.user.state,
                
    )
                 # Get the total count of students for the selected year and district
    total_students_count_year = school_data.aggregate(Sum('total_students'))['total_students__sum']
    total_students =total_students_count_year
    ttotal_dropout_students = contactEnquiry.objects.filter(mystate__iexact=user_state,Year=year).count()
    percentage_dropout = (ttotal_dropout_students / total_students) * 100  if total_students is not None and total_students != 0 else 0 #my change
    percentage_dropout = round(percentage_dropout, 4)
    
    # age_group_0_5 = contactEnquiry.objects.filter(mystate__iexact=user_state, age__range=(0, 5)).count()
    age_group_0_5 = contactEnquiry.objects.filter(mystate__iexact=user_state,age__gte=1,age__lte=5,Year=year).count()
    age_group_6_10 = contactEnquiry.objects.filter(mystate__iexact=user_state, age__gte=6,age__lte=10,Year=year).count()
    age_group_11_15 = contactEnquiry.objects.filter(mystate__iexact=user_state, age__gte=11,age__lte=15,Year=year).count()
    age_group_16_20 = contactEnquiry.objects.filter(mystate__iexact=user_state, age__gte=16,age__lte=20,Year=year).count()


    male_dropout_students=contactEnquiry.objects.filter(gender__iexact='male',mystate__iexact=user_state,Year=year).count()
    female_dropout_students=contactEnquiry.objects.filter(gender__iexact='female',mystate__iexact=user_state,Year=year).count()
    total_dropout_fm_student = male_dropout_students + female_dropout_students
    
   
    totaldropout_OPEN = contactEnquiry.objects.filter(mystate__iexact=user_state,caste__iexact='open',Year=year).count()
    totaldropout_ST = contactEnquiry.objects.filter(mystate__iexact=user_state,caste__iexact='st',Year=year).count()
    totaldropout_SC = contactEnquiry.objects.filter(mystate__iexact=user_state,caste__iexact='sc',Year=year).count()
    totaldropout_OBC = contactEnquiry.objects.filter(mystate__iexact=user_state,caste__iexact='obc',Year=year).count()

    income_range_0 = (0,10000)
    income_range_1 = (10001, 50000)
    income_range_2 = (50001, 100000)
    # income_range_3 = (100001, float('inf'))

    total_dropout_range_0 = contactEnquiry.objects.filter(mystate__iexact=user_state,  income__range=income_range_0,Year=year).count()
    total_dropout_range_1 = contactEnquiry.objects.filter(mystate__iexact=user_state,  income__range=income_range_1,Year=year).count()
    total_dropout_range_2 = contactEnquiry.objects.filter(mystate__iexact=user_state, income__range=income_range_2,Year=year).count()
    total_dropout_range_3 = contactEnquiry.objects.filter(mystate__iexact=user_state,  income__gte=100001,Year=year).count()

    reason_indices = contactEnquiry.objects.filter(mystate__iexact=user_state,Year=year).values_list('reason', flat=True).distinct()
    dropout_reason_counts = contactEnquiry.objects.filter(mystate__iexact=user_state,Year=year).values('reason').annotate(total_r_dropouts=Count('id'))
    dropout_reason_dict = {item['reason']: item['total_r_dropouts'] for item in dropout_reason_counts}
    
    school_indices = contactEnquiry.objects.filter(mystate__iexact=user_state,Year=year).values_list('schoolindex', flat=True).distinct()
    dropout_counts = contactEnquiry.objects.filter(mystate__iexact=user_state,Year=year).values('schoolindex').annotate(total_dropouts=Count('id'))
    dropout_dict = {item['schoolindex']: item['total_dropouts'] for item in dropout_counts}


    combined_data = []
    for school_index in school_indices:
        total_dropout_students = dropout_dict.get(school_index, 0)

        # Fetch total students separately
        school_data = SchoolYearData.objects.filter(
            school__username=school_index,  # Assuming the username is the school index
            year=year,
            state=user_state,          
        ).first()

        total_students = school_data.total_students if school_data else 0

        male_dropout_students_school_wise = contactEnquiry.objects.filter(
            gender='male',
            schoolindex=school_index,
            mystate__iexact=user_state,
            Year=year
        ).count()

        female_dropout_students_school_wise = contactEnquiry.objects.filter(
            gender='female',
            schoolindex=school_index,
            mystate__iexact=user_state,
            Year=year
        ).count()

        dropout_ratio = (total_dropout_students / total_students) * 100 if total_students > 0 else 0
        dropout_ratio = round(dropout_ratio, 2)

        combined_data.append({
            'school_index': school_index,
            'total_dropout_students': total_dropout_students,
            'total_students': total_students,
            'male_dropout_students_school_wise': male_dropout_students_school_wise,
            'female_dropout_students_school_wise': female_dropout_students_school_wise,
            'dropout_ratio': dropout_ratio,
        })
         # below variable for city wise counting 
    
    dropout_counts_city = contactEnquiry.objects.filter(mystate__iexact=user_state, Year=year).values('city').annotate(
        total_dropouts=Count('id')
    )
    dropout_dict_city = {item['city']: item['total_dropouts'] for item in dropout_counts_city}


    cities = contactEnquiry.objects.filter(mystate__iexact=user_state, Year=year).values_list('city', flat=True).distinct()
    total_students_data_city = SchoolYearData.objects.filter(
    school__state=user_state,
    year=year
    ).values('district').annotate(total_students=Sum('total_students'))

    total_students_dict_city = {data['district']: data['total_students'] for data in total_students_data_city}

    # Combine data for the table
    combined_data_city = []
    for city in cities:
        total_dropout_students_city = dropout_dict_city.get(city, 0)
        total_students_city = total_students_dict_city.get(city, 0)
        
        male_dropout_students_city = contactEnquiry.objects.filter(
            gender='male',
            city=city,
            mystate__iexact=user_state,
            Year=year
        ).count()

        female_dropout_students_city = contactEnquiry.objects.filter(
            gender='female',
            city=city,
            mystate__iexact=user_state,
            Year=year
        ).count()

        # Calculate dropout ratio for the city
        dropout_ratio_city = (total_dropout_students_city / total_students_city) * 100 if total_students_city > 0 else 0
        dropout_ratio_city = round(dropout_ratio_city, 2)

        combined_data_city.append({
            'city': city,
            'total_dropout_students': total_dropout_students_city,
            'total_students': total_students_city,
            'male_dropout_students_city':male_dropout_students_city,
            'female_dropout_students_city':female_dropout_students_city,
            'dropout_ratio_city':dropout_ratio_city,
        })
    user_state=request.user.state
    suggestions = SuggestionDis.objects.filter(state_name__iexact=user_state)

    pending_district = CustomUser.objects.filter(is_district_user=True, is_approved=False,state__iexact=user_state)
    approved_district = CustomUser.objects.filter(is_district_user=True, is_approved=True,state__iexact=user_state)


    totaldropout_Private = contactEnquiry.objects.filter(mystate__iexact=user_state,s_category__iexact='Private',Year=year).count()
    totaldropout_Government = contactEnquiry.objects.filter(mystate__iexact=user_state,s_category__iexact='Government',Year=year).count()
    totaldropout_SemiGovernment = contactEnquiry.objects.filter(mystate__iexact=user_state,s_category__iexact='SemiGovernment',Year=year).count()
    total_dropout_private_ratio = (totaldropout_Private/ttotal_dropout_students)*100 if ttotal_dropout_students is not None and ttotal_dropout_students != 0 else 0
    total_dropout_private_ratio = round(total_dropout_private_ratio, 2)

    total_dropout_goverm_ratio = (totaldropout_Government/ttotal_dropout_students)*100 if ttotal_dropout_students is not None and ttotal_dropout_students != 0 else 0
    total_dropout_goverm_ratio = round(total_dropout_goverm_ratio, 2)

    top_schools = sorted(combined_data, key=itemgetter('dropout_ratio'), reverse=True)[:3]

    top_districts = sorted(combined_data_city, key=itemgetter('dropout_ratio_city'), reverse=True)[:3]

    suggestion_from_state_to_district = Suggestion.objects.filter(state_name__iexact=user_state)
    suggestion_from_state_to_school = Suggestion_state_to_sch.objects.filter(state_name__iexact=user_state)

    
    # context = {
    #     'dropout_counts': dropout_dict,
    #     # Other context variables
    # }
    return render(request, 'gov_index.html',{
        'total_students': total_students,
        'ttotal_dropout_students': ttotal_dropout_students,
        'percentage_dropout': percentage_dropout,
        'age_group_0_5':age_group_0_5,
        'age_group_6_10':age_group_6_10,
        'age_group_11_15':age_group_11_15,
        'age_group_16_20':age_group_16_20,
        'male_dropout_students':male_dropout_students,
        'female_dropout_students':female_dropout_students,
        'total_dropout_fm_student':total_dropout_fm_student,
        'totaldropout_OPEN':totaldropout_OPEN,
        'totaldropout_ST':totaldropout_ST,
        'totaldropout_SC':totaldropout_SC,
        'totaldropout_OBC':totaldropout_OBC,
        'total_dropout_range_0':total_dropout_range_0,
        'total_dropout_range_1':total_dropout_range_1,
        'total_dropout_range_2':total_dropout_range_2,
        'total_dropout_range_3':total_dropout_range_3,
        'reason_indices':reason_indices,
        'dropout_reason_counts':dropout_reason_dict,
        'school_indices':school_indices,
        'dropout_counts':dropout_dict,
        'cities':cities,
        'dropout_counts_city':dropout_dict_city,
        'suggestions':suggestions,
        'pending_district':pending_district,
        'approved_district':approved_district,
        'year':year,
        'total_students_count_year':total_students_count_year,
        'combined_data':combined_data,
        'combined_data_city':combined_data_city,
        'totaldropout_Private':totaldropout_Private,
        'totaldropout_Government':totaldropout_Government,
        'totaldropout_SemiGovernment':totaldropout_SemiGovernment,
        'total_dropout_private_ratio':total_dropout_private_ratio,
        'total_dropout_goverm_ratio':total_dropout_goverm_ratio,
        'top_schools':top_schools,
        'top_districts':top_districts,
        'suggestion_from_state_to_district':suggestion_from_state_to_district,
        'suggestion_from_state_to_school':suggestion_from_state_to_school


        
        })





def gov_index_filtered(request):

    if request.user.is_anonymous or not request.user.is_government_user :
        return redirect("/logingov")
    
    year = request.GET.get('year', '')
    
    user_state = request.user.state

    school_data = SchoolYearData.objects.filter(
        year=year,
        state=request.user.state,
                
    )
                # Get the total count of students for the selected year and district
    total_students_count_year = school_data.aggregate(Sum('total_students'))['total_students__sum']
    total_students =total_students_count_year
    ttotal_dropout_students = contactEnquiry.objects.filter(mystate__iexact=user_state,Year=year).count()
    percentage_dropout = (ttotal_dropout_students / total_students) * 100 if total_students is not None and total_students != 0 else 0
    percentage_dropout = round(percentage_dropout, 4)
    # age_group_0_5 = contactEnquiry.objects.filter(mystate__iexact=user_state, age__range=(0, 5)).count()
    age_group_0_5 = contactEnquiry.objects.filter(mystate__iexact=user_state,age__gte=1,age__lte=5,Year=year).count()
    age_group_6_10 = contactEnquiry.objects.filter(mystate__iexact=user_state, age__gte=6,age__lte=10,Year=year).count()
    age_group_11_15 = contactEnquiry.objects.filter(mystate__iexact=user_state, age__gte=11,age__lte=15,Year=year).count()
    age_group_16_20 = contactEnquiry.objects.filter(mystate__iexact=user_state, age__gte=16,age__lte=20,Year=year).count()


    male_dropout_students=contactEnquiry.objects.filter(gender__iexact='male',mystate__iexact=user_state,Year=year).count()
    female_dropout_students=contactEnquiry.objects.filter(gender__iexact='female',mystate__iexact=user_state,Year=year).count()
    total_dropout_fm_student = male_dropout_students + female_dropout_students
    
   
    totaldropout_OPEN = contactEnquiry.objects.filter(mystate__iexact=user_state,caste__iexact='open',Year=year).count()
    totaldropout_ST = contactEnquiry.objects.filter(mystate__iexact=user_state,caste__iexact='st',Year=year).count()
    totaldropout_SC = contactEnquiry.objects.filter(mystate__iexact=user_state,caste__iexact='sc',Year=year).count()
    totaldropout_OBC = contactEnquiry.objects.filter(mystate__iexact=user_state,caste__iexact='obc',Year=year).count()

    income_range_0 = (0,10000)
    income_range_1 = (10001, 50000)
    income_range_2 = (50001, 100000)
    # income_range_3 = (100001, float('inf'))

    total_dropout_range_0 = contactEnquiry.objects.filter(mystate__iexact=user_state,  income__range=income_range_0,Year=year).count()
    total_dropout_range_1 = contactEnquiry.objects.filter(mystate__iexact=user_state,  income__range=income_range_1,Year=year).count()
    total_dropout_range_2 = contactEnquiry.objects.filter(mystate__iexact=user_state, income__range=income_range_2,Year=year).count()
    total_dropout_range_3 = contactEnquiry.objects.filter(mystate__iexact=user_state,  income__gte=100001,Year=year).count()

    reason_indices = contactEnquiry.objects.filter(mystate__iexact=user_state,Year=year).values_list('reason', flat=True).distinct()
    dropout_reason_counts = contactEnquiry.objects.filter(mystate__iexact=user_state,Year=year).values('reason').annotate(total_r_dropouts=Count('id'))
    dropout_reason_dict = {item['reason']: item['total_r_dropouts'] for item in dropout_reason_counts}
    
    school_indices = contactEnquiry.objects.filter(mystate__iexact=user_state,Year=year).values_list('schoolindex', flat=True).distinct()
    dropout_counts = contactEnquiry.objects.filter(mystate__iexact=user_state,Year=year).values('schoolindex').annotate(total_dropouts=Count('id'))
    dropout_dict = {item['schoolindex']: item['total_dropouts'] for item in dropout_counts}


    combined_data = []
    for school_index in school_indices:
        total_dropout_students = dropout_dict.get(school_index, 0)

        # Fetch total students separately
        school_data = SchoolYearData.objects.filter(
            school__username=school_index,  # Assuming the username is the school index
            year=year,
            state=user_state,          
        ).first()

        total_students = school_data.total_students if school_data else 0

        male_dropout_students_school_wise = contactEnquiry.objects.filter(
            gender='male',
            schoolindex=school_index,
            mystate__iexact=user_state,
            Year=year
        ).count()

        female_dropout_students_school_wise = contactEnquiry.objects.filter(
            gender='female',
            schoolindex=school_index,
            mystate__iexact=user_state,
            Year=year
        ).count()

        dropout_ratio = (total_dropout_students / total_students) * 100 if total_students > 0 else 0
        dropout_ratio = round(dropout_ratio, 2)

        combined_data.append({
            'school_index': school_index,
            'total_dropout_students': total_dropout_students,
            'total_students': total_students,
            'male_dropout_students_school_wise': male_dropout_students_school_wise,
            'female_dropout_students_school_wise': female_dropout_students_school_wise,
            'dropout_ratio': dropout_ratio,
        })

     # below variable for city wise counting 
    dropout_counts_city = contactEnquiry.objects.filter(mystate__iexact=user_state, Year=year).values('city').annotate(
        total_dropouts=Count('id')
    )
    dropout_dict_city = {item['city']: item['total_dropouts'] for item in dropout_counts_city}


    cities = contactEnquiry.objects.filter(mystate__iexact=user_state, Year=year).values_list('city', flat=True).distinct()
    total_students_data_city = SchoolYearData.objects.filter(
    school__state=user_state,
    year=year
    ).values('district').annotate(total_students=Sum('total_students'))

    total_students_dict_city = {data['district']: data['total_students'] for data in total_students_data_city}

    # Combine data for the table
    combined_data_city = []
    for city in cities:
        total_dropout_students_city = dropout_dict_city.get(city, 0)
        total_students_city = total_students_dict_city.get(city, 0)
        
        male_dropout_students_city = contactEnquiry.objects.filter(
            gender='male',
            city=city,
            mystate__iexact=user_state,
            Year=year
        ).count()

        female_dropout_students_city = contactEnquiry.objects.filter(
            gender='female',
            city=city,
            mystate__iexact=user_state,
            Year=year
        ).count()

        # Calculate dropout ratio for the city
        dropout_ratio_city = (total_dropout_students_city / total_students_city) * 100 if total_students_city > 0 else 0
        dropout_ratio_city = round(dropout_ratio_city, 2)
        combined_data_city.append({
            'city': city,
            'total_dropout_students': total_dropout_students_city,
            'total_students': total_students_city,
            'male_dropout_students_city':male_dropout_students_city,
            'female_dropout_students_city':female_dropout_students_city,
            'dropout_ratio_city':dropout_ratio_city,
        })
    user_state=request.user.state
    suggestions = SuggestionDis.objects.filter(state_name__iexact=user_state)

    pending_district = CustomUser.objects.filter(is_district_user=True, is_approved=False,state__iexact=user_state)
    approved_district = CustomUser.objects.filter(is_district_user=True, is_approved=True,state__iexact=user_state)


    totaldropout_Private = contactEnquiry.objects.filter(mystate__iexact=user_state,s_category__iexact='Private',Year=year).count()
    totaldropout_Government = contactEnquiry.objects.filter(mystate__iexact=user_state,s_category__iexact='Government',Year=year).count()
    totaldropout_SemiGovernment = contactEnquiry.objects.filter(mystate__iexact=user_state,s_category__iexact='SemiGovernment',Year=year).count()
    total_dropout_private_ratio = (totaldropout_Private/ttotal_dropout_students)*100 if ttotal_dropout_students is not None and ttotal_dropout_students != 0 else 0
    total_dropout_private_ratio = round(total_dropout_private_ratio, 2)
    total_dropout_goverm_ratio = (totaldropout_Government/ttotal_dropout_students)*100 if ttotal_dropout_students is not None and ttotal_dropout_students != 0 else 0
    total_dropout_goverm_ratio = round(total_dropout_goverm_ratio, 2)
    

    top_schools = sorted(combined_data, key=itemgetter('dropout_ratio'), reverse=True)[:3]
    top_districts = sorted(combined_data_city, key=itemgetter('dropout_ratio_city'), reverse=True)[:3]


    suggestion_from_state_to_district = Suggestion.objects.filter(state_name__iexact=user_state)
    suggestion_from_state_to_school = Suggestion_state_to_sch.objects.filter(state_name__iexact=user_state)

    
    # context = {
    #     'dropout_counts': dropout_dict,
    #     # Other context variables
    # }
    return render(request, 'gov_index.html',{
        'total_students': total_students,
        'ttotal_dropout_students': ttotal_dropout_students,
        'percentage_dropout': percentage_dropout,
        'age_group_0_5':age_group_0_5,
        'age_group_6_10':age_group_6_10,
        'age_group_11_15':age_group_11_15,
        'age_group_16_20':age_group_16_20,
        'male_dropout_students':male_dropout_students,
        'female_dropout_students':female_dropout_students,
        'total_dropout_fm_student':total_dropout_fm_student,
        'totaldropout_OPEN':totaldropout_OPEN,
        'totaldropout_ST':totaldropout_ST,
        'totaldropout_SC':totaldropout_SC,
        'totaldropout_OBC':totaldropout_OBC,
        'total_dropout_range_0':total_dropout_range_0,
        'total_dropout_range_1':total_dropout_range_1,
        'total_dropout_range_2':total_dropout_range_2,
        'total_dropout_range_3':total_dropout_range_3,
        'reason_indices':reason_indices,
        'dropout_reason_counts':dropout_reason_dict,
        'school_indices':school_indices,
        'dropout_counts':dropout_dict,
        'cities':cities,
        'dropout_counts_city':dropout_dict_city,
        'suggestions':suggestions,
        'pending_district':pending_district,
        'approved_district':approved_district,
        'year':year,
        'total_students_count_year':total_students_count_year,
        'combined_data':combined_data,
        'combined_data_city':combined_data_city,
        'totaldropout_Private':totaldropout_Private,
        'totaldropout_Government':totaldropout_Government,
        'totaldropout_SemiGovernment':totaldropout_SemiGovernment,
        'total_dropout_private_ratio':total_dropout_private_ratio,
        'total_dropout_goverm_ratio':total_dropout_goverm_ratio,
        'top_schools':top_schools,
        'top_districts':top_districts,
        'suggestion_from_state_to_district':suggestion_from_state_to_district,
        'suggestion_from_state_to_school':suggestion_from_state_to_school,
        })








def loginUsergov(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # total_students =100 last my change
        year=2023
        user = authenticate(username=username,password=password)
        if user is not None and user.is_government_user :
            login(request,user)
            user_state = request.user.state
            school_data = SchoolYearData.objects.filter(
            year=year,
            state=request.user.state,
                )
                        # Get the total count of students for the selected year and district
            total_students_count_year = school_data.aggregate(Sum('total_students'))['total_students__sum']
            total_students =total_students_count_year
            ttotal_dropout_students = contactEnquiry.objects.filter(mystate__iexact=user_state,Year=year).count()
            percentage_dropout = (ttotal_dropout_students / total_students) * 100 if total_students is not None and total_students != 0 else 0
            percentage_dropout = round(percentage_dropout, 4)

            age_group_0_5 = contactEnquiry.objects.filter(mystate__iexact=user_state,age__gte=1,age__lte=5,Year=year).count()
            age_group_6_10 = contactEnquiry.objects.filter(mystate__iexact=user_state, age__gte=6,age__lte=10,Year=year).count()
            age_group_11_15 = contactEnquiry.objects.filter(mystate__iexact=user_state, age__gte=11,age__lte=15,Year=year).count()
            age_group_16_20 = contactEnquiry.objects.filter(mystate__iexact=user_state, age__gte=16,age__lte=20,Year=year).count()

            male_dropout_students=contactEnquiry.objects.filter(gender__iexact='male',mystate__iexact=user_state,Year=year).count()
            female_dropout_students=contactEnquiry.objects.filter(gender__iexact='female',mystate__iexact=user_state,Year=year).count()
            total_dropout_fm_student = (male_dropout_students + female_dropout_students)

            totaldropout_OPEN = contactEnquiry.objects.filter(mystate__iexact=user_state,caste__iexact='open',Year=year).count()
            totaldropout_ST = contactEnquiry.objects.filter(mystate__iexact=user_state,caste__iexact='st',Year=year).count()
            totaldropout_SC = contactEnquiry.objects.filter(mystate__iexact=user_state,caste__iexact='sc',Year=year).count()
            totaldropout_OBC = contactEnquiry.objects.filter(mystate__iexact=user_state,caste__iexact='obc',Year=year).count()

            income_range_0 = (0,10000)
            income_range_1 = (10000, 50000)
            income_range_2 = (50000, 100000)
            # income_range_3 = (100000, float('inf'))


            total_dropout_range_0 = contactEnquiry.objects.filter(mystate__iexact=user_state,  income__range=income_range_0,Year=year).count()
            total_dropout_range_1 = contactEnquiry.objects.filter(mystate__iexact=user_state,  income__range=income_range_1,Year=year).count()
            total_dropout_range_2 = contactEnquiry.objects.filter(mystate__iexact=user_state, income__range=income_range_2,Year=year).count()
            total_dropout_range_3 = contactEnquiry.objects.filter(mystate__iexact=user_state,  income__gte=100001,Year=year).count()

            reason_indices = contactEnquiry.objects.filter(mystate__iexact=user_state,Year=year).values_list('reason', flat=True).distinct()
            dropout_reason_counts = contactEnquiry.objects.filter(mystate__iexact=user_state,Year=year).values('reason').annotate(total_r_dropouts=Count('id'))
            dropout_reason_dict = {item['reason']: item['total_r_dropouts'] for item in dropout_reason_counts}

            # below variable for school wise counting 
            school_indices = contactEnquiry.objects.filter(mystate__iexact=user_state,Year=year).values_list('schoolindex', flat=True).distinct()
            dropout_counts = contactEnquiry.objects.filter(mystate__iexact=user_state,Year=year).values('schoolindex').annotate(total_dropouts=Count('id'))
            dropout_dict = {item['schoolindex']: item['total_dropouts'] for item in dropout_counts}

            # below variable for city wise counting 
            dropout_counts_city = contactEnquiry.objects.filter(mystate__iexact=user_state, Year=year).values('city').annotate(
                total_dropouts=Count('id')
            )
            dropout_dict_city = {item['city']: item['total_dropouts'] for item in dropout_counts_city}


            cities = contactEnquiry.objects.filter(mystate__iexact=user_state, Year=year).values_list('city', flat=True).distinct()
            total_students_data_city = SchoolYearData.objects.filter(
                school__state=user_state,
                year=year
            ).values('district').annotate(total_students=Sum('total_students'))

            total_students_dict_city = {data['district']: data['total_students'] for data in total_students_data_city}

            # Combine data for the table
            combined_data_city = []
            for city in cities:
                total_dropout_students_city = dropout_dict_city.get(city, 0)
                total_students_city = total_students_dict_city.get(city, 0)


                male_dropout_students_city = contactEnquiry.objects.filter(
                    gender='male',
                    city=city,
                    mystate__iexact=user_state,
                    Year=year
                ).count()

                female_dropout_students_city = contactEnquiry.objects.filter(
                    gender='female',
                    city=city,
                    mystate__iexact=user_state,
                    Year=year
                ).count()

                # Calculate dropout ratio for the city
                dropout_ratio_city = (total_dropout_students_city / total_students_city) * 100 if total_students_city > 0 else 0
                dropout_ratio_city = round(dropout_ratio_city, 2)
                combined_data_city.append({
                    'city': city,
                    'total_dropout_students': total_dropout_students_city,
                    'total_students': total_students_city,
                    'male_dropout_students_city':male_dropout_students_city,
                    'female_dropout_students_city':female_dropout_students_city,
                    'dropout_ratio_city':dropout_ratio_city,
                })
            # city_counts = contactEnquiry.objects.filter(mystate__iexact=user_state).values('city').annotate(total_dropouts=Count('id'))
            # city_counts_dict = {item['city']: item['total_dropouts'] for item in city_counts}
            user_state=request.user.state
            suggestions = SuggestionDis.objects.filter(state_name__iexact=user_state)

            pending_district = CustomUser.objects.filter(is_district_user=True, is_approved=False,state__iexact=user_state)
            approved_district = CustomUser.objects.filter(is_district_user=True, is_approved=True,state__iexact=user_state)

            school_data = SchoolYearData.objects.filter(
                year=year,
                state=request.user.state,
                
            )
            combined_data = []
            for school_index in school_indices:
                total_dropout_students = dropout_dict.get(school_index, 0)

                # Fetch total students separately
                school_data = SchoolYearData.objects.filter(
                    school__username=school_index,  # Assuming the username is the school index
                    year=year,
                    state=user_state,
                    
                ).first()

                total_students = school_data.total_students if school_data else 0

                male_dropout_students_school_wise = contactEnquiry.objects.filter(
                    gender='male',
                    schoolindex=school_index,
                    mystate__iexact=user_state,
                    Year=year
                ).count()

                female_dropout_students_school_wise = contactEnquiry.objects.filter(
                    gender='female',
                    schoolindex=school_index,
                    mystate__iexact=user_state,
                    Year=year
                ).count()

                dropout_ratio = (total_dropout_students / total_students) * 100 if total_students > 0 else 0
                dropout_ratio = round(dropout_ratio, 2)
                combined_data.append({
                    'school_index': school_index,
                    'total_dropout_students': total_dropout_students,
                    'total_students': total_students,
                    'male_dropout_students_school_wise': male_dropout_students_school_wise,
                    'female_dropout_students_school_wise': female_dropout_students_school_wise,
                    'dropout_ratio': dropout_ratio,
                })

                # Get the total count of students for the selected year and district
            total_students_count_year = SchoolYearData.objects.filter(
                year=year,
                state=request.user.state,
            ).aggregate(Sum('total_students'))['total_students__sum']

            totaldropout_Private = contactEnquiry.objects.filter(mystate__iexact=user_state,s_category__iexact='Private',Year=year).count()
            totaldropout_Government = contactEnquiry.objects.filter(mystate__iexact=user_state,s_category__iexact='Government',Year=year).count()
            totaldropout_SemiGovernment = contactEnquiry.objects.filter(mystate__iexact=user_state,s_category__iexact='SemiGovernment',Year=year).count()
            total_dropout_private_ratio = (totaldropout_Private/ttotal_dropout_students)*100 if ttotal_dropout_students is not None and ttotal_dropout_students != 0 else 0
            total_dropout_private_ratio = round(total_dropout_private_ratio, 2)
            total_dropout_goverm_ratio = (totaldropout_Government/ttotal_dropout_students)*100 if ttotal_dropout_students is not None and ttotal_dropout_students != 0 else 0
            total_dropout_goverm_ratio = round(total_dropout_goverm_ratio, 2)

            top_schools = sorted(combined_data, key=itemgetter('dropout_ratio'), reverse=True)[:3]

            top_districts = sorted(combined_data_city, key=itemgetter('dropout_ratio_city'), reverse=True)[:3]

            suggestion_from_state_to_district = Suggestion.objects.filter(state_name__iexact=user_state)
            suggestion_from_state_to_school = Suggestion_state_to_sch.objects.filter(state_name__iexact=user_state)

            


            return render(request, 'gov_index.html',{
            'total_students': total_students,
            'ttotal_dropout_students': ttotal_dropout_students,
            'percentage_dropout': percentage_dropout,
            'age_group_0_5':age_group_0_5,
            'age_group_6_10':age_group_6_10,
            'age_group_11_15':age_group_11_15,
            'age_group_16_20':age_group_16_20,
            'male_dropout_students':male_dropout_students,
            'female_dropout_students':female_dropout_students,
            'total_dropout_fm_student':total_dropout_fm_student,
            'totaldropout_OPEN':totaldropout_OPEN,
            'totaldropout_ST':totaldropout_ST,
            'totaldropout_SC':totaldropout_SC,
            'totaldropout_OBC':totaldropout_OBC,
            'total_dropout_range_0':total_dropout_range_0,
            'total_dropout_range_1':total_dropout_range_1,
            'total_dropout_range_2':total_dropout_range_2,
            'total_dropout_range_3':total_dropout_range_3,
            'reason_indices':reason_indices,
            'dropout_reason_counts':dropout_reason_dict,
            'school_indices':school_indices,
            'dropout_counts':dropout_dict,
            # 'dropout_counts_city': dropout_dict_city,  # For city-wise
            # 'cities': cities,
            # 'city_counts':city_counts_dict,
            'cities':cities,
            'dropout_counts_city':dropout_dict_city,
            'suggestions':suggestions,
            'pending_district':pending_district,
            'approved_district':approved_district,
            'year':year,
            'total_students_count_year':total_students_count_year,
            'combined_data':combined_data,
            'combined_data_city':combined_data_city,
            'totaldropout_Private':totaldropout_Private,
            'totaldropout_Government':totaldropout_Government,
            'totaldropout_SemiGovernment':totaldropout_SemiGovernment,
            'total_dropout_private_ratio':total_dropout_private_ratio,
            'total_dropout_goverm_ratio':total_dropout_goverm_ratio,
            'top_schools':top_schools,
            'top_districts':top_districts,
            'suggestion_from_state_to_district':suggestion_from_state_to_district,
            'suggestion_from_state_to_school':suggestion_from_state_to_school,

            })
        
        else:
            return render(request, 'gov_login.html')

    return render(request, 'gov_login.html')   

def approve_district(request, distrct_id):
    district = get_object_or_404(CustomUser, id=distrct_id)
    district.is_approved = True
    district.save()
    # Add logic to notify the school about approval
    # ...
    return redirect('/gov_index')

def logoutUsergov(request):
   logout(request)
   return redirect("/logingov")  



# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SchoolSignUpForm
from django.http import JsonResponse
def school_signup(request):
    if request.method == 'POST':
        form = SchoolSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_school_user = True
            user.is_approved = False
            user.password=make_password(user.password)
            user.save()
            login(request, user)  # Log in the user after signing up
            return redirect('/school_index')  # Redirect to the school dashboard or any other page
        else:
           print(form.errors)
    else:
        form = SchoolSignUpForm()

    return render(request, 'school_signup.html', {'form': form})



def government_signup(request):
    if request.method == 'POST':
        form = GovernmentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.is_government_user = True
            state_id = form.cleaned_data.get('state_id')
            state = form.cleaned_data.get('state')
            state_ids = {'Andhra Pradesh': '1', 'Arunachal Pradesh': '2',
            'Assam': '3','Bihar': '4','Chhattisgarh': '5','Goa': '6','Gujarat': '7',
            'Haryana': '8','Himachal Pradesh': '9','Jharkhand': '10','Karnataka': '11','Kerala': '12',
            'Madhya Pradesh': '13','Maharashtra': '14','Manipur': '15','Meghalaya': '16','Mizoram': '17',
            'Nagaland': '18','Odisha': '19','Punjab': '20','Rajasthan': '21','Sikkim': '22',
            'Tamil Nadu': '23','Telangana': '24','Tripura': '25','Uttar Pradesh': '26','Uttarakhand': '27',
             'West Bengal': '28','Delhi': '30'}

            if state_id != state_ids.get(state, ''):                
                
                return render(request, 'gov_login.html')
            user.save()
            login(request, user)  # Log in the user after signing up
            return redirect('/gov_index')  # Redirect to the school dashboard or any other page
    else:
        form = GovernmentSignUpForm()

    return render(request, 'gov_login.html', {'form': form})

# views.py


   

def saveEnquiry(request):
    
    # user_dist = request.user.District
    # user_school = request.user.username
    # user_state = request.user.state
    
    # username=request.user.username
    # suggestions = SuggestionDis.objects.filter(district_name__iexact=user_dist,school_name__iexact=username)
    # suggestions_G_to_S = Suggestion_state_to_sch.objects.filter(school_name__iexact=user_school,state_name__iexact=user_state)
    
      
    # school_data = SchoolYearData.objects.filter(school=request.user,district=request.user.District)
    if request.method=="POST":
        current_user = request.user
        name=request.POST.get('name')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        caste=request.POST.get('caste')
        s_category=request.POST.get('s_category')
        Distance=request.POST.get('Distance')
        area=request.POST.get('area')
        city=request.POST.get('city')
        income=request.POST.get('income')
        reason=request.POST.get('reason')
        foccupation=request.POST.get('foccupation')
        schoolindex=request.POST.get('schoolindex')
        mystate=request.POST.get('mystate')
        studentid=request.POST.get('studentid')
        Year=request.POST.get('Year')
        en=contactEnquiry(name=name,age=age,gender=gender,caste=caste,s_category=s_category,Distance=Distance,area=area,city=city,income=income,reason=reason,foccupation=foccupation,schoolindex=schoolindex,mystate=mystate,studentid=studentid,user=current_user,Year=Year)
        en.save()
        


    # context = {'enquiries': enquiries, 'suggestions': suggestions,'suggestions_G_to_S':suggestions_G_to_S,'school_data':school_data,}
    # enquiries = contactEnquiry.objects.filter(user=request.user)
    return redirect('/school_index')




@login_required(login_url='{% url "login" %}')  # Replace 'your_login_url' with the actual login URL
def delete_student_data(request, pk):
    student = get_object_or_404(contactEnquiry, pk=pk)
    
    # Check if the user has permission to delete the data
    # You might want to implement your own logic here based on your requirements
    
    student.delete()
    return redirect('/school_index')  # Redirect to the view after deletion

# district code

@login_required(login_url='{% url "login" %}')  # Replace 'your_login_url' with the actual login URL
def delete_suggesstion_from_district_to_school(request, pk):
    student = get_object_or_404(SuggestionDis, pk=pk)
    
    # Check if the user has permission to delete the data
    # You might want to implement your own logic here based on your requirements
    
    student.delete()
    return redirect('/district_index')  # Redirect to the view after deletion


@login_required(login_url='{% url "login" %}')  # Replace 'your_login_url' with the actual login URL
def delete_suggesstion_from_government_to_district(request, pk):
    student = get_object_or_404(Suggestion, pk=pk)
    
    # Check if the user has permission to delete the data
    # You might want to implement your own logic here based on your requirements
    
    student.delete()
    return redirect('/gov_index')  # Redirect to the view after deletion


@login_required(login_url='{% url "login" %}')  # Replace 'your_login_url' with the actual login URL
def delete_suggesstion_from_state_to_school(request, pk):
    student = get_object_or_404(Suggestion_state_to_sch, pk=pk)
    
    # Check if the user has permission to delete the data
    # You might want to implement your own logic here based on your requirements
    
    student.delete()
    return redirect('/gov_index')  # Redirect to the view after deletion



from django.db.models import Sum
def district_index(request):
    if request.user.is_anonymous or not request.user.is_district_user or not request.user.is_approved:
        return redirect("/logindis")
    
    year=2023

    user_dist = request.user.District
    student_data = contactEnquiry.objects.filter(city__iexact=user_dist,Year=year)

    suggestions = Suggestion.objects.filter(district_name__iexact=user_dist)
    # context = {'student_data': student_data, 'suggestions': suggestions}
    user_state = request.user.state
    age_group_0_5 = contactEnquiry.objects.filter(mystate__iexact=user_state,city__iexact=user_dist,age__gte=1,age__lte=5,Year=year).count()
    age_group_6_10 = contactEnquiry.objects.filter(mystate__iexact=user_state,city__iexact=user_dist,age__gte=6,age__lte=10,Year=year).count()
    age_group_11_15 = contactEnquiry.objects.filter(mystate__iexact=user_state,city__iexact=user_dist, age__gte=11,age__lte=15,Year=year).count()
    age_group_16_20 = contactEnquiry.objects.filter(mystate__iexact=user_state,city__iexact=user_dist, age__gte=16,age__lte=20,Year=year).count()

    male_dropout_students=contactEnquiry.objects.filter(gender__iexact='male',mystate__iexact=user_state,city__iexact=user_dist,Year=year).count()
    female_dropout_students=contactEnquiry.objects.filter(gender__iexact='female',mystate__iexact=user_state,city__iexact=user_dist,Year=year).count()
    total_dropout_fm_student = (male_dropout_students + female_dropout_students)

    
    income_range_0 = (0,10000)
    income_range_1 = (10000, 50000)
    income_range_2 = (50000, 100000)
    # income_range_3 = (100000, float('inf'))


    total_dropout_range_0 = contactEnquiry.objects.filter(mystate__iexact=user_state,  income__range=income_range_0,city__iexact=user_dist,Year=year).count()
    total_dropout_range_1 = contactEnquiry.objects.filter(mystate__iexact=user_state,  income__range=income_range_1,city__iexact=user_dist,Year=year).count()
    total_dropout_range_2 = contactEnquiry.objects.filter(mystate__iexact=user_state, income__range=income_range_2,city__iexact=user_dist,Year=year).count()
    total_dropout_range_3 = contactEnquiry.objects.filter(mystate__iexact=user_state,  income__gte=100001,city__iexact=user_dist,Year=year).count()



    school_indices = contactEnquiry.objects.filter(mystate__iexact=user_state, city__iexact=user_dist, Year=year).values_list('schoolindex', flat=True).distinct()
    dropout_counts = contactEnquiry.objects.filter(mystate__iexact=user_state, city__iexact=user_dist, Year=year).values('schoolindex').annotate(total_dropouts=Count('id'))
    dropout_dict = {item['schoolindex']: item['total_dropouts'] for item in dropout_counts}
    total_students_data = SchoolYearData.objects.filter(school__in=school_indices, year=year, state=user_state, district=user_dist)
    total_students_dict = {data.school_id: data.total_students for data in total_students_data}

    combined_data = []
    for school_index in school_indices:
        total_dropout_students = dropout_dict.get(school_index, 0)


        # Fetch total students separately
        school_data = SchoolYearData.objects.filter(
            school__username=school_index,  # Assuming the username is the school index
            year=year,
            state=user_state,
            district=user_dist
        ).first()

        male_dropout_students_school_wise = contactEnquiry.objects.filter(
            gender='male',
            schoolindex=school_index,
            mystate__iexact=user_state,
            city=user_dist,
            Year=year
        ).count()

        female_dropout_students_school_wise = contactEnquiry.objects.filter(
            gender='female',
            schoolindex=school_index,
            mystate__iexact=user_state,
            city=user_dist,
            Year=year
        ).count()

        total_students = school_data.total_students if school_data else 0
        dropout_ratio = (total_dropout_students / total_students) * 100 if total_students > 0 else 0
        dropout_ratio = round(dropout_ratio, 2)

        combined_data.append({
            'school_index': school_index,
            'total_dropout_students': total_dropout_students,
            'total_students': total_students,
            'male_dropout_students_school_wise':male_dropout_students_school_wise,
            'female_dropout_students_school_wise':female_dropout_students_school_wise,
            'dropout_ratio':dropout_ratio,


        })


    pending_schools = CustomUser.objects.filter(is_school_user=True, is_approved=False,District__iexact=user_dist)
    approved_school = CustomUser.objects.filter(is_school_user=True, is_approved=True,District__iexact=user_dist)

    school_data = SchoolYearData.objects.filter(
            year=year,
            state=request.user.state,
            district=request.user.District
        )
        # Get the total count of students for the selected year and district
    total_students_count_year = school_data.aggregate(Sum('total_students'))['total_students__sum']

    ttotal_dropout_students = contactEnquiry.objects.filter(mystate__iexact=user_state,Year=year,city=user_dist).count()

    distance_range_0 = (0,5)
    distance_range_1 = (6, 15)
    distance_range_2 = (16, 30)

    total_dropout_dist_range_0 = contactEnquiry.objects.filter(mystate__iexact=user_state,  Distance__range=distance_range_0,city__iexact=user_dist,Year=year).count()
    total_dropout_dist_range_1 = contactEnquiry.objects.filter(mystate__iexact=user_state,  Distance__range=distance_range_1,city__iexact=user_dist,Year=year).count()
    total_dropout_dist_range_2 = contactEnquiry.objects.filter(mystate__iexact=user_state, Distance__range=distance_range_2,city__iexact=user_dist,Year=year).count()
    total_dropout_dist_range_3 = contactEnquiry.objects.filter(mystate__iexact=user_state,  Distance__gte=31,city__iexact=user_dist,Year=year).count()
    
    tdropout_ratio = (ttotal_dropout_students/total_students_count_year)*100 if total_students_count_year is not None and total_students_count_year != 0 else 0
    tdropout_ratio = round(tdropout_ratio, 2)


    suggestion_from_district_to_school = SuggestionDis.objects.filter(district_name__iexact=user_dist,state_name__iexact=user_state)
    return render(request, 'district_index.html',{
        'student_data':student_data,
        'suggestions':suggestions,
        'age_group_0_5':age_group_0_5,
        'age_group_6_10':age_group_6_10,
        'age_group_11_15':age_group_11_15,
        'age_group_16_20':age_group_16_20,
        'male_dropout_students':male_dropout_students,
        'female_dropout_students':female_dropout_students,
        'total_dropout_fm_student':total_dropout_fm_student,
        'total_dropout_range_0':total_dropout_range_0,
        'total_dropout_range_1':total_dropout_range_1,
        'total_dropout_range_2':total_dropout_range_2,
        'total_dropout_range_3':total_dropout_range_3,
        'school_indices':school_indices,
        'dropout_counts':dropout_dict,
        'pending_schools':pending_schools,
        'approved_school':approved_school,
        'year':year,
        'total_students_count_year':total_students_count_year,
        'combined_data':combined_data,
        'ttotal_dropout_students':ttotal_dropout_students,
        'tdropout_ratio':tdropout_ratio,
        'total_dropout_dist_range_0':total_dropout_dist_range_0,
        'total_dropout_dist_range_1':total_dropout_dist_range_1,
        'total_dropout_dist_range_2':total_dropout_dist_range_2,
        'total_dropout_dist_range_3':total_dropout_dist_range_3,
        'suggestion_from_district_to_school':suggestion_from_district_to_school,
    })





def district_index_filtered(request):
    if request.user.is_anonymous or not request.user.is_district_user or not request.user.is_approved:
        return redirect("/logindis")

    year = request.GET.get('year', '')
    user_dist = request.user.District
    student_data = contactEnquiry.objects.filter(city__iexact=user_dist,Year=year)

    suggestions = Suggestion.objects.filter(district_name__iexact=user_dist)
    # context = {'student_data': student_data, 'suggestions': suggestions}
    user_state = request.user.state
    age_group_0_5 = contactEnquiry.objects.filter(mystate__iexact=user_state,city__iexact=user_dist,age__gte=1,age__lte=5,Year=year).count()
    age_group_6_10 = contactEnquiry.objects.filter(mystate__iexact=user_state,city__iexact=user_dist,age__gte=6,age__lte=10,Year=year).count()
    age_group_11_15 = contactEnquiry.objects.filter(mystate__iexact=user_state,city__iexact=user_dist, age__gte=11,age__lte=15,Year=year).count()
    age_group_16_20 = contactEnquiry.objects.filter(mystate__iexact=user_state,city__iexact=user_dist, age__gte=16,age__lte=20,Year=year).count()

    male_dropout_students=contactEnquiry.objects.filter(gender__iexact='male',mystate__iexact=user_state,city__iexact=user_dist,Year=year).count()
    female_dropout_students=contactEnquiry.objects.filter(gender__iexact='female',mystate__iexact=user_state,city__iexact=user_dist,Year=year).count()
    total_dropout_fm_student = (male_dropout_students + female_dropout_students)

    
    income_range_0 = (0,10000)
    income_range_1 = (10000, 50000)
    income_range_2 = (50000, 100000)
    # income_range_3 = (100000, float('inf'))


    total_dropout_range_0 = contactEnquiry.objects.filter(mystate__iexact=user_state,  income__range=income_range_0,city__iexact=user_dist,Year=year).count()
    total_dropout_range_1 = contactEnquiry.objects.filter(mystate__iexact=user_state,  income__range=income_range_1,city__iexact=user_dist,Year=year).count()
    total_dropout_range_2 = contactEnquiry.objects.filter(mystate__iexact=user_state, income__range=income_range_2,city__iexact=user_dist,Year=year).count()
    total_dropout_range_3 = contactEnquiry.objects.filter(mystate__iexact=user_state,  income__gte=100001,city__iexact=user_dist,Year=year).count()

    school_indices = contactEnquiry.objects.filter(mystate__iexact=user_state, city__iexact=user_dist, Year=year).values_list('schoolindex', flat=True).distinct()
    dropout_counts = contactEnquiry.objects.filter(mystate__iexact=user_state, city__iexact=user_dist, Year=year).values('schoolindex').annotate(total_dropouts=Count('id'))
    dropout_dict = {item['schoolindex']: item['total_dropouts'] for item in dropout_counts}

    
    combined_data = []
    for school_index in school_indices:
        total_dropout_students = dropout_dict.get(school_index, 0)

        # Fetch total students separately
        school_data = SchoolYearData.objects.filter(
            school__username=school_index,  # Assuming the username is the school index
            year=year,
            state=user_state,
            district=user_dist
        ).first()

        male_dropout_students_school_wise = contactEnquiry.objects.filter(
            gender='male',
            schoolindex=school_index,
            mystate__iexact=user_state,
            city=user_dist,
            Year=year
        ).count()

        female_dropout_students_school_wise = contactEnquiry.objects.filter(
            gender='female',
            schoolindex=school_index,
            mystate__iexact=user_state,
            city=user_dist,
            Year=year
        ).count()

        total_students = school_data.total_students if school_data else 0
        dropout_ratio = (total_dropout_students / total_students) * 100 if total_students > 0 else 0
        dropout_ratio = round(dropout_ratio, 2)

        combined_data.append({
            'school_index': school_index,
            'total_dropout_students': total_dropout_students,
            'total_students': total_students,
            'male_dropout_students_school_wise':male_dropout_students_school_wise,
            'female_dropout_students_school_wise':female_dropout_students_school_wise,
            'dropout_ratio':dropout_ratio,


        })

    pending_schools = CustomUser.objects.filter(is_school_user=True, is_approved=False,District__iexact=user_dist)
    approved_school = CustomUser.objects.filter(is_school_user=True, is_approved=True,District__iexact=user_dist)

    school_data = SchoolYearData.objects.filter(
            year=year,
            state=request.user.state,
            district=request.user.District
        )
        # Get the total count of students for the selected year and district
    total_students_count_year = school_data.aggregate(Sum('total_students'))['total_students__sum']

    ttotal_dropout_students = contactEnquiry.objects.filter(mystate__iexact=user_state,Year=year,city=user_dist).count()

    tdropout_ratio = (ttotal_dropout_students/total_students_count_year)*100 if total_students_count_year is not None and total_students_count_year != 0 else 0
    tdropout_ratio = round(tdropout_ratio, 2)

    distance_range_0 = (0,5)
    distance_range_1 = (6, 15)
    distance_range_2 = (16, 30)

    total_dropout_dist_range_0 = contactEnquiry.objects.filter(mystate__iexact=user_state,  Distance__range=distance_range_0,city__iexact=user_dist,Year=year).count()
    total_dropout_dist_range_1 = contactEnquiry.objects.filter(mystate__iexact=user_state,  Distance__range=distance_range_1,city__iexact=user_dist,Year=year).count()
    total_dropout_dist_range_2 = contactEnquiry.objects.filter(mystate__iexact=user_state, Distance__range=distance_range_2,city__iexact=user_dist,Year=year).count()
    total_dropout_dist_range_3 = contactEnquiry.objects.filter(mystate__iexact=user_state,  Distance__gte=31,city__iexact=user_dist,Year=year).count()

    suggestion_from_district_to_school = SuggestionDis.objects.filter(district_name__iexact=user_dist,state_name__iexact=user_state)
    
            
    return render(request, 'district_index.html',{
        'student_data':student_data,
        'suggestions':suggestions,
        'age_group_0_5':age_group_0_5,
        'age_group_6_10':age_group_6_10,
        'age_group_11_15':age_group_11_15,
        'age_group_16_20':age_group_16_20,
        'male_dropout_students':male_dropout_students,
        'female_dropout_students':female_dropout_students,
        'total_dropout_fm_student':total_dropout_fm_student,
        'total_dropout_range_0':total_dropout_range_0,
        'total_dropout_range_1':total_dropout_range_1,
        'total_dropout_range_2':total_dropout_range_2,
        'total_dropout_range_3':total_dropout_range_3,
        'school_indices':school_indices,
        'dropout_counts':dropout_dict,
        'pending_schools':pending_schools,
        'approved_school':approved_school,
        'year':year,
        'total_students_count_year':total_students_count_year,
        'combined_data':combined_data,
        'ttotal_dropout_students':ttotal_dropout_students,
        'tdropout_ratio':tdropout_ratio,
        'total_dropout_dist_range_0':total_dropout_dist_range_0,
        'total_dropout_dist_range_1':total_dropout_dist_range_1,
        'total_dropout_dist_range_2':total_dropout_dist_range_2,
        'total_dropout_dist_range_3':total_dropout_dist_range_3,
        'suggestion_from_district_to_school':suggestion_from_district_to_school,
    })
















def loginUserdis(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)

        year=2023
        if user is not None and user.is_district_user and user.is_approved:
            login(request,user)
            user_dist = request.user.District
            student_data = contactEnquiry.objects.filter(city__iexact=user_dist,Year=year)
            suggestions = Suggestion.objects.filter(district_name__iexact=user_dist)
            user_state = request.user.state
            age_group_0_5 = contactEnquiry.objects.filter(mystate__iexact=user_state,city__iexact=user_dist,age__gte=1,age__lte=5,Year=year).count()
            age_group_6_10 = contactEnquiry.objects.filter(mystate__iexact=user_state,city__iexact=user_dist,age__gte=6,age__lte=10,Year=year).count()
            age_group_11_15 = contactEnquiry.objects.filter(mystate__iexact=user_state,city__iexact=user_dist, age__gte=11,age__lte=15,Year=year).count()
            age_group_16_20 = contactEnquiry.objects.filter(mystate__iexact=user_state,city__iexact=user_dist, age__gte=16,age__lte=20,Year=year).count()

            male_dropout_students=contactEnquiry.objects.filter(gender__iexact='male',mystate__iexact=user_state,city__iexact=user_dist,Year=year).count()
            female_dropout_students=contactEnquiry.objects.filter(gender__iexact='female',mystate__iexact=user_state,city__iexact=user_dist,Year=year).count()
            total_dropout_fm_student = (male_dropout_students + female_dropout_students)


            income_range_0 = (0,10000)
            income_range_1 = (10000, 50000)
            income_range_2 = (50000, 100000)
            # income_range_3 = (100000, float('inf'))


            total_dropout_range_0 = contactEnquiry.objects.filter(mystate__iexact=user_state,  income__range=income_range_0,city__iexact=user_dist,Year=year).count()
            total_dropout_range_1 = contactEnquiry.objects.filter(mystate__iexact=user_state,  income__range=income_range_1,city__iexact=user_dist,Year=year).count()
            total_dropout_range_2 = contactEnquiry.objects.filter(mystate__iexact=user_state, income__range=income_range_2,city__iexact=user_dist,Year=year).count()
            total_dropout_range_3 = contactEnquiry.objects.filter(mystate__iexact=user_state,  income__gte=100001,city__iexact=user_dist,Year=year).count()


            pending_schools = CustomUser.objects.filter(is_school_user=True, is_approved=False,District__iexact=user_dist)
            approved_school = CustomUser.objects.filter(is_school_user=True, is_approved=True,District__iexact=user_dist)

            school_indices = contactEnquiry.objects.filter(mystate__iexact=user_state, city__iexact=user_dist, Year=year).values_list('schoolindex', flat=True).distinct()
            dropout_counts = contactEnquiry.objects.filter(mystate__iexact=user_state, city__iexact=user_dist, Year=year).values('schoolindex').annotate(total_dropouts=Count('id'))
            dropout_dict = {item['schoolindex']: item['total_dropouts'] for item in dropout_counts}

            
            combined_data = []
            for school_index in school_indices:
                total_dropout_students = dropout_dict.get(school_index, 0)

                # Fetch total students separately
                school_data = SchoolYearData.objects.filter(
                    school__username=school_index,  # Assuming the username is the school index
                    year=year,
                    state=user_state,
                    district=user_dist
                ).first()
                
                male_dropout_students_school_wise = contactEnquiry.objects.filter(
                    gender='male',
                    schoolindex=school_index,
                    mystate__iexact=user_state,
                    Year=year,
                    city=user_dist
                ).count()

                female_dropout_students_school_wise = contactEnquiry.objects.filter(
                    gender='female',
                    schoolindex=school_index,
                    mystate__iexact=user_state,
                    Year=year,
                    city=user_dist
                ).count()

                total_students = school_data.total_students if school_data else 0
                dropout_ratio = (total_dropout_students / total_students) * 100 if total_students > 0 else 0
                dropout_ratio = round(dropout_ratio, 2)


                combined_data.append({
                    'school_index': school_index,
                    'total_dropout_students': total_dropout_students,
                    'total_students': total_students,
                    'male_dropout_students_school_wise':male_dropout_students_school_wise,
                    'female_dropout_students_school_wise':female_dropout_students_school_wise,
                    'dropout_ratio':dropout_ratio,


                })


            school_data = SchoolYearData.objects.filter(
                year=year,
                state=request.user.state,
                district=request.user.District
            )
        # Get the total count of students for the selected year and district
            total_students_count_year = school_data.aggregate(Sum('total_students'))['total_students__sum']

            ttotal_dropout_students = contactEnquiry.objects.filter(mystate__iexact=user_state,Year=year,city=user_dist).count()

            
            tdropout_ratio = (ttotal_dropout_students/total_students_count_year)*100 if total_students_count_year is not None and total_students_count_year != 0 else 0
            tdropout_ratio = round(tdropout_ratio, 2)


            distance_range_0 = (0,5)
            distance_range_1 = (6, 15)
            distance_range_2 = (16, 30)
            


            total_dropout_dist_range_0 = contactEnquiry.objects.filter(mystate__iexact=user_state,  Distance__range=distance_range_0,city__iexact=user_dist,Year=year).count()
            total_dropout_dist_range_1 = contactEnquiry.objects.filter(mystate__iexact=user_state,  Distance__range=distance_range_1,city__iexact=user_dist,Year=year).count()
            total_dropout_dist_range_2 = contactEnquiry.objects.filter(mystate__iexact=user_state, Distance__range=distance_range_2,city__iexact=user_dist,Year=year).count()
            total_dropout_dist_range_3 = contactEnquiry.objects.filter(mystate__iexact=user_state,  Distance__gte=31,city__iexact=user_dist,Year=year).count()

            suggestion_from_district_to_school = SuggestionDis.objects.filter(district_name__iexact=user_dist,state_name__iexact=user_state)
            # context = {'student_data': student_data, 'suggestions': suggestions}
            # login(request,user)
            return render(request,'district_index.html',{
                'student_data':student_data,
                'suggestions':suggestions,
                'age_group_0_5':age_group_0_5,
                'age_group_6_10':age_group_6_10,
                'age_group_11_15':age_group_11_15,
                'age_group_16_20':age_group_16_20,
                'male_dropout_students':male_dropout_students,
                'female_dropout_students':female_dropout_students,
                'total_dropout_fm_student':total_dropout_fm_student,
                'total_dropout_range_0':total_dropout_range_0,
                'total_dropout_range_1':total_dropout_range_1,
                'total_dropout_range_2':total_dropout_range_2,
                'total_dropout_range_3':total_dropout_range_3,
                'school_indices':school_indices,
                'dropout_counts':dropout_dict,
                'pending_schools':pending_schools,
                'approved_school':approved_school,
                'year':year,
                'total_students_count_year':total_students_count_year,
                'combined_data':combined_data,
                'ttotal_dropout_students':ttotal_dropout_students,
                'tdropout_ratio':tdropout_ratio,
                'total_dropout_dist_range_0':total_dropout_dist_range_0,
                'total_dropout_dist_range_1':total_dropout_dist_range_1,
                'total_dropout_dist_range_2':total_dropout_dist_range_2,
                'total_dropout_dist_range_3':total_dropout_dist_range_3,
                'suggestion_from_district_to_school':suggestion_from_district_to_school
            })
        else:
            return render(request, 'District_login.html')

    return render(request, 'District_login.html')

def logoutUserdis(request):
   logout(request)
   return redirect("/logindis")

def district_signup(request):
    if request.method == 'POST':
        form = DistrictSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password=make_password(user.password)
            user.is_district_user = True
            user.is_approved=False
            user.save()
            login(request, user)
            return redirect('/district_index')  # Redirect to the district dashboard or any other page
    else:
        form = DistrictSignUpForm()

    return render(request, 'District_login.html', {'form': form})

# def pending_registrations_Dist(request):
#     user_dist = request.user.District
#     pending_schools = CustomUser.objects.filter(is_school_user=True, is_approved=False,District__iexact=user_dist)
#     return render(request, 'district_index.html', {'pending_schools': pending_schools})

def approve_school(request, school_id):
    school = get_object_or_404(CustomUser, id=school_id)
    school.is_approved = True
    school.save()
    # Add logic to notify the school about approval
    # ...
    return redirect('/district_index')

def suggestion(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['state_name'] = request.user.state
        form = SuggestionForm(post_data)
        if form.is_valid():
            form.save()
              # Redirect to the government dashboard or any other page
            return redirect('/gov_index')
            
            
    else:
        form = SuggestionForm()

    return render(request, 'suggestion.html', {'form': form})


def suggestionDist(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        # Set the district_name value in the copy
        post_data['district_name'] = request.user.District
        post_data['state_name'] = request.user.state

        form = SuggestionDistForm(post_data)
        if form.is_valid():
            form.save()

              # Redirect to the government dashboard or any other page
            return redirect('/district_index')
            
    else:
        form = SuggestionForm()

    return render(request, 'suggestion.html', {'form': form})


# views.py

def Suggestion_G_to_S(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        # Set the state_name value in the copy
        post_data['state_name'] = request.user.state

        form = SuggestionStateToSchForm(post_data)
        if form.is_valid():
            form.save()

              # Redirect to the government dashboard or any other page
            return redirect('/gov_index')
            
    else:
        form = SuggestionStateToSchForm()

    return render(request, 'suggestion.html', {'form': form})





def getback(request):
    return render(request,'index.html')




#machine Learning here

X = [[19, 0, 0, 5, 0.37122903700888404], [15, 0, 0, 7, 0.20840098835157078], [14, 0, 1, 1, 1.3289612334313128], [19, 1, 1, 8, 0.030669565030239116], [15, 1, 2, 5, 0.4973830606669081], [16, 0, 0, 7, 1.081584053624978], [16, 1, 0, 8, 0.9789841053070825], [14, 1, 2, 4, 0.20940573341703286], [19, 0, 2, 2, 0.18806773301737756], [17, 1, 3, 6, 0.8065391615313388], [16, 0, 2, 2, 1.1102032006413616], [19, 0, 1, 8, 0.31289863564074666], [19, 0, 2, 1, 0.07753429449538993], [16, 1, 2, 2, 1.0137306456324862], [19, 1, 1, 8, 0.6972484480082773], [17, 0, 2, 3, 1.1771529828706437], [18, 1, 3, 7, 0.26760318206346717], [15, 1, 0, 1, 0.4520126379713594], [19, 0, 3, 2, 0.4303845644691554], [18, 1, 2, 1, 1.8260174302390662], [18, 1, 2, 2, 0.6084713940869422], [15, 1, 0, 5, 0.1680685605459451], [18, 0, 2, 4, 0.8492274906766116], [15, 0, 2, 8, 0.6637189292543021], [16, 1, 1, 1, 0.9184768227851147], [14, 0, 3, 2, 0.11577008844679412], [15, 1, 1, 5, 0.5147985801447647], [17, 0, 1, 5, 0.7226627712854758], [19, 1, 3, 8, 0.6668986852281515], [15, 0, 2, 1, 0.9851348322999925], [15, 0, 0, 1, 0.13540130477166495], [14, 1, 0, 4, 0.9643440860215053], [17, 0, 1, 8, 0.7645400238948626], [17, 0, 0, 2, 0.3642064422990165], [17, 1, 3, 1, 0.21712738547534827], [17, 1, 0, 4, 0.38348712690817954], [18, 1, 1, 7, 0.5654625550660793], [17, 0, 0, 8, 0.18898086103446765], [19, 0, 0, 4, 0.8690483678218756], [17, 1, 1, 7, 0.6666101215719537], [17, 0, 3, 5, 0.282805364886987], [17, 1, 1, 4, 0.31227244835344653], [14, 0, 2, 1, 2.3705044653632634], [17, 0, 0, 2, 0.15979741529863778], [18, 0, 1, 7, 1.490841208727103], [15, 0, 0, 7, 0.27677593540663764], [16, 0, 2, 4, 0.6011067969830857], [15, 1, 3, 6, 0.08253024400246053], [17, 0, 0, 4, 0.24086912078839426], [15, 1, 0, 4, 0.3367217715713455], [15, 1, 2, 1, 0.9032290820471162], [14, 0, 2, 2, 2.0664613591909777], [18, 0, 2, 5, 1.277129257850932], [16, 0, 2, 8, 0.10087617094654425], [14, 1, 2, 1, 2.1845374617737003], [15, 1, 1, 8, 0.5716123953555263], [14, 0, 0, 3, 1.7114522483358239], [18, 0, 3, 3, 1.3694613099082806], [16, 0, 2, 4, 1.0468786587364773], [14, 1, 3, 3, 0.2839211289575666], [15, 1, 0, 3, 0.5226372805379156], [19, 0, 2, 3, 1.0786991062562066], [14, 1, 1, 4, 0.3400301427515214], [16, 0, 1, 1, 0.76779089853595], [16, 1, 0, 5, 0.7682284694332887], [18, 1, 2, 1, 0.7213153913528147], [15, 1, 0, 2, 0.35326095073104435], [19, 1, 3, 2, 0.6412346250495966], [15, 1, 0, 7, 3.43146463164074], [18, 0, 2, 7, 2.322831359866465], [16, 1, 0, 5, 0.27813885365311436], [19, 1, 2, 7, 0.765773711847719], [15, 0, 3, 7, 1.2599207558671137], [18, 1, 3, 1, 0.3974191735736218], [15, 1, 2, 8, 0.44145497386054044], [19, 0, 3, 3, 0.9281992990432888], [18, 1, 0, 4, 0.3101781521889242], [15, 0, 0, 1, 0.7635180081725743], [18, 0, 3, 7, 1.354854163731154], [19, 1, 3, 7, 0.25419852783534624], [19, 0, 0, 7, 0.32381149342088256], [19, 1, 0, 4, 1.1933142901258396], [15, 1, 2, 8, 0.3803208949344818], [18, 1, 1, 8, 0.2607006711020278], [15, 1, 3, 4, 0.6485258305792312], [14, 1, 1, 5, 0.4063680118474639], [18, 0, 1, 3, 0.6475155664706904], [19, 0, 1, 2, 0.43046429625487365], [16, 1, 3, 1, 0.768903260576664], [17, 0, 3, 8, 2.23282584478277], [16, 1, 3, 4, 0.20785750003378697], [16, 1, 3, 1, 0.3777063377509513], [19, 1, 1, 8, 1.5631547440885962], [18, 0, 3, 1, 2.0531828786363855], [17, 0, 3, 3, 1.0879445449065703], [17, 1, 1, 8, 0.43750946252838757], [17, 1, 3, 5, 1.534699782975645], [14, 0, 2, 4, 2.3015321434212606], [14, 0, 1, 4, 3.2924788888011998], [15, 0, 1, 8, 1.5188252710759012], [15, 1, 2, 6, 1.2724118529632409], [18, 0, 1, 5, 1.6105594174114533], [14, 1, 3, 7, 0.16613418530351437], [18, 0, 0, 5, 1.4725121781489214], [14, 1, 3, 6, 1.7942010715411283], [19, 1, 0, 7, 0.10661135876957886], [17, 1, 3, 3, 0.18698568872987478], [19, 1, 3, 8, 0.7289800420324634], [18, 1, 2, 4, 0.9026171637248935], [17, 0, 3, 7, 0.05324262367817792], [17, 1, 1, 8, 0.6415798105920322], [16, 1, 2, 5, 3.076522506619594], [15, 0, 1, 7, 0.5049299008617196], [15, 1, 3, 8, 0.5789559543230016], [16, 0, 3, 4, 0.887862770519597], [18, 1, 3, 6, 0.758464976965532], [18, 1, 2, 8, 0.463512711771298], [16, 0, 0, 4, 0.17202437742167878], [19, 0, 1, 4, 0.2602635304366765], [19, 1, 0, 4, 0.325790001843167], [16, 0, 2, 1, 0.7136625173931029], [14, 0, 2, 3, 0.10388754371805219], [14, 1, 3, 8, 0.3444111437556287], [15, 0, 2, 8, 0.21167795455456256], [17, 1, 0, 1, 0.36059156154849936], [18, 1, 0, 4, 1.4720078354554358], [17, 0, 3, 8, 0.30115540659728346], [18, 1, 2, 1, 0.6353559940884986], [19, 0, 2, 2, 0.546640510053948], [15, 0, 1, 1, 0.48035250609804075], [19, 1, 2, 1, 0.49283589489340607], [19, 1, 3, 2, 0.4517058751077719], [19, 0, 3, 2, 1.1007702832818123], [15, 1, 1, 2, 0.6664234396048496], [16, 1, 3, 2, 0.6458219590385396], [16, 1, 2, 8, 0.09307330394645057], [18, 0, 3, 6, 0.06294375934230194], [14, 0, 0, 5, 0.8171937405879657], [17, 1, 2, 3, 0.6345855925639039], [17, 0, 3, 6, 0.3596020339089778], [16, 0, 1, 6, 0.7264482839496521], [17, 1, 3, 1, 0.09726491797626914], [16, 1, 2, 2, 0.5513846544715447], [14, 1, 3, 1, 1.0112762389406118], [16, 1, 3, 1, 0.5043893129770992], [18, 0, 2, 8, 0.1218109122558886], [14, 0, 1, 5, 3.154002713704206], [17, 0, 1, 2, 0.1234073947958344], [19, 0, 3, 5, 0.6157787686771493], [16, 1, 3, 8, 0.7374958279692938]]
y = [0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1]




X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)






def predict_dropout(request):
    if request.method == 'POST':
        # age = 18
        age = int(request.POST.get('age'))
        # gender =0
        gender = int(request.POST.get('gender'))
        caste = int(request.POST.get('caste'))
        # caste = 0
        distance = int(request.POST.get('distance'))
        # area = 3
        income = int(request.POST.get('income'))
        # income = 76845390
        fee = int(request.POST.get('fee'))

        rat = fee/income
        # Create a new data point as a list of lists
        new_data = [[age, gender, caste, distance, rat]]

        # Load the trained KNN model (you might want to save and load the model)
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(X_train, y_train)  # Make sure to load training data

        # Make predictions using the trained KNN model
        predictions = knn.predict(new_data)

        # Store the prediction in the database (optional)
        DropoutPrediction.objects.create(
            age=age, gender=gender, caste=caste, distance=distance, income=income, prediction=predictions, fee=fee
        )

        # Determine dropout status
        dropout_status = "dropout" if predictions[0] == 1 else "not dropout"
        return render(request, 'school_index.html', {'dropout_status': dropout_status})

    return render(request, 'school_index.html')



def SchoolYearDataStore(request):
    
    
    if request.method == 'POST':
        school=request.user
        year=request.POST.get('year1')
        total_students=request.POST.get('totalstu')
        state=request.user.state
        district=request.user.District
        en=SchoolYearData(school=school,year=year,total_students=total_students,state=state,district=district)
        en.save()

    return redirect('/school_index')

import pandas as pd
from django.conf import settings
import os

def predict_batch_dropout(request):

    if request.user.is_anonymous or not request.user.is_school_user or not request.user.is_approved:
        return redirect("/login")
        
    user_dist = request.user.District
    user_school = request.user.username
    user_state = request.user.state
    
    username=request.user.username
    suggestions = SuggestionDis.objects.filter(district_name__iexact=user_dist,school_name__iexact=username)
    suggestions_G_to_S = Suggestion_state_to_sch.objects.filter(school_name__iexact=user_school,state_name__iexact=user_state)
    
      
    enquiries = contactEnquiry.objects.filter(user=request.user)
    school_data = SchoolYearData.objects.filter(school=request.user,district=request.user.District)
    context = {'enquiries': enquiries, 'suggestions': suggestions,'suggestions_G_to_S':suggestions_G_to_S,'school_data':school_data}
    if request.method == 'POST' and request.FILES['excel_file']:
        # Get the uploaded file
        excel_file = request.FILES['excel_file']
        upload_dir = 'uploads'
        
        # Construct the file path
        file_path = os.path.join(settings.STATIC_ROOT, upload_dir, excel_file.name)

        # Ensure the 'uploads' directory exists
        os.makedirs(os.path.join(settings.STATIC_ROOT, upload_dir), exist_ok=True)

        # Save the uploaded file to the specified path
        with open(file_path, 'wb') as destination:
            for chunk in excel_file.chunks():
                destination.write(chunk)

        # Assuming the Excel file has columns: 'age', 'gender', 'caste', 'distance', 'income', 'fee'
        # Adjust these column names based on your actual Excel file
        columns_needed = ['age', 'gender', 'caste', 'distance', 'income', 'fee','student_id']

        try:
            # Read the Excel file into a Pandas DataFrame
            df = pd.read_excel(file_path, engine='openpyxl')

            # Filter DataFrame to include only required columns
            df = df[columns_needed]

            # Calculate 'rat' for each student
            df['rat'] = df['fee'] / df['income']

            # Create a new data frame with the required features
            new_data = df[['age', 'gender', 'caste', 'distance', 'rat']]

            # Load the trained KNN model (you might want to save and load the model)
            knn = KNeighborsClassifier(n_neighbors=5)

            import warnings
            warnings.filterwarnings("ignore", category=UserWarning)
            knn.fit(X_train, y_train)  # Make sure to load training data
            warnings.resetwarnings()
            # Make predictions using the new data frame
            predictions = knn.predict(new_data)

            print("Predictions:", predictions)
            # Store the predictions in the database (optional)
            # DropoutPrediction.objects.bulk_create([
            #     DropoutPrediction(
            #         age=row['age'],
            #         gender=row['gender'],
            #         caste=row['caste'],
            #         distance=row['distance'],
            #         income=row['income'],
            #         fee=row['fee'],
            #         prediction=prediction
            #     )
            #     for _, (index, row), prediction in zip(df.iterrows(), df.iterrows(), predictions)
            # ])
            data_with_predictions = pd.concat([new_data, pd.Series(predictions, name='prediction'), df['student_id'],df['income'],df['fee']], axis=1)


            data_with_predictions['dropout_status'] = data_with_predictions['prediction'].apply(
                lambda x: "dropout" if x == 1 else "not dropout"
            )

            print(data_with_predictions)
            print(data_with_predictions.columns)
            print(len(data_with_predictions))
            return render(request, 'school_index.html', {'data_with_predictions': data_with_predictions,'context':context})
        except Exception as e:
            return render(request, 'school_index.html', {'error_message': f'Error processing Excel file: {e}'})

    return render(request, 'school_index.html')