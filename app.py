from dotenv import load_dotenv

from webapp import create_app

if __name__ == "__main__":
    # Load .env file
    load_dotenv()

    # Create and run app
    app = create_app(debug=True)
    app.run()
