import subprocess

def run_command(command):
    """Run a shell command and print the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

def get_token(email, password):
    """Helper function to get JWT token for a user."""
    login_command = f'flask login {email} {password}'
    result = subprocess.run(login_command, shell=True, capture_output=True, text=True)
    token_line = [line for line in result.stdout.split('\n') if "JWT Token" in line]
    token = token_line[0].split(": ")[1] if token_line else None
    return token

if __name__ == "__main__":
    # Set environment variables for Flask app
    run_command('export FLASK_APP=app.py')

    # Register admin user with different credentials
    admin_username = 'adminuser2'
    admin_email = 'adminuser2@example.com'
    admin_password = 'adminpassword123'

    print("Registering admin user:")
    run_command(f'flask register {admin_username} {admin_email} {admin_password} admin')

    # Register student user with different credentials
    student_username = 'studentuser2'
    student_email = 'studentuser2@example.com'
    student_password = 'studentpassword123'

    print("\nRegistering student user:")
    run_command(f'flask register {student_username} {student_email} {student_password} student')

    # Login as admin
    print("\nLogging in as admin:")
    admin_token = get_token(admin_email, admin_password)

    # Login as student
    print("\nLogging in as student:")
    student_token = get_token(student_email, student_password)

    if admin_token and student_token:
        # Admin creates a cohort
        print("\nAdmin creating a cohort:")
        run_command(f'flask create-cohort "Admin Test Cohort" "This is a test cohort created by admin" {admin_token}')
        
        # Admin creates a class with the cohort_id (assuming the cohort_id is 1)
        print("\nAdmin creating a class:")
        run_command(f'flask create-class "Admin Test Class" "This is a test class created by admin" 1 {admin_token}')

        # List all classes (accessible by both roles)
        print("\nListing all classes as admin:")
        run_command(f'flask list-classes {admin_token}')

        print("\nListing all classes as student:")
        run_command(f'flask list-classes {student_token}')

        # Assign user to class
        print("\nAdmin assigning student to class:")
        run_command(f'flask assign-user-to-class {student_email} 1 {admin_token}')

        # Student creates a project with the class_id (assuming the class_id is 1)
        print("\nStudent creating a project:")
        run_command(f'flask create-project "Student Test Project" "This is a test project by a student" "https://github.com/studentuser2/testproject" {student_email} 1 {student_token}')

        # List all projects (accessible by both roles)
        print("\nListing all projects as admin:")
        run_command(f'flask list-projects {admin_token}')

        print("\nListing all projects as student:")
        run_command(f'flask list-projects {student_token}')

        # Admin deletes a student user
        print("\nAdmin deleting a user:")
        run_command(f'flask delete-user 2 {admin_token}')
    else:
        print("Failed to obtain JWT tokens for admin or student.")
