import g4f

index = 1
chosen_model = g4f.models.gpt_35_turbo
maintain_context = True

ver_list = ["GPT-3.5-Turbo", "GPT-3.5-Turbo16k", "GPT-4", "GPT-4-Turbo32k"]

messages = []

def set_model(idx):
    index = idx

def ask_gpt(messages: list)->str:
    if index == 0:
        chosen_model = g4f.models.gpt_35_turbo
        response = g4f.ChatCompletion.create(
            model=chosen_model,
            messages=messages)
    elif index == 1:
        chosen_model = g4f.models.gpt_35_turbo_16k
        response = g4f.ChatCompletion.create(
            model=chosen_model,
            messages=messages)
    elif index == 2:
        chosen_model = g4f.models.gpt_4
        response = g4f.ChatCompletion.create(
            model=chosen_model,
            messages=messages)
    elif index == 3:
        chosen_model = g4f.models.gpt_4_32k
        response = g4f.ChatCompletion.create(
            model=chosen_model,
            messages=messages)
    else:
        print("Unknown error")

    return response




def get_responce(prompt:str)->str:
    if maintain_context == True:
        messages.append({"role": "user", "content": prompt})

        resp = ask_gpt(messages)
        messages.append({"role": "assistant", "content": resp})
    elif maintain_context == False:
        messages.append({"role": "user", "content": prompt})

        resp = ask_gpt(messages)
        messages.clear()
    return resp

