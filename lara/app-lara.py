# SnackCoin Streamlit WebApp


# Imports
import os
from ast import Num


import json
from pathlib import Path
from dotenv import load_dotenv
import datetime

import sqlite3
# import pandas as pd

from web3 import Web3

import streamlit as st


# Load .env
load_dotenv()

# Create Web3 instance with Ganache URI
# w3 = Web3(Web3.HTTPProvider(os.getenv("WEB_PROVIDER_URI")))

# Get the acccounts from Ganache
# accounts = w3.eth.accounts


# Load the contract
@st.cache(allow_output_mutation=True)
def load_contract():

    with open(Path("abi.json")) as abi_:
        abi = json.load(abi_)

    contract_address = os.getenv("SMART_CONTRACT_DEPLOYED_ADDRESS")

    contract = w3.eth.contract(
        address=contract_address,
        abi=abi
    )

    return contract


# contract = load_contract()


# Load menu database
st.markdown("# Snack Menu")
st.markdown("## ...")
st.text("\n")
st.text("\n")

con = sqlite3.connect('snack.db', timeout=10)
cur = con.cursor()


menu_items = dict()

# Display the menu with streamlit
def display_menu():

    # Get all the rows in Food table
    #   that are in Menu1
    res = cur.execute(
        '''
        SELECT * FROM Food
        WHERE id IN (
            SELECT food_id from MenuItems
            WHERE menu_id = 1
        );
        '''
    ).fetchall()

    for row in res:
        id_, name_, about_, category_, image_, unit_price_ = row

        menu_items[name_] = [id_, about_, category_, image_, unit_price_]

        st.image(image_, width=200)
        st.markdown(f'### {name_}')
        st.markdown(f'{about_}')
        st.markdown(f'{unit_price_} ETH')


display_menu()


st.markdown("## Order Food")
st.text("\n")
st.text("\n")

cart = dict()

if st.button("Start an order"):
    
    query = "INSERT INTO Orders (customer_id, order_total, time) VALUES (1, 0.000, datetime('now'))"
    cur.execute(query)
    con.commit()
    
    st.write("Order started. Add items to cart below..")


def place_order(num):
    
    key1 = num
    key2 = num + 3
    
    order_item = st.selectbox("Select an item", menu_items, key=key1)
    item_quantity = st.number_input("Enter quantity:", min_value=1, key=key2)
    
    if st.button(f"Add item #{num} Cart"):
        
        query = "SELECT id FROM Orders ORDER BY id DESC LIMIT 1 OFFSET 0"
        res = cur.execute(query)
        
        
        for row in res:
            order_id = int(str(row).strip('(,)'))
            
        st.write(order_id)

        item_total = menu_items[order_item][4] * item_quantity
        
        cart[order_item] = [order_item, item_quantity]
        
        query = '''
                INSERT INTO OrderItems (order_id, food_id, menu_id, quantity, item_total)
                VALUES
                        (:order_id_, :food_id_, 1, :item_quantity_, :item_total_)
                '''
        params = {
            "order_id_": order_id,
            "food_id_": menu_items[order_item][0],
            "item_quantity_": item_quantity,
            "item_total_": item_total
        }
        
        cur.execute(query, params)
        
        for x in cart.keys():
            
            query = f"SELECT order_total FROM Orders WHERE id = {order_id}"
            cur.execute(query)
            order_total = float(str(row).strip('(,)'))            
            
            
            
            price = menu_items[cart[x][0]][4]
            cart_total = order_total + cart[x][1] * price
            st.write(cart_total)
            query = f"UPDATE Orders SET order_total = {cart_total} WHERE id = {order_id}"
            cur.execute(query)
            con.commit()


place_order(1)
place_order(2)
place_order(3)

# query = "SELECT order_total FROM Orders WHERE id = :order_id_"
# params = {'order_total_': cart_total, 'order_id_':order_id}
# res = cur.execute(query, params)

# for row in res:
#     order_total = float(str(row).strip('(,)'))

# st.markdown(f'## Cart Total: {order_total}')

con.close()