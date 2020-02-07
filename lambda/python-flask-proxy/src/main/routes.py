from controller import cars_controller


def register_routes(app):
    cars_controller.register_routes(app)
