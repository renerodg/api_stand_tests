import sender_stand_request
import data

def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body

def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()

    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]
    print(str_user)

    assert users_table_response.text.count(str_user) == 1

# Prueba 1. Creación de un nuevo usuario o usuaria
# El parámetro "firstName" contiene dos caracteres
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

test_create_user_2_letter_in_first_name_get_success_response()

# Prueba 2. Creación de un nuevo usuario o usuaria
# El parámetro "firstName" contiene 15 caracteres
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")


test_create_user_15_letter_in_first_name_get_success_response()

#Prueba 3 PREPARACION
# Función de prueba negativa
def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)

    print(f"Response status code: {response.status_code}")
    print(f"Response body: {response.json()}")

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == ("El nombre que ingresaste es incorrecto. "
                                         "Los nombres solo pueden contener caracteres latinos,  "
                                         "los nombres deben tener al menos 2 caracteres y no más de 15 caracteres")


#PRUEBA 3
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

test_create_user_1_letter_in_first_name_get_error_response()

# Prueba 4. Error
# El parámetro "firstName" contiene 16 caracteres
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")

test_create_user_16_letter_in_first_name_get_error_response()