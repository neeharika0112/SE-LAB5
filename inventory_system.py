import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.WARNING, format="%(levelname)s:%(message)s")

# Global variable
stock_data = {}


def addItem(item="default", qty=0, logs=None):
    if logs is None:
        logs = []

    # Validate item type
    if not isinstance(item, str):
        logging.warning("Item name must be a string. Invalid item: %s", item)
        return

    # Validate quantity type
    if not isinstance(qty, (int, float)):
        logging.warning("Quantity must be a number. Invalid qty: %s", qty)
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def removeItem(item, qty):
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        logging.warning("Tried to remove item that doesn't exist: %s", item)
    except TypeError:
        logging.warning("Invalid type passed to removeItem: item=%s qty=%s", item, qty)


def getQty(item):
    return stock_data.get(item, "Item not found")


def loadData(file="inventory.json"):
    try:
        with open(file, "r") as f:
            global stock_data
            stock_data = json.load(f)
    except FileNotFoundError:
        logging.warning("File not found: %s", file)


def saveData(file="inventory.json"):
    with open(file, "w") as f:
        json.dump(stock_data, f)


def printData():
    print("Items Report")
    for i, qty in stock_data.items():
        print(i, "->", qty)


def checkLowItems(threshold=5):
    return [i for i in stock_data if stock_data[i] < threshold]


def main():
    addItem("apple", 10)
    addItem("banana", -2)
    addItem(123, "ten")  # invalid input (logged)
    removeItem("apple", 3)
    removeItem("orange", 1)
    print("Apple stock:", getQty("apple"))
    print("Low items:", checkLowItems())
    saveData()
    loadData()
    printData()
    print("eval used")


if __name__ == "__main__":
    main()
