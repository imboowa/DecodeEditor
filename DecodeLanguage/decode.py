from customtkinter import CTkTextbox
from interface import settings


def mathOperations(operation: str, vars: dict, flags: dict, tempResult: str, tempVar1: str, tempVar2: str) -> tuple[dict, str, str]:

    """ Carries Out The Mathematical Operations """

    var1 = tempVar1
    var2 = tempVar2

    # Check If var1 In vars
    if var1 in vars:
        var1 = vars[var1]

    # Check If var2 In vars
    if var2 in vars:
        var2 = vars[var2]

    result: int = 0
    try:
        match operation:
            case "add":
                result = int(var1) + int(var2)
            case "sub":
                result = int(var1) - int(var2)
            case "mul":
                result = int(var1) * int(var2)
            case "div":
                # Division By Zero
                if int(var2) == 0:
                    flags["zero_division"] = 1
                    flags["no_errors"] = False
                    return flags, None, None
                else:
                    # Enforce Integer Division
                    result = int(var1) // int(var2)
    except ValueError:
        flags["not_integer"] = 1
        flags["no_errors"] = False
        return flags, None, None

    return flags, tempResult, str(result)


def setVariable(vars: dict, tempArg1: str, tempArg2: str) -> dict:

    """ Sets A New Variable """

    # Is This Variable Already Existing
    if tempArg1 in vars:
        # Is "Value" A Variable Too
        if tempArg2 in vars:
            vars[tempArg1] = vars[tempArg2]
            return vars
        else:
            vars[tempArg1] = tempArg2
            return vars

    # Imagine It Is A New Variable
    # Is "Value" A Variable
    if tempArg2 in vars:
        tempArg2 = vars[tempArg2]

    # Create A New Variable
    vars[tempArg1] = tempArg2
    return vars


def printr(vars: dict, tempArg1: str) -> str:

    """ Print A Value To Screen """

    # If Value Is A Variable
    if tempArg1 in vars:
        return vars[tempArg1]
    else:
        return tempArg1

