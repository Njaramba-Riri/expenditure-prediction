from faker import Faker

fake = Faker()

for i in range(10):
    cout = fake.country()
    
    x = input("Choose a number: ")
    print(f"{i}: {cout}")
