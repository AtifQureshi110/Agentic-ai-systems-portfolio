def route_query(state):

    qtype = getattr(state, "query_type", "simple")

    qtype = str(qtype).lower()

    routing_map = {
        "complex": "complex",
        "simple": "simple"
    }

    return routing_map.get(qtype, "simple")