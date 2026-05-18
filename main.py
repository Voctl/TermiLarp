from term_image.image import from_file
import requests
import json

def chat(prompt: str, personality: str) -> str:
    return "This is your answer"

def load_character():
    with open("character.json", "r", encoding="utf-8") as f:
        character = json.load(f)
    return character

def display_image(character_image: str, width: int, height: int):
    image = from_file(character_image)
    image.set_size(width=width, height=height)
    image.draw()

def main():

    character = load_character()

    character_name = character["name"]
    character_personality = character["personality"]
    character_image = character["image"]

    display_image(character_image, 50, 20)

    while True:
        prompt = input("You: ")

        if prompt in ["exit", "quit", "leave"]:
            return

        answer = chat(prompt, character_personality)

        print(f"{character_name}: {answer}")

if __name__ == "__main__":
    main()