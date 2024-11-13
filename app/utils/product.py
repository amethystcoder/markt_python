def parse_dict(product, images):
    return {
        "seller_id": product.seller_id,
        "product_name": product.name,
        "description": product.description,
        "product_price": product.price,
        "quantity": product.stock_quantity,
        "category": product.category,
        "product_id": product.product_id,
        "product_images": [image.image_name for image in images] if images is not None else []
    }
