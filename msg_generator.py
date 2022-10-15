from random import randint, choice

def custom_message(tool: str) -> str:
    #Generates a random number between 0 and 99
    rand = randint(0,100)

    hardware_members = ["@Jørgen Knoph",
                        "@Petter Nilsen",
                        "@Anette Hatlen",
                        "@Hauk Bjørneklett",
                        "@Filip Paw",
                        "@Magnus Cederkvist",
                        "@Erik Gabrielsen",
                        "@Sindre Nordtveit"]
    
    generic_messages_for_item = ["I have found a {tool}",
                                 "You may have misplaced a {tool}",
                                 "{tool} detected"]

    hate_messages = ["social credit deducted :social_credit:",
                     "excecution date: 马公鸡",
                     "castration imminent",
                     "you are a disgrace to your family",
                     ]

    #15 % chance of getting a hate message
    if rand < 15:
        return choice(hardware_members) + f". {tool} detected, " + choice(hate_messages)
    else:
        return choice(generic_messages_for_item).format(tool=tool)