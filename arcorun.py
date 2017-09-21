import discord
import os
import json
import subprocess
import hastebin
from datetime import datetime

def look_for_code(msg):
    """Checks the discord message for a code block. If there's no code, it returns an empty string."""
    
    try:
        code = msg.split("```")[1] # Looks for anything wrapped in a ``` block
        while code[0] == "`": # Gets rid of any extra `
            code = code[1:]
        return code.split("\n")
    except IndexError: # There's no ``` in the message content
        return ""


def detect_language(msg, code):
    """Checks code language and gives the following functions information regarding how to run the code."""
    
    lang_dict = {}
    for language in os.listdir(os.path.dirname(os.path.realpath(__file__)) + "/languages"):
        if language != "README.md": # That's not a .json file!
            with open(os.path.dirname(os.path.realpath(__file__)) + "/languages/" + language) as langjson:
                lang_dict[language[:-5]] = json.load(langjson)
    
    # Check markdown
    for language in lang_dict.keys():
        if code[0].lower() in lang_dict[language]["known_naming"]:
            code[0] = "" # Erase markdown language
            markdown_language = language

    # Check argument
    try:
        argument_provided = msg.split("```")[0].split(" ")[1].strip()
        for language in lang_dict.keys():
            if argument_provided.lower() in lang_dict[language]["known_naming"]:
                return lang_dict[language], code
    except IndexError:
        pass
    
    try:
        return lang_dict[markdown_language], code
    except UnboundLocalError: # There's no valid markdown
        return "", code

def create_file(language, extension, code, compiled):
    """create a file with the code provided, so it can be run or compiled later."""

    if not os.path.isdir(os.path.dirname(os.path.realpath(__file__)) + "/code"): # Generates /code folder if it doesn't exist
        os.mkdir(os.path.dirname(os.path.realpath(__file__)) + "/code")

    if not os.path.isdir(os.path.dirname(os.path.realpath(__file__)) + "/code/" + language): # Generates /code/language folder if it doesn't exist
        os.mkdir(os.path.dirname(os.path.realpath(__file__)) + "/code/" + language)
            
    file_path = "%s/code/%s/%s%s" % (os.path.dirname(os.path.realpath(__file__)), language, datetime.now().strftime("%d-%m-%Y_%H:%M:%S.%f"),  extension)
    with open(file_path, "a") as file: # Open the file to write on
        for line in code:
            file.write("%s\n" % line)

    if compiled: # Creates a special character free copy for compiling if it's needed
        file_compiled = "%s/code/%s/exec" % (os.path.dirname(os.path.realpath(__file__)), language)
        if not os.path.exists(file_compiled):
            os.mkdir(file_compiled)

        try:
            os.remove(file_compiled + "/plaincode" + extension)
        except FileNotFoundError:
            pass
        with open(file_compiled + "/plaincode" + extension, "a") as file: # Open the file to write on
            for line in code:
                file.write("%s\n" % line)
    else:
        file_compiled = ""


    return file_path, file_compiled
    




