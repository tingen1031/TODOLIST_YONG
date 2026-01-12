# ===== Color Codes (ANSI) =====
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"


# ===== Helpers =====
def money(n: float) -> str:
    return f"RM {n:.2f}"


def ask_int(prompt, min_val=None, max_val=None):
    s = input(prompt).strip()
    if not s.isdigit():
        return None
    v = int(s)
    if min_val is not None and v < min_val:
        return None
    if max_val is not None and v > max_val:
        return None
    return v


def ask_float(prompt, min_val=None):
    s = input(prompt).strip()
    try:
        v = float(s)
    except ValueError:
        return None
    if min_val is not None and v < min_val:
        return None
    return v


# ===== Product Setup (User fills the list) =====
def setup_products():
    products = []
    print(BLUE + "\n=== Supermarket Product Setup ===" + RESET)
    print("Enter product details. Press Enter on product name to finish.\n")

    while True:
        name = input("Enter product name (Enter to finish): ").strip()
        if name == "":
            break

        price = ask_float("Enter product price (> 0): ", min_val=0.01)
        if price is None:
            print(RED + "Invalid price. Please try again.\n" + RESET)
            continue

        stock = ask_int("Enter product stock (>= 0): ", min_val=0)
        if stock is None:
            print(RED + "Invalid stock. Please try again.\n" + RESET)
            continue

        product_id = len(products) + 1
        products.append({
            "id": product_id,
            "name": name,
            "price": float(price),
            "stock": int(stock)
        })

        print(GREEN + "Product added.\n" + RESET)

    if not products:
        print(YELLOW + "No products were added. A default sample set will be used.\n" + RESET)
        products = [
            {"id": 1, "name": "Bread", "price": 3.50, "stock": 20},
            {"id": 2, "name": "Milk", "price": 6.20, "stock": 15},
            {"id": 3, "name": "Eggs", "price": 9.90, "stock": 10},
        ]

    return products


# ===== Display =====
def show_products(products):
    print(BLUE + "\n===== PRODUCT LIST =====" + RESET)
    if not products:
        print(RED + "No products available." + RESET)
        return

    print(YELLOW + "No.  Product                 Price       Stock" + RESET)
    print("-" * 50)

    for i, p in enumerate(products, start=1):
        stock_color = GREEN if p["stock"] > 0 else RED
        name = p["name"][:20]
        print(f"{i:<4} {name:<22} {money(p['price']):<10} {stock_color}{p['stock']}{RESET}")


def show_cart(cart):
    print(PURPLE + "\n===== YOUR CART =====" + RESET)
    if not cart:
        print(RED + "Cart is empty." + RESET)
        return 0.0

    print(YELLOW + "No.  Product                 Price       Qty   Subtotal" + RESET)
    print("-" * 60)

    total = 0.0
    for i, c in enumerate(cart, start=1):
        subtotal = c["price"] * c["qty"]
        total += subtotal
        name = c["name"][:20]
        print(
            f"{i:<4} {name:<22} {money(c['price']):<10} "
            f"{CYAN}{c['qty']:<5}{RESET} {GREEN}{money(subtotal)}{RESET}"
        )

    print("-" * 60)
    print(GREEN + f"TOTAL: {money(total)}" + RESET)
    return total


# ===== Cart Logic =====
def find_cart_item(cart, product_id):
    for item in cart:
        if item["product_id"] == product_id:
            return item
    return None


def add_to_cart(products, cart):
    if not products:
        print(RED + "No products to add." + RESET)
        return

    show_products(products)
    idx = ask_int("Enter product number to add: ", 1, len(products))
    if idx is None:
        print(RED + "Invalid product number." + RESET)
        return

    p = products[idx - 1]
    if p["stock"] <= 0:
        print(RED + "Out of stock." + RESET)
        return

    qty = ask_int(f"Enter quantity (1-{p['stock']}): ", 1, p["stock"])
    if qty is None:
        print(RED + "Invalid quantity." + RESET)
        return

    # deduct stock
    p["stock"] -= qty

    # update cart
    existing = find_cart_item(cart, p["id"])
    if existing:
        existing["qty"] += qty
    else:
        cart.append({
            "product_id": p["id"],
            "name": p["name"],
            "price": p["price"],
            "qty": qty
        })

    print(GREEN + "Added to cart." + RESET)


