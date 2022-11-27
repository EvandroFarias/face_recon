import sys

input_num = sys.argv[1]

def teste_fp(number):
    with open('guardianface\\src\\testedeescrita.txt',"w") as f:
        f.write(f'{number}\n')

if __name__ == '__main__':
    teste_fp(input_num)