from app import app


def main():
    while True:
        try:
            app.run()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
