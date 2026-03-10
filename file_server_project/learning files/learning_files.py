from pathlib import Path



def read_file():
    #open file
    file = open('characters.txt', 'r')

    #read the file
    # content = file.read()
    # print(content)

    #new method to read in lines
    lines = file.readlines()
    for line in lines:
        print(line)

    #close the file
    file.close()


def write_to_file(filename):
    characters = ['a', 'b', 'c']
    #open file
    file = open(filename, 'w+')

    #write to the file
    for c in characters:
        file.write (c+ '\n')

    #למקם את האינדקס בהתחלה
    file.seek(0,0)
    content = file.read()
    print(content)



    #close the file
    file.close()



def write_to_file_from_the_end(filename):
    characters = ['more', 'more']
    file = open(filename, 'a')
    for c in characters:
        file.write(c+'\n')


def create_path():
    #directory path
    script_dir = Path(__file__).parent
    #file path
    path = script_dir/'characters'
    #making the directory
    path.mkdir(parents= True, exist_ok=True)

    path = path / 'zelda.txt'

    #file = path.open('w')
   # file.write("ganon")

    #file = path.open('a')
    #file.write(('\nLink'))

    # file = path.open('r')
    # content = file.read()
    # print(content)
    #
    # file.close()

    path.write_text("hello")
    content = path.read_text()
    print(content)




def open_file():
    path = Path(__file__).parent
    path = path / 'does' / 'not' / 'exist.txt'

    try:
        file = path.open('r')
        content = file.read()
        print(content)
        file.close()
    except Exception as e:
        print(f"unexpected error {e}")
        print(f"{path} does not exist")


def open_file1():
    path = Path(__file__).parent / 'characters.txt'
    data = {'a', 'b', 'c'}

    #context managers --> auto closes
    with path.open('w') as file:
        for d in data:
            file.write(d + '\n')





def main():
    #write_to_file('characters.txt')
    #read_file()
    #write_to_file_from_the_end('characters.txt')
    #create_path()
    open_file1()


if __name__=="__main__":
    main()