from train_model import *

def get_password_strength(password):
    model = get_model()
    password_matrix = password_features(password).reshape(1, -1)
    strength = model.predict(password_matrix)
    return strength[0] * 5



if __name__ == "__main__":
    while True:
        password = input("Enter a password: ")
        score = get_password_strength(password)
        print ("Password strength: " + str(score))