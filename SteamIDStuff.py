import math

def shorten_appid(longId) -> str:
    UNsige = int(longId) & 0xFFFFFFFF
    return str(UNsige)


if __name__ == "__main__":
    Tests = shorten_appid("-1724118575")
    print(Tests)