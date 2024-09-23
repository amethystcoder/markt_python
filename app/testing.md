## AUTH

1. **Buyer Registration Endpoint (/auth/register/buyer)**:
    - **Endpoint:** `POST /auth/register/buyer`
    - **Request Body:**
        ```json
        {
            "email": "buyer@example.com",
            "phone_number": "1234567890",
            "username": "buyer_username",
            "password": "buyer_password",
            "profile_picture": "buyer_profile_picture_url",
            "shipping_address": "Buyer Street, Buyer City, Buyer State, Buyer Country, 12345",
            "address": {
                "longitude": 123.456,
                "latitude": 45.678,
                "house_number": 123,
                "street": "Buyer Street",
                "city": "Buyer City",
                "state": "Buyer State",
                "country": "Buyer Country",
                "postal_code": 12345
            }
        }
        ```

2. **Seller Registration Endpoint (/auth/register/seller)**:
    - **Endpoint:** `POST /auth/register/seller`
    - **Request Body:**
        ```json
        {
            "email": "seller@example.com",
            "phone_number": "9876543210",
            "username": "seller_username",
            "password": "seller_password",
            "profile_picture": "seller_profile_picture_url",
            "shop_name": "Seller Shop",
            "description": "Description of the seller's shop",
            "directions": "Directions to the shop",
            "category": "Shop Category",
            "address": {
                "longitude": 98.765,
                "latitude": 54.321,
                "house_number": 456,
                "street": "Seller Street",
                "city": "Seller City",
                "state": "Seller State",
                "country": "Seller Country",
                "postal_code": 54321
            }
        }
        ```

3. **Create Buyer Account Endpoint (/auth/create-buyer)**:
    - **Endpoint:** `POST /auth/create-buyer`
    - **Request Body:**
        ```json
        {
            "username": "existing_user",
            "password": "buyer_password",
            "profile_picture": "buyer_profile_picture_url",
            "shipping_address": "Buyer Updated Street, Buyer Updated City, Buyer Updated State, Buyer Updated Country, 54321"
        }
        ```

4. **Create Seller Account Endpoint (/auth/create-seller)**:
    - **Endpoint:** `POST /auth/create-seller`
    - **Request Body:**
        ```json
        {
            "username": "existing_user",
            "password": "seller_password",
            "profile_picture": "seller_profile_picture_url",
            "shop_name": "Updated Seller Shop",
            "description": "Updated description of the seller's shop",
            "directions": "Updated directions to the shop",
            "category": "Updated Shop Category"
        }
        ```

5. **Switch Role Endpoint (/auth/switch-role)**:
    - **Endpoint:** `POST /auth/switch-role`
    - **Request Body:**
        ```json
        {}
        ```

6. **User Login Endpoint (/auth/login)**:
    - **Endpoint:** `POST /auth/login`
    - **Request Body (Buyer Login):**
        ```json
        {
            "email": "buyer@example.com",
            "username": "buyer_username",
            "password": "buyer_password",
            "account_type": "buyer"
        }
        ```
    - **Request Body (Seller Login):**
        ```json
        {
            "email": "seller@example.com",
            "username": "seller_username",
            "password": "seller_password",
            "account_type": "seller"
        }
        ```

7. **User Logout Endpoint (/auth/logout)**:
    - **Endpoint:** `POST /auth/logout`
    - **Request Body:**
        ```json
        {}
        ```
      