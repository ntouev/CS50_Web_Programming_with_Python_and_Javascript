# Project 3: Pinocchio

*This project is not complete yet. It is missing the part where shopping cart collects the data given by the user and shows them to the sceen. After that it should request via Ajax request the server for the price, to display it too. Then the user should be able to send the order, meaning a table of orders should be created in the server to be updated with each order every time.*

## Objectives

* Become more comfortable with Django.
* Gain experience with relational database design.

## Overview

In this project, you’ll build an web application for handling a pizza restaurant’s online orders. Users will be able to browse the restaurant’s menu, add items to their cart, and submit their orders. Meanwhile, the restaurant owners will be able to add and update menu items, and view orders that have been placed.

## Milestones

This is the recommended way to approach this project.

* Complete the Menu, Adding Items, and Registration/Login/Logout steps.
* Complete the Shopping Cart and Placing an Order steps.
* Complete the Viewing Orders and Personal Touch steps.

## Run

First, make sure you have python3, pip3 and virtualenv installed.

Then do:
* in /Project3/orders/static/orders/css/ run $ sass --watch style.scss:style.css
* Back in root directory run $ python3 -m venv venv
* $ . venv/bin/activate
* $ pip3 install django
* $ export PINOCCHIO_SECRET_KEY="your_key"
* $ python3 manage.py migrate
* Now initialize with some data your DB (examples in /pizza/initializedb.txt)
* $ python3 manage.py runserver

## Requirements

* Menu: Your web application should support all of the available menu items for Pinnochio’s Pizza & Subs (a popular pizza place in Cambridge). It’s up to you, based on analyzing the menu and the various types of possible ordered items (small vs. large, toppings, additions, etc.) to decide how to construct your models to best represent the information. Add your models to orders/models.py, make the necessary migration files, and apply those migrations.
* Adding Items: Using Django Admin, site administrators (restaurant owners) should be able to add, update, and remove items on the menu. Add all of the items from the Pinnochio’s menu into your database using either the Admin UI or by running Python commands in Django’s shell.
* Registration, Login, Logout: Site users (customers) should be able to register for your web application with a username, password, first name, last name, and email address. Customers should then be able to log in and log out of your website.
* Shopping Cart: Once logged in, users should see a representation of the restaurant’s menu, where they can add items (along with toppings or extras, if appropriate) to their virtual “shopping cart.” The contents of the shopping should be saved even if a user closes the window, or logs out and logs back in again.
* Placing an Order: Once there is at least one item in a user’s shopping cart, they should be able to place an order, whereby the user is asked to confirm the items in the shopping cart, and the total (no need to worry about tax!) before placing an order.
* Viewing Orders: Site administrators should have access to a page where they can view any orders that have already been placed.
* Personal Touch: Add at least one additional feature of your choosing to the web application. Possibilities include: allowing site administrators to mark orders as complete and allowing users to see the status of their pending or completed orders, integrating with the Stripe API to allow users to actually use a credit card to make a purchase during checkout, or supporting sending users a confirmation email once their purchase is complete. If you need to use any credentials (like passwords or API credentials) for your personal touch, be sure not to store any credentials in your source code, better to use environment variables!

## FAQs

What is a “Special” pizza?

It’s up to you to decide what a “special” pizza means, and to implement it accordingly. It could be one particular set of toppings, allowing up to 5 different types of toppings, or something else entirely!

## Hints

Unlike in Project 1, you shouldn’t need to build your application’s entire login and authentication system yourself. Feel free to use Django’s built-in users and authentication system to simplify the process of logging users in and out.
Before diving into writing your models, you’ll likely want to think carefully about the different types of menu items and how best to organize them. Some questions to consider include: how should you represent the different prices for large and small versions of the same dish? Where do toppings fit into your model for pizzas, and how do you calculate the ultimate price of a pizza? How will you make the custom add-ons for the subs work?
