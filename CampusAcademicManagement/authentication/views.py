from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from .forms import LoginForm


# Login view
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            rollno = form.cleaned_data["rollno"]
            password = form.cleaned_data["password"]

            # Querying MySQL tables
            cursor = connection.cursor()
            cursor.execute(
                "SELECT password FROM authentication WHERE rollno = %s", [rollno]
            )
            user_data = cursor.fetchone()

            if user_data and user_data[0] == password:
                # Fetch user role
                cursor.execute("SELECT role FROM roles WHERE rollno = %s", [rollno])
                user_role = cursor.fetchone()[0]  # type: ignore

                # Save user data in session
                request.session["rollno"] = rollno
                request.session["role"] = user_role

                # Redirect based on user role
                if user_role == "student":
                    return redirect("student_home")
                else:
                    return redirect(
                        "home"
                    )  # Redirect to a generic home page for other roles

            messages.error(request, "Invalid roll number or password")
    else:
        form = LoginForm()

    return render(request, "authentication/login.html", {"form": form})


# Home view for generic roles
def home_view(request):
    if "rollno" in request.session:
        rollno = request.session["rollno"]
        role = request.session["role"]
        return render(
            request, "authentication/home.html", {"rollno": rollno, "role": role}
        )
    return redirect("login")


# Student dashboard view
def student_home(request):
    if "rollno" in request.session and request.session["role"] == "student":
        # Render the student dashboard page
        return render(request, "authentication/student_dashboard.html")
    else:
        # Redirect to login if not a student
        return redirect("login")


# Student Profile View
def student_profile_view(request):
    if "rollno" in request.session and request.session["role"] == "student":
        rollno = request.session["rollno"]

        # Query to fetch student details
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT studentID, name, deptID, phnNo, dob, personalMail, section, 
                   date_of_joining, fathername, mothername, fatherphn, motherphn, 
                   father_occupation, mother_occupation, fatherEducation, motherEducation,
                   address, hostel_or_dayScholar, collegeBus, aadharNo, fee_reimbursement 
            FROM studentpersonalinfo 
            WHERE studentID = %s
            """,
            [rollno],
        )

        student_data = cursor.fetchone()
        if student_data:
            # Creating a dictionary for easier access in the template
            student_info = {
                "studentID": student_data[0],
                "name": student_data[1],
                "deptID": student_data[2],
                "phnNo": student_data[3],
                "dob": student_data[4],
                "personalMail": student_data[5],
                "section": student_data[6],
                "date_of_joining": student_data[7],
                "fathername": student_data[8],
                "mothername": student_data[9],
                "fatherphn": student_data[10],
                "motherphn": student_data[11],
                "father_occupation": student_data[12],
                "mother_occupation": student_data[13],
                "fatherEducation": student_data[14],
                "motherEducation": student_data[15],
                "address": student_data[16],
                "hostel_or_dayScholar": student_data[17],
                "collegeBus": student_data[18],
                "aadharNo": student_data[19],
                "fee_reimbursement": student_data[20],
            }
            print(student_info)
            return render(
                request,
                "authentication/student_profile.html",
                {"student_info": student_info},
            )
        else:
            messages.error(request, "Student details not found.")
            return redirect("student_home")

    # Redirect to login if the session is not valid
    return redirect("login")
