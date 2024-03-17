from flask import Flask, render_template, request, redirect, url_for, session
import os

authentication_data = {
    "admin@example.com": {
        "id": 1,
        "email": "admin@example.com",
        "username": "admin",
        "password": "password"
    },
    "user@example.com": {
        "id": 2,
        "email": "dieter@example.com",
        "username": "dieter",
        "password": "password"
    }
}

user_data = {
    1: {
        "user_id": 1,
        "first_name": "Administrator",
        "family_name": "",
        "data": "This is admin's data."
    },
    2: {
        "user_id": 2,
        "first_name": "Dieter",
        "family_name": "Verbruggen",
        "data": "This is user's data."
    }
}

def is_email(email_or_username):
    # A simple check to see if the input looks like an email
    return "@" in email_or_username

def handle_login(user, password):
    # Check if the input is an email or a username
    if "@" in user:
        # Handle email login
        if user in authentication_data and password == authentication_data[user]["password"]:
            # Correct email and password, store user in session
            session['user'] = user
            return None
        else:
            # Incorrect email or password, return error message
            return "Invalid email or password."
    else:
        # Handle username login
        for email, data in authentication_data.items():
            if data["username"] == user and password == data["password"]:
                # Correct username and password, store user in session
                session['user'] = email
                return None

        # Incorrect username or password, return error message
        return "Invalid username or password."