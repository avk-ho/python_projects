# https://www.programmingexpert.io/projects/async-point-of-sale-system

import asyncio
from inventory import Inventory
from order import Order

### FUNCTION PROVIDED WITH TEMPLATE
def display_catalogue(catalogue):
    burgers = catalogue["Burgers"]
    sides = catalogue["Sides"]
    drinks = catalogue["Drinks"]

    print("--------- Burgers -----------\n")
    for burger in burgers:
        item_id = burger["id"]
        name = burger["name"]
        price = burger["price"]
        print(f"{item_id}. {name} ${price}")

    print("\n---------- Sides ------------")
    for side in sides:
        sizes = sides[side]

        print(f"\n{side}")
        for size in sizes:
            item_id = size["id"]
            size_name = size["size"]
            price = size["price"]
            print(f"{item_id}. {size_name} ${price}")

    print("\n---------- Drinks ------------")
    for beverage in drinks:
        sizes = drinks[beverage]

        print(f"\n{beverage}")
        for size in sizes:
            item_id = size["id"]
            size_name = size["size"]
            price = size["price"]
            print(f"{item_id}. {size_name} ${price}")

    print("\n------------------------------\n")

###
async def main():
    print("Welcome to the ProgrammingExpert Burger Bar!")

    inventory = Inventory()
    total_num_of_items_task = asyncio.create_task(inventory.get_number_of_items())

    print("Loading catalogue...")
    catalogue = await inventory.get_catalogue()
    display_catalogue(catalogue)

    total_num_of_items = await total_num_of_items_task

    generate_new_order = True
    while generate_new_order:
        order = Order(inventory)

        order_ids = order.get_user_order(total_num_of_items)
        item_status = await order.place_orders(order_ids)
        order.fill_items(item_status)

        total_price = order.calculate_total_order_price()
        await order.conclude_order(total_price)

        while True:
            do_new_order = input(
                "Would you like to make another order (yes/no)? ")
            if do_new_order == "yes":
                generate_new_order = True
                break
            elif do_new_order == "no":
                print("Goodbye!")
                generate_new_order = False
                break
            else:
                print("Invalid input.")


if __name__ == "__main__":
    asyncio.run(main())