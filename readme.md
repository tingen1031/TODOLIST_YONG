Supermarket System

## Project Description

The **Supermarket System** is a console-based Python application that simulates basic supermarket operations.
Users are able to **manage products**, **add items to a shopping cart**, and **perform checkout operations** through an interactive menu.

This system is developed using **basic Python programming concepts** and does not rely on any external database or libraries.

---

## Objectives

* To apply Python **lists** to store and manage data dynamically
* To practice **loops and conditional statements** for menu-driven programs
* To implement **input validation** to prevent invalid user input
* To simulate a real-world supermarket shopping and checkout process

---

## Features

### Product Management

* Add new products (name, price, stock)
* Edit existing product details
* Delete products
* View all available products

### Shopping Cart

* Add products to cart
* View cart items
* Update cart item quantity
* Remove items from cart

### Checkout

* Calculate total amount
* Validate payment amount
* Display receipt with change
* Clear cart after checkout

---

## Programming Concepts Used

* Python List
* Dictionary
* While Loop
* If / Else Conditional Statements
* Functions
* Input Validation

---

## Data Structure

### Product
{
  "id": 1,
  "name": "Bread",
  "price": 3.50,
  "stock": 20
}

### Cart Item
{
  "product_id": 1,
  "name": "Bread",
  "price": 3.50,
  "qty": 2
}

---

## How to Run the Program

1. Install Python 3
2. Open a terminal in the project folder
3. Run the program using the following command:

---

## How to Use

1. Start the program
2. Add products into the system
3. View product list
4. Add products to shopping cart
5. Modify or remove cart items if necessary
6. Proceed to checkout
7. Exit the system

---

## Input Validation

The system ensures that:

* Product price must be greater than 0
* Stock quantity cannot be negative
* Cart quantity cannot exceed available stock
* Payment amount must be sufficient

Invalid input will be handled gracefully without terminating the program.

---

## File Structure
Supermarket.py
README.md

---

## Conclusion

This Supermarket System demonstrates how a simple real-world application can be implemented using basic Python programming techniques.
It provides practical experience in handling user input, data storage using lists, and control flow logic.

---

## Author
Yong Ting En
Diploma in Digital Creative Content

Assignment 3

## Link
https://github.com/tingen1031/TODOLIST_YONG
