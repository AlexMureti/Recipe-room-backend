#!/usr/bin/env python3
"""
Seed script to populate test data for Recipe Room application.
Run this after deploying to create initial test data.
"""

from app import create_app, db
from models import User, Recipe, RecipeGroup, Comment, Rating, Bookmark
from datetime import datetime, timedelta

def seed_database():
    """Create test data in the database."""
    app = create_app()
    
    with app.app_context():
        # Clear existing data for clean seed
        print("🌱 Clearing existing database...")
        db.drop_all()
        db.create_all()
        print("✅ Database cleared and recreated")
        
        print("🌱 Seeding database with test data...")
        
        # Create test users
        users = []
        user_data = [
            {'username': 'john_chef', 'email': 'john@example.com', 'password': 'password123'},
            {'username': 'sarah_cook', 'email': 'sarah@example.com', 'password': 'password123'},
            {'username': 'mike_baker', 'email': 'mike@example.com', 'password': 'password123'},
            {'username': 'emma_foodie', 'email': 'emma@example.com', 'password': 'password123'},
        ]
        
        for data in user_data:
            user = User(username=data['username'], email=data['email'])
            user.set_password(data['password'])
            users.append(user)
            db.session.add(user)
        
        db.session.commit()
        print(f"✅ Created {len(users)} test users")
        
        # Create test recipes
        recipes = []
        recipe_data = [
            {
                'recipe_title': 'Simple Spaghetti Carbonara',
                'recipe_description': 'Classic Italian pasta with bacon and eggs',
                'recipe_country': 'Italy',
                'recipe_ingredients': [
                    {'name': 'Spaghetti', 'quantity': '400g'},
                    {'name': 'Bacon', 'quantity': '200g'},
                    {'name': 'Eggs', 'quantity': '4'},
                    {'name': 'Parmesan', 'quantity': '100g'}
                ],
                'recipe_procedure': [
                    {'step': 1, 'instruction': 'Cook spaghetti in boiling water'},
                    {'step': 2, 'instruction': 'Fry bacon until crispy'},
                    {'step': 3, 'instruction': 'Beat eggs with parmesan'},
                    {'step': 4, 'instruction': 'Mix pasta with bacon'},
                    {'step': 5, 'instruction': 'Add egg mixture off heat'}
                ],
                'recipe_people_served': 4,
                'recipe_prep_time': 10,
                'recipe_cook_time': 20,
                'recipe_image_url': 'https://images.unsplash.com/photo-1612874742237-6526221fcffb?w=500',
                'owner': users[0]
            },
            {
                'recipe_title': 'Vegetable Stir Fry',
                'recipe_description': 'Quick and healthy Asian-style stir fry',
                'recipe_country': 'China',
                'recipe_ingredients': [
                    {'name': 'Mixed Vegetables', 'quantity': '500g'},
                    {'name': 'Soy Sauce', 'quantity': '3 tbsp'},
                    {'name': 'Garlic', 'quantity': '3 cloves'},
                    {'name': 'Oil', 'quantity': '2 tbsp'}
                ],
                'recipe_procedure': [
                    {'step': 1, 'instruction': 'Heat oil in wok'},
                    {'step': 2, 'instruction': 'Add garlic'},
                    {'step': 3, 'instruction': 'Add vegetables'},
                    {'step': 4, 'instruction': 'Stir fry for 5-7 minutes'},
                    {'step': 5, 'instruction': 'Add soy sauce and serve'}
                ],
                'recipe_people_served': 3,
                'recipe_prep_time': 15,
                'recipe_cook_time': 10,
                'recipe_image_url': 'https://images.unsplash.com/photo-1603043097490-3d9c0e081198?w=500',
                'owner': users[1]
            },
            {
                'recipe_title': 'Chocolate Chip Cookies',
                'recipe_description': 'Classic homemade cookies with chocolate',
                'recipe_country': 'USA',
                'recipe_ingredients': [
                    {'name': 'Flour', 'quantity': '2 cups'},
                    {'name': 'Butter', 'quantity': '200g'},
                    {'name': 'Sugar', 'quantity': '150g'},
                    {'name': 'Chocolate Chips', 'quantity': '200g'}
                ],
                'recipe_procedure': [
                    {'step': 1, 'instruction': 'Cream butter and sugar'},
                    {'step': 2, 'instruction': 'Mix in flour'},
                    {'step': 3, 'instruction': 'Add chocolate chips'},
                    {'step': 4, 'instruction': 'Spoon onto baking tray'},
                    {'step': 5, 'instruction': 'Bake at 350°F for 12 minutes'}
                ],
                'recipe_people_served': 8,
                'recipe_prep_time': 15,
                'recipe_cook_time': 12,
                'recipe_image_url': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=500',
                'owner': users[2]
            },
            {
                'recipe_title': 'Tom Yum Soup',
                'recipe_description': 'Spicy Thai soup with shrimp',
                'recipe_country': 'Thailand',
                'recipe_ingredients': [
                    {'name': 'Shrimp', 'quantity': '300g'},
                    {'name': 'Lemongrass', 'quantity': '2 stalks'},
                    {'name': 'Ginger', 'quantity': '1 piece'},
                    {'name': 'Chili', 'quantity': '2-3'},
                    {'name': 'Stock', 'quantity': '1L'}
                ],
                'recipe_procedure': [
                    {'step': 1, 'instruction': 'Heat stock'},
                    {'step': 2, 'instruction': 'Add lemongrass, ginger, chili'},
                    {'step': 3, 'instruction': 'Simmer for 5 minutes'},
                    {'step': 4, 'instruction': 'Add shrimp'},
                    {'step': 5, 'instruction': 'Cook until shrimp is pink'}
                ],
                'recipe_people_served': 4,
                'recipe_prep_time': 20,
                'recipe_cook_time': 20,
                'recipe_image_url': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500',
                'owner': users[3]
            },
            {
                'recipe_title': 'Simple Tomato Pasta',
                'recipe_description': 'Classic Italian pasta with fresh tomatoes',
                'recipe_country': 'Italy',
                'recipe_ingredients': [
                    {'name': 'Pasta', 'quantity': '500g'},
                    {'name': 'Tomatoes', 'quantity': '4 large'},
                    {'name': 'Garlic', 'quantity': '2 cloves'},
                    {'name': 'Olive Oil', 'quantity': '4 tbsp'},
                    {'name': 'Basil', 'quantity': 'handful'}
                ],
                'recipe_procedure': [
                    {'step': 1, 'instruction': 'Cook pasta'},
                    {'step': 2, 'instruction': 'Sauté garlic in olive oil'},
                    {'step': 3, 'instruction': 'Add chopped tomatoes'},
                    {'step': 4, 'instruction': 'Simmer for 15 minutes'},
                    {'step': 5, 'instruction': 'Mix with pasta, add basil'}
                ],
                'recipe_people_served': 4,
                'recipe_prep_time': 10,
                'recipe_cook_time': 20,
                'recipe_image_url': 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=500',
                'owner': users[0]
            }
        ]
        
        for data in recipe_data:
            owner = data.pop('owner')
            recipe = Recipe(recipe_owner_id=owner.id, **data)
            recipes.append(recipe)
            db.session.add(recipe)
        
        db.session.commit()
        print(f"✅ Created {len(recipes)} test recipes")
        
        # Create test groups
        groups = []
        group_data = [
            {
                'group_name': 'Weekend Cooking Club',
                'group_description': 'A group for sharing weekend recipes and tips',
                'group_image_url': 'https://images.unsplash.com/photo-1556910103-1c02745aefb4?w=500',
                'owner': users[0],
                'members': [users[0], users[1], users[2]]
            },
            {
                'group_name': 'Healthy Eaters',
                'group_description': 'Share healthy and nutritious recipes',
                'group_image_url': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500',
                'owner': users[1],
                'members': [users[1], users[2], users[3]]
            },
            {
                'group_name': 'International Cuisine',
                'group_description': 'Explore recipes from around the world',
                'group_image_url': 'https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=500',
                'owner': users[3],
                'members': [users[0], users[2], users[3]]
            }
        ]
        
        for data in group_data:
            members = data.pop('members')
            owner = data.pop('owner')
            group = RecipeGroup(group_owner_id=owner.id, **data)
            
            # Add members to group
            for member in members:
                group.group_members.append(member)
            
            groups.append(group)
            db.session.add(group)
        
        db.session.commit()
        print(f"✅ Created {len(groups)} test groups")
        
        # Now add recipes to groups (after groups are created)
        for i, group in enumerate(groups):
            for j, recipe in enumerate(recipes[:2]):  # Add first 2 recipes
                # Add recipe directly to the association table with proper fields
                from models import recipe_group_members
                stmt = recipe_group_members.insert().values(
                    rgm_recipe_id=recipe.recipe_id,
                    rgm_group_id=group.group_id,
                    rgm_added_by=group.group_owner_id
                )
                db.session.execute(stmt)
        
        db.session.commit()
        
        # Create test ratings
        for i, recipe in enumerate(recipes):
            rating = Rating(
                recipe_id=recipe.recipe_id,
                user_id=users[i % len(users)].id,
                rating_value=(i % 5) + 1  # Ratings 1-5
            )
            db.session.add(rating)
        
        db.session.commit()
        print(f"✅ Created {len(recipes)} test ratings")
        
        # Create test bookmarks
        for i, recipe in enumerate(recipes):
            user_idx = (i + 1) % len(users)
            bookmark = Bookmark(
                recipe_id=recipe.recipe_id,
                user_id=users[user_idx].id
            )
            db.session.add(bookmark)
        
        db.session.commit()
        print(f"✅ Created {len(recipes)} test bookmarks")
        
        # Create test comments
        for i, recipe in enumerate(recipes):
            comment = Comment(
                recipe_id=recipe.recipe_id,
                user_id=users[i % len(users)].id,
                comment_text=f"This is a great recipe! Really enjoyed making it."
            )
            db.session.add(comment)
        
        db.session.commit()
        print(f"✅ Created test comments")
        
        print("\n🎉 Database seeding complete!")
        print(f"\nTest Users (use these to login):")
        for user in user_data:
            print(f"  Email: {user['email']}, Password: {user['password']}")
        print(f"\nTotal Data Created:")
        print(f"  - Users: {len(users)}")
        print(f"  - Recipes: {len(recipes)}")
        print(f"  - Groups: {len(groups)}")
        print(f"  - Ratings: {len(recipes)}")
        print(f"  - Bookmarks: {len(recipes)}")

if __name__ == '__main__':
    seed_database()
