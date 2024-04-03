

# Django REST Framework Hospital Management API

This API provides endpoints for managing key aspects of a hospital system, including patients, doctors, general managers, and assistants.

## Getting Started

### Prerequisites:

- Python 3.x
- Django Rest Framework

### Installation:

1. Clone the repository:
   ```bash
   git clone https://github.com/cristiol/Django_rest_framework_Hospital_Management_API.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Make database migrations and apply them:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Running the API:

1. Start the development server:
   ```bash
   python manage.py runserver
   ```
2. Access the API at `http://127.0.0.1:8000/`.

## Authentication

Most API endpoints require authentication using a custom token-based system. To obtain a token:

1. Make a POST request to `/api/login/` with username and password credentials.
2. The response will contain a token to include in the `Authorization` header of subsequent requests (e.g., `Authorization: Token <your_token>`).

## API Documentation

- **Interactive API Documentation:** Explore the API endpoints interactively at `/api/schema/swagger-ui/`.
- **Raw API Schema:** Access the raw API schema data at `/api/schema/`.

## Endpoints

### User Groups

The API caters to different user groups with specific functionalities:

- **Doctors:** Can register patients, view/update patient profiles (with permission), update recommended treatment for assigned patients.
- **General Managers:** Can register doctors and patients, view/update all profiles, and manage user permissions.
- **Assistants:** Can register (by general managers), login, view/update their profiles (with permission), and update applied treatment for assigned patients (if authorized).

---

Here's a summarized list of the API endpoints for various functionalities in the system along with their descriptions and authentication/permission requirements:

### Assistant API Endpoints:
1. **Assistant Registration**
   - URL: `/api/assistant/registration/`
   - Method: POST
   - Permission: Required (`IsGeneralManager`)
   - Description: Registers a new assistant in the system.
  
2. **Assistant Login**
   - URL: `/api/assistant/login/`
   - Method: POST
   - Permission: Not required
   - Description: Authenticates an assistant and returns a token.
  
3. **Assistant Profile Retrieval**
   - URL: `/api/assistant/assistant-profile/{id}/`
   - Method: GET
   - Permission: Required (`IsGeneralManager`)
   - Description: Retrieves the profile details of a specific assistant.
  
4. **Assistant Profile Update**
   - URL: `/api/assistant/assistant-profile/{id}/`
   - Method: PUT
   - Permission: Required (`IsGeneralManager`)
   - Description: Updates the profile information of a specific assistant.
  
5. **Assistant Profile Deletion**
   - URL: `/api/assistant/assistant-profile/{id}/`
   - Method: DELETE
   - Permission: Required (`IsGeneralManager`)
   - Description: Deletes the profile of a specific assistant.

### Doctor API Endpoints:
1. **Doctor Registration**
   - URL: `/api/doctor/registration/`
   - Method: POST
   - Permission: Required (`IsGeneralManager`)
   - Description: Registers a new doctor in the system.
  
2. **Doctor Login**
   - URL: `/api/doctor/login/`
   - Method: POST
   - Permission: Not required
   - Description: Authenticates a doctor and returns a token.
  
3. **Doctor Profile Retrieval**
   - URL: `/api/doctor/doctor-profile/{id}/`
   - Method: GET
   - Permission: Required (`IsGeneralManager`)
   - Description: Retrieves the profile details of a specific doctor.
  
4. **Doctor Profile Update**
   - URL: `/api/doctor/doctor-profile/{id}/`
   - Method: PUT
   - Permission: Required (`IsGeneralManager`)
   - Description: Updates the profile information of a specific doctor.
  
5. **Doctor Profile Deletion**
   - URL: `/api/doctor/doctor-profile/{id}/`
   - Method: DELETE
   - Permission: Required (`IsGeneralManager`)
   - Description: Deletes the profile of a specific doctor.

### General Manager API Endpoints:
1. **General Manager Registration**
   - URL: `/api/general-manager/registration/`
   - Method: POST
   - Permission: Required (`IsAdmin`)
   - Description: Registers a new general manager in the system.

2. **General Manager Login**
   - URL: `/api/general-manager/login/`
   - Method: POST
   - Permission: Required
   - Description: Authenticates a general manager and returns a token.

### Patient API Endpoints:
1. **Patient Registration**
   - URL: `/api/patient/registration/`
   - Method: POST
   - Permission: Required (`IsGeneralManager` or `IsDoctor`)
   - Description: Registers a new patient in the system.

2. **Patient Login**
   - URL: `/api/patient/login/`
   - Method: POST
   - Permission: Not required
   - Description: Authenticates a patient and returns a token.

3. **Patient Profile Retrieval**
   - URL: `/api/patient/patient-profile/{id}/`
   - Method: GET
   - Permission: Required (`IsGeneralManager`)
   - Description: Retrieves the profile details of a specific patient.

4. **Patient Profile Update**
   - URL: `/api/patient/patient-profile/{id}/`
   - Method: PUT
   - Permission: Required (`IsGeneralManager`)
   - Description: Updates the profile information of a specific patient.

5. **Patient Profile Deletion**
   - URL: `/api/patient/patient-profile/{id}/`
   - Method: DELETE
   - Permission: Required (`IsGeneralManager`)
   - Description: Deletes the profile of a specific patient.

6. **Update Applied Treatment**
   - URL: `/api/patient/update-applied-treatment/{id}/`
   - Method: PUT
   - Permission: Requires Assistant to be assigned to the Patient
   - Description: Updates the applied treatment field of a patient's profile.

7. **Update Recommended Treatment**
   - URL: `/api/patient/update-recommended-treatment/{id}/`
   - Method: PUT
   - Permission: Requires Doctor to be associated with the Patient
   - Description: Updates the recommended treatment field of a patient's profile.

### Report API Endpoints:
1. **Doctor-Patient Report**
   - URL: `/api/report/doctor-patient-report/`
   - Method: GET
   - Permission: Required (`IsGeneralManager`)
   - Description: Retrieves a report on doctor-patient interactions.

2. **Patient Treatment Report**
   - URL: `/api/report/patient-treatment-report/{id}/`
   - Method: GET
   - Permission: Required (`IsGeneralManager` or `IsDoctor`)
   - Description: Retrieves a report on a specific patient's treatment history.

### Schema and Treatment API Endpoints:
1. **Schema**
   - URL: `/api/schema/`
   - Method: GET
   - Description: Retrieves the API schema.

2. **Treatment Creation**
   - URL: `/api/treatment/creation/`
   - Method: POST
   - Description: Creates a new treatment.

3. **Treatment Detail**
   - URL: `/api/treatment/treatment-detail/{id}/`
   - Method: GET, PUT, DELETE
   - Permission: Required (`IsGeneralManager` or `IsDoctor`)
   - Description: Retrieves, updates, or deletes details of a specific treatment.

You can clone the project repository mentioned at the beginning to access and test these API endpoints locally. Remember to install the required packages from the `requirements.txt` file and run the server using `python manage.py runserver`.
