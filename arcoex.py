import discord
from subprocess import Popen, PIPE, TimeoutExpired
import logging
import os
from sys import path
from credentials import token
from datetime import datetime

# Enable logging
logging.basicConfig(level=logging.INFO)

bot_client = discord.Client()


@bot_client.event
async def on_ready():
    print('Logged in as')
    print(bot_client.user.name)
    print(bot_client.user.id)
    print('------')
    await bot_client.change_presence(game=discord.Game(name='Mention me for instructions!'))


@bot_client.event
async def on_message(msg):
    with open("botlog", "a") as log:
        log.write("%s %s MSG: %s\n" % (datetime.now(), msg.author, msg.content))
        print("%s %s MSG: %s\n" % (datetime.now(), msg.author, msg.content))
    if msg.content.startswith('!test'):  # Test function
        await bot_client.send_message(msg.channel, 'Test received!')
    elif msg.content.startswith('<@350327901788569612>') and msg.author != ("Arcoex Bot"):  # Toggled when the bot is mentioned
        await code(msg)


def check_code(message):
    """Checks if the message actually does have code to run"""
    try:
        primitive_code = message.split("```")[1]
    except IndexError:
        return 0
    return primitive_code.split("\n")


def check_lang(message, code):
    """Checks if there's an argument or a language specified in the code."""
    compatible_languages = {
        "python": ("python", "py", "pycode"),
        "bash": ("bash", "sh"),
        "rust": ("rust", "rs"),
        "javascript": ("javascript", "js"),
        "guile": ("guile"),
        "cpp": ("c++", "cpp")}

    detected_lang = ""
    try:
        argument = message.split("```")[0].split(" ")[1]  # Checks argument
    except IndexError:
        argument = ""
    for language, diff_naming in compatible_languages.items():
        if argument.lower() in diff_naming:
            detected_lang = language
 
    if code[0] == "":
        if detected_lang != "":
            return detected_lang, code
        else:
            return 0, code
    else:
        for language, diff_naming in compatible_languages.items():
            if code[0] in diff_naming:
                detected_lang = language
                code[0] = ""
                return detected_lang, code
            
    return 0, code


def build_exec(lang, code):
    """Creates a file with the provided code in it."""
    lang_to_filetype = {
        "python": ".py",
        "bash": ".bash",
        "rust": ".rs",
        "javascript": ".js",
        "guile": ".scm",
        "cpp": ".cpp"}
    date = str(datetime.now())
    filename = "%s/%s/%s%s" % (path[0], lang, date.replace(" ", "--"), lang_to_filetype[lang])
    with open(filename, "a") as file:
        for line in code:
            file.write("%s\n" % line)
    return filename


def run_code(lang, filename):
    """Runs a file and returns the stdout, stderr and a flag if the process timed out."""
    loop_flag = False
    if lang == "python":
        process = Popen(["umlbox", "--cwd", "/arcoex", "-B", "-fw", "/arcoex", "-f", "/bot/python", "-m", "512M", "-T", "10", "python3", filename], stdout=PIPE, stderr=PIPE)
    elif lang == "bash":
        process = Popen(["umlbox", "--cwd", "/arcoex", "-B", "-fw", "/arcoex", "-f", "/bot/bash", "-m", "512M", "-T", "10", "bash", filename], stdout=PIPE, stderr=PIPE)
    elif lang == "javascript":
        process = Popen(["umlbox", "--cwd", "/arcoex", "-B", "-fw", "/arcoex", "-f", "/bot/javascript", "-m", "512M", "-T", "10", "nodejs", filename], stdout=PIPE, stderr=PIPE)
    elif lang == "guile":
        process = Popen(["umlbox", "--cwd", "/arcoex", "-B", "-fw", "/arcoex", "-f", "/bot/guile", "-m", "512M", "-T", "10", "guile", "--no-auto-compile", filename], stdout=PIPE, stderr=PIPE)
    elif lang == "cpp":
        os.system("rm /bot/cpp/compiled/*")
        os.system("cp " + filename + " /bot/cpp/compiled/temptext.cpp")
        os.system("g++ /bot/cpp/compiled/temptext.cpp")
        process = Popen(["umlbox", "--cwd", "/arcoex", "-B", "-fw", "/arcoex", "-f", "/bot/cpp", "-m", "512M", "-T", "10", "/bot/cpp/compiled/a.out"], stdout=PIPE, stderr=PIPE)
    elif lang == "rust":
        os.system("rm /bot/rust/compiled/*")
        os.system("cp " + filename + " /bot/rust/compiled/temptext.rs")
        os.system("rustc /bot/rust/compiled/temptext.rs -o /bot/rust/compiled/tempexec")
        process = Popen(["umlbox", "--cwd", "/arcoex", "-B", "-fw", "/arcoex", "-f", "/bot/rust", "-m", "512M", "-T", "10", "/bot/rust/compiled/tempexec"], stdout=PIPE, stderr=PIPE)
    try:
        stdout, stderr = process.communicate(timeout=5)
    except TimeoutExpired:
        stdout, stderr, loop_flag = timeout(process)
    return stdout.decode("utf-8"), stderr.decode("utf-8"), loop_flag


def timeout(process):
    """If the process timed out, returns the last 5 lines of output and kills the process"""
    line_number = 0
    stderr = b""
    stdout = b""
    while line_number < 6:
        stdout += process.stdout.readline()
        line_number += 1
    process.kill()
    loop_flag = True
    return stdout, stderr, loop_flag


async def code(msg):
    """Grabs the code from a message, identifies the language, runs it and sends the output."""
    code = check_code(msg.content)
    if not code:
        if msg.content == ("<@350327901788569612>"):
            await bot_client.send_message(msg.channel, "Arcoex stands for **ar**bitrary **co**de **ex**ecution, and that's what this bot does! There are two ways to use me (you can use both at the same time if you want to):\n\n**1.** Mention me among with the language of the code you want to run, and then add the code warped in between \`\`\`, making a code block. (This method overrides the next one if both are specified at the same time) Here's an example:\n\n<@350327901788569612> bash ```\n echo(\"I'm using the first method!\")```\n**2.** Mention me among your code warped in between \`\`\`, and specify the language of your code right after the first set of \`\`\` (This method will add syntax markdown to your code). Here's an example:\n\n<@350327901788569612> ```bash\n echo(\"I'm using the second method!\")```\nSo far, the supported languages are bash, rust, cpp, javascript, guile and python. Message Kurolox if you want to add more!")

        else:
            await bot_client.send_message(msg.channel, "There's no code to run.")
    else:
        lang, code = check_lang(msg.content, code)
        if not lang:
            await bot_client.send_message(msg.channel, "The language wasn't specified.")
        else:
            filename = build_exec(lang, code)
            output, error, loop_flag = run_code(lang, filename)
            if error:
                await bot_client.send_message(msg.channel, "The bot has encountered the following error when running your %s code. \n```\n%s```" % (lang, error))
            elif loop_flag:
                await bot_client.send_message(msg.channel, "I'm sorry, but your request took too long. Here are the last 5 lines from the output.\n```\n%s```" % output)
            else:
                await bot_client.send_message(msg.channel, "Here's the output of your %s code. \n```\n%s```" % (lang, output))


bot_client.run(token)
