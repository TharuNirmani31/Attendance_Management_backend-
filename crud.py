from database import attendance_table, employee_table, embedding_table, faces_table

# Attendance
def get_all_attendance():
    return attendance_table.scan().get("Items", [])

# Employee details
def get_all_employees():
    return employee_table.scan().get("Items", [])

# Embeddings
def get_all_embeddings():
    return embedding_table.scan().get("Items", [])

# Employee faces
def get_all_faces():
    return faces_table.scan().get("Items", [])
