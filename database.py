import sqlite3


def createDatabase(cursor) -> None:
    cursor.execute(
        """CREATE TABLE RECIPES (
                recipeName VARCHAR(50) NOT NULL,
                servings INT check(servings >= 0),
                cookTime INT check(cookTime >= 0),
                PRIMARY KEY (recipeName));"""
    )
    cursor.execute(
        """CREATE TABLE INGREDIENTS (
                ingredientName VARCHAR(50) NOT NULL,
                stored INT check(stored >= 0),
                PRIMARY KEY (ingredientName));"""
    )
    cursor.execute(
        """CREATE TABLE TOOLS (
                toolName VARCHAR(50) NOT NULL,
                clean INT check(clean >= 0),
                PRIMARY KEY (toolName));"""
    )
    cursor.execute(
        """CREATE TABLE USES (
                recName VARCHAR(50) NOT NULL,
                toolName VARCHAR(50) NOT NULL,
                amount INT check(amount >= 0),
                PRIMARY KEY (recName, toolName),
                FOREIGN KEY (recName) REFERENCES RECIPES(recipeName),
                FOREIGN KEY (toolName) REFERENCES TOOLS(toolName));"""
    )
    cursor.execute(
        """CREATE TABLE CONSUMES (
                recName VARCHAR(50) NOT NULL,
                ingName VARCHAR(50) NOT NULL,
                amount INT check(amount >= 0),
                PRIMARY KEY (recName, ingName),
                FOREIGN KEY (recName) REFERENCES RECIPES(recipeName),
                FOREIGN KEY (ingName) REFERENCES INGREDIENTS(ingredientName));"""
    )


def newRecipe(cursor, recipeName: str, servings: int = 0, cookTime: int = 0) -> None:
    try:
        cursor.execute(f"""INSERT INTO RECIPES VALUES ('{recipeName}', '{servings}', '{cookTime}')""")
        print(f"Recipe {recipeName} created.")
    except sqlite3.Error as error:
        print("Failed to create new recipe, ", error)


def newIngredient(cursor, ingredName: str, stored: int = 0) -> None:
    try:
        cursor.execute(f"""INSERT INTO INGREDIENTS VALUES ('{ingredName}', '{stored}')""")
        print(f"Ingredient {ingredName} created.")
    except sqlite3.Error as error:
        print("Failed to create new ingredient,", error)


def newTool(cursor, toolName: str, numAvail: int = 0) -> None:
    try:
        cursor.execute(f"""INSERT INTO TOOLS VALUES ('{toolName}', '{numAvail}')""")
        print(f"Tool {toolName} created.")
    except sqlite3.Error as error:
        print("Failed to create new tool,", error)


def removeRecipe(cursor, recipeName) -> None:
    if (input(f"Confirm you want to delete recipe '{recipeName}' (yes or no): ").lower() == "no"):
        return
    try:
        cursor.execute(f"""DELETE FROM RECIPES WHERE recipeName = '{recipeName}'""")
        print(f"Recipe {recipeName} deleted.")
    except sqlite3.Error as error:
        print("Failed to delete recipe,", error)


def removeIngredient(cursor, ingredientName) -> None:
    if (input(f"Confirm you want to delete ingredient '{ingredientName}' (yes or no): ").lower() == "no"):
        return
    try:
        cursor.execute(f"""DELETE FROM INGREDIENTS WHERE ingredientName = '{ingredientName}'""")
        print(f"Ingredient {ingredientName} deleted.")
    except sqlite3.Error as error:
        print("Failed to delete ingredient,", error)


def removeTool(cursor, toolName) -> None:
    if (input(f"Confirm you want to delete tool '{toolName}' (yes or no): ").lower() == "no"):
        return
    try:
        cursor.execute(f"""DELETE FROM TOOLS WHERE toolName = '{toolName}'""")
        print(f"Tool {toolName} deleted.")
    except sqlite3.Error as error:
        print("Failed to delete tool,", error)


