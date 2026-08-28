from html import escape


def format_students_html(students):
    if not students:
        return "<p>No students found.</p>"

    items = []
    for student in students:
        items.append(
            "<li>"
            f"{int(student['student_id'])} - "
            f"{escape(str(student['student_name']))} - "
            f"{escape(str(student['subject_code']))}"
            "</li>"
        )
    return "<ul>" + "".join(items) + "</ul>"


def format_student_html(student):
    return (
        f"<p>ID: {int(student['student_id'])}<br>"
        f"Name: {escape(str(student['student_name']))}<br>"
        f"Subject: {escape(str(student['subject_code']))}</p>"
    )
