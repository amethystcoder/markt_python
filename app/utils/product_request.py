def parse_requests(request, buyer, user_details):
    return {
        "buyer_name": buyer.username,
        "city": user_details.city,
        "state": user_details.state,
        "profile_image": user_details.profile_image,
        "query_id": request.unique_id,
        "message": request.product_description,
        "buyer_id": request.buyer_id,
        "category": request.category,
        "stale_time": request.created_at
    }
