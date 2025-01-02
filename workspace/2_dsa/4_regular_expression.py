# Regular expression in Python: a sequence of characters that forms a search pattern in a string
# usually used for pattern matching with strings speacially for search and replace

# Raw string: a string prefixed with r, which makes it a raw string. It means that the string is considered as it is,
# without any special characters being processed.
normal_string = "This is a normal\n string"

print(normal_string) # This is a normal <new line> string

raw_string = r"This is a raw\n string"

print(raw_string) # This is a raw\n string

# Meta characters: characters that have a special meaning in regular expressions
# . ^ $ * + ? { } [ ] \ | ( )
# re module: provides support for working with regular expressions
import re

line = "Better to die rather than to be a coward"
# re.match(): checks for a match only at the beginning of the string
searhObj = re.match(r'Better', line)

start = searhObj.start()
end = searhObj.end()
print(start, end) # 0 6
print("searhObj.group(): ", searhObj.group()) # Better

# re.search(): searches the string for a match, and returns a match object if there is a match
matchObj = re.search(r'coward', line)

print(matchObj.start(), matchObj.end()) # 34 40
print("matchObj.group(): ", matchObj.group()) # coward


matchObj = re.match(r'coward', line, re.M|re.I) # re.M: multiline, re.I: ignore case

if matchObj:
    print("match --> matchObj.group(): ", matchObj.group())
else:
    print("No match!!")

# No Match!!

searhObj = re.search(r'coward', line, re.M|re.I)

if searhObj:
    print("search --> searhObj.group(): ", searhObj.group())
else:
    print("Not found!!")

# search --> searhObj.group():  coward

# re.findall(): returns a list containing all matches
findallObj = re.findall(r'to', line)

print(findallObj) # ['to', 'to']

findallObj = re.findall(r"\w*", line)

print(findallObj) # ['Better', '', 'to', '', 'die', '', 'rather', '', 'than', '', 'to', '', 'be', '', 'a', '', 'coward', '']


# TODO check remaining methods of re module