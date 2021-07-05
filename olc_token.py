#!/usr/bin/python3

from enum import Enum


class OLCToken:
    class Types(Enum):
        # literals
        INTEGER = 1
        IDENTIFIER = 2

        # keywords
        VAR = 101
        FUNC = 102
        RETURN = 103
        IF = 104
        ELSE = 105
        WHILE = 106
        SEMICOLON = 107
        PRINT = 108
        CLASS = 109

        # math operators
        ASSIGNMENT = 201
        ADDITION = 202
        SUBTRACTION = 203
        MULTIPLICATION = 204
        DIVISION = 205
        MODULO = 206

        # comparison operators
        EQUALITY = 301
        INEQUALITY = 302
        LESS_THAN = 303
        LESS_EQUAL = 304
        GREATER_THAN = 305
        GREATER_EQUAL = 306

        # logical operators
        AND = 401
        OR = 402
        NOT = 403

        # enclosures
        LEFT_PAREN = 501
        RIGHT_PAREN = 502
        LEFT_CURLY = 503
        RIGHT_CURLY = 504
        LEFT_SQUARE = 505
        RIGHT_SQUARE = 506

        EOF = 999

    def __init__(self, tokenType, literal, line):
        self.type = tokenType
        self.literal = literal
        self.line = line
