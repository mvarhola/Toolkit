#!/usr/bin/env python2.7
#encoding=UTF-8

__author__ = 'setr'

from TreeGenerator import Node
from TreeGenerator import testCall
from os.path import exists
import codecs
from sys import argv, exit
import argparse

class TextParser:
    def __init__(self):
        self.HEADER = "*"
        self.VERBOSITY = False

    def getText(self, fileIn):
        theText = []
        if exists(fileIn):
            with codecs.open(fileIn, 'r', encoding='UTF-8') as r:
                for line in r:
                    theText.append(line.strip())
            return theText
        else:
            exit("File does not exist")

    def getLevel(self, line):
        if len(line):
            if line[0] == self.HEADER:
                count = 0
                for char in line:
                    if char == self.HEADER:
                        count += 1
                    else:
                        break
                return count
        return None

    def cleanLine(self, line):
        return line.strip(self.HEADER).lstrip()

    def findPreviousLevelAndAttach(self, parent, newNode):
        if self.VERBOSITY:
            print "FOR NODE", newNode.name
            print "LOOKING FOR", newNode.level
            print "AT", parent.name
        if parent.level < newNode.level:
            parent.addChild(newNode)
            return parent
        else:
            return self.findPreviousLevelAndAttach(parent.Parent, newNode)

    def levelChanged(self, level, lastLevel):
        if level == lastLevel:
            return False
        else:
            return True

    def parseText(self, theText):
        root = Node(None)
        Parent = root
        newNode = Node(None)
        lastLevel = 0

        for line in theText:
            level = self.getLevel(line)
            line = self.cleanLine(line)
            if level is not None:  # Happens when there's no HEADER on the line
                newNode = Node(line)
                newNode.level = level
                self.findPreviousLevelAndAttach(Parent, newNode)
                if self.levelChanged(level, lastLevel):
                    Parent = newNode
                lastLevel = level
                if Parent is None:
                    print "We shouldn't be here"
            else:
                if self.VERBOSITY:
                    print "IGNORED LINE:", line
        return root

    def startParse(self, isFile, fileIn):
        theText = ""
        if isFile:
            theText = self.getText(fileIn)
        else:
            theText = [line.strip() for line in fileIn.splitlines()]
        root = self.parseText(theText)
        return root

def parseCommandLine():
    parser = argparse.ArgumentParser(
            prog="Tree-Generator",
            description="Generates a tree representation of a hierarchy from the specified file")

    # Positional Args
    parser.add_argument(
            "infile",
            default=None,
            nargs='?',
            help="File to be parsed. Necessary unless -t is used")
    parser.add_argument(
            "outfile",
            default=None,
            nargs='?',
            help="specify output file. Ifot specified, prints tree to screen")

    # Flags
    parser.add_argument(
            "-d", "--default",
            action="store_true",
            help="sets outfile to infile_OUT")
    parser.add_argument(
            "-t", "--test",
            action="store_true",
            help="runs test outline")
    parser.add_argument(
            "-H", "--header",
            default="*",
            help="Header identifier used in the infile")
    parser.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="increase verbosity ")
    return parser.parse_args()


if __name__ == "__main__":

    parser = TextParser()
    args = parseCommandLine()

    # and now to deal with our options
    parser.HEADER = args.header
    parser.VERBOSITY = args.verbose

    if args.test:
        testCall()
    elif args.infile is None:
        exit("Expecting input file")
    else:
        if args.default:
            outFile = args.infile + "_OUT"
        else:
            outFile = args.outfile

        root = parser.startParse(True, args.infile)
        output = root.printAll()
        output.encode("UTF-8")

        if not len(output):
            exit("Could not find any parseable lines")
        if outFile is None:
            print output
        else:
            with codecs.open(outFile, 'w', encoding="UTF-8") as w:
                w.write(output)
                w.write("\n")


