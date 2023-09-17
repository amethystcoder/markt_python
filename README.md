# Markt E-Commerce Project

## Project Overview

The Markt E-Commerce Project is a revolutionary e-commerce application that bridges the gap between local sellers and buyers, providing a seamless and natural online shopping experience. Our mission is to enable local sellers to expand their reach, increase sales, and connect with buyers in innovative ways while allowing buyers to enjoy the market-like shopping experience from the comfort of their homes.

### Key Functionalities

1. **Proximity-Based Product Presentation:** Products are intelligently presented to buyers based on the proximity of the seller to the buyer's location and the availability of the product. This ensures that products are showcased to buyers from nearby sellers with reputable ratings and feedback, facilitating quick and efficient product delivery.

2. **Seller-Buyer Interactions:** We recreate the natural interactions that occur in a physical marketplace. Buyers can easily communicate with sellers, negotiate product prices, and switch between related sellers effortlessly.

3. **Advanced Product Search:** Our platform offers advanced product search capabilities, allowing buyers to easily find products they are looking for. Buyers can use the search bar to discover products, or they can inquire about products even when they don't know the exact product name.

4. **Chat Functionality:** Our chat feature enables real-time communication between buyers and sellers, enhancing the shopping experience and fostering trust and transparency.

## Project Structure

The project structure follows best practices for Flask-based applications, organized into logical components:

- **app:** Contains the main application logic and configuration files.
- **templates:** Stores HTML templates for rendering views.
- **static:** Holds static assets like CSS, JavaScript, and images.
- **tests:** Includes unit and integration tests for ensuring code quality.
- **migrations:** Manages database schema changes using SQLAlchemy-Migrate.
- **config:** Stores configuration files for different environments (development, production, testing).
- **venv:** Virtual environment for isolating project dependencies.

## Technologies Used

Our project utilizes industry-standard technologies and libraries to ensure a robust and scalable solution:

- **Flask:** A micro web framework for building web applications.
- **SQLAlchemy ORM:** Provides database management capabilities and object-relational mapping.
- **Flask-SocketIO:** Implements WebSocket functionality for real-time chat.
- **Flask-Smorest:** Simplifies the creation of RESTful APIs with automatic documentation.
- **Other Flask Dependencies:** We leverage various Flask extensions to enhance functionality and maintainability.

## Getting Started

To set up the development environment and run the Flask application locally, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/amethystcoder/markt_python.git
   cd markt_python
   ```

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install project dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure your database connection in `config.py`.

5. Run the application:
   ```
   flask run
   ```

6. Access the application in your web browser at `http://localhost:5000`.

## API Documentation

You can access the API documentation to explore available endpoints and their usage.

- **Swagger UI:** The API documentation is available through Swagger UI. To access it, follow these steps:

  1. Start the application as described in the [Getting Started](#getting-started) section.

  2. Open your web browser and navigate to `http://localhost:5000/swagger-ui`.

The API documentation provides details about available endpoints, request and response schemas, and allows you to interact with the API.

**Note:** This documentation is auto-generated using Flask-Smorest and provides a comprehensive view of the API's capabilities.

## Contribution

Contributions to the project are welcome! If you would like to contribute code, please follow these steps:

1. Fork the repository.

2. Clone your forked repository to your local machine.

3. Create a new branch for your feature or bug fix.

4. Make your changes, commit, and push to your forked repository.

5. Create a pull request to the main repository with a clear description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
