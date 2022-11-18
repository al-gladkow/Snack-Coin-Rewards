/* Inserts menu data into snack.db */

BEGIN;

insert into Menus (id)
values
        (1);

insert into Food (name, about, category, image, unitprice)
values
        ("Hotdog", "No ketchup", "Entree", "./Images/hotdog.png", 0.004),
        ("Pizza", "One slice", "Entree", "./Images/pizza.png", 0.006),
        ("Fries", "Salty!", "Side", "./Images/fries.png", 0.002),
        ("Milkshake", "Chocolate & Vanilla", "Drink", "./Images/shake.png", 0.005),
        ("Cake", "Chocolate ganache", "Desert", "./Images/truffle.png", 0.003);

insert into MenuItems (menu_id, food_id)
values
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (1, 6);

END;