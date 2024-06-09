import csv
import re
from pprint import pprint


def parse_row(row: list[dict]) -> list:
    payload = {}
    for person in row:
        name = person.get("lastname")
        first_name = person.get("firstname")
        surname = person.get("surname")
        a = parse_name((name, first_name, surname))
        person.update(a)
        b = parse_phone(person.get("phone"))
        person.update(b)
        key = ' '.join((person.get("lastname"), person.get("firstname")))
        payload.setdefault(key, []).append(person)
    for person, data in payload.items():
        payload[person] = merge(data)
    return list(payload.values())


def merge(dicts: list[dict]) -> dict:
    payload = {}
    for di in dicts:
        for k, v in di.items():
            if di.get(k) is not None:
                payload[k] = di.get(k)
    return payload

def parse_name(name: tuple[str, str, str]) -> dict:
    for i in range(len(name)):
        if len(name[i].split(" ")) == 3:
            lastname, firstname, surname = name[i].split(" ")
            return {"lastname": lastname, "firstname": firstname, "surname": surname}
        elif len(name[0].split(" ")) == 2:
            last, first = name[0].split(" ")
            return {"lastname": last, "firstname": first, "surname": name[-1]}
        elif len(name[1].split(" ")) == 2:
            first, sur = name[1].split(" ")
            return {"lastname": name[0], "firstname": first, "surname": sur}
        else:
            return {"lastname": name[0], "firstname": name[1], "surname": name[2]}


def parse_phone(phone: str) -> dict:
    if phone:
        if "доб" in phone:
            add = phone.split(" ")
            s = list(map(lambda x: x.strip("()"), add[-2:]))
            x = add[:-2]
            x.extend(s)
            phone = " ".join(x)

        if re.search(r"\+7[0-9]{10}$", phone):
            phone = f"{phone[:2]}({phone[2:5]}){phone[5:8]}-{phone[8:10]}-{phone[10:]}"
        elif re.search(r"8\s[0-9]{3}-", phone):
            phone = f"+7({phone[2:5]}){phone[6:9]}-{phone[10:12]}-{phone[12:]}"
        elif re.search(r"\+7\s\([0-9]{3}\)", phone):
            phone = phone.split(" ")
            if "доб." in phone:
                phone = ''.join(phone[:3]) + " " + ''.join(phone[3:])
            else:
                phone = ''.join(phone[:3])
        elif re.search(r"8\([0-9]{3}\)", phone):
            phone = f"+7{phone[1:]}"
        else:
            return {'phone': phone}
        return {'phone': phone}
    else:
        return {'phone': phone}


if __name__ == "__main__":
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # список словарей - каждый слварь - строка из csv файла
        payload = []
        for row in reader:
            myfixedrow = {k: (None if v == "" else v) for k, v in row.items()}
            payload.append(myfixedrow)
            print(myfixedrow)
        print("------------")

    parsed_file = parse_row(payload)  # список обработынных записей
    print()
    # TODO 2: сохраните получившиеся данные в другой файл

    with open("NEW_phonebook.csv", "w", encoding="utf-8") as f:
        fieldnames = parsed_file[0].keys()
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        for row in parsed_file:
            writer.writerow(row)
