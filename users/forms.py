from django import forms
from django.db.models import Q
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from users.models import User, Patient, Doctor, Comment, Questionaire

class UserRegForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "middle_name",
            "last_name",
        )
class DoctorRegForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password", max_length=100, widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Password Comfirmation", max_length=100, widget=forms.PasswordInput
    )
    class Meta:
        model = Doctor
        fields = ("email", "hpname", "specialty", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is registered.")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data["email"], self.cleaned_data["password1"],
        )
        user = super().save(commit=False)
        user.is_doctor = True
        if commit:
            user.save()
        return user


class PatientRegForm(forms.ModelForm):
    gender = forms.ChoiceField(label="Gender", choices=[
                               ("Male", "Male"), ("Female", "Female")])

    class Meta:
        model = Patient
        fields = ("email", "fullname", "phonenumber", "birthday", "gender")

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control email-field'}),
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
            'phonenumber': forms.NumberInput(attrs={'class': 'form-control phonenumber'}),
            'birthday': forms.NumberInput(attrs={'class': 'form-control birthday', 'type': 'date', 'placeholder': 'dd/mm/yyyy', 'id': 'datepicker'}),
            'gender': forms.Select(attrs={'class': 'form-control gender'}),

        }

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data["email"], self.cleaned_data["password1"],
        )
        user = super().save(commit=False)
        user.is_patient = True
        if commit:
            user.save()
        return user


class PatientLoginForm(forms.Form):
    query = forms.CharField(label="Patient's fullname")

    def clean(self, *args, **kwargs):
        query = self.clean_data.get("query")
        user_qs_final = User.objects.filter(Q(fullname_iexact=query))

        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError("Invalid Patient's fullname.")
        user_obj = user_qs_final.first()
        self.clean_data["user_obj"] = user_obj
        return super(PatientLoginForm, self).clean(*args, **kwargs)


class DoctorLoginForm(forms.Form):
    query = forms.CharField(label="Email address")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        query = self.clean_data.get("query")
        password = self.clean_data.get("password")
        user_qs_final = User.Objects.filter(Q(email_iexact=query)).distinct()

        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError("Invalid credentials. Please register")
        user_obj = user_qs_final.first()
        if not user_obj.check_password("password"):
            raise forms.ValidationError("Credentials are not correct")
        self.clean_data["user_obj"] = user_obj

        return super(DoctorLoginForm, self).clean(*args, **kwargs)


class CommentForm(forms.ModelForm):
    recommendation = forms.CharField(label="Recommendation", max_length=10000,)

    class Meta:
        model = Comment
        fields = ("comment",)


class QuestionaireForm(forms.ModelForm):
    weight = forms.FloatField(label="Weight", required=True)
    height = forms.FloatField(label="Height", required=True)
    occupation = forms.CharField(
        label="Occupation", max_length=1000, required=True)
    how_long = forms.CharField(
        label="For how long?", max_length=100, required=False)
    knee_pain = forms.ChoiceField(
        label="Any knee pain in the last 12 months?",
        choices=[("Yes", "Yes"), ("No", "No")],
        required=True,
    )
    knee_long = forms.ChoiceField(
        label="Did the pain persist?",
        choices=[("Yes", "Yes"), ("No", "No")],
        required=False,
    )
    didoc = forms.ChoiceField(
        label="Did you visit the hospital",
        choices=[("Yes", "Yes"), ("No", "No")],
        required=False,
    )
    walking = forms.ChoiceField(
        label="Limitations walking",
        choices=[("Yes", "Yes"), ("No", "No")],
        required=True,
    )
    getting_up = forms.ChoiceField(
        label="Limitations when getting up?",
        choices=[("Yes", "Yes"), ("No", "No")],
        required=True,
    )
    stiffness = forms.ChoiceField(
        label="Any knee stiffness during last 12 months?",
        choices=[("Yes", "Yes"), ("No", "No")],
        required=True,
    )
    prosthesis = forms.ChoiceField(
        label="Do you have a prosthesis in one or both knees?",
        choices=[("Yes", "Yes"), ("No", "No")],
        required=True,
    )
    surgery = forms.ChoiceField(
        label="Have you had surgical interventions in one of your knees?",
        choices=[("Yes", "Yes"), ("No", "No")],
        required=True,
    )

    class Meta:
        model = Questionaire
        fields = (
            "weight",
            "height",
            "occupation",
            "how_long",
            "knee_pain",
            "knee_long",
            "didoc",
            "stiffness",
            "how_long",
            "walking",
            "getting_up",
            "prosthesis",
            "surgery",
        )
class DoctorAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Doctor
        fields = ('fullname', 'email','specialty')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2    

    def save(self, commit=True):
        # Save the provided password in hashed format
        doctor = super(DoctorAdminCreationForm, self).save(commit=False)
        doctor.set_password(self.cleaned_data["password1"])
        if commit:
            doctor.save()
        return doctor    

class DoctorAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model=Doctor
        fields=('fullname','email', 'password' ,'active','admin','staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]            