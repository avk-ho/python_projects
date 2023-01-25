import asyncio

TAX_RATE = 0.05
COMBO_DISCOUNT = 15 # in %

class Order:
    def __init__(self, inventory):
        self.inventory = inventory
        self.items = {
            "Burgers": {"quantity": 0},
            "Sides": {"quantity": 0},
            "Drinks": {"quantity": 0},
        }
        self.subtotal = 0

    """
    self.items structure
    self.items = {
      "Burgers": {
            "quantity": int,
            id: {
              "info": inventory.get_item(id),
              "order_quantity": int,
              "to_process_quantity": int,
          },
      }
    }
    """

    
    def get_user_order(self, total_num_of_items):
        print("Please enter the number of items that you would like to add to your order. Enter q to complete your order.")
        
        order_ids = []
        end_order = False
        while not end_order:
            item_id_order = input("Enter an item number: ")

            if item_id_order == "q":
                end_order = True
                continue

            try:
                item_id_order = int(item_id_order)
            except:
                print("Please enter a valid number.")
                continue

            valid_id = 0 < item_id_order < total_num_of_items + 1

            if not valid_id:
                print(f"Please enter a number above 0 and below {total_num_of_items + 1}.")
                continue

            order_ids.append(item_id_order)
        
        return order_ids


    async def place_orders(self, order_ids):
        print("Placing order...")

        get_stock_tasks = []
        item_infos_tasks = []

        for id in order_ids:
            stock = asyncio.create_task(self.inventory.get_stock(id))
            info = asyncio.create_task(self.inventory.get_item(id))
            get_stock_tasks.append(stock)
            item_infos_tasks.append(info)

        items_status = []
        for i in range(len(item_infos_tasks)):
            item = await asyncio.gather(get_stock_tasks[i], item_infos_tasks[i])
            items_status.append(item)

        return items_status

    
    def fill_items(self, items_status):
        stock = {}

        for item in items_status:
            item_stock = item[0]
            id = item[1]["id"]

            if id not in stock:
                stock[id] = item_stock

            # item out of stock
            if stock[id] < 1:
                print(
                    f"Unfortunately item number {id} is out of stock and has been removed from your order. Sorry!")

            # item in stock
            else:
                category = item[1]["category"]
                stock[id] -= 1

                if category == "Burgers":
                    burgers = self.items["Burgers"]
                    burgers["quantity"] += 1
                    burgers[id] = burgers.get(id, {})
                    burgers[id]["info"] = item[1]
                    burgers[id]["order_quantity"] = burgers[id].get("order_quantity", 0) + 1
                    burgers[id]["to_process_quantity"] = burgers[id]["order_quantity"]
                elif category == "Sides":
                    sides = self.items["Sides"]
                    sides["quantity"] += 1
                    sides[id] = sides.get(id, {})
                    sides[id]["info"] = item[1]
                    sides[id]["order_quantity"] = sides[id].get("order_quantity", 0) + 1
                    sides[id]["to_process_quantity"] = sides[id]["order_quantity"]
                elif category == "Drinks":
                    drinks = self.items["Drinks"]
                    drinks["quantity"] += 1
                    drinks[id] = drinks.get(id, {})
                    drinks[id]["info"] = item[1]
                    drinks[id]["order_quantity"] = drinks[id].get("order_quantity", 0) + 1
                    drinks[id]["to_process_quantity"] = drinks[id]["order_quantity"]


    def calculate_total_order_price(self):
        self.calculate_subtotal()

        tax = round(self.subtotal * TAX_RATE, 2)
        total_price = round(self.subtotal + tax, 2)

        print(f"\nSubtotal: ${self.subtotal}")
        print(f"Tax: ${tax}")
        print(f"Total: ${total_price}")

        return total_price


    async def conclude_order(self, total_price):
        if total_price == 0:
            print("The order is empty and has been cancelled.")
            return

        while True:
            confirm_order = input(f"Would you like to purchase this order for ${total_price} (yes/no)? ")
            if confirm_order == "yes":
                print("Thank you for your order!")
                await self.decrement_all_items()
                break
            elif confirm_order == "no":
                print("No problem, please come again!")
                break
            else:
                print("Invalid input.")

    
    def calculate_subtotal(self):
        burgers = self.items["Burgers"]
        sides = self.items["Sides"]
        drinks = self.items["Drinks"]
        num_of_combos = min(
            burgers["quantity"],
            sides["quantity"],
            drinks["quantity"]
        )

        print("Here is a summary of your order: \n")

        while num_of_combos > 0:
            self.add_combo_price_to_subtotal()
            num_of_combos -= 1

        self.add_items_price_to_subtotal()


    def add_combo_price_to_subtotal(self):
        combo_ids = []
        
        for category_dict in self.items.values():
            combo_ids.append(self.find_most_expensive(category_dict))

        for category in self.items.values():
            for id, item in category.items():
                if id == "quantity":
                    continue
                
                if id in combo_ids:
                    item["to_process_quantity"] -= 1
                    
                    if item["info"]["category"] == "Burgers":
                        burger = item["info"]

                    elif item["info"]["category"] == "Sides":
                        side = item["info"]

                    elif item["info"]["category"] == "Drinks":
                        drink = item["info"]
        
        discount = 1 - (COMBO_DISCOUNT / 100)
        combo_price = round((burger["price"] + side["price"] + drink["price"]) * discount, 2)
        self.subtotal += combo_price

        side_name = side["size"] + " " + side["subcategory"]
        drink_name = drink["size"] + " " + drink["subcategory"]

        print(f"${combo_price} Burger Combo")
        print(f"  {burger['name']}")
        print(f"  {side_name}")
        print(f"  {drink_name}")


    def find_most_expensive(self, item_dict):
        most_expensive_item_id = 0
        most_expensive_item_price = 0

        for id in item_dict:
            if id == "quantity":
                continue

            quantity = item_dict[id]["to_process_quantity"]
            if quantity < 1:
                continue

            price = item_dict[id]["info"]["price"]
            if most_expensive_item_id == 0:
                most_expensive_item_id = id
                most_expensive_item_price = price

            if most_expensive_item_price < price:
                most_expensive_item_id = id
                most_expensive_item_price = price

        return most_expensive_item_id

    
    def add_items_price_to_subtotal(self):
        price = 0

        for category in self.items.values():
            for id, item in category.items():
                if id == "quantity":
                    continue

                quantity = item["to_process_quantity"]
                if quantity <= 0:
                    continue

                price += (item["info"]["price"] * quantity)
                item["to_process_quantity"] = 0

                if item["info"]["category"] == "Burgers":
                    print(f'${item["info"]["price"]} {item["info"]["name"]} * {quantity}')
                else:
                    item_name = item["info"]["size"] + " " + item["info"]["subcategory"]
                    print(f'${item["info"]["price"]} {item_name} * {quantity}')
                    
        self.subtotal += round(price, 2)


    async def decrement_all_items(self):
        tasks = []

        for category in self.items.values():
            for id, item in category.items():
                if id == "quantity":
                    continue

                quantity = item["order_quantity"]
                for _ in range(quantity):
                    task = asyncio.create_task(self.inventory.decrement_stock(id))
                    tasks.append(task)

        await asyncio.gather(*tasks)