def executeLine(lineContent: str, vars: dict, flags: dict, execCounter: int, tempIndex: int, tempValue: str, IF_FLAG: int, codeSpan: int, output_position: int, output_destination: CTkTextbox) -> tuple[dict, dict, int, int, int, int, int]:

    """ Executes A Line Of Code """

    # Error Checking
    if not lineContent:
        return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position
    # Remove Newline Character
    lineContent = lineContent.strip("\n")
    # Get Command
    tempCommand = lineContent.split(" ")

    # Printr To result Screen
    if tempCommand[0] == "printr" and IF_FLAG == 1:
        # Even Empty Arguments Lead To Newline
        if len(tempCommand) == 1 or "" in tempCommand:
            output_destination.configure(state="normal")
            output_destination.insert("end", '\n')
            output_destination.configure(state="disabled")
        else:
            tempArg1: str = tempCommand[1]
            result = printr(vars, tempArg1)
            output_destination.configure(state="normal")
            output_destination.insert("end", f'{result}' if len(str(result)) <= settings.limit * 10 else f"{str(result)[:settings.limit * 10]}...")
            output_destination.tag_add("normal_text", f"{output_position}.0", f"{output_position}.end")
            output_destination.configure(state="disabled")
            # Putting Update Here Because Newline Characters Cannot Work With Tags
            output_position += 1
        return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position

    # Comments
    elif tempCommand[0] == "//" and IF_FLAG == 1:
        return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position

    # Check If Anything In tempCommand Has A Length 0 Meaning We Got No Arguments Still
    # Only printr Can Have No Arguments Because No Arguments To printr Means Newline Character
    # Only // (comments) Can Have Empty Slots (No Arguments) And No Arguments Are Ignored
    if "" in tempCommand:
        flags["argument_error"] = 1
        flags["no_errors"] = False
        return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position

    # Initializing Or Setting Variables
    elif tempCommand[0] == "set" and IF_FLAG == 1:
        tempArg1: str = tempCommand[1]
        tempArg2: str = tempCommand[2]
        if not tempArg1 or not tempArg2:
            return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position
        else:
            vars = setVariable(vars, tempArg1, tempArg2)

    elif tempCommand[0] == "add" and IF_FLAG == 1:
        tempResultVar = tempCommand[1]
        tempArg1: str = tempCommand[2]
        tempArg2: str = tempCommand[3]
        if not tempArg1 or not tempArg2 or not tempResultVar:
            return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position
        else:
            flags, tempResult, value = mathOperations(tempCommand[0], vars, flags, tempResultVar, tempArg1, tempArg2)
            if tempResult is None or value is None:
                 return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position
            if tempResult in vars:
                vars[tempResult] = str(value)
            else:
                # If Not A Variable
                # Create One With The result
                vars[tempResult] = str(value)

    elif tempCommand[0] == "sub" and IF_FLAG == 1:
        tempResultVar = tempCommand[1]
        tempArg1: str = tempCommand[2]
        tempArg2: str = tempCommand[3]
        if not tempArg1 or not tempArg2 or not tempResultVar:
            return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position
        else:
            flags, tempResult, value = mathOperations(tempCommand[0], vars, flags, tempResultVar, tempArg1, tempArg2)
            if tempResult is None or value is None:
                 return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position
            if tempResult in vars:
                vars[tempResult] = str(value)
            else:
                # If Not A Variable
                # Create One With The result
                vars[tempResult] = str(value)

    elif tempCommand[0] == "mul" and IF_FLAG == 1:
        tempResultVar = tempCommand[1]
        tempArg1: str = tempCommand[2]
        tempArg2: str = tempCommand[3]
        if not tempArg1 or not tempArg2 or not tempResultVar:
            return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position
        else:
            flags, tempResult, value = mathOperations(tempCommand[0], vars, flags, tempResultVar, tempArg1, tempArg2)
            if tempResult is None or value is None:
                 return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position
            if tempResult in vars:
                vars[tempResult] = str(value)
            else:
                # If Not A Variable
                # Create One WIth The result
                vars[tempResult] = str(value)

    elif tempCommand[0] == "div" and IF_FLAG == 1:
        tempResultVar = tempCommand[1]
        tempArg1: str = tempCommand[2]
        tempArg2: str = tempCommand[3]
        if not tempArg1 or not tempArg2 or not tempResultVar:
            return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position
        else:
            flags, tempResult, value = mathOperations(tempCommand[0], vars, flags, tempResultVar, tempArg1, tempArg2)
            if tempResult is None or value is None:
                return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position
            if tempResult in vars:
                vars[tempResult] = str(value)
            else:
                # If Not A Variable
                # Create One With The result
                vars[tempResult] = str(value)

    elif tempCommand[0] == "when" and IF_FLAG == 1:
        tempCondition = tempCommand[1]
        if not tempCondition:
            return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position
        else:
            tempValue = tempCondition
            tempIndex = execCounter

    elif tempCommand[0] == "end" and IF_FLAG == 1:
        # Handles Nested Loops Hence No Errors
        if not tempValue:
            # Skip It Then - Not Helping In Code
            return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position
        else:
            # Is tempValue A Variable
            if tempValue in vars:
                try:
                    if int(vars[tempValue]) != 0:
                        execCounter = tempIndex - 1
                    return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position
                except ValueError:
                    flags["not_integer"] = 1
                    flags["no_errors"] = False
                    return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position
            try:
                # Is tempValue Just A Number
                if int(tempValue) != 0:
                    execCounter = tempIndex - 1
                else:
                    tempIndex = 0
                    tempValue = ""
            except ValueError:
                flags["not_integer"] = 1
                flags["no_errors"] = False

    elif tempCommand[0] == "if" and IF_FLAG == 1:
        tempConditionVar1 = tempCommand[1]
        tempConditionVar2 = tempCommand[2]
        if not tempConditionVar1 or not tempConditionVar2:
            return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position
        else:
            if tempConditionVar1 in vars:
                tempConditionVar1 = vars[tempConditionVar1]
            if tempConditionVar2 in vars:
                tempConditionVar2 = vars[tempConditionVar2]
            try:
                # Do They Match Whether Variables Or Values
                if int(tempConditionVar1) == int(tempConditionVar2):
                    IF_FLAG = 1
                else:
                    IF_FLAG = 0
            except ValueError:
                flags["not_integer"] = 1
                flags["no_errors"] = False

    elif tempCommand[0] == "done":
        # Release Execution When Locked
        if IF_FLAG == 0:
            IF_FLAG = 1

    elif tempCommand[0] == "branch" and IF_FLAG == 1:
        # Big Reminder: Comments Are Valid Indexes When Using Branch Meaning A Comment Is Counted As Pseudocode And Has An Index
        # When Using branch Please Consider Comments Too As Valid Indexes In Code (Do Not Skipp Them)
        # Gives User Explicit Control Over Program Flow
        if len(tempCommand) == 2:
            tempUserCounter: str = tempCommand[1]
        else:
            flags["argument_error"] = 1
            flags["no_errors"] = False
            return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position
        try:
            tempCounter = int(tempUserCounter)
            if 1 <= tempCounter < codeSpan:
                execCounter = tempCounter - 2
            else:
                flags["out_of_bounds"] = 1
                flags["no_errors"] = False
        except ValueError:
            flags["not_integer"] = 1
            flags["no_errors"] = False

    elif tempCommand[0] == "stop" and IF_FLAG == 1:
        # End Program
        flags["no_errors"] = False

    else:
        # If Code Could Be Run Then Failed
        if IF_FLAG == 1:
            flags["bad_command"] = 1
            flags["no_errors"] = False

    return vars, flags, execCounter, tempIndex, tempValue, IF_FLAG, output_position