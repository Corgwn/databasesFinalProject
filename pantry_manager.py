import sqlite3

from database import *

def main():
    cursor, dbConnection = startDB()

    # Check if database is empty, creating the needed tables if it is.
    if (cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall() == []):
        createDatabase(cursor)

    while True:
        userIn = input("Input Command: ").lower().split()
        if len(userIn) == 0:
            continue
        match userIn[0]:
            case "new":
                if len(userIn) < 3:
                    print("Please provide what you wish to create.")
                    continue
                match userIn[1]:
                    case "recipe":
                        if len(userIn) < 5:
                            print("Please provide all the information: name, servings, cook time")
                            continue
                        newRecipe(cursor, userIn[2], int(userIn[3]), int(userIn[4]))
                    case "ingredient":
                        if len(userIn) < 4:
                            print("Please provide all the information: name, amount in storage (g)")
                            continue
                        newIngredient(cursor, userIn[2], int(userIn[3]))
                    case "tool":
                        if len(userIn) < 4:
                            print("Please provide all the information: name, number clean")
                            continue
                        newTool(cursor, userIn[2], int(userIn[3]))
                    case _:
                        print("Please provide what you wish to create.")
            case "remove":
                if len(userIn) < 3:
                    print("Please provide what you wish to remove.")
                    continue
                match userIn[1]:
                    case "recipe":
                        removeRecipe(cursor, userIn[2])
                    case "ingredient":
                        removeIngredient(cursor, userIn[2])
                    case "tool":
                        removeTool(cursor, userIn[2])
                    case _:
                        print("Please provide what you wish to remove.")
            case "modify":
                if len(userIn) < 3:
                    print("Please provide what you wish to modify.")
                    continue
                match userIn[1]:
                    case "recipe":
                        modifyRecipe(cursor, userIn[2])
                    case "ingredient":
                        modifyIngredient(cursor, userIn[2])
                    case "tool":
                        modifyTool(cursor, userIn[2])
                    case _:
                        print("Please provide what you wish to modify.")
            case "search":
                if len(userIn) == 1:
                    print("Please provide what you wish to search.")
                    continue
                match userIn[1]:
                    case "recipe":
                        searchRecipe(cursor, userIn[2])
                    case "ingredient":
                        searchIngredient(cursor, userIn[2])
                    case "tool":
                        searchTool(cursor, userIn[2])
                    case _:
                        print("Please provide what you wish to search.")
            case "list":
                if len(userIn) == 1:
                    print("Please provide what you wish to list.")
                    continue
                match userIn[1]:
                    case "recipe":
                        listRecipe(cursor)
                    case "ingredient":
                        listIngredient(cursor)
                    case "tool":
                        listTool(cursor)
                    case _:
                        print("Please provide what you wish to list.")
            case "make":
                if len(userIn) == 1:
                    print("Please provide what you wish to make.")
                    continue
                makeRecipe(cursor, userIn[1])
            case "exit":
                print("Closing the program...")
                break
            case _:
                print("Please input a correct command.")
        dbConnection.commit()
        print()

    stopDB(dbConnection)


if __name__ == "__main__":
    main()
