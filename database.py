import boto3
import os
from dotenv import load_dotenv

load_dotenv()

dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

attendance_table = dynamodb.Table("AttendanceLog")
employee_table = dynamodb.Table("EmployeeDetails")
embedding_table = dynamodb.Table("EmployeeEmbedding")
faces_table = dynamodb.Table("EmployeeFaces")