def run_compiler(file_path, language, compiler_exec, extension, flags = ""):
    """runs the compiler and generates an executable."""


    run_process = subprocess.Popen([compiler_exec] + flags + [file_path + "/executable", file_path + "/plaincode" + extension], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = run_process.communicate(timeout=60)
        if stdout:
            return "", stdout.decode("utf-8")
        elif stderr:
            return "", stderr.decode("utf-8")
        else:
            return file_path + "/executable", ""
    except subprocess.TimeoutExpired:
        run_process.kill()
        return 0



def execute_code(file_path, run_command, flags):
    """Creates a subprocess that runs the file, then grabs the stdout and stderr of said process."""
    
    timeout_flag = False
    if run_command: # For non-compiled languages
        run_process = subprocess.Popen([run_command] + flags + [file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        run_process = subprocess.Popen([file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        stdout, stderr = run_process.communicate(timeout=8)
    except subprocess.TimeoutExpired:
        stdout, stderr, timeout_flag = timeout(run_process)

    return stdout.decode("utf-8"), stderr.decode("utf-8"), timeout_flag


def timeout(process):
    """If the process timed out, returns the last 5 lines of output and kills the process"""
    line_number = 0
    stderr = b""
    stdout = b""
    while line_number <= 5:
        stdout += process.stdout.readline()
        line_number += 1
    process.kill()
    timeout_flag = True
    return stdout, stderr, timeout_flag

async def send_instructions(msg, client):
    """Sends the user who mentioned the bot all the instructions of how to use it."""

    supported_languages_raw = os.listdir(os.path.dirname(os.path.realpath(__file__)) + "/languages")
    supported_languages = []
    for language_raw in supported_languages_raw:
        if language_raw == "README.md":
            pass
        else:
            supported_languages.append(language_raw[:-5])

    instructions = ("Arcoex stands for **ar**bitrary **co**de **ex**ecution, and that's what this bot does! There are two ways to use me (you can use both at the same time if you want to):"
    "\n\n**1.** Mention me among with the language of the code you want to run, and then add the code warped in between \`\`\`, making a code block. (This method overrides the next one if"
    "both are specified at the same time) Here's an example:\n\n<@" + client.user.id + "> bash ```\n echo(\"I'm using the first method!\")```\n**2.** Mention me among your code warped in between"
    "\`\`\`, and specify the language of your code right after the first set of \`\`\` (This method will add syntax markdown to your code). Here's an example:\n\n<@350327901788569612> ```bash"
    "\n echo(\"I'm using the second method!\")```\nSo far, the supported languages are " + ", ".join(supported_languages[:-1]) + " and " + supported_languages[-1] + "."
    "\n\nMessage Kurolox if you want to add more, or check out the Github page if you want to contribute: https://github.com/Kurolox/ArcoexBot")

    await client.send_message(msg.author, instructions)
    if msg.server != None: # If the bot wasn't mentioned in a private chat
        await client.send_message(msg.channel, "I've sent you the bot instructions via PM.")


async def bot_reply(msg, client, signal, code_output="", compiler_output="", language=""):
    """Makes the bot reply depending on the signal."""
    
    try:
        if signal == 0: # There was no code detected on the message
            await client.send_message(msg.channel, "I'm sorry, but I'm not seeing any code to run.")
        elif signal == 1: # There was only a mention of the bot
            await send_instructions(msg, client)
        elif signal == 2: # detect_language() couldn't detect the language
            await client.send_message(msg.channel, "I'm sorry, but you didn't specify the language of the code or it isn't supported yet.")
        elif signal == 3: # The compiler ran into issues
            await client.send_message(msg.channel, "I've encountered the following error when compiling your %s code. \n```\n%s```" % (language, compiler_output))
        elif signal == 4: # The process timeouted
            await client.send_message(msg.channel, "I'm sorry, but your request took too long. Here are the last 5 lines from the output.\n```\n%s```" % code_output)
        elif signal == 5: # There were errors when running the code
            await client.send_message(msg.channel, "I've encountered the following error when running your %s code. \n```\n%s```" % (language, code_output))
        elif signal == 6: # Everything went well
            await client.send_message(msg.channel, "Here's the output of your %s code. \n```\n%s```" % (language, code_output))
    except discord.errors.HTTPException: # Unless the message was +2000 characters
        try:
            await client.send_message(msg.channel, "I'm sorry, but the output is too long for Discord. You can check the output of your %s code here. %s" % (language, hastebin.post(code_output)))
        except KeyError: # Not even hastebin wants the output
            await client.send_message(msg.channel, "I'm sorry, but the output is too long for Discord. Hell, it's even too long for hastebin. Though luck, I guess. *¯\_(ツ)_/¯*")
async def code(msg, client):
    """Grab the code block from a message, run it and return the output."""
    
    code = look_for_code(msg.content)
    if not code:
        if msg.content != ("<@%s>" % client.user.id): # if the message content is not just a mention
            await bot_reply(msg, client, 0)
        else: # if the message content is only a mention to the bot
            await bot_reply(msg, client, 1)
    else:
        lang_json, code = detect_language(msg.content, code)
        if not lang_json: # The language wasn't detected
            await bot_reply(msg, client, 2)
        else:
            file_path, compiled_copy = create_file(lang_json["language"], lang_json["file_extension"], code, lang_json["compiled"])
            if lang_json["compiled"]: # Code needs to be compiled
                exec_path, compiler_output = run_compiler(compiled_copy, lang_json["language"], lang_json["compiler_exec"],lang_json["file_extension"], flags= lang_json["compiler_flags"])
                if compiler_output: # Errors when compiling
                    await bot_reply(msg, client, 3, compiler_output=compiler_output, language=lang_json["language"])
                else:
                    output, error, timeout_flag = execute_code(exec_path, lang_json["exec"], lang_json["exec_flags"])
                    if timeout_flag: # The process did timeout
                        await bot_reply(msg, client, 4, code_output=output)
                    elif error: # There's something on stderr
                        await bot_reply(msg, client, 5, code_output=error, language=lang_json["language"])
                    else: # Everything went fine
                        await bot_reply(msg, client, 6, code_output=output, language=lang_json["language"])

            else: # Code can be run directly
                output, error, timeout_flag = execute_code(file_path, lang_json["exec"], lang_json["exec_flags"])
                if timeout_flag: # The process did timeout
                    await bot_reply(msg, client, 4, code_output=output)
                elif error: # There's something on stderr
                    await bot_reply(msg, client, 5, code_output=error, language=lang_json["language"])
                else: # Everything went fine
                    await bot_reply(msg, client, 6, code_output=output, language=lang_json["language"])