def modifyRecipe(cursor, recipeName) -> None:
    while True:
        try:
            userIn = input("Input Modification: ").lower().split()
            if len(userIn) == 0:
                continue
            match userIn[0]:
                case "back":
                    break
                case "add":
                    if len(userIn) == 1:
                        print("Please provide something you wish to add.")
                        continue
                    match userIn[1]:
                        case "tool":
                            if len(userIn) < 4:
                                print("Please provide enough information: name and amount")
                                continue
                            cursor.execute(f"""INSERT INTO USES VALUES ('{recipeName}', '{userIn[2]}', '{userIn[3]}')""")
                        case "ingredient":
                            if len(userIn) < 4:
                                print("Please provide enough information: name and amount")
                                continue
                            cursor.execute(f"""INSERT INTO CONSUMES VALUES ('{recipeName}', '{userIn[2]}', '{userIn[3]}')""")
                        case _:
                            print("Please provide something you wish to add.")
                case "remove":
                    if len(userIn) == 1:
                        print("Please provide something you wish to remove.")
                        continue
                    match userIn[1]:
                        case "tool":
                            if len(userIn) < 3:
                                print("Please provide a name")
                                continue
                            cursor.execute(f"""DELETE FROM USES WHERE recName = '{recipeName}' AND toolName = '{userIn[2]}'""")
                        case "ingredient":
                            if len(userIn) < 3:
                                print("Please provide a name")
                                continue
                            cursor.execute(f"""DELETE FROM CONSUMES WHERE recName = '{recipeName}' AND ingName = '{userIn[2]}'""")
                        case _:
                            print("Please provide something you wish to remove.")
                case "change":
                    if len(userIn) == 1:
                        print("Please provide what you wish to change.")
                        continue
                    match userIn[1]:
                        case "tool":
                            if len(userIn) < 4:
                                print("Please provide enough information: name and amount")
                                continue
                            cursor.execute(f"""UPDATE USES SET amount = {userIn[3]} WHERE recName = '{recipeName}' AND toolName = '{userIn[2]}'""")
                        case "ingredient":
                            if len(userIn) < 4:
                                print("Please provide enough information: name and amount")
                                continue
                            cursor.execute(f"""UPDATE CONSUMES SET amount = {userIn[3]} WHERE recName = '{recipeName}' AND ingName = '{userIn[2]}'""")
                        case "servings":
                            if len(userIn) < 3:
                                print("Please provide a number of servings")
                                continue
                            cursor.execute(f"""UPDATE RECIPES SET servings = {userIn[2]} WHERE recipeName = '{recipeName}'""")
                        case "time":
                            if len(userIn) < 3:
                                print("Please provide a cooking time")
                                continue
                            cursor.execute(f"""UPDATE RECIPES SET cookTime = {userIn[2]} WHERE recipeName = '{recipeName}'""")
                        case _:
                            print("Please provide what you wish to change.")
                case _:
                    print("Please input a correct command.")
        except sqlite3.Error as error:
            print("Modification failed,", error)


def modifyIngredient(cursor, ingredientName) -> None:
    while True:
        try:
            userIn = input("Input Modification: ").lower().split()
            if len(userIn) == 0:
                continue
            match userIn[0]:
                case "back":
                    break
                case "add":
                    if len(userIn) == 1:
                        print("Please provide the amount you wish to add.")
                        continue
                    cursor.execute(f"""UPDATE INGREDIENTS SET stored = stored + {userIn[1]} WHERE ingredientName = '{ingredientName}'""")
                case "remove":
                    if len(userIn) == 1:
                        print("Please provide the amount you wish to remove.")
                        continue
                    cursor.execute(f"""UPDATE INGREDIENTS SET stored = stored - {userIn[1]} WHERE ingredientName = '{ingredientName}'""")
                case _:
                    print("Please input a correct command.")
        except sqlite3.Error as error:
            print("Modification failed,", error)


def modifyTool(cursor, toolName) -> None:
    while True:
        try:
            userIn = input("Input Modification: ").lower().split()
            if len(userIn) == 0:
                continue
            match userIn[0]:
                case "back":
                    break
                case "add":
                    if len(userIn) == 1:
                        print("Please provide the number you wish to add.")
                        continue
                    cursor.execute(f"""UPDATE TOOLS SET clean = clean + {userIn[1]} WHERE toolName = '{toolName}'""")
                case "remove":
                    if len(userIn) == 1:
                        print("Please provide the number you wish to remove.")
                        continue
                    cursor.execute(f"""UPDATE TOOLS SET clean = clean - {userIn[1]} WHERE toolName = '{toolName}'""")
                case _:
                    print("Please input a correct command.")
        except sqlite3.Error as error:
            print("Modification failed,", error)


def searchRecipe(cursor, recipeName) -> None:
    try:
        result = cursor.execute(f"""SELECT * FROM RECIPES WHERE recipeName = '{recipeName}'""").fetchone()
        uses = cursor.execute(f"""SELECT toolName, amount FROM USES WHERE recName = '{recipeName}'""").fetchall()
        consumes = cursor.execute(f"""SELECT ingName, amount FROM CONSUMES WHERE recName = '{recipeName}'""").fetchall()
        if result is None:
            print("Failed to find recipe in database")
            return
        print(f"Recipe Name: {result[0]}\nServings: {result[1]}\nTime to Cook: {result[2]} minutes\nCan be Made: {isMakable(cursor, recipeName)}")
        print("Tools: ", end="")
        for tool in uses:
            print(tool[0], tool[1], end=", ")
        print("\nIngredients: ", end="")
        for ing in consumes:
            print(ing[0], str(ing[1]) + "g", end=", ")
        print()
    except sqlite3.Error as error:
        print("Failed to find recipe,", error)


def searchIngredient(cursor, ingredientName) -> None:
    try:
        result = cursor.execute(f"""SELECT * FROM INGREDIENTS WHERE ingredientName = '{ingredientName}'""").fetchone()
        consumedIn = cursor.execute(f"""SELECT recName FROM CONSUMES WHERE ingName = '{ingredientName}'""").fetchall()
        if result is None:
            print("Failed to find ingredient in database")
            return
        print(f"Ingredient Name: {result[0]}\nStored: {result[1]} grams")
        print("Used In: ", end="")
        for rec in consumedIn:
            print(rec[0], end=", ")
        print()
    except sqlite3.Error as error:
        print("Failed to find ingredient,", error)


