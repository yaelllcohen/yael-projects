from pathlib import Path
import json

path = Path(__file__).parent / 'characters.json'

characters = {
    "noa": 27,
    "yael": 2,
    "adir": 3
}

def write_json():
    with path.open('w') as file:
        json.dump(characters, file, indent= 2)


def read_json():
    with path.open('r') as file:
        data = json.load(file)
    return data


def main():
    write_json()
    data = read_json()
    print(data)

if __name__ == "__main__":
    main()