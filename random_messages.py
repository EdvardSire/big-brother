from random import randint, choice


def custom_message(tool: str) -> str:
    hardware_members = [
        "<@Jørgen Knoph>",
        "<@Petter Nilsen>",
        "<@Anette Hatlen>",
        "<@Hauk Bjørneklett>",
        "<@Filip Paw>",
        "<@Magnus Cederkvist>",
        "<@Erik Gabrielsen>",
        "<@Sindre Nordtveit>",
    ]

    generic_messages_for_item = [
        "I have found {tool}!",
        "You may have misplaced {tool}",
        "{tool} detected.",
        "There are {tool} on the workbench!"
    ]

    hate_messages = [
        "Social credit deducted :social_credit:",
        "Excecution date: 马公鸡",
        "Castration imminent",
        "You are a disgrace to your family"
    ]

    # 15 percent chance of getting a hate message
    rand = randint(0, 100)
    if rand < 15:
        return f"{tool} detected. {choice(hate_messages)} {choice(hardware_members)}"
    # return choice(hardware_members) + f". {tool} detected, " + choice(hate_messages)
    else:
        return choice(generic_messages_for_item).format(tool=tool)

