import os
import random

from faker import Faker


def create_word():
    fake = Faker()
    return fake.sentence().split()[0]


def run():
    max_depth = 4

    project_url = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    random.randrange(0, max_depth)

    for _ in range(max_depth):
        path = project_url + '/fixtures/Voluptates/' + create_word()
        os.makedirs(path)

        with open(path + '/t.csv', 'w+') as file:
            line = ''
            for _ in range(random.randrange(2, 15)):
                num = random.randrange(0, 100)
                line += str(num)
                line += ','

            file.write(line)




