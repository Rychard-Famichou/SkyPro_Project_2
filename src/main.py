from models.app import FlightApp


# Функция для взаимодействия с пользователем
def program_runner() -> None:
    app = FlightApp()
    app.run()


if __name__ == "__main__":
    program_runner()
