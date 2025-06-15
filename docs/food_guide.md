# Station Food Guide

This document summarizes basic cooking mechanics and a sampling of recipes inspired by /tg/station13.  Food items prevent hunger and many require special machinery to prepare.  Meals restore the player's `nutrition` stat when eaten.

## Core Mechanics

- **Butchering** – Harvest meat by attacking corpses in combat mode or using a gibber.
- **Knife & Rolling Pin** – Slice bread or flatten dough for use in other recipes.
- **Processor** – Processes raw ingredients such as cutlets or vegetables.
- **Griddle** – Cooks raw meatballs, patties and other grillables.
- **Grinder** – Grinds food items into reagents for sauces or condiments.
- **Oven** – Bakes dough into bread, cakes and pies.
- **Microwave** – Boils or warms food like eggs or rice.
- **Stove** – Heats soups and sauces to the proper temperature.

Many recipes are started from the crafting menu once the required items are on the same tile.  In this codebase the **kitchen system** also loads structured recipes from `data/food_recipes.yaml` and allows chefs to cook using the `cook` command.

Example recipe data:

```yaml
- output: burger
  inputs: [bun, patty]
  nutrition: 25
```

When a chef runs `cook bun patty` and has those items in their inventory a new food item is created that provides 25 nutrition.

## Sample Recipes

### Burger
- **Ingredients:** bun, cooked patty
- **Method:** Combine using the crafting menu.

### Sausage
- **Ingredients:** raw meatball, raw cutlet
- **Method:** Craft a raw sausage then grill until cooked.

### Pancakes
- **Ingredients:** pancake batter
- **Method:** Splash batter on a griddle and cook until brown.

### Pizza Bread
- **Ingredients:** flat dough
- **Method:** Bake in an oven to create pizza bread which can be topped with additional ingredients.

### Boiled Egg
- **Ingredients:** egg
- **Method:** Microwave until cooked.

### Grilled Cheese
- **Ingredients:** bun, cheese wedge
- **Method:** Grill until the cheese melts.

### Fried Fish
- **Ingredients:** raw fish fillet
- **Method:** Fry in oil until crispy.

### Omelette
- **Ingredients:** egg, milk
- **Method:** Cook in a pan until fluffy.

These examples only scratch the surface—see the original TG food guide for a full listing of burgers, breads, cakes, soups, stews and more.

## Additional Items

The kitchen now supports more ingredients and dishes drawn from Space Station 13.
Notable additions include bread loaves, cakes, full pizzas, fries and cold treats
like ice cream.  Sandwiches, hot dogs, muffins, cookies and pies can also be
cooked when the proper ingredients are gathered.

