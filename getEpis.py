from os import remove

def create_input_file(url, totalEps):
    remove("./input.txt")

    for ep in range(1, int(totalEps) + 1):
        with open("input.txt", "a", encoding='utf-8') as file:
            file.write(url + "/" + str(ep) + "/" + "\n")
    print("Finished")
