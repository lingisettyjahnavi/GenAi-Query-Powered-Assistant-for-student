from studentapp.models import Student

# FIXED: Changed function name from get_Student_data to get_student_data to match your imports
def get_student_data(user):
    # FIXED: Use lowercase 'student' for the variable to avoid breaking the Student model reference
    student = Student.objects.get(user=user)

    return {
        "student_id": student.id,
        "first_name": student.user.first_name,
        "last_name": student.user.last_name,
        "username": student.user.username,
        "contact": student.address,
        "course": student.course
    }

# Convert student database into text to provide to AI
def student_data_to_context(student_data):
    return f"""
Student Information:
Name: {student_data["first_name"]} {student_data["last_name"]}
Username: {student_data["username"]}
Contact: {student_data["contact"]}
Address: {student_data["contact"]}
Course: {student_data["course"]}
"""