def update_cart_qty(products, cart):
    if not cart:
        print(RED + "Cart is empty." + RESET)
        return

    show_cart(cart)
    idx = ask_int("Enter cart item number to update: ", 1, len(cart))
    if idx is None:
        print(RED + "Invalid cart item number." + RESET)
        return

    item = cart[idx - 1]

    # find matching product for stock adjustments
    product = None
    for p in products:
        if p["id"] == item["product_id"]:
            product = p
            break

    if product is None:
        print(RED + "Product not found (data error)." + RESET)
        return

    current_qty = item["qty"]
    max_qty = current_qty + product["stock"]

    new_qty = ask_int(f"Enter new quantity (1-{max_qty}): ", 1, max_qty)
    if new_qty is None:
        print(RED + "Invalid quantity." + RESET)
        return

    diff = new_qty - current_qty
    if diff > 0:
        product["stock"] -= diff      # take more stock
    elif diff < 0:
        product["stock"] += (-diff)   # return stock

    item["qty"] = new_qty
    print(GREEN + "Cart quantity updated." + RESET)


def remove_from_cart(products, cart):
    if not cart:
        print(RED + "Cart is empty." + RESET)
        return

    show_cart(cart)
    idx = ask_int("Enter cart item number to remove: ", 1, len(cart))
    if idx is None:
        print(RED + "Invalid cart item number." + RESET)
        return

    item = cart.pop(idx - 1)

    # return stock to product
    for p in products:
        if p["id"] == item["product_id"]:
            p["stock"] += item["qty"]
            break

    print(GREEN + "Removed from cart." + RESET)


def checkout(cart):
    total = show_cart(cart)
    if not cart:
        return

    pay = ask_float(f"Enter payment amount (>= {total:.2f}): ", min_val=total)
    if pay is None:
        print(RED + "Invalid payment." + RESET)
        return

    change = pay - total

    print(BLUE + "\n===== RECEIPT =====" + RESET)
    for c in cart:
        line_total = c["price"] * c["qty"]
        print(f"{c['name']} x{c['qty']} = {money(line_total)}")

    print("-" * 30)
    print(YELLOW + f"TOTAL   : {money(total)}" + RESET)
    print(CYAN + f"PAYMENT : {money(pay)}" + RESET)
    print(GREEN + f"CHANGE  : {money(change)}" + RESET)
    print(GREEN + "Thank you. Please come again!" + RESET)

    cart.clear()


# ===== Main =====
def main():
    products = setup_products()  # user fills products list
    cart = []

    while True:
        print(CYAN + "\n========== SUPERMARKET ==========" + RESET)
        print(GREEN + "1. View Products" + RESET)
        print(GREEN + "2. Add to Cart" + RESET)
        print(GREEN + "3. View Cart" + RESET)
        print(GREEN + "4. Update Cart Quantity" + RESET)
        print(GREEN + "5. Remove from Cart" + RESET)
        print(YELLOW + "6. Checkout" + RESET)
        print(RED + "7. Exit" + RESET)

        choice = input("Choose (1-7): ").strip()

        if choice == "1":
            show_products(products)
        elif choice == "2":
            add_to_cart(products, cart)
        elif choice == "3":
            show_cart(cart)
        elif choice == "4":
            update_cart_qty(products, cart)
        elif choice == "5":
            remove_from_cart(products, cart)
        elif choice == "6":
            checkout(cart)
        elif choice == "7":
            print(YELLOW + "Exiting Supermarket... Bye!" + RESET)
            break
        else:
            print(RED + "Invalid choice. Please enter 1-7." + RESET)


if __name__ == "__main__":
    main()