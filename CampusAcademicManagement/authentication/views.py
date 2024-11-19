from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from .forms import LoginForm
from decimal import Decimal
from django.utils.timezone import now


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


def student_home(request):
    if "rollno" in request.session and request.session["role"] == "student":
        rollno = request.session["rollno"]

        # Query to fetch semester-wise results (with grade points and credits)
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT 
                ce.semester, 
                c.courseName, 
                sr.grade, 
                c.credits
            FROM 
                course_enrollment ce
            JOIN 
                courses c ON ce.courseID = c.courseID
            JOIN 
                studentresultsinfo sr ON ce.courseID = sr.courseID AND ce.studentID = sr.studentID
            WHERE 
                ce.studentID = %s
            ORDER BY 
                ce.semester
            """,
            [rollno],
        )

        semester_results = cursor.fetchall()

        # Define grade points mapping
        grade_points = {
            "O": 10.0,
            "A+": 9.0,
            "A": 8.0,
            "B+": 7.0,
            "B": 6.0,
            "C": 5.0,
            "P": 4.0,
            "F": 0.0,
        }

        gpas = {}
        for result in semester_results:
            semester, course_name, grade, credits = result
            grade_point = Decimal(
                grade_points.get(grade, 0)
            )  # Convert grade_point to Decimal
            credits = Decimal(credits)  # Ensure credits is a Decimal

            if semester not in gpas:
                gpas[semester] = {
                    "total_points": Decimal(0),
                    "total_credits": Decimal(0),
                }

            gpas[semester]["total_points"] += grade_point * credits
            gpas[semester]["total_credits"] += credits

        # Calculate GPA for each semester
        semester_gpas = {
            semester: gpas[semester]["total_points"] / gpas[semester]["total_credits"]
            for semester in gpas
        }

        # Pass semester GPAs and semester names to the template
        return render(
            request,
            "authentication/student_dashboard.html",
            {
                "semesters": list(semester_gpas.keys()),
                "gpas": [round(gpa, 2) for gpa in semester_gpas.values()],
            },
        )

    else:
        # Redirect to login if the user is not logged in or not a student
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
        student_info = {}
        if student_data:
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

            cursor.execute(
                """
            SELECT 
                ce.semester, 
                c.courseName, 
                sr.grade
            FROM 
                course_enrollment ce
            JOIN 
                courses c ON ce.courseID = c.courseID
            JOIN 
                studentresultsinfo sr ON ce.courseID = sr.courseID AND ce.studentID = sr.studentID
            WHERE 
                ce.studentID = %s
            ORDER BY 
                ce.semester
            """,
                [rollno],
            )

            semester_results = cursor.fetchall()

            # Structure the data into a dictionary to easily access results by semester
            results_by_semester = {}
            for result in semester_results:
                semester = result[0]
                if semester not in results_by_semester:
                    results_by_semester[semester] = []
                results_by_semester[semester].append(
                    {"courseName": result[1], "grade": result[2]}
                )

            return render(
                request,
                "authentication/student_profile.html",
                {
                    "student_info": student_info,
                    "results_by_semester": results_by_semester,
                },
            )
        else:
            messages.error(request, "Student details not found.")
            return redirect("student_home")

    # Redirect to login if the session is not valid
    return redirect("login")


def announcements_list(request):
    # Fetch announcements from the database
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT announcementID, title, type, published, description FROM announcements ORDER BY published DESC;"
        )
        announcements = cursor.fetchall()

    # Prepare the data for the template
    announcements_data = [
        {
            "id": ann[0],
            "title": ann[1],
            "type": ann[2],
            "published": ann[3].strftime("%Y-%m-%d %H:%M"),
            "description": ann[4],
        }
        for ann in announcements
    ]

    # Render the announcements template with the data
    return render(
        request,
        "authentication/announcements.html",
        {"announcements": announcements_data},
    )


def event_registration(request):
    cursor = connection.cursor()

    # Execute a query to fetch all event registrations
    query = "SELECT * FROM eventregistration"
    cursor.execute(query)

    # Fetch all rows from the executed query
    rows = cursor.fetchall()

    # Manually convert the rows into a list of dictionaries
    columns = [column[0] for column in cursor.description]  # type: ignore # Get column names from the cursor description
    events = [
        dict(zip(columns, row)) for row in rows
    ]  # Convert each row to a dictionary

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Debug print statement to verify the fetched data
    print(events)

    # Render the template with the fetched data
    return render(request, "authentication/event_registration.html", {"events": events})


def suggestion_view(request):
    student_id = request.session["rollno"]
    if request.method == "POST":
        # Get data from the form
        suggestion_type = request.POST.get("type")
        message = request.POST.get("message")

        # Insert the suggestion into the database
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO suggestion (type, message, date_time, studentID)
                VALUES (%s, %s, %s, %s)
                """,
                [suggestion_type, message, now(), student_id],
            )

        # Redirect to the same page to display the updated suggestions
        return redirect("suggestion")

    # Fetch suggestions for the logged-in user
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT suggestionID, type, message, date_time 
            FROM suggestion 
            WHERE studentID = %s 
            ORDER BY date_time DESC
            """,
            [student_id],
        )
        suggestions = cursor.fetchall()

    # Prepare suggestions as a list of dictionaries for easy use in the template
    suggestion_list = [
        {
            "id": suggestion[0],
            "type": suggestion[1],
            "message": suggestion[2],
            "date_time": suggestion[3],
        }
        for suggestion in suggestions
    ]

    # Define the suggestion types
    suggestion_types = [
        "Faculty",
        "Department",
        "Infrastructure",
        "Course",
        "Management",
        "Ragging",
        "Others",
    ]

    return render(
        request,
        "authentication/suggestion.html",
        {"suggestions": suggestion_list, "types": suggestion_types},
    )