def searchTool(cursor, toolName) -> None:
    try:
        result = cursor.execute(f"""SELECT * FROM TOOLS WHERE toolName = '{toolName}'""").fetchone()
        usedIn = cursor.execute(f"""SELECT recName FROM USES WHERE toolName = '{toolName}'""").fetchall()
        if result is None:
            print("Failed to find tool in database")
            return
        print(f"Tool Name: {result[0]}\nNumber Clean: {result[1]}")
        print("Used In: ", end="")
        for rec in usedIn:
            print(rec[0], end=", ")
        print()
    except sqlite3.Error as error:
        print("Failed to find tool,", error)


def listRecipe(cursor) -> None:
    try:
        results = cursor.execute(f"""SELECT recipeName FROM RECIPES""").fetchall()
        if results is None:
            print("Failed to find any recipes in database")
        print(f"{len(results)} recipes found:")
        for name in results:
            print(name[0])
    except sqlite3.Error as error:
        print("Failed to find recipe,", error)


def listIngredient(cursor) -> None:
    try:
        results = cursor.execute(f"""SELECT ingredientName, stored FROM INGREDIENTS""").fetchall()
        if results is None:
            print("Failed to find any ingredients in database")
        print(f"{len(results)} ingredients found:")
        for ing in results:
            print(ing[0], ing[1], "grams")
    except sqlite3.Error as error:
        print("Failed to find ingredient,", error)


def listTool(cursor) -> None:
    try:
        results = cursor.execute(f"""SELECT toolName, clean FROM TOOLS""").fetchall()
        if results is None:
            print("Failed to find any tools in database")
        print(f"{len(results)} tools found:")
        for tool in results:
            print(tool[0], tool[1], "clean")
    except sqlite3.Error as error:
        print("Failed to find tool,", error)


def makeRecipe(cursor, recipeName: str) -> None:
    if not isMakable(cursor, recipeName):
        print("You don't have enough to make this recipe")
        return

    ingsNeeded = cursor.execute(f"""SELECT ingName, amount FROM CONSUMES WHERE recName = '{recipeName}'""").fetchall()
    toolsNeeded = cursor.execute(f"""SELECT toolName, amount FROM USES WHERE recName = '{recipeName}'""").fetchall()
    for i in range(len(ingsNeeded)):
        cursor.execute(f"""UPDATE INGREDIENTS SET stored = stored - {ingsNeeded[i][1]} WHERE ingredientName = '{ingsNeeded[i][0]}'""")
    for i in range(len(toolsNeeded)):
        cursor.execute(f"""UPDATE TOOLS SET clean = clean - {toolsNeeded[i][1]} WHERE toolName = '{toolsNeeded[i][0]}'""")
    print(f"{recipeName} has been made")


def isMakable(cursor, recipeName: str) -> bool:
    try:
        ingsNeeded = cursor.execute(f"""SELECT ingName, amount FROM CONSUMES WHERE recName = '{recipeName}'""").fetchall()
        ingsStored = [cursor.execute(f"""SELECT ingredientName, stored FROM INGREDIENTS WHERE ingredientName = '{ing[0]}'""").fetchone() for ing in ingsNeeded]
        toolsNeeded = cursor.execute(f"""SELECT toolName, amount FROM USES WHERE recName = '{recipeName}'""").fetchall()
        toolsStored = [cursor.execute(f"""SELECT toolName, clean FROM TOOLS WHERE toolName = '{tool[0]}'""").fetchone() for tool in toolsNeeded]
    except sqlite3.Error as error:
        print("Failed to find an ingredient or tool,", error)
        return False
    
    result = True
    for i in range(len(ingsNeeded)):
        if ingsStored[i] is None:
            print(f"You need {ingsNeeded[i][1]}g of {ingsNeeded[i][0]} and have none.")
            result = False
            continue
        if ingsNeeded[i][1] > ingsStored[i][1]:
            print(f"You need {ingsNeeded[i][1] - ingsStored[i][1]}g more of {ingsNeeded[i][0]}")
            result = False
    for i in range(len(toolsNeeded)):
        if toolsStored[i] is None:
            print(f"You need {toolsNeeded[i][1]} of {toolsNeeded[i][0]} and have none.")
            result = False
            continue
        if toolsNeeded[i][1] > toolsStored[i][1]:
            print(f"You need {toolsNeeded[i][1] - toolsStored[i][1]} more of {toolsNeeded[i][0]}") 
            result = False
    return result


def startDB():
    dbConnection = sqlite3.connect("data.db")
    cursor = dbConnection.cursor()
    return cursor, dbConnection


def stopDB(dbConnection):
    dbConnection.commit()
    dbConnection.close()


if __name__ == "__main__":
    pass
