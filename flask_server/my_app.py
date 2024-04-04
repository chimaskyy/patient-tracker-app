"""Application entry point"""

from . import (
    CORS,
    AuthApiError,
    AuthRetryableError,
    app,
    create_client,
    datetime,
    environ,
    json,
    jsonify,
    jwt,
    load_dotenv,
    make_response,
    request,
    time,
    timedelta,
    wraps,
    g
)

cor = CORS(app, resources={r"/*": {"origins": "*"}})
load_dotenv()
url = environ.get("SUPABASE_URL")
key = environ.get("SUPABASE_API_KEY")


supabase = create_client(url, key)


# error handler
@app.errorhandler(404)
def not_found(error):
    """404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({"error": "Not found", "message": error}), 404)


# check status route
@app.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """Status of API"""
    return jsonify({"status": "OK"})


#######################      api routes for medics      #######################
# get all medics
@app.route("/api/v1/medics", methods=["GET"], strict_slashes=False)
def get_medics():
    """get all medics"""
    try:
        data = supabase.table("medics").select("*").execute()
        # Assert we pulled real data.
        if not len(data.data) > 0:
            return jsonify({"message": "No medic found!"}), 404
        return jsonify({"count": len(data.data), "data": data.data}), 200
    except Exception as error:
        return jsonify({"message": "An error occurred!", "error": error})


# get medic by id
@app.route("/api/v1/medics/<medic_id>", methods=["GET"], strict_slashes=False)
def get_medic_by_id(medic_id):
    """get medic by id"""
    try:
        data = supabase.table("medics").select("*").eq("id", medic_id).execute()
        if not len(data.data) > 0:
            return jsonify({"message": "Medic not found!"}), 404
        return data.data
    except Exception as error:
        return jsonify({"message": "An error occurred!", "error": error})


# update medic by id
@app.route("/api/v1/medics/<medic_id>", methods=["PATCH"], strict_slashes=False)
def update_medic(medic_id):
    """update medic by id"""
    try:
        medic_data = request.get_json()
        data = supabase.table("medics").update(medic_data).eq("id", medic_id).execute()
        if not len(data.data) > 0:
            return jsonify({"message": "Medic not found!"}), 404
        return data.data
    except Exception as error:
        return jsonify({"message": "An error occurred!", "error": error})


# delete medic by id
@app.route("/api/v1/medics/<medic_id>", methods=["DELETE"], strict_slashes=False)
def delete_medic_by_id(medic_id):
    """get all users"""
    try:
        supabase.table("medics").delete().eq("id", medic_id).execute()
        return {}
    except Exception as error:
        return jsonify({"message": "An error occurred!", "error": error})


###################      api route for medical history     ####################
# create an authorization decorator
def authorize_medic(func):
    """routes are protected and accessed by medics only"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """functools wrapper function"""
        token = request.headers.get("Authorization").split("Bearer ")[1]
        try:
            payload = jwt.decode(token, environ.get("SECRET_KEY"), algorithms=["HS256"])
            if payload["category"] == "medic":
                g.user = payload
                return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 401

    return wrapper

# create patient's medical record
@app.route(
    "/api/v1/patients/<patient_id>/medical_record",
    methods=["POST"],
    strict_slashes=False,
)
# @authorize_medic
def create_medical_record(patient_id):
    """create medical record"""
    try:
        req_data = request.get_json()
        req_data["patient_id"] = patient_id
        data = supabase.table("medical_records").insert(req_data).execute()
        if not len(data.data) > 0:
            return jsonify({"message": "Could not create medical record!"})
        return data.data, 201
    except Exception as error:
        return jsonify({"message": "An error occurred!", "error": error})


# get patient's medical record
@app.route(
    "/api/v1/patients/<patient_id>/medical_record",
    methods=["GET"],
    strict_slashes=False,
)
def get_medical_record(patient_id):
    """get medical record"""
    try:
        data = (
            supabase.table("medical_records")
            .select("*")
            .eq("patient_id", patient_id)
            .execute()
        )
        if not len(data.data) > 0:
            return jsonify({"message": "Medical record not found!"}), 404
        return data.data
    except Exception as error:
        return jsonify({"message": "An error occurred!", "error": error})

# update patient's medical record
@app.route(
    "/api/v1/patients/<patient_id>/medical_record",
    methods=["PATCH"],
    strict_slashes=False,
)
# @authorize_medic
def update_medical_record(patient_id):
    """update medical record"""
    try:
        req_data = request.get_json()
        data = (
            supabase.table("medical_records")
            .update(req_data)
            .eq("patient_id", patient_id)
            .execute()
        )
        if not len(data.data) > 0:
            return jsonify({"message": "Medical record not found!"}), 404
        return data.data
    except Exception as error:
        return jsonify({"message": "An error occurred!", "error": error})


# delete patient's medical record
@app.route(
    "/api/v1/patients/<patient_id>/medical_record",
    methods=["DELETE"],
    strict_slashes=False,
)
# @authorize_medic
def delete_medical_record(patient_id):
    """delete medical record"""
    try:
        supabase.table("medical_records").delete().eq(
            "patient_id", patient_id
        ).execute()
        return {}
    except Exception as error:
        return jsonify({"message": "An error occurred!", "error": error})


######################      api routes for patients      ######################
# get all patients
@app.route("/api/v1/patients", methods=["GET"], strict_slashes=False)
def get_patients():
    """get all users"""
    try:
        data = supabase.table("patients").select("*").execute()
        if not len(data.data) > 0:
            return jsonify({"message": "No patient found!"}), 404
        return jsonify({"count": len(data.data), "data": data.data}), 200
    except Exception as error:
        return jsonify({"message": "An error occurred!", "error": error})


# get patient by id
@app.route("/api/v1/patients/<patient_id>", methods=["GET"], strict_slashes=False)
def patients_by_id(patient_id):
    """get patient by id"""
    try:
        data = supabase.table("patients").select("*").eq("id", patient_id).execute()
        if not len(data.data) > 0:
            return jsonify({"message": "Patient not found!"}), 404
        return data.data
    except Exception as error:
        return jsonify({"message": "An error occurred!", "error": error})

# update patient by id
@app.route(
    "/api/v1/patients/<patient_id>", methods=["PUT", "PATCH"], strict_slashes=False
)
def update_patients(patient_id):
    """update patient by id"""
    try:
        update_data = request.get_json()
        data = (
            supabase.table("patients")
            .update(update_data)
            .eq("id", patient_id)
            .execute()
        )
        if not len(data.data) > 0:
            return jsonify({"message": "Patient not found!"}), 404
        return data.data
    except Exception as error:
        return jsonify({"message": "An error occurred!", "error": error})

# delete patient by id
@app.route("/api/v1/patients/<patient_id>", methods=["DELETE"], strict_slashes=False)
def delete_patients_by_id(patient_id):
    """delete patient by id"""
    try:
        supabase.table("patients").delete().eq("id", patient_id).execute()
        return {}
    except Exception as error:
        return jsonify({"message": "An error occurred!", "error": error})


######################      api routes for users      ######################
# get all users
@app.route("/api/v1/users", methods=["GET"], strict_slashes=False)
def users():
    """get all users"""
    try:
        data = supabase.table("users").select("*").execute()
        if not len(data.data) > 0:
            return jsonify({"message": "No user found!"}), 404
        return jsonify({"count": len(data.data), "data": data.data}), 200
    except Exception as error:
        return jsonify({"message": "An error occurred!", "error": error})

# get user by id
@app.route("/api/v1/users/<user_id>", methods=["GET"], strict_slashes=False)
def user_by_id(user_id):
    """get all users"""
    try:
        data = supabase.table("users").select("*").eq("id", user_id).execute()
        if not len(data.data) > 0:
            return jsonify({"message": "User not found!"}), 404
        return data.data
    except Exception as error:
        return jsonify({"message": "An error occurred!", "error": error})

# update user by id
@app.route("/api/v1/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user_data(user_id):
    """get all users"""
    try:
        update_data = request.get_json()
        data = supabase.table("users").update(update_data).eq("id", user_id).execute()
        if not len(data.data) > 0:
            return jsonify({"message": "User not found!"}), 404
        return data.data
    except Exception as error:
        return jsonify({"message": "An error occurred!", "error": error})

# delete user by id
@app.route("/api/v1/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user_by_id(user_id):
    """get all users"""
    try:
        supabase.table("users").delete().eq("id", user_id).execute()

        return {}
    except Exception as error:
        return jsonify({"message": "An error occurred!", "error": error})


########################   authentication routes   #############################
# sign up route
@app.route("/auth/v1/signup", methods=["POST"], strict_slashes=False)
def signup():
    """signup function"""
    session = None
    try:
        user_data = request.get_json()
        session = supabase.auth.sign_up(
            {
                "email": user_data.get("email"),
                "password": user_data.get("password"),
            }
        )

        age_years = None
        age_months = None
        birthdate = None
        # check if user is patient
        if user_data.get("category") == "patient":
            birthdate = user_data.get("dob")
            birthdate = birthdate[:10]
            string_format = "%Y-%m-%d"

            # convert birthdate to datetime object
            birthdate_obj = datetime.strptime(birthdate, string_format)

            # Get today's date
            today = datetime.today()

            # Calculate the difference between today's date and the birthdate
            age_years = today.year - birthdate_obj.year
            age_months = today.month - birthdate_obj.month
            if age_months < 0:
                age_years -= 1
                age_months += 12

        # check if the user is signed up
        if session is not None:
            time.sleep(2)
            # Retrieve additional profile information
            session_data = json.loads(session.model_dump_json())
            user_id = session_data.get("user", {}).get("id")

            data = (
                supabase.table("users")
                .update(
                    {
                        "first_name": user_data.get("first_name"),
                        "last_name": user_data.get("last_name"),
                        "category": user_data.get("category"),
                        "age_years": age_years,
                        "age_months": age_months,
                        "specialization": user_data.get("specialization"),
                        "dob": birthdate,
                        "gender": user_data.get("gender"),
                        "address": user_data.get("address"),
                    }
                )
                .eq("id", user_id)
                .execute()
            )
            if not len(data.data) > 0:
                return "Could not create user!"
        return data.data
    except (AuthApiError, AuthRetryableError) as error:
        return jsonify({"message": "Sign up failed!", "error": error.message})


# sign in route
@app.route("/auth/v1/signin", methods=["POST"], strict_slashes=False)
def signin():
    """signin function"""
    session = None
    try:
        user_data = request.get_json()
        session = supabase.auth.sign_in_with_password(
            {
                "email": user_data.get("email"),
                "password": user_data.get("password"),
            }
        )

        if session is not None:
            time.sleep(2)
            session_data = json.loads(session.model_dump_json())
            user_id = session_data.get("user", {}).get("id")
            user_email = session_data.get("user", {}).get("email")

            user_category = supabase.table("users").select("category").eq(
                "email", user_data["email"]
            ).execute()

            token = generate_token(
                user_id=user_id,
                email=user_email,
                category=user_category.data[0]["category"],
            )
            return jsonify({"access_token": token})
        else:
            return jsonify({"message": "Sign in failed!"})
    except (AuthApiError, AuthRetryableError) as error:
        return jsonify({"message": "Sign in failed!", "error": error.message})


# generate access token for user authorization
def generate_token(user_id, email, category):
    """generate token"""
    custom_claims = {
        "sub": user_id,
        "email": email,
        "category": category,
    }

    payload = {
        **custom_claims,
        "exp": datetime.utcnow() + timedelta(days=1),
    }
    secret_key = environ.get("SECRET_KEY")
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


# sign out route
@app.route("/auth/v1/signout", methods=["POST"], strict_slashes=False)
def signout():
    """signout function"""
    try:
        supabase.auth.sign_out()
        if not supabase.auth.get_session():
            return jsonify({"message": "Sign out successful!"})
    except (AuthApiError, AuthRetryableError) as error:
        return jsonify({"message": "Sign out failed!", "error": error.message})

########################   storage route   #############################
# user profile picture upload
@app.route("/profile_pic_upload", methods=["POST"], strict_slashes=False)
def profile_pic_upload():
    """upload profile picture"""
    try:
        file = request.files["file"]
        req_token = request.headers.get("Authorization").split("Bearer ")[1]
        payload = jwt.decode(req_token, environ.get("SECRET_KEY"), algorithms=["HS256"])
        user_id = payload["sub"]

        file_name = file.filename
        file.save(f"images/{user_id}.png")

        data = (
            supabase.storage.from_("profile_image")
            .upload(f"images/{user_id}.png", f"{file_name}")
        )

        if not len(data.data) > 0:
            return jsonify({"message": "Could not upload file!"}), 404

        # update user profile picture
        data = (
            supabase.table("users")
            .update({"profile_pic": data.data[0]["url"]})
            .eq("id", user_id)
            .execute()
        )
        if not len(data.data) > 0:
            return jsonify({"message": "Could not update user profile picture!"}), 404
        return data.data
    except Exception as error:
        return jsonify({"message": "An error occurred!", "error": error})


if __name__ == "__main__":
    HOST = environ.get("SERVER_HOST", "localhost")
    PORT = int(environ.get("SERVER_PORT", 5555))

    print(f"Server running on {HOST}:{PORT}")

    app.run(debug=True, host=HOST, port=PORT)
